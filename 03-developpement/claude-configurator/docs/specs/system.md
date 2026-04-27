# System Design — Authentication & Stripe Integration

**Document Type**: Technical System Design  
**Date**: 2026-04-27  
**Status**: Ready for ACT phase  
**Audience**: Engineering, Architecture

---

## Overview

This document describes the complete system architecture for implementing secure, automated user authentication via Stripe payment and Supabase magic link flow. The system ensures that only users who have successfully paid via Stripe can access the /chat function, with data protected via Row-Level Security (RLS) and automatic retention policies.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Browser                               │
├─────────────────────────────────────────────────────────────────┤
│  localStorage (JWT)  →  Authorization: Bearer <jwt>              │
└──────────────────────────────┬──────────────────────────────────┘
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
         ┌──────────────┐           ┌──────────────┐
         │ Frontend App │           │ Stripe.com   │
         ├──────────────┤           ├──────────────┤
         │ /pricing.md  │           │ Checkout UI  │
         │ /success.md  │           │ Payment Proc │
         │ /chat        │           │              │
         │ /auth/...    │           └──────────────┘
         └──────┬───────┘                  ▲
                │                          │
   (1) POST /create-checkout               │
   (2) GET /success.html?session_id        │ (3) User pays
   (3) GET /auth/magic-link-callback       │
   (4) POST /chat (with JWT)               │
                │                          │
                ▼                          │
    ┌────────────────────────────────────────┐
    │   Supabase Edge Functions              │
    │ (HTTP → Edge Runtime)                  │
    ├────────────────────────────────────────┤
    │ • create-checkout()                    │
    │   - Calls Stripe API                   │
    │   - Returns checkout URL               │
    │                                        │
    │ • stripe-webhook()                     │
    │   - Validates signature                │
    │   - Creates user via admin API         │
    │   - Sends magic link                   │
    │   - Inserts diagnostics row            │
    │                                        │
    │ • chat() [MODIFIED]                    │
    │   - Validates JWT from header          │
    │   - Checks paid_at status              │
    │   - Enforces RLS on diagnostics        │
    └───────────┬──────────────────────────┘
                │
                ▼
    ┌────────────────────────────────────────┐
    │   Supabase Backend (Postgres)          │
    │ (Database + Auth)                      │
    ├────────────────────────────────────────┤
    │ auth.users (managed by Supabase)       │
    │ • id (UUID)                            │
    │ • email (UNIQUE)                       │
    │ • encrypted_password                   │
    │ • created_at                           │
    │ • (magic link token stored by SB)      │
    │                                        │
    │ public.diagnostics (new columns)       │
    │ • id (UUID, PK)                        │
    │ • stripe_session_id (VARCHAR UNIQUE)   │
    │ • client_id (UUID FK → auth.users)     │
    │ • paid_at (TIMESTAMP, 30-day marker)   │
    │ • created_at                           │
    │ • content (diagnostic data)            │
    │ • [+ existing columns]                 │
    │                                        │
    │ public.stripe_events (optional audit)  │
    │ • id (UUID, PK)                        │
    │ • stripe_event_id (VARCHAR UNIQUE)     │
    │ • event_type                           │
    │ • processed_at                         │
    │ • response_code                        │
    │ • error_message                        │
    │                                        │
    │ RLS Policies (enforced at DB layer)    │
    │ diagnostics: (auth.uid()=client_id)    │
    │             OR (role='admin')          │
    │                                        │
    │ pg_cron Jobs (automated cleanup)       │
    │ • delete-expired-diagnostics (daily)   │
    │   DELETE FROM diagnostics              │
    │   WHERE paid_at < NOW()-'30 days'      │
    └────────────────────────────────────────┘
                 ▲
                 │
         (Stripe → Webhook)
         POST /functions/v1/stripe-webhook
         stripe-signature: HMAC-SHA256
```

---

## Key Flows

### 1. Payment → User Creation Flow

**Participants**: User, Stripe, Supabase Edge Function, Postgres

**Happy Path** (6 steps):
1. **User initiates payment**
   - Frontend: `POST /functions/v1/create-checkout` (email)
   - Edge Function: Calls Stripe API, returns checkout URL
   - Browser: Redirected to `https://checkout.stripe.com/pay/cs_xyz`

2. **User completes payment**
   - User enters card details (Stripe handles)
   - Stripe processes payment
   - Stripe generates `checkout.session.completed` event

3. **Stripe sends webhook** (5 retries with exponential backoff)
   - `POST /functions/v1/stripe-webhook`
   - Header: `stripe-signature: t=<timestamp>,v1=<signature>`
   - Body: `{id: "evt_...", type: "checkout.session.completed", data: {...}}`

4. **Edge Function validates & processes**
   - Step A: Extract & validate signature via `Stripe.webhooks.constructEvent(body, header, secret)`
   - Step B: If invalid → return 400, log attempt
   - Step C: Check idempotence: `SELECT stripe_session_id FROM diagnostics WHERE stripe_session_id = 'cs_xyz'`
     - If exists → return 200 (already processed)
     - If new → continue to Step D
   - Step D: Extract email from webhook, call `supabase.auth.admin.inviteUserByEmail(email)`
     - On failure: retry 3 times with 1s delay
     - After 3 failures: return 500, log error
   - Step E: Insert diagnostic row: `INSERT INTO diagnostics (stripe_session_id, client_id, paid_at) VALUES (...)`

5. **Supabase sends magic link** (auto, via inviteUserByEmail)
   - Email: "Confirm your sign-in" (Supabase template)
   - Link: `https://app.com/auth/magic-link-callback?token=<token>`
   - Token: Valid 24 hours

6. **User receives magic link**
   - User clicks email link
   - Redirected to `/auth/magic-link-callback?token=XXX`
   - Frontend: Calls `supabase.auth.verifyOtp({email, token, type: 'magiclink'})`
   - JWT obtained, stored in localStorage
   - Redirected to `/chat?onboarded=true`

**Error Cases**:
- Signature invalid → 400, log attempt, no processing
- inviteUserByEmail() fails 3x → 500, log error, Stripe retries
- Database INSERT fails → 500, log error
- Email already exists → Supabase throws, log, return 500

---

### 2. Chat Access & JWT Validation Flow

**Participants**: User (browser), Frontend, /chat Edge Function, Postgres

**Happy Path**:
1. **User sends chat request**
   - Frontend: `POST /functions/v1/chat`
   - Header: `Authorization: Bearer <jwt_token>`
   - Body: `{message: "Analyze my business..."}`

2. **/chat extracts & validates JWT**
   - Extract Authorization header
   - Verify format: `^Bearer\s+.+$`
   - Call `supabase.auth.getUser(jwt)` (validates signature & expiry)
   - Returns: `{user: {id: UUID, email, ...}, aud: "authenticated", ...}`
   - On failure (invalid, expired, no header) → return 401, generic message

3. **Check payment status**
   - Query: `SELECT paid_at FROM diagnostics WHERE client_id = user.id ORDER BY paid_at DESC LIMIT 1`
   - If no row found → return 403 (not paid)
   - If row found and `NOW() - paid_at <= '30 days'::interval` → proceed
   - If `NOW() - paid_at > '30 days'` → return 403 (retention expired)

4. **Execute chat logic**
   - Existing diagnostic processing logic
   - RLS enforced: Query returns only rows where `client_id = user.id` OR `auth.role() = 'admin'`
   - Insert/update diagnostic row with response data
   - Return 200 with diagnostic_id + response

5. **Error responses**
   - 401 Unauthorized: "Session expired. Please sign in again."
   - 403 Forbidden: "Access denied."
   - 500 Internal Server Error: "Processing failed. Please retry."

---

## Security Architecture

### 1. Authentication Layer

**Mechanism**: JWT issued by Supabase auth, validated server-side

**Properties**:
- **Issuer**: Supabase (kid: project-id)
- **Algorithm**: HS256 (HMAC-SHA256)
- **TTL**: 1 hour (3600 seconds)
- **Claims**:
  - `sub`: user UUID
  - `email`: user email
  - `aud`: "authenticated"
  - `iat`: issued at
  - `exp`: expiration (iat + 3600)
  - `role`: user role (e.g., "authenticated", "admin")

**Validation**:
- Signature verified via Supabase secret key (server-side only)
- Expiry checked: `NOW() < exp`
- No client-side decoding without server validation
- Fresh validation on every /chat request (not cached)

**Storage**:
- Frontend: localStorage (survives page reload)
- Transport: Authorization header (HTTPS enforced)
- Never in URL, cookies, or logs

---

### 2. Authorization Layer

**Mechanism**: Row-Level Security (RLS) + paid_at validity window

**RLS Policy**:
```sql
CREATE POLICY "users can view own diagnostics" ON diagnostics
  FOR SELECT USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );

CREATE POLICY "users can insert own diagnostics" ON diagnostics
  FOR INSERT WITH CHECK (
    auth.uid()::uuid IS NOT NULL
  );

CREATE POLICY "users can update own diagnostics" ON diagnostics
  FOR UPDATE USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );

CREATE POLICY "users can delete own diagnostics" ON diagnostics
  FOR DELETE USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );
```

**Payment Window Validation**:
- Every /chat request checks: `NOW() - paid_at <= '30 days'`
- Not cached in JWT (checked on every request)
- User ID verified from JWT, not from request body

---

### 3. Webhook Security

**Mechanism**: HMAC-SHA256 signature verification + idempotence check

**Signature Verification**:
- Stripe includes: `stripe-signature: t=<timestamp>,v1=<hmac>`
- Server calls: `Stripe.webhooks.constructEvent(body, header, secret)`
- Stripe library validates: timestamp (within 5 min), HMAC (matches secret)
- If invalid → return 400, log attempt
- Never process unsigned webhooks

**Idempotence**:
- Check before user creation: `SELECT 1 FROM diagnostics WHERE stripe_session_id = 'cs_xyz'`
- If exists → return 200 immediately
- If new → create user + diagnostic
- Database constraint: `UNIQUE(stripe_session_id)` prevents race conditions

**Retry Logic**:
- On inviteUserByEmail() failure: retry 3 times with 1s delay
- After 3 failures: return 500, log error, let Stripe retry
- Stripe's built-in retry (5x, exponential backoff) handles delivery guarantees

---

### 4. Data Retention & Cleanup

**Mechanism**: pg_cron scheduled deletion of diagnostics rows after 30 days

**Policy**:
- **Delete**: diagnostics rows where `paid_at < NOW() - '30 days'`
- **Keep**: auth.users entries (allows re-purchase, re-authentication)
- **Frequency**: Daily at 2 AM UTC
- **Atomicity**: Single DELETE statement, no application-level logic

**Cron Job Definition**:
```sql
SELECT cron.schedule(
  'delete-expired-diagnostics',
  '0 2 * * *',  -- Daily at 2 AM UTC
  'DELETE FROM diagnostics WHERE paid_at < NOW() - interval ''30 days'''
);
```

---

## Threat Model & Mitigations

| Threat | Attack Vector | Mitigation | Validation |
|--------|------|-----------|------------|
| **JWT Forgery** | Attacker forges JWT, signs with different key | Signature verified via Supabase secret (server-side only) | 401 on invalid signature, expired JWT |
| **Webhook Replay** | Attacker replays Stripe webhook 10 times | stripe_session_id UNIQUE constraint prevents duplicates | Test: replay webhook, verify 1 user + 1 diagnostic |
| **Signature Spoofing** | Attacker crafts webhook with fake HMAC | Stripe.webhooks.constructEvent validates with secret | 400 on invalid signature |
| **Cross-Tenant Access** | User A tries to read User B's diagnostics | RLS policy enforced at DB layer (not app-level) | User A cannot SELECT/UPDATE User B's rows |
| **Data Leakage** | Error messages reveal user existence or payment status | Generic 401/403, no details about paid_at | Test: 403 for unpaid, no "not paid" message |
| **Magic Link Hijacking** | Attacker intercepts email or uses expired link | Link valid 24h, hashed token, verified server-side | Test: 1-hour-old token rejected |
| **Service Downtime** | Webhook fails, user never receives magic link | Stripe retries webhook 5x; app logs failures for manual recovery | Test: Check logs, verify Stripe retry |
| **Unauthorized /chat Access** | Attacker calls /chat without JWT or valid payment | JWT validation + paid_at check on every request | Test: 401 without token, 403 without payment |
| **Paid Status Cache Bypass** | Attacker modifies JWT to inject paid_at claim | paid_at fetched from DB on every request, not from JWT | Test: Old user cannot access after 30 days |

---

## Data Model

### auth.users (Supabase-managed)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PRIMARY KEY | User ID (owned by Supabase) |
| email | VARCHAR | UNIQUE, NOT NULL | Email address |
| encrypted_password | BYTEA | | Password hash (handled by Supabase) |
| email_confirmed_at | TIMESTAMP | | Set after magic link clicked |
| created_at | TIMESTAMP | DEFAULT NOW() | User creation time |

### diagnostics (new auth-gated version)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Diagnostic row ID |
| stripe_session_id | VARCHAR | UNIQUE, NOT NULL | Stripe checkout session ID (idempotence key) |
| client_id | UUID | NOT NULL, FK → auth.users(id) | Ownership link for RLS |
| paid_at | TIMESTAMP WITH TZ | NOT NULL | Purchase timestamp (retention marker) |
| created_at | TIMESTAMP WITH TZ | DEFAULT NOW() | Diagnostic creation |
| content | JSONB | | Diagnostic data (existing column) |
| metadata | JSONB | | Additional metadata |

**Indexes**:
- `idx_diagnostics_client_id` on (client_id) — for user lookups
- `idx_diagnostics_paid_at` on (paid_at) — for retention cleanup
- `idx_diagnostics_stripe_session_id` on (stripe_session_id) — for idempotence check

### stripe_events (optional audit log)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Event record ID |
| stripe_event_id | VARCHAR | UNIQUE, NOT NULL | Stripe event ID (for deduplication) |
| event_type | VARCHAR | NOT NULL | e.g., "checkout.session.completed" |
| processed_at | TIMESTAMP WITH TZ | DEFAULT NOW() | When processed |
| response_code | INT | | HTTP response code (200, 400, 500) |
| error_message | TEXT | | Error details (if failure) |

---

## Deployment Architecture

### Environment Variables (Server-side only)

```bash
# Stripe credentials
STRIPE_PUBLISHABLE_KEY=pk_test_...  # Safe to expose in frontend (read-only)
STRIPE_SECRET_KEY=sk_test_...       # NEVER expose (full access)
STRIPE_PRICE_ID=price_...           # Product price configuration
STRIPE_WEBHOOK_SECRET=whsec_...     # Webhook signature secret

# Supabase credentials
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_ANON_KEY=eyJ...            # Public, read-only (frontend)
SUPABASE_SERVICE_ROLE_KEY=eyJ...    # Admin access, server-side only
```

### Deployment Order

1. **Database**: Apply migrations (columns, constraints, RLS policies, pg_cron)
2. **stripe-webhook**: Deploy Edge Function (must exist for webhooks)
3. **create-checkout**: Deploy Edge Function (frontend calls this)
4. **chat**: Deploy modified /chat (with JWT validation)
5. **Frontend**: Update with JWT integration (localStorage, Authorization header)

---

## Monitoring & Observability

### Logs to Capture

- **Webhook Processing**:
  - Signature validation (pass/fail)
  - User creation (success/fail with error)
  - Idempotence check (already exists / new)
  - Database INSERT (success/fail)

- **/chat Requests**:
  - JWT validation (pass/fail, expiry vs invalid sig)
  - Payment status check (found/not found, within window / expired)
  - RLS enforcement (row count returned)

### Alerts to Create

- Webhook signature validation failures (possible attacker)
- inviteUserByEmail() repeated failures (service issue)
- Diagnostic rows not being cleaned after 30 days (pg_cron failure)
- JWT validation failures >10x per minute (possible attack)

### Metrics to Track

- Payment → chat access time (should be <1 min if instant)
- JWT 401 rate (normal: <1% of requests)
- Webhook processing latency (should be <2s)
- Diagnostic cleanup success rate (should be 100%)

---

## Standards & Conventions

- **API Response Format**: `{status: "success"|"error", data?: {...}, error?: {...}}`
- **Error Codes**: Standard HTTP (200, 400, 401, 403, 500)
- **Timestamps**: TIMESTAMP WITH TIME ZONE (UTC)
- **UUIDs**: gen_random_uuid() in Postgres
- **Logging**: JSON format with timestamp, level, context, message (no secrets)

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-27  
**Next Review**: 2026-05-27 (post-implementation)
