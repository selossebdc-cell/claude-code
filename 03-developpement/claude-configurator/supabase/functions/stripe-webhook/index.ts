import { createClient } from "https://esm.sh/@supabase/supabase-js@2.38.0";

const stripe_secret_key = Deno.env.get("STRIPE_SECRET_KEY");
const stripe_webhook_secret = Deno.env.get("STRIPE_WEBHOOK_SECRET");
const supabase_url = Deno.env.get("SUPABASE_URL");
const supabase_service_role_key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
const app_url = Deno.env.get("APP_URL");

interface StripeEvent {
  id: string;
  type: string;
  data: {
    object: {
      id?: string;
      customer_email?: string;
      status?: string;
      metadata?: Record<string, string>;
    };
  };
}

async function verifyStripeSignature(
  body: string,
  signature: string
): Promise<StripeEvent | null> {
  if (!stripe_webhook_secret) {
    console.error("STRIPE_WEBHOOK_SECRET not configured");
    return null;
  }

  // Stripe signature format: t=<timestamp>,v1=<signature>
  const signatureParts = signature.split(",");
  const timestamp = signatureParts
    .find((s) => s.startsWith("t="))
    ?.split("=")[1];
  const v1Sig = signatureParts
    .find((s) => s.startsWith("v1="))
    ?.split("=")[1];

  if (!timestamp || !v1Sig) {
    console.error("Invalid signature format");
    return null;
  }

  // Signed content is: {timestamp}.{body}
  const signedContent = `${timestamp}.${body}`;
  const encoder = new TextEncoder();
  const secretBytes = encoder.encode(stripe_webhook_secret);
  const messageBytes = encoder.encode(signedContent);

  const key = await crypto.subtle.importKey(
    "raw",
    secretBytes,
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );

  const computedSignature = await crypto.subtle.sign("HMAC", key, messageBytes);
  const computedHex = Array.from(new Uint8Array(computedSignature))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");

  // Compare signatures using timing-safe comparison
  const matches = timingSafeEqual(v1Sig, computedHex);

  if (!matches) {
    console.error("Signature verification failed");
    return null;
  }

  // Parse and return event
  try {
    const event = JSON.parse(body) as StripeEvent;
    return event;
  } catch {
    console.error("Failed to parse event body");
    return null;
  }
}

function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return result === 0;
}

async function createMagicLink(email: string): Promise<string | null> {
  if (!supabase_url || !supabase_service_role_key) {
    console.error("Supabase configuration missing");
    return null;
  }

  const supabase = createClient(supabase_url, supabase_service_role_key);

  try {
    // Generate magic link
    const { data, error } = await supabase.auth.admin.generateLink({
      type: "magiclink",
      email,
      options: {
        redirectTo: `${app_url}/auth/callback`,
      },
    });

    if (error) {
      console.error("Generate link error:", error);
      return null;
    }

    if (!data?.properties?.action_link) {
      console.error("No magic link generated");
      return null;
    }

    console.log(`Magic link generated for ${email}`);
    return data.properties.action_link;
  } catch (err) {
    console.error("Exception generating magic link:", err);
    return null;
  }
}

async function recordWebhookEvent(
  stripeEventId: string,
  eventType: string,
  eventData: unknown,
  clientEmail: string,
  responseCode: number,
  errorMessage?: string
): Promise<void> {
  if (!supabase_url || !supabase_service_role_key) {
    console.error("Supabase configuration missing");
    return;
  }

  const supabase = createClient(supabase_url, supabase_service_role_key);

  try {
    await supabase.from("stripe_events").insert({
      stripe_event_id: stripeEventId,
      event_type: eventType,
      event_data: eventData,
      processed_at: new Date().toISOString(),
      response_code: responseCode,
      error_message: errorMessage || null,
      client_email: clientEmail,
    });
  } catch (err) {
    console.error("Failed to record webhook event:", err);
  }
}

async function checkEventAlreadyProcessed(stripeEventId: string): Promise<boolean> {
  if (!supabase_url || !supabase_service_role_key) {
    console.error("Supabase configuration missing");
    return false;
  }

  const supabase = createClient(supabase_url, supabase_service_role_key);

  try {
    const { data, error } = await supabase
      .from("stripe_events")
      .select("id")
      .eq("stripe_event_id", stripeEventId)
      .limit(1);

    if (error) {
      console.error("Query error:", error);
      return false;
    }

    return data && data.length > 0;
  } catch (err) {
    console.error("Exception checking event:", err);
    return false;
  }
}

Deno.serve(async (req) => {
  // Only accept POST
  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ error: "Method not allowed" }),
      { status: 405, headers: { "Content-Type": "application/json" } }
    );
  }

  // Get signature from headers
  const signature = req.headers.get("stripe-signature");
  if (!signature) {
    return new Response(
      JSON.stringify({ error: "Missing stripe-signature header" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  // Read body
  const body = await req.text();

  // Verify signature
  const event = await verifyStripeSignature(body, signature);
  if (!event) {
    return new Response(
      JSON.stringify({ error: "Signature verification failed" }),
      { status: 401, headers: { "Content-Type": "application/json" } }
    );
  }

  // Check if event already processed (idempotence)
  const alreadyProcessed = await checkEventAlreadyProcessed(event.id);
  if (alreadyProcessed) {
    console.log(`Event ${event.id} already processed, skipping`);
    return new Response(
      JSON.stringify({ status: "ok", message: "Event already processed" }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  }

  const clientEmail = event.data.object.customer_email || "unknown";
  let responseCode = 200;
  let errorMessage: string | undefined;

  try {
    // Handle Stripe events
    if (event.type === "payment_intent.succeeded") {
      const metadata = event.data.object.metadata as Record<string, string> | undefined;
      const emailFromMetadata = metadata?.email;
      const emailFromCustomer = event.data.object.customer_email;
      const finalEmail = emailFromMetadata || emailFromCustomer;

      if (!finalEmail) {
        throw new Error("No customer email in payment intent");
      }

      const magicLinkEmail = await createMagicLink(finalEmail);
      if (!magicLinkEmail) {
        throw new Error("Failed to create magic link");
      }

      console.log(`Magic link sent to ${finalEmail}`);
    } else if (event.type === "charge.failed") {
      console.log(`Charge failed for ${clientEmail}`);
      // Could send notification email here
    } else {
      console.log(`Unhandled event type: ${event.type}`);
    }

    // Record successful webhook processing
    await recordWebhookEvent(
      event.id,
      event.type,
      event.data,
      clientEmail,
      200
    );

    return new Response(
      JSON.stringify({ status: "ok", event_id: event.id }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    console.error(`Webhook processing error:`, errorMsg);

    responseCode = 500;
    errorMessage = errorMsg;

    // Record failed webhook processing
    await recordWebhookEvent(
      event.id,
      event.type,
      event.data,
      clientEmail,
      500,
      errorMessage
    );

    return new Response(
      JSON.stringify({ error: "Webhook processing failed" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
});
