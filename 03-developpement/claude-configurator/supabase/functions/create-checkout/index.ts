import { createClient } from "https://esm.sh/@supabase/supabase-js@2.38.0";

const stripe_secret_key = Deno.env.get("STRIPE_SECRET_KEY");
const stripe_price_id = Deno.env.get("STRIPE_PRICE_ID");
const supabase_url = Deno.env.get("SUPABASE_URL");
const supabase_anon_key = Deno.env.get("SUPABASE_ANON_KEY");
const app_url = Deno.env.get("APP_URL");

interface CheckoutRequest {
  email?: string;
  priceId?: string;
}

interface StripeCheckoutSession {
  url: string;
  id: string;
}

async function createStripeCheckout(email: string, priceId?: string): Promise<StripeCheckoutSession | null> {
  const selectedPriceId = priceId || stripe_price_id;

  if (!stripe_secret_key || !selectedPriceId) {
    console.error("Stripe configuration missing");
    return null;
  }

  try {
    const checkoutData = new URLSearchParams({
      payment_method_types: JSON.stringify(["card"]),
      mode: "payment",
      line_items: JSON.stringify([
        {
          price: selectedPriceId,
          quantity: 1,
        },
      ]),
      success_url: `${app_url}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${app_url}/`,
      customer_email: email,
      metadata: JSON.stringify({
        email: email,
        created_at: new Date().toISOString(),
      }),
    });

    const response = await fetch("https://api.stripe.com/v1/checkout/sessions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${stripe_secret_key}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: checkoutData.toString(),
    });

    const data = await response.json() as Record<string, unknown>;

    if (!response.ok) {
      const errorMsg = (data.error as Record<string, string> | undefined)?.message || "Unknown error";
      console.error("Stripe API error:", errorMsg);
      return null;
    }

    return {
      url: data.url as string,
      id: data.id as string,
    };
  } catch (err) {
    console.error("Exception creating checkout:", err);
    return null;
  }
}

async function validateRequest(req: Request): Promise<string | null> {
  // Validate JWT (optional for landing page, required for authenticated users)
  const authHeader = req.headers.get("authorization");
  if (authHeader) {
    const token = authHeader.replace("Bearer ", "");
    if (!supabase_url || !supabase_anon_key) {
      console.error("Supabase configuration missing");
      return null;
    }

    const supabase = createClient(supabase_url, supabase_anon_key);
    const {
      data: { user },
      error,
    } = await supabase.auth.getUser(token);

    if (error || !user) {
      console.error("JWT validation failed:", error);
      return null;
    }

    return user.email || null;
  }

  return null;
}

Deno.serve(async (req) => {
  // Only accept POST
  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ error: "Method not allowed" }),
      { status: 405, headers: { "Content-Type": "application/json" } }
    );
  }

  // Parse request body
  let body: CheckoutRequest;
  try {
    body = await req.json() as CheckoutRequest;
  } catch {
    return new Response(
      JSON.stringify({ error: "Invalid JSON" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  // Get email (either from JWT or from request body)
  let email = body.email;

  if (!email) {
    const jwtEmail = await validateRequest(req);
    email = jwtEmail;
  }

  // Validate email
  if (!email) {
    return new Response(
      JSON.stringify({ error: "Email required" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return new Response(
      JSON.stringify({ error: "Invalid email format" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  // Create Stripe checkout session (with optional priceId)
  const session = await createStripeCheckout(email, body.priceId);
  if (!session) {
    return new Response(
      JSON.stringify({ error: "Failed to create checkout session" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }

  return new Response(
    JSON.stringify({
      status: "ok",
      session_id: session.id,
      url: session.url,
    }),
    {
      status: 200,
      headers: { "Content-Type": "application/json" },
    }
  );
});
