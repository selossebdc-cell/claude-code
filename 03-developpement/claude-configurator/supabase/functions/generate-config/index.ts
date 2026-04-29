import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";
import { assembleConfigPackage, type DiagnosticLike } from "./assemble-config.ts";
import { isPaymentCheckSkipped } from "../_shared/payment-bypass.ts";

const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY") || "";
const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";

interface GenerateConfigRequest {
  session_id: string;
}

interface AuthValidationResult {
  valid: boolean;
  userId?: string;
  error?: string;
}

interface PaymentCheckResult {
  hasPaid: boolean;
  paidAt?: string;
  error?: string;
}

async function validateJWT(token: string): Promise<AuthValidationResult> {
  if (!supabaseUrl || !supabaseAnonKey) {
    return { valid: false, error: "Supabase configuration missing" };
  }
  try {
    const supabase = createClient(supabaseUrl, supabaseAnonKey);
    const {
      data: { user },
      error,
    } = await supabase.auth.getUser(token);
    if (error || !user) {
      return { valid: false, error: "Invalid or expired JWT" };
    }
    return { valid: true, userId: user.id };
  } catch (err) {
    const msg = err instanceof Error ? err.message : "JWT validation failed";
    return { valid: false, error: msg };
  }
}

async function checkPaymentStatus(userId: string): Promise<PaymentCheckResult> {
  if (!supabaseUrl || !supabaseAnonKey) {
    return { hasPaid: false, error: "Supabase configuration missing" };
  }
  try {
    const supabase = createClient(supabaseUrl, supabaseAnonKey);
    const { data, error } = await supabase
      .from("diagnostics")
      .select("paid_at")
      .eq("client_id", userId)
      .not("paid_at", "is", null)
      .gt("paid_at", new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString())
      .limit(1);
    if (error) {
      console.error("Payment check query error:", error);
      return { hasPaid: false, error: "Payment verification failed" };
    }
    if (data && data.length > 0) {
      return { hasPaid: true, paidAt: data[0].paid_at };
    }
    return {
      hasPaid: false,
      error: "No active payment. Please purchase access.",
    };
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Payment check failed";
    return { hasPaid: false, error: msg };
  }
}

function sseLine(payload: Record<string, unknown>): string {
  return `data: ${JSON.stringify(payload)}\n\n`;
}

function corsHeaders(): HeadersInit {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers":
      "Content-Type, Authorization, X-Configurator-Dev-Key",
  };
}

async function handler(req: Request): Promise<Response> {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders() });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  const authHeader = req.headers.get("authorization");
  if (!authHeader?.startsWith("Bearer ")) {
    return new Response(JSON.stringify({ error: "Missing Authorization Bearer token" }), {
      status: 401,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  const token = authHeader.replace("Bearer ", "");
  const jwtValidation = await validateJWT(token);
  if (!jwtValidation.valid || !jwtValidation.userId) {
    return new Response(JSON.stringify({ error: jwtValidation.error || "Unauthorized" }), {
      status: 401,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  const userId = jwtValidation.userId;

  if (!isPaymentCheckSkipped(req)) {
    const paymentCheck = await checkPaymentStatus(userId);
    if (!paymentCheck.hasPaid) {
      return new Response(
        JSON.stringify({
          error: paymentCheck.error || "Payment required",
          code: "PAYMENT_REQUIRED",
        }),
        {
          status: 403,
          headers: { ...corsHeaders(), "Content-Type": "application/json" },
        }
      );
    }
  }

  let body: GenerateConfigRequest;
  try {
    body = (await req.json()) as GenerateConfigRequest;
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON body" }), {
      status: 400,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  const session_id = body.session_id;
  if (!session_id) {
    return new Response(JSON.stringify({ error: "Missing session_id" }), {
      status: 400,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  if (!serviceKey || !supabaseUrl) {
    return new Response(JSON.stringify({ error: "Server misconfiguration" }), {
      status: 500,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  const admin = createClient(supabaseUrl, serviceKey);

  const { data: row, error: fetchError } = await admin
    .from("diagnostics")
    .select("metadata, session_id, client_id")
    .eq("session_id", session_id)
    .eq("client_id", userId)
    .maybeSingle();

  if (fetchError) {
    console.error("generate-config fetch:", fetchError);
    return new Response(JSON.stringify({ error: "Failed to load diagnostic session" }), {
      status: 500,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  if (!row?.metadata) {
    return new Response(JSON.stringify({ error: "Diagnostic session not found" }), {
      status: 404,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  const meta = row.metadata as Record<string, unknown>;
  const diagnosticInput: DiagnosticLike = {
    session_id: session_id,
    client_name: typeof meta.client_name === "string" ? meta.client_name : undefined,
    synthesis: meta.synthesis as DiagnosticLike["synthesis"],
    living_proposal: meta.living_proposal as DiagnosticLike["living_proposal"],
  };

  const packageForResponse = assembleConfigPackage(session_id, diagnosticInput);

  const persistPayload = {
    ...packageForResponse,
    markdown_bundle: truncatePersistMarkdown(packageForResponse.markdown_bundle),
  };

  const mergedMetadata = {
    ...meta,
    generated_package: persistPayload,
  };

  const { error: saveError } = await admin
    .from("diagnostics")
    .update({
      metadata: mergedMetadata,
      updated_at: new Date().toISOString(),
    })
    .eq("session_id", session_id)
    .eq("client_id", userId);

  if (saveError) {
    console.error("generate-config persist:", saveError);
  }

  const wantsJson = req.headers.get("accept")?.includes("application/json");

  if (wantsJson) {
    return new Response(JSON.stringify(packageForResponse), {
      status: 200,
      headers: { ...corsHeaders(), "Content-Type": "application/json" },
    });
  }

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    start(controller) {
      const send = (obj: Record<string, unknown>) => {
        controller.enqueue(encoder.encode(sseLine(obj)));
      };

      send({
        type: "progress",
        phase: "validation",
        percent: 15,
        validation: packageForResponse.validation,
      });
      send({ type: "progress", phase: "assembly", percent: 60 });
      send({
        type: "progress",
        phase: saveError ? "persist_skipped" : "persisted",
        percent: 90,
        persisted: !saveError,
      });
      send({
        type: "complete",
        package: packageForResponse,
      });
      controller.close();
    },
  });

  return new Response(stream, {
    status: 200,
    headers: {
      ...corsHeaders(),
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}

function truncatePersistMarkdown(md: string): string {
  const max = 12000;
  if (md.length <= max) return md;
  return `${md.slice(0, max - 20)}\n…(truncated for storage)`;
}

Deno.serve(handler);
