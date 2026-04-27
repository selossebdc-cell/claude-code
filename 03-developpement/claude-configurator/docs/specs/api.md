# API Specification — Authentication & Stripe Integration

**Document Type**: API Specification  
**Date**: 2026-04-27  
**Status**: Ready for ACT phase  
**Audience**: Frontend & Backend Engineers

---

## Overview

This document specifies all HTTP endpoints required for the auth-stripe feature:
1. **create-checkout** (NEW) — Generate Stripe checkout session
2. **stripe-webhook** (NEW) — Receive & process Stripe events
3. **chat** (MODIFY) — Add JWT validation & payment status check
4. **magic-link-callback** (FRONTEND) — Handle magic link verification

All endpoints use HTTPS, JSON, and standard HTTP status codes.

---

## 1. POST /functions/v1/create-checkout

**Purpose**: Generate a Stripe checkout session and return the checkout URL to the frontend

**HTTP Method**: POST  
**Content-Type**: application/json  
**Authentication**: None (public endpoint)  
**CORS**: Allow origin from frontend domain only

### Request

**Body**:
```json
{
  "email": "user@example.com"
}
```

**Parameters**:
- `email` (STRING, required): User's email address (validated via RFC 5322 pattern)

**Headers**:
```
POST /functions/v1/create-checkout HTTP/1.1
Host: xyz.supabase.co
Content-Type: application/json
```

### Response

**Success (200 OK)**:
```json
{
  "url": "https://checkout.stripe.com/pay/cs_live_xyz123...",
  "sessionId": "cs_live_xyz123"
}
```

**Properties**:
- `url` (STRING): Stripe Checkout URL (redirect browser to this)
- `sessionId` (STRING): Session ID for reference (used in webhook)

**Error (400 Bad Request)** — Invalid email:
```json
{
  "error": "Invalid email address"
}
```

**Error (500 Internal Server Error)** — Stripe API failure:
```json
{
  "error": "Payment processing failed. Please try again."
}
```

### Acceptance Criteria

- [ ] Accepts POST with JSON body (email required)
- [ ] Validates email format (basic regex: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`)
- [ ] Calls Stripe API: `stripe.checkout.sessions.create({...})`
- [ ] Returns valid Stripe Checkout URL
- [ ] Sets success URL: `{APP_URL}/success.html?session_id=cs_xyz`
- [ ] Sets cancel URL: `{APP_URL}/pricing.html`
- [ ] Returns 400 if email invalid or missing
- [ ] Returns 500 if Stripe API fails
- [ ] **NEVER** exposes STRIPE_SECRET_KEY in response or logs
- [ ] **NEVER** exposes STRIPE_PUBLISHABLE_KEY in response

### Implementation Notes

**Environment Variables Required**:
```bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...  # Only used in frontend, not here
STRIPE_PRICE_ID=price_...
```

**Pseudocode**:
```typescript
export async function createCheckout(req: Request) {
  const { email } = await req.json();

  // Validate email
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return new Response(
      JSON.stringify({ error: 'Invalid email address' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  try {
    const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY'));
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: Deno.env.get('STRIPE_PRICE_ID'),
          quantity: 1
        }
      ],
      mode: 'payment',
      success_url: `${Deno.env.get('APP_URL')}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${Deno.env.get('APP_URL')}/pricing.html`,
      customer_email: email
    });

    return new Response(
      JSON.stringify({
        url: session.url,
        sessionId: session.id
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Stripe API error:', error.message);
    return new Response(
      JSON.stringify({ error: 'Payment processing failed. Please try again.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
```

---

## 2. POST /functions/v1/stripe-webhook

**Purpose**: Receive Stripe webhook event, verify signature, create user, send magic link

**HTTP Method**: POST  
**Content-Type**: application/json  
**Authentication**: Signature verification via Stripe secret  
**CORS**: Not applicable (Stripe calls this, not browser)

### Request

**Headers**:
```
POST /functions/v1/stripe-webhook HTTP/1.1
Host: xyz.supabase.co
Content-Type: application/json
stripe-signature: t=<timestamp>,v1=<signature>
```

**Body** (example):
```json
{
  "id": "evt_1234567890",
  "type": "checkout.session.completed",
  "created": 1234567890,
  "data": {
    "object": {
      "id": "cs_live_xyz123",
      "customer_email": "user@example.com",
      "payment_status": "paid"
    }
  }
}
```

**Parameters**:
- `stripe-signature` (HEADER, required): Signature for verification (format: `t=<timestamp>,v1=<hmac>`)
- Event body: Raw request body (string, NOT parsed JSON)

### Response

**Success (200 OK)**:
```json
{
  "received": true
}
```

**Error (400 Bad Request)** — Invalid signature:
```json
{
  "error": "Invalid signature"
}
```

**Error (500 Internal Server Error)** — Processing failure:
```json
{
  "error": "Processing failed"
}
```

### Acceptance Criteria

#### Signature Verification
- [ ] Extracts `stripe-signature` header
- [ ] Calls `stripe.webhooks.constructEvent(body, header, secret)`
- [ ] Returns 400 if signature invalid
- [ ] **NEVER** logs STRIPE_WEBHOOK_SECRET
- [ ] Logs invalid signature attempt (timestamp, IP, attempt details)
- [ ] Does NOT process invalid events

#### Idempotence
- [ ] Checks: `SELECT 1 FROM diagnostics WHERE stripe_session_id = 'cs_...'`
- [ ] If exists: return 200 (skip user creation)
- [ ] If new: continue to user creation
- [ ] Database constraint: `UNIQUE(stripe_session_id)` prevents race conditions

#### User Creation (Retry Logic)
- [ ] Extracts email from event: `event.data.object.customer_email`
- [ ] Calls `supabaseAdmin.auth.admin.inviteUserByEmail(email, {redirectTo: '/auth/magic-link-callback'})`
- [ ] **Retries immediately 3 times with 1s delay** if failure
- [ ] After 3 failures: return 500, log error details
- [ ] Returns 200 immediately after success (user created, magic link sent)

#### Diagnostic Entry
- [ ] Inserts row into `diagnostics` table:
  ```sql
  INSERT INTO diagnostics (
    stripe_session_id,
    client_id,
    paid_at,
    created_at
  ) VALUES (
    'cs_live_xyz123',
    (SELECT id FROM auth.users WHERE email = 'user@example.com'),
    NOW(),
    NOW()
  )
  ```
- [ ] `client_id` = UUID of newly created auth.users entry
- [ ] `paid_at` = current timestamp (used for 30-day retention)

#### Error Handling
- [ ] Returns 200 on success
- [ ] Returns 400 on invalid signature (never processes)
- [ ] Returns 500 on Stripe API error or database failure
- [ ] All errors logged with: timestamp, event ID, error type, stack trace

### Implementation Notes

**Environment Variables Required**:
```bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

**Pseudocode**:
```typescript
export async function stripeWebhook(req: Request) {
  const sig = req.headers.get('stripe-signature');
  const body = await req.text();  // Raw body (string)

  // Verify signature
  let event;
  try {
    const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY'));
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      Deno.env.get('STRIPE_WEBHOOK_SECRET')
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', {
      timestamp: new Date().toISOString(),
      error: err.message
    });
    return new Response(
      JSON.stringify({ error: 'Invalid signature' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Only process checkout.session.completed
  if (event.type !== 'checkout.session.completed') {
    return new Response(
      JSON.stringify({ received: true }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const session = event.data.object;
  const sessionId = session.id;
  const email = session.customer_email;

  // Check idempotence
  const supabaseAdmin = createClient(
    Deno.env.get('SUPABASE_URL'),
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
  );

  const { data: existing } = await supabaseAdmin
    .from('diagnostics')
    .select('id')
    .eq('stripe_session_id', sessionId)
    .limit(1);

  if (existing && existing.length > 0) {
    return new Response(
      JSON.stringify({ received: true }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Create user (with retries)
  let user;
  let retries = 0;
  while (retries < 3) {
    try {
      const { data, error } = await supabaseAdmin.auth.admin.inviteUserByEmail(email, {
        redirectTo: `${Deno.env.get('APP_URL')}/auth/magic-link-callback`
      });
      if (!error) {
        user = data.user;
        break;
      }
      retries++;
      if (retries < 3) await new Promise(r => setTimeout(r, 1000));
    } catch (err) {
      retries++;
      if (retries < 3) await new Promise(r => setTimeout(r, 1000));
    }
  }

  if (!user) {
    console.error('inviteUserByEmail failed after 3 retries:', { email });
    return new Response(
      JSON.stringify({ error: 'Processing failed' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Insert diagnostic row
  const { error: insertError } = await supabaseAdmin
    .from('diagnostics')
    .insert({
      stripe_session_id: sessionId,
      client_id: user.id,
      paid_at: new Date().toISOString(),
      created_at: new Date().toISOString()
    });

  if (insertError) {
    console.error('Diagnostic insert failed:', { sessionId, error: insertError.message });
    return new Response(
      JSON.stringify({ error: 'Processing failed' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }

  return new Response(
    JSON.stringify({ received: true }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
}
```

---

## 3. POST /functions/v1/chat [MODIFIED]

**Purpose**: Process diagnostic chat request; now with JWT validation & payment status check

**HTTP Method**: POST  
**Content-Type**: application/json  
**Authentication**: Bearer JWT token (Authorization header)  
**CORS**: Allow frontend origin

### Request

**Headers**:
```
POST /functions/v1/chat HTTP/1.1
Host: xyz.supabase.co
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

**Body**:
```json
{
  "message": "Analyze my business model..."
}
```

**Parameters**:
- `message` (STRING, required): User's chat message
- `Authorization` (HEADER, required): Bearer token with JWT

### Response

**Success (200 OK)**:
```json
{
  "response": "Based on your data...",
  "diagnostic_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Error (401 Unauthorized)** — Missing or invalid JWT:
```json
{
  "error": "Unauthorized"
}
```

**Error (403 Forbidden)** — User not paid or retention expired:
```json
{
  "error": "Forbidden"
}
```

**Error (500 Internal Server Error)**:
```json
{
  "error": "Processing failed"
}
```

### Acceptance Criteria

#### JWT Extraction & Validation
- [ ] Reads `Authorization: Bearer <token>` header
- [ ] Returns 401 if header missing or malformed
- [ ] Calls `supabase.auth.getUser(jwt)` to validate signature & expiry
- [ ] Returns 401 if JWT invalid, expired, or signature mismatch
- [ ] Extracts `user.id` (UUID) from validated JWT

#### Payment Status Check
- [ ] Queries: `SELECT paid_at FROM diagnostics WHERE client_id = user.id ORDER BY paid_at DESC LIMIT 1`
- [ ] Returns 403 if no row found (user never paid)
- [ ] Returns 403 if `NOW() - paid_at > '30 days'` (retention expired)
- [ ] Proceeds if `paid_at` is valid and within 30 days

#### Chat Processing
- [ ] Executes diagnostic chat logic (existing implementation)
- [ ] Inserts/updates diagnostics row with response data
- [ ] Returns 200 with chat response + diagnostic_id
- [ ] Response respects RLS: user can only read their own diagnostics

#### Error Messages
- [ ] Generic 401 for all JWT errors (no details)
- [ ] Generic 403 for all payment errors (no details)
- [ ] Frontend interprets: 401 → "Session expired", 403 → "Purchase required"

### Implementation Notes

**Modified Pseudocode** (add to existing /chat function):
```typescript
export async function chat(req: Request) {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL'),
    Deno.env.get('SUPABASE_ANON_KEY')
  );

  // 1. Extract JWT from header
  const authHeader = req.headers.get('Authorization');
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return new Response(
      JSON.stringify({ error: 'Unauthorized' }),
      { status: 401, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const jwt = authHeader.substring(7);

  // 2. Validate JWT
  const { data: { user }, error: userError } = await supabase.auth.getUser(jwt);
  if (userError || !user) {
    return new Response(
      JSON.stringify({ error: 'Unauthorized' }),
      { status: 401, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // 3. Check payment status
  const { data: diagnostics, error: queryError } = await supabase
    .from('diagnostics')
    .select('paid_at')
    .eq('client_id', user.id)
    .order('paid_at', { ascending: false })
    .limit(1);

  if (queryError || !diagnostics || diagnostics.length === 0) {
    return new Response(
      JSON.stringify({ error: 'Forbidden' }),
      { status: 403, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const paidAt = new Date(diagnostics[0].paid_at);
  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
  if (paidAt < thirtyDaysAgo) {
    return new Response(
      JSON.stringify({ error: 'Forbidden' }),
      { status: 403, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // 4. Proceed with existing chat logic
  const { message } = await req.json();
  
  // ... existing diagnostic processing ...
  
  const response = 'Based on your data...';
  const diagnosticId = '550e8400-e29b-41d4-a716-446655440000';

  return new Response(
    JSON.stringify({
      response: response,
      diagnostic_id: diagnosticId
    }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
}
```

---

## 4. GET /auth/magic-link-callback [FRONTEND]

**Purpose**: Handle magic link click, verify OTP, establish session

**Route Type**: Frontend page/component (not backend API)  
**Parameters**: `token=<token>&email=<email>` (URL query params, auto-appended by Supabase)

### Implementation

**Pseudocode** (React/SPA):
```typescript
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createClient } from '@supabase/supabase-js';

export function MagicLinkCallback() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const verifyToken = async () => {
      const params = new URLSearchParams(window.location.search);
      const token = params.get('token');
      const email = params.get('email');

      if (!token || !email) {
        setError('Invalid magic link');
        return;
      }

      const supabase = createClient(
        process.env.REACT_APP_SUPABASE_URL!,
        process.env.REACT_APP_SUPABASE_ANON_KEY!
      );

      const { data, error } = await supabase.auth.verifyOtp({
        email: email,
        token: token,
        type: 'magiclink'
      });

      if (error) {
        setError('Magic link expired or invalid. Please request a new one.');
        return;
      }

      // JWT obtained, store in localStorage
      const { data: { session } } = await supabase.auth.getSession();
      if (session?.access_token) {
        localStorage.setItem('jwt', session.access_token);
      }

      // Redirect to chat
      navigate('/chat?onboarded=true');
    };

    verifyToken();
  }, [navigate]);

  return (
    <div>
      {error ? (
        <div>
          <p>Error: {error}</p>
          <a href="/pricing">Back to pricing</a>
        </div>
      ) : (
        <p>Signing you in...</p>
      )}
    </div>
  );
}
```

### Acceptance Criteria

- [ ] Route: `/auth/magic-link-callback?token=<token>&email=<email>`
- [ ] Extracts `token` and `email` from query params
- [ ] Calls `supabase.auth.verifyOtp({email, token, type: 'magiclink'})`
- [ ] On success: session established, JWT stored in localStorage
- [ ] Redirects to `/chat?onboarded=true`
- [ ] On failure: show error "Link expired or invalid", link to `/pricing`

---

## 5. POST /functions/v1/success.html [FRONTEND]

**Purpose**: Display success message after Stripe payment

**Route Type**: Frontend static page or component  
**Parameters**: `session_id=<session_id>` (URL query param)

### Implementation

**HTML/React Template**:
```html
<div>
  <h1>Payment Successful!</h1>
  <p id="message">Magic link sent to your email. Check your inbox (and spam folder).</p>
  <p>You will be redirected in <span id="countdown">5</span> seconds...</p>
  <a href="/pricing" id="backLink">Or click here to go back</a>
</div>

<script>
  const params = new URLSearchParams(window.location.search);
  const sessionId = params.get('session_id');

  if (!sessionId) {
    document.getElementById('message').textContent = 'Error: No session ID found';
  }

  let count = 5;
  const interval = setInterval(() => {
    count--;
    document.getElementById('countdown').textContent = count;
    if (count <= 0) {
      clearInterval(interval);
      // Wait for user to click email link, or show "check email" message
      // This page is informational; the /auth/magic-link-callback handles the actual signin
    }
  }, 1000);
</script>
```

### Acceptance Criteria

- [ ] Route: `/success.html?session_id=cs_xyz`
- [ ] Shows: "Magic link sent to your email"
- [ ] Auto-redirects (or countdown) after 5 seconds (or shows "Check email" button)
- [ ] No manual email entry (automatic via Stripe)

---

## Error Handling Summary

| Scenario | HTTP Code | Response | Frontend Action |
|----------|-----------|----------|-----------------|
| Missing Authorization header | 401 | `{error: "Unauthorized"}` | Redirect to `/pricing` |
| Invalid/expired JWT | 401 | `{error: "Unauthorized"}` | Redirect to `/pricing` |
| User not paid | 403 | `{error: "Forbidden"}` | Show "Purchase required" |
| Payment retention expired (>30d) | 403 | `{error: "Forbidden"}` | Show "Purchase required" |
| Stripe API error | 500 | `{error: "..."}` | "Processing failed, retry" |
| Database error | 500 | `{error: "..."}` | "Server error, retry" |
| Invalid signature (webhook) | 400 | `{error: "Invalid signature"}` | (Stripe retries) |
| Magic link expired | N/A | (Supabase error) | "Link expired, go to /pricing" |

---

## Security Standards

- **All endpoints**: HTTPS only (browser enforces for Authorization header)
- **Signature verification**: HMAC-SHA256 (Stripe → constructEvent)
- **JWT validation**: Server-side signature + expiry check
- **No secrets in logs**: STRIPE_SECRET_KEY, SERVICE_ROLE_KEY, JWT never logged
- **No secrets in responses**: Error messages generic (no "user not paid" vs "no user")
- **RLS enforced**: All queries on diagnostics filtered by client_id

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-27  
**Review Status**: Ready for implementation
