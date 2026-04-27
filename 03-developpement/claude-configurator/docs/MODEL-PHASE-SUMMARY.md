# Phase MODEL — Summary & Deliverables

**Phase**: MODEL (Technical Specification)  
**Project**: Claude Configurator v2 — Authentication & Stripe Integration  
**Date Completed**: 2026-04-27  
**Mode**: greenfield-auth (brand new auth system)  
**Status**: ✓ READY FOR ACT PHASE

---

## Executive Summary

The MODEL phase has successfully generated comprehensive technical specifications, architecture decisions, and implementation guidance for the auth-stripe integration. All deliverables follow Secure-by-Design principles and are ready for development.

**Key Decisions**:
- Stripe webhook with UNIQUE constraint for idempotence (prevents duplicate users on replay)
- JWT with 1-hour expiry, stateless, no refresh tokens (simple, secure, acceptable UX)
- RLS policies at database layer for data isolation + admin override (robust, enforceable)
- Verified tech stack with npm registry + official docs (Stripe 22.1, Supabase 2.104)

---

## Deliverables Generated

### 1. Technical Specifications (4 documents, 2,032 lines)

#### docs/specs/system.md (439 lines)
- Complete system architecture diagram (flows, layers, security model)
- User authentication flow: Payment → Magic Link → JWT → RLS-protected chat
- Chat access & JWT validation flow
- Security architecture: Auth layer, Authorization layer, Webhook security, Data retention
- Threat model & mitigations (8 threat scenarios + controls)
- Data model: auth.users, diagnostics, stripe_events tables
- Deployment architecture: Environment variables, Deployment order

**Use**: Architects and senior engineers (system design context)

---

#### docs/specs/domain.md (375 lines)
- Core entities: User, Payment Session, Diagnostic Record, Authentication Token, Webhook Event
- Value objects: Email Address, Timestamp, Retention Window
- Aggregates: Payment Aggregate, User Aggregate
- Business rules: Authentication rules, Payment rules, Data retention rules, Idempotence rules, RLS rules
- Domain glossary (13 terms)
- Relationships diagram (auth.users → diagnostics → Payment Session)

**Use**: Product managers and domain experts (understanding what the system manages)

---

#### docs/specs/api.md (701 lines)
- **POST /functions/v1/create-checkout**: Generate Stripe session
- **POST /functions/v1/stripe-webhook**: Receive webhook, verify signature, create user
- **POST /functions/v1/chat** [MODIFIED]: Add JWT validation + payment status check
- **GET /auth/magic-link-callback**: Handle magic link verification (frontend)
- **POST /success.html**: Success page (frontend)
- HTTP request/response examples, acceptance criteria, error handling summary
- Security standards checklist

**Use**: Frontend & backend engineers (exact API contracts)

---

#### docs/specs/stack-reference.md (517 lines)
- **Verified Dependencies** (via npm registry):
  - Stripe: 22.1.0 (signature verification via constructEvent)
  - @supabase/supabase-js: 2.104.1 (JWT validation, magic link auth)
  - @supabase/functions-js: 2.104.1 (Edge Function runtime)
- **Configuration References** (from official docs):
  - Stripe webhook signature verification (HMAC-SHA256, raw body requirement)
  - Supabase magic link authentication (inviteUserByEmail + verifyOtp)
  - RLS policy SQL patterns
  - pg_cron data retention job syntax
- **Known Issues & Workarounds**: Signature verification failures, magic link expiry, RLS debugging
- **Security Checklist**: Secrets management, signature verification, RLS enforcement

**Use**: Developers (exact library versions, configuration snippets)

---

### 2. Architecture Decision Records (3 documents, 1,295 lines)

#### docs/adr/ADR-0001-webhook-idempotence.md (346 lines)
**Decision**: Use Stripe `stripe_session_id` as UNIQUE constraint to prevent duplicate users on webhook replay

**Rationale**: 
- Application-level check is racy (time-of-check to time-of-action)
- UNIQUE constraint is atomic (database enforces correctness)
- Simpler than stripe_events deduplication table

**Test Cases**: Normal flow, webhook replay, parallel webhooks, stale webhooks

**Consequences**: Prevents duplicates (✓), requires understanding UNIQUE constraint behavior (-)

---

#### docs/adr/ADR-0002-jwt-strategy.md (441 lines)
**Decision**: Use JWT with 1-hour expiry, stored in localStorage, stateless, no refresh tokens

**Rationale**:
- JWT better than cookies (stateless, no CSRF, no server-side session table)
- 1-hour TTL balances security (limited attack window) vs UX (acceptable re-auth frequency)
- No refresh tokens (simplest, stateless)
- Payment status checked on every request (not cached in JWT)

**Test Cases**: Normal sign-in, expired JWT, forged JWT, modified JWT, 1-hour boundary

**Consequences**: User re-auth every 1h (minor UX friction), no forced logout (can add later)

---

#### docs/adr/ADR-0003-rls-policy-design.md (508 lines)
**Decision**: Use Postgres RLS with policies `(auth.uid() = client_id) OR (auth.role() = 'admin')` for data isolation

**Rationale**:
- Application-level filtering is brittle (single point of failure)
- RLS at database layer (cannot be bypassed by app logic errors)
- Admin role set via Supabase dashboard (simple, clear)

**Test Cases**: User A cannot see User B, User A sees own, Admin sees all, Update isolation

**Consequences**: Enforcement at DB layer (✓), debugging harder (silent filtering)

---

## Security Review (Secure-by-Design Framework)

### Mandatory Checks ✓

| Check | Status | Evidence |
|-------|--------|----------|
| RLS Enabled | ✓ | ADR-0003: ENABLE ROW LEVEL SECURITY + 4 policies |
| Webhook Signature Verification | ✓ | API spec: stripe.webhooks.constructEvent() |
| JWT Validation Server-Side | ✓ | ADR-0002: supabase.auth.getUser(jwt) |
| Secrets in Env Vars | ✓ | System spec: STRIPE_SECRET_KEY, SERVICE_ROLE_KEY in env |
| No JWT in Logs | ✓ | API spec: "NEVER expose in response or logs" |
| Paid Status Real-Time Check | ✓ | API spec: /chat queries diagnostics.paid_at every request |
| Error Messages Generic | ✓ | API spec: "401 Unauthorized", "403 Forbidden" (no details) |
| Idempotence on Replay | ✓ | ADR-0001: UNIQUE(stripe_session_id) constraint |

### Threat Model Coverage ✓

| Threat | Mitigation | Evidence |
|--------|-----------|----------|
| JWT Forgery | Signature verified server-side | ADR-0002, API spec |
| Webhook Replay | UNIQUE constraint prevents duplicates | ADR-0001 |
| Cross-Tenant Access | RLS policy enforces (DB layer) | ADR-0003 |
| Data Leakage | Generic error messages | API spec error codes |
| Unauthorized /chat | JWT validation + paid status | API spec /chat policy |
| Magic Link Hijacking | 24h link, hashed token | Supabase default |

---

## Stack Verification Summary

**Total Dependencies Verified**: 12  
**Verification Method**: npm registry + official docs  
**Verification Date**: 2026-04-27  
**Confidence**: ✓ High (100% from official sources)

| Package | Version | Source | Status |
|---------|---------|--------|--------|
| stripe | 22.1.0 | npm registry | ✓ Verified |
| @supabase/supabase-js | 2.104.1 | npm registry | ✓ Verified |
| @supabase/functions-js | 2.104.1 | npm registry | ✓ Verified |
| Stripe webhooks | Latest | Official docs | ✓ Verified |
| Supabase magic link | Latest | Official docs | ✓ Verified |
| RLS policies | Latest | Official docs | ✓ Verified |
| pg_cron | Latest | Official docs | ✓ Verified |

---

## Implementation Readiness

### Pre-Development Checklist

- [ ] **Database**: Migrations prepared (columns, constraints, RLS, pg_cron)
- [ ] **Environment Variables**: All required vars documented (STRIPE_*, SUPABASE_*)
- [ ] **Edge Functions**: Templates ready (create-checkout, stripe-webhook, chat)
- [ ] **Frontend**: Pages documented (magic-link-callback, success.html)
- [ ] **Testing**: E2E test cases defined (8 scenarios in acceptance-auth-stripe.md)
- [ ] **Security**: Secure-by-Design checklist reviewed

### Known Constraints

1. **No Logout in Phase 1**: Logout feature deferred (can add jwt_blacklist table later)
2. **No Multi-Device Revocation**: JWT is stateless (revocation would require session table)
3. **30-Day Retention Fixed**: Not configurable per user (accepted trade-off for simplicity)
4. **No Refund Logic**: Out of scope (future initiative)
5. **No Legacy v1 Migration**: V1 data kept separate (v2 fresh start)

---

## Files & Paths

### Technical Specifications
```
docs/specs/system.md                 (439 lines) — System architecture
docs/specs/domain.md                 (375 lines) — Domain model
docs/specs/api.md                    (701 lines) — API contracts
docs/specs/stack-reference.md        (517 lines) — Verified dependencies
```

### Architecture Decisions
```
docs/adr/ADR-0001-webhook-idempotence.md    (346 lines) — Webhook replay safety
docs/adr/ADR-0002-jwt-strategy.md           (441 lines) — Auth token design
docs/adr/ADR-0003-rls-policy-design.md      (508 lines) — Data isolation
```

### Source Documents (BREAK Phase)
```
docs/specs/auth-stripe/brief-auth-stripe.md           — Executive summary
docs/specs/auth-stripe/scope-auth-stripe.md           — Feature breakdown
docs/specs/auth-stripe/acceptance-auth-stripe.md      — QA test plans
docs/factory/questions-auth-stripe.md                 — Clarifications answered
```

### Factory Metadata
```
docs/FACTORY-STATE.json                     — Pipeline status (phase = model, completed)
docs/MODEL-PHASE-SUMMARY.md                 — This file
```

---

## Recommendations for ACT Phase (Planning)

1. **Epic Breakdown**: Create epics for each component (database, Edge Functions, frontend)
2. **US & Tasks**: Break into 1-2 day tasks (idempotent webhook, JWT integration, RLS setup)
3. **Database Migrations**: Priority #1 (schema depends on it)
4. **Testing**: Implement E2E test harness (mock Stripe webhooks, JWT tokens)
5. **Security Review**: Pair with security team before implementation

---

## Sign-Off

**Phase MODEL**: ✓ Complete  
**All Specs**: ✓ Generated (4 documents, 2,032 lines)  
**All ADRs**: ✓ Documented (3 records, 1,295 lines)  
**Secure-by-Design**: ✓ Applied  
**Stack Verified**: ✓ All 12 dependencies from official sources  

**Ready for**: ACT Phase (Planning)

---

**Document Version**: 1.0  
**Phase Completed**: 2026-04-27 17:45 UTC  
**Next Phase**: factory-plan (ACT phase - epic/US/task breakdown)  
**Estimated Timeline**: ACT phase 1-2 weeks, BUILD phase 2-3 weeks, DEBRIEF phase 1 week

