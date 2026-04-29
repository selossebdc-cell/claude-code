/**
 * POST — Issue a Supabase user JWT for QA/curl without opening the browser.
 * Protected by CONFIGURATOR_DEV_KEY (same secret as payment bypass header).
 *
 * Requires secrets:
 * - CONFIGURATOR_DEV_KEY
 * - DEV_LOGIN_PASSWORD (password assigned / used for minted users)
 *
 * Body: { "email": "you@domain.com" }
 */
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";

const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY") || "";
const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
const devGate = Deno.env.get("CONFIGURATOR_DEV_KEY") || "";
const sharedPassword = Deno.env.get("DEV_LOGIN_PASSWORD") || "";

function cors(): HeadersInit {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers":
      "Content-Type, Authorization, X-Configurator-Dev-Key",
  };
}

async function getLatestDiagnosticSessions(
  admin: ReturnType<typeof createClient>,
  userId: string,
) {
  const { data, error } = await admin
    .from("diagnostics")
    .select("session_id, updated_at, diagnostic_status")
    .eq("client_id", userId)
    .order("updated_at", { ascending: false })
    .limit(5);

  if (error) {
    console.error("getLatestDiagnosticSessions:", error);
    return [];
  }

  return data || [];
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: cors() });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...cors(), "Content-Type": "application/json" },
    });
  }

  const key = req.headers.get("x-configurator-dev-key") || "";
  if (!devGate || key !== devGate) {
    return new Response(JSON.stringify({ error: "Forbidden" }), {
      status: 403,
      headers: { ...cors(), "Content-Type": "application/json" },
    });
  }

  if (!sharedPassword) {
    return new Response(
      JSON.stringify({
        error:
          "DEV_LOGIN_PASSWORD secret missing — set it in Edge Function secrets",
      }),
      {
        status: 503,
        headers: { ...cors(), "Content-Type": "application/json" },
      },
    );
  }

  let email = "";
  try {
    const body = (await req.json()) as { email?: string };
    email = (body.email || "").trim().toLowerCase();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON" }), {
      status: 400,
      headers: { ...cors(), "Content-Type": "application/json" },
    });
  }

  if (!email || !email.includes("@")) {
    return new Response(JSON.stringify({ error: "Valid email required" }), {
      status: 400,
      headers: { ...cors(), "Content-Type": "application/json" },
    });
  }

  if (!supabaseUrl || !supabaseAnonKey || !serviceKey) {
    return new Response(JSON.stringify({ error: "Server misconfiguration" }), {
      status: 500,
      headers: { ...cors(), "Content-Type": "application/json" },
    });
  }

  const admin = createClient(supabaseUrl, serviceKey);

  const { error: createErr } = await admin.auth.admin.createUser({
    email,
    password: sharedPassword,
    email_confirm: true,
  });

  if (createErr) {
    const msg = createErr.message || "";
    const likelyExists =
      /already|exists|registered|duplicate/i.test(msg) ||
      createErr.status === 422;
    if (!likelyExists) {
      console.error("createUser:", createErr);
      return new Response(
        JSON.stringify({ error: createErr.message || "createUser failed" }),
        {
          status: 500,
          headers: { ...cors(), "Content-Type": "application/json" },
        },
      );
    }

    const { data: listData } = await admin.auth.admin.listUsers({
      page: 1,
      perPage: 1000,
    });
    const existing = listData.users.find(
      (u) => (u.email || "").toLowerCase() === email,
    );
    if (!existing?.id) {
      return new Response(
        JSON.stringify({
          error:
            "User exists but could not be resolved for password reset — check Dashboard Auth users",
        }),
        {
          status: 409,
          headers: { ...cors(), "Content-Type": "application/json" },
        },
      );
    }
    const { error: updErr } = await admin.auth.admin.updateUserById(
      existing.id,
      { password: sharedPassword },
    );
    if (updErr) {
      console.error("updateUser password:", updErr);
      return new Response(JSON.stringify({ error: updErr.message }), {
        status: 500,
        headers: { ...cors(), "Content-Type": "application/json" },
      });
    }
  }

  const userClient = createClient(supabaseUrl, supabaseAnonKey);
  const { data: sessionData, error: signErr } =
    await userClient.auth.signInWithPassword({
      email,
      password: sharedPassword,
    });

  if (signErr || !sessionData.session) {
    console.error("signIn:", signErr);
    return new Response(
      JSON.stringify({
        error:
          signErr?.message ||
          "signIn failed — user may exist with another password; reset user or align DEV_LOGIN_PASSWORD",
      }),
      {
        status: 401,
        headers: { ...cors(), "Content-Type": "application/json" },
      },
    );
  }

  const appUrl =
    Deno.env.get("APP_URL")?.replace(/\/$/, "") ||
    "https://setup.csbusiness.fr";
  const latestSessions = await getLatestDiagnosticSessions(
    admin,
    sessionData.session.user.id,
  );
  const preferredSessionId = latestSessions[0]?.session_id || null;

  return new Response(
    JSON.stringify({
      access_token: sessionData.session.access_token,
      expires_at: sessionData.session.expires_at,
      refresh_token: sessionData.session.refresh_token,
      token_type: "bearer",
      user_id: sessionData.session.user.id,
      chat_url: `${appUrl}/chat.html`,
      setup_url: appUrl,
      latest_sessions: latestSessions,
      preferred_session_id: preferredSessionId,
      next_steps: {
        generate_config:
          "POST /functions/v1/generate-config with Authorization: Bearer access_token and body { session_id }",
        session_hint:
          preferredSessionId
            ? `Use preferred_session_id=${preferredSessionId} for first generate-config call`
            : "No diagnostic session yet: call /functions/v1/chat first to create one",
        payment_bypass:
          "For tests: set SKIP_PAYMENT_CHECK=true and/or send X-Configurator-Dev-Key on both chat and generate-config",
      },
    }),
    {
      status: 200,
      headers: { ...cors(), "Content-Type": "application/json" },
    },
  );
});
