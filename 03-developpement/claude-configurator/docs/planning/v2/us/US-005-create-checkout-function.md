# US-005: create-checkout Edge Function

**EPIC**: EPIC-3 (Checkout Initiation)  
**User Story**: As a frontend engineer, I need a checkout endpoint so that users can initiate payment to the Stripe checkout.

---

## Acceptance Criteria

- [ ] Edge Function endpoint: `POST /functions/v1/create-checkout`
- [ ] Accepts JSON request body: `{ "email": "user@example.com" }`
- [ ] Validates email format (rejects invalid or missing emails)
- [ ] Calls Stripe API to create checkout session with STRIPE_PRICE_ID
- [ ] Returns 200 with `{ "url": "https://checkout.stripe.com/...", "sessionId": "cs_xyz..." }`
- [ ] Success URL: `{APP_URL}/success.html?session_id=cs_xyz`
- [ ] Cancel URL: `{APP_URL}/pricing.html`
- [ ] Returns 400 on invalid email or missing field
- [ ] Returns 500 on Stripe API failure (with error message, no key leakage)
- [ ] STRIPE_SECRET_KEY never exposed in logs or response

## Definition of Done

1. Edge Function code written and deployed
2. Valid email generates unique Stripe checkout URL
3. Session ID returned to frontend
4. Invalid email returns 400
5. Stripe API error returns 500 with safe error message
6. STRIPE_SECRET_KEY not logged or exposed
7. Success/cancel URLs configured correctly

## Technical Details

**Handler Structure**:
```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import Stripe from "https://esm.sh/stripe@22.1.0";

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY'));
const APP_URL = Deno.env.get('APP_URL') || 'https://app.com';

serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 });

  const { email } = await req.json().catch(() => ({}));

  // 1. Validate email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || typeof email !== 'string' || !emailRegex.test(email)) {
    return new Response(
      JSON.stringify({ error: 'Invalid email' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // 2. Create Stripe session
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: Deno.env.get('STRIPE_PRICE_ID'),
          quantity: 1
        }
      ],
      mode: 'payment',
      customer_email: email,
      success_url: `${APP_URL}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${APP_URL}/pricing.html`
    });

    return new Response(
      JSON.stringify({
        url: session.url,
        sessionId: session.id
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (err) {
    console.error('Stripe API error:', { error: err.message, timestamp: new Date().toISOString() });
    return new Response(
      JSON.stringify({ error: 'Payment processing failed' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
});
```

**Environment Variables Required**:
- `STRIPE_SECRET_KEY`: Stripe secret API key
- `STRIPE_PRICE_ID`: Hardcoded Stripe price ID (from Stripe dashboard)
- `APP_URL`: Application URL (default: https://app.com)

## Dependencies

None (can be deployed independently, but frontend will call it after EPIC-2 is deployed).

## Related Specs

- Scope: **Section 1** (create-checkout Edge Function)
- Brief: **Objective 1** (Generate checkout session, return URL to frontend)
