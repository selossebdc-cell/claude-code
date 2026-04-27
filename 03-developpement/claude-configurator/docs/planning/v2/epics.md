# EPICs — Auth/Stripe Integration v2

**Planning Version**: v2  
**Project**: Claude Configurator  
**Feature**: Authentication & Stripe Payment Integration  
**Mode**: Greenfield (auth-stripe subsystem)  
**Status**: Planning Complete  
**Date**: 2026-04-27

---

## Overview

Five EPICs decompose the auth/Stripe integration into independently deployable components. Each EPIC has explicit dependencies and a clear success path.

### Epic Dependencies

```
EPIC-1 (Database) ← EPIC-2 (Stripe Webhook) ← EPIC-3 (Checkout)
         ↓
EPIC-4 (Chat Auth) ← EPIC-5 (Frontend)
```

**Deployment Order**: 1 → 2 → 3 → 4 → 5

---

## EPIC-1: Database Schema & Security

**Objective**: Establish schema, RLS policies, and automated cleanup for auth/payment data.

**Scope**:
- Create/modify `diagnostics` table columns (stripe_session_id, client_id, paid_at)
- Create `stripe_events` table (audit log)
- Implement RLS policies (user isolation, admin override)
- Setup pg_cron daily cleanup job (30-day retention)
- Create indexes for performance

**Dependencies**: None (foundation EPIC)

**Success Criteria**:
- [ ] All migrations applied without errors
- [ ] RLS prevents cross-user access in queries
- [ ] Cleanup job deletes >30-day-old diagnostics daily
- [ ] stripe_session_id uniqueness enforced (UNIQUE constraint)
- [ ] No auth.users data deleted (retention preserves for re-purchase)

**Effort Estimate**: ~4 hours (2-3 tasks)

---

## EPIC-2: Stripe Webhook Handler

**Objective**: Receive, verify, and process Stripe webhooks securely.

**Scope**:
- Build `stripe-webhook` Edge Function
- Implement HMAC-SHA256 signature verification
- Create user via `inviteUserByEmail()` with retry logic (3x, 1s delay)
- Store event in `diagnostics` table with idempotence check
- Log all events for audit trail

**Dependencies**: EPIC-1 (database must exist)

**Success Criteria**:
- [ ] Webhook signature verification rejects invalid events
- [ ] Idempotence: replayed webhooks do not create duplicate users
- [ ] Retry logic: user creation succeeds even with transient failures
- [ ] Magic link sent automatically (inviteUserByEmail side effect)
- [ ] All events logged with timestamp, event ID, outcome

**Effort Estimate**: ~6 hours (2-3 tasks)

---

## EPIC-3: Checkout Initiation

**Objective**: Generate Stripe checkout sessions via Edge Function.

**Scope**:
- Build `create-checkout` Edge Function
- Accept email from frontend request body
- Call Stripe API with hardcoded STRIPE_PRICE_ID
- Return checkout URL + session ID
- Handle errors (invalid email, API failures)

**Dependencies**: EPIC-2 (webhook must be live before checkout can be completed)

**Success Criteria**:
- [ ] Valid email generates unique Stripe checkout URL
- [ ] Session ID returned to frontend for tracking
- [ ] Success URL points to `/success.html?session_id=...`
- [ ] Cancel URL points to `/pricing.html`
- [ ] Stripe secret key never exposed in logs or response

**Effort Estimate**: ~3 hours (1-2 tasks)

---

## EPIC-4: Chat Authorization & Validation

**Objective**: Enforce JWT and payment validation on `/chat` function.

**Scope**:
- Modify existing `/chat` Edge Function
- Extract JWT from Authorization header
- Validate signature and expiry (1-hour TTL)
- Check payment status (paid_at within 30 days)
- Return 401/403 for auth/payment failures
- RLS enforces user isolation

**Dependencies**: EPIC-1 (diagnostics table required), EPIC-2 (users created via webhook)

**Success Criteria**:
- [ ] Missing JWT returns 401
- [ ] Expired JWT returns 401
- [ ] Unpaid users return 403
- [ ] Expired retention (>30 days) returns 403
- [ ] Valid JWT + payment allows request to proceed
- [ ] RLS prevents user A from seeing user B's diagnostics

**Effort Estimate**: ~4 hours (1-2 tasks)

---

## EPIC-5: Frontend Integration

**Objective**: Connect frontend to checkout, authentication, and JWT-protected endpoints.

**Scope**:
- Create `/auth/magic-link-callback?token=XXX` page
- Implement `verifyOtp()` flow (sign-in with magic link)
- Store JWT in localStorage after successful sign-in
- Modify `/chat` page to send JWT in Authorization header
- Create `/success.html?session_id=XXX` page (payment confirmation)
- Handle error flows (401 → /pricing, 403 → error message)

**Dependencies**: EPIC-3 (checkout created), EPIC-4 (chat endpoint secured)

**Success Criteria**:
- [ ] Magic link callback auto-signs-in user and redirects to `/chat`
- [ ] JWT persisted in localStorage across refresh
- [ ] `/chat` requests include Authorization header with JWT
- [ ] 401 response clears localStorage and redirects to `/pricing`
- [ ] 403 response shows "Purchase required" message
- [ ] Success page shows confirmation and waits for magic link click

**Effort Estimate**: ~5 hours (2-3 tasks)

---

## Cross-Epic Notes

**Sequencing**: Deploy in order 1 → 2 → 3 → 4 → 5. Later EPICs cannot proceed without earlier dependencies.

**Testing Strategy**: Each EPIC includes unit/integration tests. E2E test covers all 5 EPICs together (complete payment → access /chat).

**Rollback**: Each EPIC can be rolled back independently (e.g., disable RLS, revert migrations, deactivate webhook endpoint).

