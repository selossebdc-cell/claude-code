# TASK-0006: Implement create-checkout Edge Function

**Epic**: EPIC-3 (Checkout Initiation)  
**User Story**: US-005 (create-checkout Edge Function)  
**Priority**: HIGH  
**Effort**: 2 hours

---

## Overview

Build the create-checkout Edge Function to generate Stripe checkout sessions.

---

## Acceptance Criteria

- [ ] Edge Function endpoint: `POST /functions/v1/create-checkout`
- [ ] Accepts JSON body: `{ "email": "..." }`
- [ ] Validates email format (rejects invalid/missing)
- [ ] Creates Stripe checkout session with STRIPE_PRICE_ID
- [ ] Returns 200 with `{ "url": "...", "sessionId": "..." }`
- [ ] Sets success URL: `{APP_URL}/success.html?session_id={CHECKOUT_SESSION_ID}`
- [ ] Sets cancel URL: `{APP_URL}/pricing.html`
- [ ] Returns 400 on invalid email
- [ ] Returns 500 on Stripe API error (no key exposure)

---

## Definition of Done

- [ ] Edge Function deployed
- [ ] Valid email generates checkout URL
- [ ] Invalid email returns 400
- [ ] Stripe API error returns 500 with safe message
- [ ] STRIPE_SECRET_KEY not logged or exposed
- [ ] Test generates 5+ unique sessions (verify session IDs differ)

---

## Implementation

### Step 1: Create Edge Function File

Create `supabase/functions/create-checkout/index.ts`:

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import Stripe from "https://esm.sh/stripe@22.1.0";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") || "");
const APP_URL = Deno.env.get("APP_URL") || "https://app.com";

interface RequestBody {
  email?: string;
}

function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return typeof email === "string" && emailRegex.test(email);
}

serve(async (req) => {
  // 1. Check method
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  // 2. Parse request body
  let body: RequestBody = {};
  try {
    body = await req.json();
  } catch (_err) {
    return new Response(
      JSON.stringify({ error: "Invalid JSON" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  const { email } = body;

  // 3. Validate email
  if (!email || !validateEmail(email)) {
    return new Response(
      JSON.stringify({ error: "Invalid email" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  // 4. Create Stripe session
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      line_items: [
        {
          price: Deno.env.get("STRIPE_PRICE_ID") || "",
          quantity: 1,
        },
      ],
      mode: "payment",
      customer_email: email,
      success_url: `${APP_URL}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${APP_URL}/pricing.html`,
    });

    console.log(
      "Checkout session created",
      { 
        sessionId: session.id, 
        email,
        timestamp: new Date().toISOString() 
      }
    );

    return new Response(
      JSON.stringify({
        url: session.url,
        sessionId: session.id,
      }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (err) {
    console.error(
      "Stripe API error",
      { 
        error: (err as Error).message,
        email,
        timestamp: new Date().toISOString() 
      }
    );

    return new Response(
      JSON.stringify({ error: "Payment processing failed" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
});
```

### Step 2: Deploy Edge Function

```bash
# Deploy to Supabase
supabase functions deploy create-checkout

# Verify deployment
supabase functions list
```

### Step 3: Configure Environment Variables

In Supabase dashboard, set Edge Function secrets:
- `STRIPE_SECRET_KEY`
- `STRIPE_PRICE_ID`
- `APP_URL`

---

## Testing

### Test 1: Valid Email

```bash
curl -X POST https://your-project.supabase.co/functions/v1/create-checkout \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

Expected response:
```json
{
  "url": "https://checkout.stripe.com/pay/cs_xyz...",
  "sessionId": "cs_xyz..."
}
```

### Test 2: Invalid Email

```bash
curl -X POST https://your-project.supabase.co/functions/v1/create-checkout \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid-email"}'
```

Expected: 400 response with `"error": "Invalid email"`

### Test 3: Missing Email

```bash
curl -X POST https://your-project.supabase.co/functions/v1/create-checkout \
  -H "Content-Type: application/json" \
  -d '{}'
```

Expected: 400 response with `"error": "Invalid email"`

### Test 4: Generate Multiple Sessions (Uniqueness)

```typescript
// Test: Generate 5 sessions with different emails
const emails = ['a@test.com', 'b@test.com', 'c@test.com', 'd@test.com', 'e@test.com'];
const sessions = await Promise.all(
  emails.map(email =>
    fetch('/functions/v1/create-checkout', {
      method: 'POST',
      body: JSON.stringify({ email })
    }).then(r => r.json())
  )
);

// Verify all sessionIds are unique
const ids = sessions.map(s => s.sessionId);
const uniqueIds = new Set(ids);
assert(uniqueIds.size === 5, 'All session IDs are unique');
```

---

## Stripe Dashboard Verification

1. Go to Stripe Dashboard → Payments → Payment Links
2. Verify new sessions listed with correct product
3. Verify success/cancel URLs point to correct paths

---

## Deployment Sequence

1. Create Edge Function code
2. Deploy to Supabase
3. Configure environment secrets
4. Test with valid/invalid emails
5. Verify Stripe dashboard shows new sessions
6. Proceed to next task

---

## Related Specs

- Scope: **Section 1** (create-checkout Edge Function)
- Brief: **Objective 1** (Generate checkout session, return URL to frontend)
