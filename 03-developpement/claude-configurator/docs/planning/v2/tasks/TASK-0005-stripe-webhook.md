# TASK-0005: Implement stripe-webhook Edge Function

**Epic**: EPIC-2 (Stripe Webhook Handler)  
**User Story**: US-004 (Stripe Webhook Handler Edge Function)  
**Priority**: CRITICAL  
**Effort**: 4 hours

---

## Overview

Build the stripe-webhook Edge Function to receive, verify, and process Stripe checkout.session.completed events.

---

## Acceptance Criteria

- [ ] Edge Function endpoint: `POST /functions/v1/stripe-webhook`
- [ ] Signature verification: rejects invalid signatures (400)
- [ ] Idempotence: webhook replay does not create duplicate user
- [ ] User creation: calls `inviteUserByEmail()` with 3-retry logic
- [ ] Diagnostics row: inserted with `stripe_session_id`, `client_id`, `paid_at`
- [ ] Error handling: all errors logged with timestamp, event ID, outcome
- [ ] Returns 200 on success, 400 on invalid signature, 500 on failure

---

## Definition of Done

- [ ] Edge Function code deployed
- [ ] Signature verification tested (reject invalid)
- [ ] Idempotence tested (webhook replay, no duplicate)
- [ ] Retry logic tested (simulate failure, verify 3 retries + log)
- [ ] Magic link sent automatically (inviteUserByEmail side effect)
- [ ] All logs contain no sensitive data (STRIPE_WEBHOOK_SECRET not exposed)

---

## Implementation

### Step 1: Create Edge Function File

Create `supabase/functions/stripe-webhook/index.ts`:

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import Stripe from "https://esm.sh/stripe@22.1.0";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.104.1";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") || "");
const supabaseAdmin = createClient(
  Deno.env.get("SUPABASE_URL") || "",
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || ""
);

interface WebhookRequest {
  method: string;
  headers: Headers;
  text: () => Promise<string>;
}

async function handleWebhook(req: WebhookRequest) {
  // 1. Extract signature and body
  const signature = req.headers.get("stripe-signature");
  const body = await req.text();

  if (!signature) {
    console.error(
      "Missing stripe-signature header",
      { timestamp: new Date().toISOString() }
    );
    return new Response(
      JSON.stringify({ error: "Invalid signature" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  // 2. Verify signature
  let event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      Deno.env.get("STRIPE_WEBHOOK_SECRET") || ""
    );
  } catch (err) {
    console.error(
      "Webhook signature verification failed",
      { 
        error: (err as Error).message,
        timestamp: new Date().toISOString() 
      }
    );
    return new Response(
      JSON.stringify({ error: "Invalid signature" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  console.log(
    "Webhook received",
    { 
      eventId: event.id, 
      eventType: event.type,
      timestamp: new Date().toISOString() 
    }
  );

  // 3. Handle checkout.session.completed
  if (event.type === "checkout.session.completed") {
    const session = event.data.object as {
      id: string;
      customer_email: string;
    };
    const email = session.customer_email;
    const stripeSessionId = session.id;

    // 4. Check idempotence
    const { data: existing, error: checkErr } = await supabaseAdmin
      .from("diagnostics")
      .select("id")
      .eq("stripe_session_id", stripeSessionId)
      .maybeSingle();

    if (checkErr) {
      console.error(
        "Idempotence check failed",
        { 
          stripeSessionId, 
          error: checkErr.message,
          timestamp: new Date().toISOString() 
        }
      );
      return new Response(
        JSON.stringify({ error: "Database error" }),
        { status: 500, headers: { "Content-Type": "application/json" } }
      );
    }

    if (existing) {
      console.log(
        "Webhook replay detected, skipping user creation",
        { 
          stripeSessionId, 
          timestamp: new Date().toISOString() 
        }
      );
      return new Response(
        JSON.stringify({ received: true }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    }

    // 5. Retry logic for user creation
    let user;
    let lastError;
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const { data, error } = await supabaseAdmin.auth.admin
          .inviteUserByEmail(email, {
            redirectTo: `${Deno.env.get("APP_URL") || "https://app.com"}/auth/magic-link-callback`,
          });

        if (error) throw error;
        user = data.user;
        break;
      } catch (err) {
        lastError = err;
        console.error(
          "inviteUserByEmail attempt failed",
          { 
            attempt: attempt + 1, 
            email, 
            error: (err as Error).message,
            timestamp: new Date().toISOString() 
          }
        );
        if (attempt < 2) {
          // Wait 1 second before retry
          await new Promise((r) => setTimeout(r, 1000));
        }
      }
    }

    if (!user) {
      console.error(
        "User creation failed after 3 retries",
        { 
          email, 
          stripeSessionId,
          error: (lastError as Error)?.message,
          timestamp: new Date().toISOString() 
        }
      );
      return new Response(
        JSON.stringify({ error: "User creation failed" }),
        { status: 500, headers: { "Content-Type": "application/json" } }
      );
    }

    // 6. Insert diagnostics row
    const now = new Date().toISOString();
    const { error: insertErr } = await supabaseAdmin
      .from("diagnostics")
      .insert({
        stripe_session_id: stripeSessionId,
        client_id: user.id,
        paid_at: now,
        created_at: now,
      });

    if (insertErr) {
      console.error(
        "Failed to insert diagnostics row",
        { 
          stripeSessionId,
          userId: user.id,
          error: insertErr.message,
          timestamp: new Date().toISOString() 
        }
      );
      return new Response(
        JSON.stringify({ error: "Database error" }),
        { status: 500, headers: { "Content-Type": "application/json" } }
      );
    }

    console.log(
      "Webhook processed successfully",
      { 
        stripeSessionId, 
        userId: user.id,
        email,
        timestamp: new Date().toISOString() 
      }
    );

    return new Response(
      JSON.stringify({ received: true }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  }

  // Acknowledge other event types
  return new Response(
    JSON.stringify({ received: true }),
    { status: 200, headers: { "Content-Type": "application/json" } }
  );
}

serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  try {
    return await handleWebhook(
      req as unknown as WebhookRequest
    );
  } catch (err) {
    console.error(
      "Unhandled webhook error",
      { 
        error: (err as Error).message,
        timestamp: new Date().toISOString() 
      }
    );
    return new Response(
      JSON.stringify({ error: "Internal error" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
});
```

### Step 2: Deploy Edge Function

```bash
# Deploy to Supabase
supabase functions deploy stripe-webhook

# Verify deployment
supabase functions list
```

### Step 3: Configure Environment Variables

In Supabase dashboard, set Edge Function secrets:
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `SUPABASE_SERVICE_ROLE_KEY` (usually pre-set)
- `APP_URL` (for magic link redirect)

### Step 4: Configure Stripe Webhook Endpoint

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint:
   - URL: `https://your-project.supabase.co/functions/v1/stripe-webhook`
   - Events: `checkout.session.completed`
   - API version: Latest
3. Copy webhook secret and add to Supabase secrets

---

## Testing

### Test 1: Verify Signature Verification

Send invalid request:
```bash
curl -X POST https://your-project.supabase.co/functions/v1/stripe-webhook \
  -H "Content-Type: application/json" \
  -H "stripe-signature: invalid" \
  -d '{}'
```

Expected: 400 response with `"error": "Invalid signature"`

### Test 2: Test With Stripe CLI (Webhook Forwarding)

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login to Stripe account
stripe login

# Forward events to local webhook
stripe listen --forward-to localhost:3000/functions/v1/stripe-webhook --events checkout.session.completed

# In another terminal, trigger test event
stripe trigger checkout.session.completed
```

Expected: Webhook received, user created, magic link sent.

### Test 3: Verify Idempotence

```bash
# Simulate webhook replay by sending same event twice
# (Stripe CLI or manual curl with saved event)

# Verify only 1 user created, not 2
psql -c "SELECT COUNT(*) FROM auth.users WHERE email = 'test@example.com';"
# Expected: 1
```

### Test 4: Test Retry Logic

Mock `inviteUserByEmail()` failure and verify retries logged:
```typescript
// In test: simulate error on attempt 1, success on attempt 2
// Check logs for "inviteUserByEmail attempt failed" (attempt 1)
// Followed by successful user creation
```

---

## Deployment Sequence

1. Create Edge Function code
2. Deploy to Supabase
3. Configure environment secrets
4. Register webhook endpoint in Stripe Dashboard
5. Test with Stripe CLI
6. Test idempotence (manual webhook replay)
7. Monitor logs for errors
8. Proceed to next task

---

## Related Specs

- Scope: **Section 2** (stripe-webhook Edge Function, Q-001, Q-002, Q-003, Q-007, Q-009)
- Brief: **Objective 1** (Automated user creation on payment)
