# US-004: Stripe Webhook Handler Edge Function

**EPIC**: EPIC-2 (Stripe Webhook Handler)  
**User Story**: As a security engineer, I need the Stripe webhook to verify and process payment events so that users are automatically created and authenticated.

---

## Acceptance Criteria

- [ ] Edge Function endpoint: `POST /functions/v1/stripe-webhook`
- [ ] Accepts `stripe-signature` header and raw request body
- [ ] Calls `Stripe.webhooks.constructEvent()` with signature verification
- [ ] Returns 400 if signature invalid (never processes event)
- [ ] Checks `diagnostics` table for existing `stripe_session_id` (idempotence)
- [ ] Calls `supabase.auth.admin.inviteUserByEmail()` with retry logic (3x, 1s delay)
- [ ] Inserts row into `diagnostics` table with `stripe_session_id`, `client_id`, `paid_at`
- [ ] Returns 200 on success, 500 on failure
- [ ] All events logged with timestamp, event ID, outcome

## Definition of Done

1. Edge Function code written and deployed
2. Signature verification rejects invalid signatures
3. Idempotence: test webhook replay, verify no duplicate user
4. Retry logic: simulate `inviteUserByEmail()` failure, verify 3 retries + log
5. Diagnostics row inserted with correct `client_id` (newly created user)
6. Error messages logged without exposing secrets (STRIPE_WEBHOOK_SECRET not in logs)

## Technical Details

**Handler Structure**:
```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import Stripe from "https://esm.sh/stripe@22.1.0";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.104.1";

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY'));
const supabaseAdmin = createClient(
  Deno.env.get('SUPABASE_URL'),
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
);

serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 });

  const signature = req.headers.get('stripe-signature');
  const body = await req.text();

  // 1. Verify signature
  let event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      Deno.env.get('STRIPE_WEBHOOK_SECRET')
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', { timestamp: new Date().toISOString() });
    return new Response(JSON.stringify({ error: 'Invalid signature' }), { status: 400 });
  }

  // 2. Handle checkout.session.completed
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const email = session.customer_email;
    const stripeSessionId = session.id;

    // 3. Check idempotence
    const { data: existing } = await supabaseAdmin
      .from('diagnostics')
      .select('id')
      .eq('stripe_session_id', stripeSessionId)
      .single();

    if (existing) {
      console.log('Webhook replay detected, skipping user creation', { stripeSessionId, timestamp: new Date().toISOString() });
      return new Response(JSON.stringify({ received: true }), { status: 200 });
    }

    // 4. Retry logic for user creation
    let user;
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const { data } = await supabaseAdmin.auth.admin.inviteUserByEmail(email, {
          redirectTo: 'https://app.com/auth/magic-link-callback'
        });
        user = data.user;
        break;
      } catch (err) {
        console.error('inviteUserByEmail failed', { attempt, email, error: err.message, timestamp: new Date().toISOString() });
        if (attempt < 2) await new Promise(r => setTimeout(r, 1000));
      }
    }

    if (!user) {
      console.error('User creation failed after 3 retries', { email, stripeSessionId, timestamp: new Date().toISOString() });
      return new Response(JSON.stringify({ error: 'User creation failed' }), { status: 500 });
    }

    // 5. Insert diagnostics row
    const { error: insertErr } = await supabaseAdmin
      .from('diagnostics')
      .insert({
        stripe_session_id: stripeSessionId,
        client_id: user.id,
        paid_at: new Date().toISOString()
      });

    if (insertErr) {
      console.error('Failed to insert diagnostics row', { error: insertErr, timestamp: new Date().toISOString() });
      return new Response(JSON.stringify({ error: 'Database error' }), { status: 500 });
    }

    console.log('Webhook processed successfully', { stripeSessionId, userId: user.id, timestamp: new Date().toISOString() });
    return new Response(JSON.stringify({ received: true }), { status: 200 });
  }

  return new Response(JSON.stringify({ received: true }), { status: 200 });
});
```

**Environment Variables Required**:
- `STRIPE_SECRET_KEY`: Stripe secret API key
- `STRIPE_WEBHOOK_SECRET`: Webhook signing secret
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Admin API key (service role)

## Dependencies

Requires:
- US-001 (diagnostics table exists)
- US-002 (RLS policies in place)

## Related Specs

- Scope: **Section 2** (stripe-webhook Edge Function, Q-001, Q-002, Q-003, Q-007, Q-009)
- Brief: **Objective 1** (Automated user creation on payment)
