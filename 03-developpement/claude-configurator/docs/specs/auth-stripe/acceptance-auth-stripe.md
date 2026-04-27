# Acceptance Criteria — Quality Gates & E2E Testing

**Document Type**: QA & Validation  
**Date**: 2026-04-27  
**Status**: Ready for MODEL phase  
**Audience**: QA, Engineering, Product

---

## Overview

This document defines all quality gates that must pass before the auth/Stripe feature ships. Includes:
- End-to-end success criteria
- Security validation checklist
- Data retention verification
- E2E test cases with detailed steps

---

## Part 1: End-to-End Success Criteria

### E2E Flow: Payment → Magic Link → Chat Access

**Precondition**: Feature deployed to staging environment with all Edge Functions, migrations, and frontend code live.

**Happy Path Test**:
1. User navigates to `/pricing.html`
2. User enters email: `test@example.com`
3. User clicks "Buy Digital Setup (€149)"
4. Clicks on create-checkout button (or form submission)
5. **Verify**: Redirected to Stripe Checkout URL (external, not app error)
6. User enters Stripe test card: `4242 4242 4242 4242`
7. User enters expiry: `12/25`, CVC: `123`
8. User completes payment
9. **Verify**: Redirected to `/success.html?session_id=cs_...`
10. **Verify**: Page displays "Magic link sent to test@example.com"
11. User checks email inbox (or test email provider)
12. **Verify**: Email received with subject containing "magic link" or "confirm"
13. User clicks link in email: `https://app.com/auth/magic-link-callback?token=<token>`
14. **Verify**: Automatically signs in (no manual password entry)
15. **Verify**: Redirected to `/chat?onboarded=true`
16. **Verify**: Chat interface visible and functional
17. User types: "Analyze my business"
18. **Verify**: /chat returns 200 with diagnostic response
19. **Verify**: Diagnostic data stored with user ID = auth.uid()
20. User opens new browser tab, navigates to `/chat`
21. **Verify**: JWT from localStorage still valid, /chat accessible
22. User closes browser (clears RAM)
23. User reopens browser, navigates to `/chat`
24. **Verify**: JWT from localStorage persists, /chat still accessible
25. Admin user logs in, queries diagnostics table
26. **Verify**: Admin can see test@example.com's diagnostic row
27. Wait 1 hour
28. User makes new /chat request
29. **Verify**: JWT expired (401 returned), user redirected to /pricing
30. User can re-purchase or request new magic link (future feature)

**Expected Result**: Green across all 30 steps. No errors, no 5xx responses, full functional flow.

---

## Part 2: Security Validation Checklist

### 2.1 JWT Security

- [ ] **JWT Signature Validation**
  - Test: Call /chat without Authorization header → 401 Unauthorized
  - Test: Call /chat with malformed JWT (random string) → 401 Unauthorized
  - Test: Call /chat with JWT signed by different key → 401 Unauthorized
  - Test: Call /chat with expired JWT (wait 1h 1min) → 401 Unauthorized
  - Verify: No 200 response without valid, non-expired JWT

- [ ] **JWT Expiry Enforcement**
  - Test: At T=0, sign user in, check JWT claim `exp`
  - Test: At T=59m, /chat request succeeds (200)
  - Test: At T=61m, /chat request fails (401)
  - Verify: JWT exactly 1 hour (3600 seconds)

- [ ] **User ID Extraction**
  - Test: Call /chat with valid JWT for user A
  - Test: Verify diagnostic row has `client_id` = user A's auth.users.id (not spoofed)
  - Verify: No way for attacker to change client_id via request body or headers

### 2.2 Stripe Webhook Security

- [ ] **Signature Verification (Q-007)**
  - Test: Send webhook without `stripe-signature` header → 400 Bad Request
  - Test: Send webhook with invalid signature → 400 Bad Request
  - Test: Send webhook with forged signature (attacker HMAC) → 400 Bad Request
  - Test: Send legitimate webhook with correct signature → 200 OK
  - Verify: No event processed if signature invalid
  - Verify: 400 response logged with timestamp, IP, attempt details

- [ ] **Secret Key Protection**
  - Test: Grep codebase for STRIPE_WEBHOOK_SECRET (should only appear in env var reference)
  - Test: Verify STRIPE_WEBHOOK_SECRET never logged (even on error)
  - Test: Verify stripe-webhook function returns 400, not internal error details
  - Verify: No secrets leaked in error messages

### 2.3 RLS (Row-Level Security)

- [ ] **User Isolation**
  - Setup: Create 2 test users (userA, userB), both pay
  - Test: User A logs in, calls /chat, saves diagnostic_id_A
  - Test: User A tries to access User B's diagnostic via direct query → 403 (RLS blocks)
  - Test: User A modifies JWT (fakes user_id = B's ID) → /chat still sees only A's data (JWT validated server-side)
  - Test: User B logs in, calls /chat
  - Test: User B's diagnostic row is different from User A's
  - Verify: RLS policy `(auth.uid()::uuid = client_id) OR (auth.role() = 'admin')` working
  - Verify: Each user sees exactly their own diagnostics, no cross-contamination

- [ ] **Admin Override**
  - Setup: Create admin user with role = 'admin' in Supabase
  - Test: Admin logs in, calls /chat
  - Test: Admin queries diagnostics table directly (via Supabase dashboard or API)
  - Verify: Admin sees all diagnostics rows (User A, User B, etc.)
  - Verify: Admin can read/update/delete any diagnostic (role override works)
  - Verify: Regular user still cannot see other users' data

- [ ] **RLS Enforcement**
  - Test: Verify RLS enabled on diagnostics table: `SELECT relrowsecurity FROM pg_class WHERE relname='diagnostics'` → true
  - Test: Verify policies exist: `SELECT * FROM pg_policies WHERE tablename='diagnostics'`
  - Verify: At least 3 policies (SELECT, INSERT, UPDATE/DELETE)

### 2.4 Idempotence (Webhook Replay Safety)

- [ ] **Stripe Session Uniqueness (Q-002, Q-009)**
  - Setup: Capture real Stripe webhook event, extract session_id = `cs_xyz`
  - Test: Send webhook with event to stripe-webhook
  - Verify: Row inserted into diagnostics with stripe_session_id = `cs_xyz`
  - Test: Replay exact same webhook immediately
  - Verify: 200 OK response (idempotent)
  - Verify: No duplicate row in diagnostics (UNIQUE constraint enforced)
  - Verify: User creation called only once (check Supabase auth.users, only 1 entry for email)
  - Test: Simulate simultaneous webhooks (same session_id, 2 requests in parallel)
  - Verify: Only 1 diagnostic row created (database constraint prevents race, Q-009)

- [ ] **Session ID Storage**
  - Test: Query diagnostics table schema
  - Verify: Column `stripe_session_id` exists, type VARCHAR, UNIQUE constraint exists
  - Verify: Index on stripe_session_id for fast lookups

### 2.5 Webhook Retry Logic (Q-001)

- [ ] **Immediate Retries on Failure**
  - Simulate: Mock supabase.auth.admin.inviteUserByEmail() to fail on first 2 calls, succeed on 3rd
  - Test: Send webhook to stripe-webhook
  - Verify: inviteUserByEmail() called exactly 3 times (immediate, no exponential backoff)
  - Verify: Diagnostic row created after 3rd retry succeeds
  - Verify: Response is 200 OK (success, not temporary failure)
  - Verify: No background queue created (retries happen synchronously)

- [ ] **Failure Logging**
  - Simulate: Mock inviteUserByEmail() to fail all 3 attempts
  - Test: Send webhook
  - Verify: 500 Internal Server Error returned
  - Verify: Error event logged with: timestamp, webhook event ID, error message, stack trace
  - Verify: STRIPE_WEBHOOK_SECRET never appears in logs

### 2.6 Data Retention & Cleanup (Q-008)

- [ ] **30-Day Deletion**
  - Setup: Insert diagnostic row with `paid_at = NOW() - '31 days'::interval`
  - Test: Run pg_cron job manually (or wait for scheduled execution at 2 AM UTC)
  - Verify: Row deleted from diagnostics table
  - Verify: Row does NOT exist in auth.users (user still exists, can re-purchase)
  - Verify: Deletion happened within 24 hours of expected time

- [ ] **Row Preservation Before 30 Days**
  - Setup: Insert diagnostic row with `paid_at = NOW() - '29 days'::interval`
  - Test: Run pg_cron cleanup job
  - Verify: Row NOT deleted (still in diagnostics table)
  - Verify: 1 day later, row is deleted

- [ ] **auth.users Not Deleted**
  - Setup: Insert diagnostic row and corresponding auth.users entry, set paid_at = NOW() - '31 days'
  - Test: Run pg_cron cleanup
  - Verify: Diagnostic row deleted
  - Verify: auth.users entry still exists (user can login if they still have JWT, or request new magic link on re-purchase)

- [ ] **Cleanup Job Scheduled**
  - Test: Query cron.job table in Supabase
  - Verify: Job named "delete-expired-diagnostics" exists
  - Verify: Schedule = '0 2 * * *' (daily at 2 AM UTC)
  - Verify: Command = `DELETE FROM diagnostics WHERE paid_at < NOW() - interval '30 days'`

### 2.7 Authorization Header Security (Q-004)

- [ ] **Bearer Token Format**
  - Test: Call /chat with `Authorization: Bearer <jwt>` → 200 OK (if valid)
  - Test: Call /chat with `Authorization: <jwt>` (no Bearer prefix) → 401 Unauthorized
  - Test: Call /chat with `Authorization: Basic <base64>` → 401 Unauthorized
  - Test: Call /chat with `Authorization: ""` (empty string) → 401 Unauthorized
  - Verify: Only `Authorization: Bearer <jwt>` accepted

- [ ] **Header Case Sensitivity**
  - Test: Call /chat with `authorization: Bearer <jwt>` (lowercase header) → 200 OK
  - Verify: Header parsing is case-insensitive (HTTP standard)

- [ ] **No JWT in URL**
  - Test: Verify create-checkout, stripe-webhook, /chat do NOT accept `?token=<jwt>` in URL
  - Test: Verify JWT never appears in query params or logs
  - Verify: LocalStorage used exclusively (not URL-based)

---

## Part 3: Data Retention Validation

### 3.1 pg_cron Execution

**Test Script** (pseudo-code):
```sql
-- Insert test row with old paid_at
INSERT INTO diagnostics (stripe_session_id, client_id, paid_at, created_at)
VALUES ('test_session_old', <user_uuid>, NOW() - INTERVAL '31 days', NOW());

-- Check row exists
SELECT COUNT(*) FROM diagnostics WHERE stripe_session_id = 'test_session_old'; -- Should be 1

-- Wait for cron execution (or manually trigger in Supabase UI)
-- Check pg_cron job ran
SELECT * FROM cron.job_run_details WHERE job_name = 'delete-expired-diagnostics' ORDER BY start_time DESC LIMIT 1;

-- Verify row deleted
SELECT COUNT(*) FROM diagnostics WHERE stripe_session_id = 'test_session_old'; -- Should be 0
```

**Acceptance**:
- [ ] Test row inserted successfully
- [ ] pg_cron job executed at scheduled time (2 AM UTC ±5 min)
- [ ] Test row deleted after execution
- [ ] Job execution time logged in cron.job_run_details
- [ ] No errors in cron job logs

### 3.2 Fresh Data Retention

**Test Script**:
```sql
-- Insert test row with recent paid_at
INSERT INTO diagnostics (stripe_session_id, client_id, paid_at, created_at)
VALUES ('test_session_fresh', <user_uuid>, NOW() - INTERVAL '10 days', NOW());

-- Check row exists after cleanup
SELECT COUNT(*) FROM diagnostics WHERE stripe_session_id = 'test_session_fresh'; -- Should still be 1
```

**Acceptance**:
- [ ] Fresh row NOT deleted by pg_cron
- [ ] Boundary tested: 29 days (kept), 30 days (deleted), 31 days (deleted)

---

## Part 4: E2E Test Cases (7-8 Detailed Scenarios)

### Test Case 1: Happy Path (Payment → Chat)

**Objective**: Verify complete end-to-end flow works

**Steps**:
1. User navigates to `/pricing.html`
2. Enters email: `e2e-test-1@example.com`
3. Clicks "Buy Now"
4. Completes Stripe payment with test card `4242 4242 4242 4242`
5. Receives magic link email
6. Clicks magic link
7. Auto-signs in, redirected to `/chat?onboarded=true`
8. Sends message: "What's my revenue?"
9. /chat returns diagnostic response with 200 OK

**Expected Result**: All steps succeed, user can chat

**Defect Criteria**: Any 4xx/5xx error, no email received, JWT invalid, chat returns error

---

### Test Case 2: JWT Validation (Invalid Token)

**Objective**: Verify /chat rejects invalid JWT

**Steps**:
1. Construct invalid JWT: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.invalid`
2. Call `/chat` with header: `Authorization: Bearer <invalid_jwt>`
3. Expect: 401 Unauthorized

**Expected Result**: 401 response, no diagnostic data returned

**Defect Criteria**: 200 response, 500 error, data leaked

---

### Test Case 3: JWT Expiration (1 Hour Boundary)

**Objective**: Verify JWT expires after 1 hour

**Steps**:
1. User signs in, obtains JWT
2. Extract `exp` claim from JWT
3. Calculate: current_time = NOW(), expiry_time = exp
4. Verify: expiry_time - current_time ≈ 3600 seconds (±10 sec tolerance)
5. Call /chat at T=0, T=30m, T=59m → all succeed (200)
6. Wait until T=61m (or mock clock)
7. Call /chat at T=61m → fails (401)

**Expected Result**: JWT valid for exactly 1 hour, then expires

**Defect Criteria**: Expires early (<1h), lasts >1h, no error on expiry

---

### Test Case 4: RLS Isolation (User A Cannot See User B)

**Objective**: Verify RLS prevents cross-user access

**Setup**:
- User A: `rls-test-a@example.com` (paid, diagnostic_id = UUID_A)
- User B: `rls-test-b@example.com` (paid, diagnostic_id = UUID_B)

**Steps**:
1. User A signs in, obtains JWT_A
2. User A calls /chat, creates diagnostic (stored with client_id = UUID_A)
3. User B signs in, obtains JWT_B
4. User B calls /chat, creates diagnostic (stored with client_id = UUID_B)
5. User A attempts: SELECT * FROM diagnostics WHERE id = UUID_B (with User A's JWT)
6. Expect: RLS blocks query, 0 rows returned (or 403 error)
7. User A attempts to modify their own diagnostic: UPDATE diagnostics SET content = '...' WHERE id = UUID_A
8. Expect: 200 OK (owns row)
9. User B attempts to modify User A's diagnostic: UPDATE diagnostics SET content = '...' WHERE id = UUID_A (with JWT_B)
10. Expect: RLS blocks, 0 rows updated

**Expected Result**: Each user sees only their own diagnostics

**Defect Criteria**: User A can see User B's data, cross-user modification succeeds

---

### Test Case 5: Idempotence (Webhook Replay)

**Objective**: Verify no duplicate user on webhook replay

**Setup**:
- Capture real Stripe webhook event: `checkout.session.completed` with session_id = `cs_test_1`
- Event contains email = `idempotent-test@example.com`

**Steps**:
1. Send webhook to `/functions/v1/stripe-webhook` → 200 OK
2. Verify: User created in auth.users (count = 1 for email)
3. Verify: Diagnostic row inserted (stripe_session_id = cs_test_1)
4. Send exact same webhook again → 200 OK
5. Verify: auth.users count still = 1 (no duplicate)
6. Verify: diagnostics count still = 1 (no duplicate row, UNIQUE constraint held)
7. Verify: inviteUserByEmail() called once per webhook (not twice on replay)

**Expected Result**: Webhook idempotent, no duplicates

**Defect Criteria**: Duplicate user created, duplicate diagnostic row, error on replay

---

### Test Case 6: Webhook Signature Validation (Attacker Forgery)

**Objective**: Verify invalid signature rejected

**Steps**:
1. Construct fake webhook event (random JSON)
2. Calculate invalid signature: `HMAC-SHA256(body, "wrong_secret")`
3. Send to `/functions/v1/stripe-webhook` with:
   - Body: fake event
   - Header: `stripe-signature: t=<timestamp>,v1=<invalid_sig>`
4. Expect: 400 Bad Request
5. Verify: No user created, no diagnostic inserted
6. Verify: Event logged (timestamp, attempt, failure reason)

**Expected Result**: 400 response, no data created

**Defect Criteria**: 200 response, user created, no error log

---

### Test Case 7: Payment Status Check (Unpaid User)

**Objective**: Verify /chat rejects unpaid users

**Setup**:
- Manually insert auth.users entry (simulate unpaid user)
- Create JWT for this user

**Steps**:
1. Call /chat with JWT for unpaid user
2. Expect: 403 Forbidden
3. Verify: No diagnostic data returned
4. Verify: No error message revealing payment status ("You haven't paid" is too specific)
5. Generic message: "Forbidden" or "Access denied"

**Expected Result**: 403 response for unpaid user

**Defect Criteria**: 200 response, data returned, 500 error

---

### Test Case 8: Data Retention Cleanup (30-Day Expiry)

**Objective**: Verify old diagnostics deleted, auth.users kept

**Setup**:
- Insert diagnostic: stripe_session_id = `cleanup_test`, paid_at = NOW() - 31 days
- Insert auth.users: email = `cleanup-test@example.com`
- Link diagnostic to this user (client_id = UUID)

**Steps**:
1. Verify: diagnostic row exists (COUNT = 1)
2. Verify: auth.users row exists for email
3. Trigger pg_cron cleanup (manually or wait 24h)
4. Verify: diagnostic row deleted (COUNT = 0)
5. Verify: auth.users row still exists (user can re-purchase)
6. Verify: Cleanup happened within 24h of 2 AM UTC

**Expected Result**: Diagnostic deleted, user kept

**Defect Criteria**: User deleted, diagnostic not deleted, cleanup failed to run

---

## Part 5: Security Checklist (Secure-by-Design Framework)

### 5.1 Threat Model: JWT Forgery / Unauthorized Access

**Threat**: Attacker forges JWT or modifies HTTP request to access `/chat` without paying

**Controls**:
- [ ] JWT signature verified via Supabase (cryptographic signing)
- [ ] JWT never decoded without validation
- [ ] User ID extracted from JWT, not request body
- [ ] paid_at checked on every /chat request (not cached in JWT)
- [ ] 1-hour JWT expiry enforces re-authentication
- [ ] RLS policy `(auth.uid() = client_id)` enforced at DB layer
- [ ] No generic "admin override" accessible to users

**Test**: Attempt to forge JWT, modify request, bypass paid_at check → all fail with 401/403

---

### 5.2 Threat Model: Webhook Replay / Duplicate Users

**Threat**: Attacker replays Stripe webhook to create duplicate accounts or cause race conditions

**Controls**:
- [ ] Signature verification prevents attacker-forged webhooks
- [ ] Idempotence via `stripe_session_id` UNIQUE constraint
- [ ] Database constraint enforced (no application-level check only)
- [ ] Webhook processed serially (Stripe sends one at a time)

**Test**: Replay webhook 10 times, verify only 1 user and 1 diagnostic row created

---

### 5.3 Threat Model: Stripe Secret Leakage

**Threat**: Attacker obtains STRIPE_WEBHOOK_SECRET from logs, code, or error messages

**Controls**:
- [ ] STRIPE_WEBHOOK_SECRET in env var only (not hardcoded)
- [ ] Never logged (even on error)
- [ ] Error messages generic ("Invalid signature") not revealing secret
- [ ] STRIPE_SECRET_KEY never sent to client

**Test**: Grep logs for "STRIPE_WEBHOOK_SECRET", "STRIPE_SECRET_KEY" → 0 results

---

### 5.4 Threat Model: Cross-Tenant Data Leakage

**Threat**: User A reads User B's diagnostics via RLS bypass

**Controls**:
- [ ] RLS enabled on diagnostics table
- [ ] Policy: `(auth.uid()::uuid = client_id) OR (auth.role() = 'admin')`
- [ ] Enforced at SQL layer (not bypassed by application)
- [ ] Admin role restricted to Supabase-created users (not accessible via frontend)

**Test**: User A cannot SELECT, UPDATE, or DELETE User B's rows

---

### 5.5 Threat Model: Magic Link Hijacking

**Threat**: Attacker intercepts magic link email or uses expired link

**Controls**:
- [ ] Magic link sent via Supabase (email verified)
- [ ] Link valid 24 hours (Supabase default)
- [ ] Link contains hashed token (not plaintext)
- [ ] /auth/magic-link-callback validates token before signin
- [ ] Old/replayed links rejected

**Test**: Attempt to use expired link → 401 or redirect to login

---

### 5.6 Threat Model: JWT Stored Insecurely

**Threat**: Attacker reads JWT from localStorage (XSS) or query params

**Controls**:
- [ ] JWT in localStorage, not sessionStorage (survives page reload, requires persistent storage)
- [ ] JWT never in URL query params
- [ ] JWT never logged or printed to console
- [ ] HTTPS enforced (browser prevents HTTP Authorization header)

**Test**: Inspect browser localStorage, verify JWT present after sign-in; verify NOT in URL or logs

---

### 5.7 Threat Model: Data Retention Failure

**Threat**: Attacker's data not deleted after 30 days, enabling unauthorized access period

**Controls**:
- [ ] pg_cron cleanup runs daily at 2 AM UTC
- [ ] Query: `DELETE FROM diagnostics WHERE paid_at < NOW() - '30 days'`
- [ ] Database enforces deletion (not application-level)
- [ ] auth.users kept (allows re-purchase, re-authentication)

**Test**: Insert 31-day-old row, verify deleted within 24h; insert 29-day-old row, verify kept

---

## Part 6: Sign-Off

**All Acceptance Criteria Met When**:
1. All E2E test cases passed (8/8 green)
2. All security validation tests passed (7 threat models, 20+ controls)
3. Data retention verified (cleanup job running, old data deleted)
4. RLS policy tested and enforced
5. Zero defects found in critical path
6. Performance acceptable (no >500ms latency on /chat)
7. Logging adequate (no secrets, sufficient debug info)

**Sign-Off Authority**: QA Lead + Security + Product

**Ready for Production When**: All checkboxes green, no P0/P1 defects, documented & communicated

