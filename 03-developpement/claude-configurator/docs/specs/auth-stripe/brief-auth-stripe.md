# Brief — Authentication Secure (Stripe → Magic Link → RLS)

**Document Type**: Executive Summary  
**Date**: 2026-04-27  
**Status**: Ready for MODEL phase  
**Audience**: Product, Engineering, Security

---

## Vision

Currently: CS Digital Setup (€149) requires manual email activation after Stripe payment.

**Problem**: Attackers can:
- Forge JWT tokens to access `/chat` without paying
- Modify HTTP requests to bypass authentication
- Replay Stripe webhooks to create duplicate user accounts

**Solution**: Fully automated, cryptographically secure flow: **Stripe payment → Supabase magic link → JWT validation → RLS-protected /chat**

**Security Posture**: Implements Secure-by-Design principles (server-side validation only, signature verification, role-based access control, time-limited data retention).

---

## Objectives

1. **OBJ-001**: Automate user creation on payment
   - Stripe webhook captures `checkout.session.completed` and verifies signature
   - Automatically creates Supabase user and sends magic link (no manual email)

2. **OBJ-002**: Enforce authentication on /chat function
   - Extract & validate JWT from Authorization header
   - Reject unauthenticated requests (401)
   - Reject unpaid users (403)

3. **OBJ-003**: Protect data with RLS + time-limited retention
   - Row-level security prevents cross-user access
   - Automatic cleanup of diagnostics after 30 days
   - Keep auth.users forever (allows re-purchase)

---

## Scope

### In Scope
- Stripe webhook integration (create-checkout, stripe-webhook Edge Functions)
- Magic link authentication flow (Supabase auth.admin.inviteUserByEmail)
- /chat function authorization & validation
- Database schema updates (diagnostics table, stripe_events table, migrations)
- RLS policies for diagnostics table
- Frontend JWT integration (localStorage, Authorization header)
- pg_cron automated cleanup (30-day retention)

### Out of Scope
- Stripe refund/cancellation logic
- Customer support tools
- Legacy v1 data migration (marked as separate initiative)
- Multi-device session management / logout revocation

---

## Success Metrics

**E2E Test**: User completes payment → receives magic link → clicks link → auto-signs in → accesses /chat with full functionality

**Quantitative**:
- [ ] Webhook signature verification: 100% of incoming events validated
- [ ] User creation success rate: >99% (3 retries, 1s delay)
- [ ] Data retention accuracy: all diagnostics >30 days deleted within 24h
- [ ] JWT validation: 0% unauthorized access to /chat without valid token

**Qualitative**:
- [ ] No user can access another user's diagnostics (RLS enforced)
- [ ] No duplicate user creation on webhook replay (idempotence verified)
- [ ] Admin can view all diagnostics (role-based override working)
- [ ] Magic link invalid after 24h (Supabase default enforced)

---

## Key Decisions from BREAK Phase

### Authentication Flow (Q-003)
- `inviteUserByEmail()` **automatically sends** magic link (no separate call needed)
- Redirect: `/auth/magic-link-callback?token=XXX` validates & auto-signs-in user
- Frontend redirects to `/chat?onboarded=true` after successful sign-in

### JWT vs paid_at Validity (Q-005)
- JWT expiration: **1 hour** (standard Supabase, stateless)
- paid_at validity window: **30 days** from purchase (separate concern)
- No refresh tokens. On JWT expiry (401), user redirected to /pricing
- User can re-purchase and get new JWT before 30-day retention expires

### Webhook Retry Logic (Q-001)
- On inviteUserByEmail() failure: **retry immediately 3 times with 1s delay**
- After 3 failures: log event and fail (do NOT queue in background)
- Stripe's built-in retry mechanism handles delivery guarantees

### Idempotence (Q-002)
- Store `stripe_session_id` as UNIQUE in diagnostics table
- Check before inviteUserByEmail(): if stripe_session_id exists, skip user creation
- Prevents duplicate accounts on replayed webhooks

### RLS Policy (Q-006)
```sql
(auth.uid()::uuid = diagnostics.client_id)
OR (auth.role() = 'admin')
```
- Regular users see only their own diagnostics
- Admin role can see all (created via Supabase auth + role assignment)

### Data Retention (Q-008)
- **DELETE diagnostics rows only** after 30 days
- **KEEP auth.users** (allows re-purchase and re-authentication)
- pg_cron: `DELETE FROM diagnostics WHERE paid_at < NOW() - '30 days'::interval`

---

## Deployment Timeline

- **Phase**: MODEL (Technical Specification)
- **Expected Duration**: 1 week (spec + ADR + decision records)
- **Next Phase**: ACT (Implementation)
- **Rollout Strategy**: Full at launch (no feature flags needed; old v1 flow deprecated)

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| JWT forgery | Signed by Supabase key, verified server-side, 1h TTL |
| Webhook replay | Idempotence via stripe_session_id UNIQUE constraint |
| Signature spoofing | Stripe.webhooks.constructEvent validates HMAC-SHA256 |
| Cross-tenant access | RLS policy enforced on every /chat query |
| Data leakage | Generic error messages (401/403), no paid_at exposed |
| Service downtime | Stripe retries webhook; app logs failures; support can manually re-trigger |

---

## Definition of Done

1. **Specs**: brief, scope, acceptance documents reviewed & signed off
2. **Architecture**: ADR for webhook idempotence, JWT strategy, RLS design
3. **Security**: Secure-by-Design checklist completed
4. **Tests**: E2E test plan with 7-8 test cases documented
5. **Ready**: Technical team ready to implement in ACT phase

