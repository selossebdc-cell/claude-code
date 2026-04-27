# Scope — Feature Breakdown & Acceptance Criteria

**Document Type**: Technical Scope  
**Date**: 2026-04-27  
**Status**: Ready for MODEL phase  
**Audience**: Engineering, QA

---

## Overview

Five major components implement the complete auth/Stripe integration:
1. **create-checkout** (NEW Edge Function)
2. **stripe-webhook** (NEW Edge Function)
3. **chat** function (MODIFY for auth enforcement)
4. **Database Migrations** (MODIFY schema)
5. **Frontend** (MODIFY for JWT integration)

Each component includes acceptance criteria, dependencies, and security requirements.

---

## 1. create-checkout Edge Function

**Purpose**: Generate Stripe checkout session, return session ID to frontend

**HTTP Signature**:
```
POST /functions/v1/create-checkout
Content-Type: application/json

Request:
{
  "email": "user@example.com"
}

Response (200):
{
  "url": "https://checkout.stripe.com/pay/cs_xyz...",
  "sessionId": "cs_xyz..."
}

Response (400/500):
{
  "error": "Invalid email" | "Stripe API error"
}
```

**Acceptance Criteria**:
- [ ] Accepts POST with JSON body (email required, validated)
- [ ] Calls Stripe API with env vars: `STRIPE_PUBLISHABLE_KEY`, `STRIPE_PRICE_ID`
- [ ] Returns valid Stripe Checkout URL + session ID
- [ ] Sets success URL → `{APP_URL}/success.html?session_id=cs_xyz`
- [ ] Sets cancel URL → `{APP_URL}/pricing.html`
- [ ] Returns 400 if email invalid or missing
- [ ] Returns 500 if Stripe API fails (with error message, no key leakage)
- [ ] No Stripe secret key exposed in response or logs

**Dependencies**:
- Stripe API credentials (STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, STRIPE_PRICE_ID)
- Environment vars configured before deployment
- Frontend ready to call endpoint

**Security Requirements**:
- [ ] STRIPE_SECRET_KEY **never** returned to client
- [ ] STRIPE_PRICE_ID hardcoded in env var (not from request)
- [ ] Email validation prevents injection
- [ ] HTTPS enforced (Supabase Edge Functions default)
- [ ] CORS configured to allow frontend origin only

---

## 2. stripe-webhook Edge Function

**Purpose**: Receive Stripe webhook, verify signature, create user, send magic link

**HTTP Signature**:
```
POST /functions/v1/stripe-webhook
Content-Type: application/json
stripe-signature: t=<timestamp>,v1=<signature>

Request (Stripe sends):
{
  "id": "evt_...",
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_xyz...",
      "customer_email": "user@example.com"
    }
  }
}

Response (200):
{
  "received": true
}

Response (400):
{
  "error": "Invalid signature"
}
```

**Acceptance Criteria**:

### Signature Verification (Q-007)
- [ ] Extracts `stripe-signature` header
- [ ] Calls `Stripe.webhooks.constructEvent(body, header, STRIPE_WEBHOOK_SECRET)`
- [ ] Returns 400 Bad Request if signature invalid
- [ ] **Logs** invalid signature event (includes timestamp, IP, attempt details)
- [ ] Does NOT attempt to process invalid events

### Idempotence (Q-002)
- [ ] Checks if `stripe_session_id` already exists in `diagnostics` table
- [ ] If exists: return 200 (success) without creating duplicate user
- [ ] If new: proceed to user creation
- [ ] Database constraint: `UNIQUE(stripe_session_id)` prevents race conditions (Q-009)

### User Creation (Q-003)
- [ ] Extracts email from `checkout.session.completed.data.object.customer_email`
- [ ] Calls `supabase.auth.admin.inviteUserByEmail(email, {redirectTo: '/auth/magic-link-callback'})`
- [ ] **Retries immediately 3 times with 1s delay** if inviteUserByEmail() fails (Q-001)
- [ ] After 3 failures: log event with error details, return 500

### Diagnostic Entry (Q-003)
- [ ] Inserts row into `diagnostics` table:
  ```sql
  INSERT INTO diagnostics (
    stripe_session_id,
    client_id,
    paid_at,
    created_at
  ) VALUES (
    'cs_xyz...',
    (SELECT id FROM auth.users WHERE email = 'user@example.com'),
    NOW(),
    NOW()
  )
  ```
- [ ] `client_id` = UUID of newly created auth.users entry
- [ ] `paid_at` = current timestamp (used for 30-day retention)

### Error Handling
- [ ] Returns 200 on success (webhook received & processed)
- [ ] Returns 400 on invalid signature (never processes)
- [ ] Returns 500 on Stripe API error or database failure (after retries)
- [ ] All errors logged with: timestamp, event ID, error type, stack trace

**Dependencies**:
- Stripe webhook secret (STRIPE_WEBHOOK_SECRET) configured in env
- Supabase auth admin client initialized with service role key
- diagnostics table created with stripe_session_id UNIQUE constraint
- stripe_events table created (optional deduplication audit log)

**Security Requirements**:
- [ ] Signature verification is **mandatory** (not optional)
- [ ] STRIPE_WEBHOOK_SECRET stored in env var, never logged
- [ ] Service role key used for admin.inviteUserByEmail() (RLS does not apply)
- [ ] Email from webhook trusted (Stripe-signed, not user-provided)
- [ ] Database transactions ensure atomicity (stripe_session_id + diagnostics row)
- [ ] No sensitive data (JWT, webhook body) logged in plain text
- [ ] Webhook endpoint rate-limited (Supabase default, or custom check)

---

## 3. chat Function — Modify for Authentication

**Purpose**: Extract & validate JWT, enforce payment status, return diagnostic results

**HTTP Signature**:
```
POST /functions/v1/chat
Content-Type: application/json
Authorization: Bearer <jwt_token>

Request:
{
  "message": "Analyze my business..."
}

Response (200):
{
  "response": "Based on your data...",
  "diagnostic_id": "uuid"
}

Response (401):
{
  "error": "Unauthorized"
}

Response (403):
{
  "error": "Forbidden"
}
```

**Acceptance Criteria**:

### JWT Extraction & Validation (Q-004)
- [ ] Reads `Authorization: Bearer <token>` header
- [ ] Returns 401 if header missing or malformed
- [ ] Calls `supabase.auth.getUser(jwt)` to validate signature & expiry
- [ ] Returns 401 if JWT invalid, expired, or signature mismatch
- [ ] Extracts `user.id` (UUID) from validated JWT

### Payment Status Check (Q-005)
- [ ] Queries diagnostics table: `SELECT paid_at FROM diagnostics WHERE client_id = user.id`
- [ ] Returns 403 if no row found (user never paid)
- [ ] Returns 403 if `paid_at` is NULL (data corrupted, should not happen)
- [ ] Returns 403 if `NOW() - paid_at > '30 days'::interval` (retention expired, Q-008)
- [ ] Proceeds if `paid_at` is valid and within 30 days

### Chat Processing
- [ ] Executes diagnostic chat logic (existing implementation)
- [ ] Inserts/updates diagnostics row with new response data
- [ ] Returns 200 with chat response + diagnostic_id
- [ ] Response respects RLS: user can only read their own diagnostics (Q-006)

### Error Messages
- [ ] Generic 401 for all JWT errors (no "token expired" vs "invalid signature")
- [ ] Generic 403 for all payment errors (no "not paid" vs "retention expired")
- [ ] Frontend interprets status code: 401 → "Session expired", 403 → "Purchase required"

**Dependencies**:
- JWT from localStorage (frontend provides)
- diagnostics table with paid_at column
- Existing /chat logic (diagnostic processing)

**Security Requirements**:
- [ ] JWT validation via Supabase auth library (cryptographically signed)
- [ ] RLS policy enforced: `(auth.uid() = client_id) OR (auth.role() = 'admin')`
- [ ] No JWT decoding without signature validation
- [ ] No expiry check bypassed (1-hour TTL enforced)
- [ ] No user ID spoofing (extracted from JWT, not request body)
- [ ] Paid status checked on **every request** (not cached in JWT)
- [ ] Error messages do not leak user existence or payment status

---

## 4. Database Migrations

**Purpose**: Create tables, constraints, and indexes for auth/Stripe flow

**Acceptance Criteria**:

### Table: diagnostics (New Columns)
- [ ] Column: `stripe_session_id` (VARCHAR, UNIQUE, NOT NULL)
- [ ] Column: `client_id` (UUID, FOREIGN KEY to auth.users, NOT NULL)
- [ ] Column: `paid_at` (TIMESTAMP WITH TIME ZONE, NOT NULL)
- [ ] Column: `created_at` (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())
- [ ] Existing columns preserved (content, metadata, etc.)

```sql
ALTER TABLE diagnostics ADD COLUMN stripe_session_id VARCHAR UNIQUE NOT NULL;
ALTER TABLE diagnostics ADD COLUMN client_id UUID NOT NULL REFERENCES auth.users(id);
ALTER TABLE diagnostics ADD COLUMN paid_at TIMESTAMP WITH TIME ZONE NOT NULL;
CREATE INDEX idx_diagnostics_client_id ON diagnostics(client_id);
CREATE INDEX idx_diagnostics_paid_at ON diagnostics(paid_at);
```

### Table: stripe_events (New, Audit/Deduplication)
Optional but recommended for webhook tracking:
```sql
CREATE TABLE stripe_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stripe_event_id VARCHAR UNIQUE NOT NULL,
  event_type VARCHAR NOT NULL,
  processed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  response_code INT,
  error_message TEXT
);
CREATE INDEX idx_stripe_events_event_id ON stripe_events(stripe_event_id);
```

### RLS Policies (Q-006)
- [ ] Enable RLS on diagnostics table
- [ ] Policy: SELECT `(auth.uid()::uuid = client_id) OR (auth.role() = 'admin')`
- [ ] Policy: INSERT `auth.uid()::uuid IS NOT NULL` (only authenticated users)
- [ ] Policy: UPDATE/DELETE `(auth.uid()::uuid = client_id) OR (auth.role() = 'admin')`

### pg_cron Job (Q-008)
- [ ] Create cron job: `DELETE FROM diagnostics WHERE paid_at < NOW() - '30 days'::interval`
- [ ] Frequency: Run daily at 2 AM UTC
- [ ] Verify: SELECT count from diagnostics shows decreasing rows for old paid_at values
- [ ] Keep auth.users untouched (allows re-purchase)

```sql
SELECT cron.schedule(
  'delete-expired-diagnostics',
  '0 2 * * *',  -- Daily at 2 AM UTC
  'DELETE FROM diagnostics WHERE paid_at < NOW() - interval ''30 days'''
);
```

**Dependencies**:
- Migration tool (Supabase CLI, or manual SQL)
- Existing diagnostics table (add columns)
- pg_cron extension enabled in Supabase project

**Security Requirements**:
- [ ] RLS enforced before any data returned (not bypassed in Edge Functions)
- [ ] stripe_session_id uniqueness prevents INSERT race conditions
- [ ] FOREIGN KEY constraint ensures referential integrity
- [ ] Cleanup job uses server time (NOW()), not client time
- [ ] Deleted data cannot be recovered (audit log optional, not required)

---

## 5. Frontend — Integrate JWT

**Purpose**: Store JWT in localStorage, send in Authorization header, handle auth flows

**Acceptance Criteria**:

### Magic Link Callback (New Page/Component)
- [ ] Route: `/auth/magic-link-callback?token=<token>`
- [ ] Extracts `token` from query param
- [ ] Calls `supabase.auth.verifyOtp({email, token, type: 'magiclink'})`
- [ ] On success: session established, JWT stored in localStorage, redirect `/chat?onboarded=true`
- [ ] On failure: show error "Link expired or invalid", link to `/pricing`
- [ ] Magic link valid 24h (Supabase default, Q-011)

### JWT Storage (Q-004, Q-015)
- [ ] Uses `localStorage.setItem('jwt', token)` after successful sign-in
- [ ] Persists across browser refresh (localStorage survives page reload)
- [ ] Cleared on logout or JWT expiry (401 response)

### /chat Authorization Header
- [ ] Reads JWT from localStorage: `const token = localStorage.getItem('jwt')`
- [ ] Sends in every `/chat` request:
  ```javascript
  fetch('/functions/v1/chat', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({message: userInput})
  })
  ```
- [ ] On 401 response: clear localStorage, redirect `/pricing` ("Session expired")
- [ ] On 403 response: show error ("You need to purchase to access this feature")

### Success Page (Q-006, Q-010)
- [ ] Route: `/success.html?session_id=cs_xyz`
- [ ] Shows: "Magic link sent to your email. Check your inbox (and spam folder)."
- [ ] Auto-redirect after 5 seconds to `/auth/magic-link-callback` (or wait for user click on link)
- [ ] Or optionally: "Waiting for verification..." with manual "Check email" button
- [ ] No manual email entry (automatic via Stripe)

### Error Handling (Q-016)
- [ ] 401 Unauthorized: "Your session has expired. Log in again."
- [ ] 403 Forbidden: "You need to complete your purchase to access this feature."
- [ ] Network error: "Connection failed. Please retry."
- [ ] Stripe error: "Payment processing failed. Please try again."

**Dependencies**:
- Supabase client library (JavaScript)
- localStorage API (all modern browsers)
- `/auth/magic-link-callback` route/page implemented
- Success page `/success.html` created

**Security Requirements**:
- [ ] localStorage only (not sessionStorage; must survive refresh)
- [ ] JWT never logged to console or sent in query params
- [ ] HTTPS enforced (browser refuses to send Authorization header over HTTP)
- [ ] No JWT decoded client-side (validation server-side only)
- [ ] On 401: immediately clear localStorage to prevent stale token usage
- [ ] CSRF protection (if forms used; Supabase handles by default)

---

## Cross-Component Dependencies

| Component | Depends On | Critical Path |
|-----------|-----------|----------------|
| create-checkout | STRIPE_PUBLISHABLE_KEY, STRIPE_PRICE_ID env vars | Must exist before frontend can call |
| stripe-webhook | STRIPE_WEBHOOK_SECRET, diagnostics table, auth.users | Webhook cannot process without schema |
| chat function | diagnostics.stripe_session_id, RLS policies, paid_at column | Must validate payment status |
| Frontend | /auth/magic-link-callback route, localStorage API | Cannot sign in without callback |
| pg_cron job | diagnostics table, paid_at column | Cleanup depends on migration completion |

---

## Deployment Order

1. **Database Migrations** (diagnostics columns, stripe_events table, RLS policies, pg_cron)
2. **stripe-webhook Edge Function** (must exist before Stripe sends webhooks)
3. **create-checkout Edge Function** (frontend calls this to start flow)
4. **chat Function** (modified with JWT validation)
5. **Frontend** (localStorage + Authorization header integration)

---

## Success Checklist

- [ ] All 5 components implemented with acceptance criteria met
- [ ] No secrets exposed (keys in env vars, not code)
- [ ] RLS tested: user A cannot see user B's diagnostics
- [ ] Webhook retries work: simulate inviteUserByEmail() failure, verify 3 retries + log
- [ ] Idempotence tested: replay webhook with same session_id, verify no duplicate user
- [ ] 30-day cleanup tested: insert old row, verify deleted within 24h
- [ ] JWT expiry tested: wait 1h, verify 401 on /chat request
- [ ] E2E flow tested: complete payment → receive magic link → click link → access /chat

