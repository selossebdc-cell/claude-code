# Planning Index — Auth/Stripe Integration v2

**Project**: Claude Configurator  
**Feature**: Authentication & Stripe Payment Integration  
**Mode**: Greenfield (auth-stripe subsystem)  
**Planning Date**: 2026-04-27  
**Status**: Planning Complete

---

## Quick Navigation

### Planning Documents
- **EPICs** → `epics.md` (5 major components)
- **User Stories** → `us/` folder (9 stories, one per US file)
- **Tasks** → `tasks/` folder (10 tasks, one per TASK file)

### Deployment Order

```
TASK-0001: Project Setup ★★★ CRITICAL
TASK-0002: Database Migrations ★★★ CRITICAL
TASK-0003: RLS Policies ★★★ CRITICAL
TASK-0004: pg_cron Setup ★★ HIGH
TASK-0005: Stripe Webhook ★★★ CRITICAL
TASK-0006: Create Checkout ★★ HIGH
TASK-0007: Chat JWT Auth ★★★ CRITICAL
TASK-0008: Magic Link Callback ★★ HIGH
TASK-0009: Frontend JWT Storage ★★ HIGH
TASK-0010: Success Page ★ MEDIUM
```

---

## EPICs Summary

### EPIC-1: Database Schema & Security (4h)
Foundation layer: database columns, RLS policies, cleanup automation.

**User Stories**:
- US-001: Database Migrations
- US-002: RLS Policies
- US-003: pg_cron Cleanup

**Status**: Ready to build
**Dependencies**: None

---

### EPIC-2: Stripe Webhook Handler (6h)
Receive and process Stripe checkout events with signature verification and user creation.

**User Stories**:
- US-004: Stripe Webhook Handler

**Status**: Ready to build
**Dependencies**: EPIC-1 (database must exist)

---

### EPIC-3: Checkout Initiation (3h)
Edge Function to generate Stripe checkout sessions.

**User Stories**:
- US-005: create-checkout Function

**Status**: Ready to build
**Dependencies**: EPIC-2 (webhook must be live before checkout completion)

---

### EPIC-4: Chat Authorization (4h)
Enforce JWT validation and payment status on /chat endpoint.

**User Stories**:
- US-006: Chat JWT Validation

**Status**: Ready to build
**Dependencies**: EPIC-1 (database), EPIC-2 (users created)

---

### EPIC-5: Frontend Integration (5h)
Magic link callback, JWT storage, authorization headers, success page.

**User Stories**:
- US-007: Magic Link Callback
- US-008: JWT Storage & Authorization
- US-009: Success Page

**Status**: Ready to build
**Dependencies**: EPIC-3 (checkout), EPIC-4 (chat endpoint)

---

## User Stories Mapping

| US ID | Title | EPIC | Effort | Status |
|-------|-------|------|--------|--------|
| US-001 | Database Migrations | EPIC-1 | 2h | Ready |
| US-002 | RLS Policies | EPIC-1 | 1.5h | Ready |
| US-003 | pg_cron Cleanup | EPIC-1 | 1h | Ready |
| US-004 | Stripe Webhook | EPIC-2 | 3-4h | Ready |
| US-005 | create-checkout | EPIC-3 | 2-3h | Ready |
| US-006 | Chat JWT Auth | EPIC-4 | 3-4h | Ready |
| US-007 | Magic Link Callback | EPIC-5 | 2h | Ready |
| US-008 | JWT Storage | EPIC-5 | 2h | Ready |
| US-009 | Success Page | EPIC-5 | 1.5h | Ready |

**Total Estimated Effort**: ~22-25 hours

---

## Tasks Mapping

| Task ID | Title | US | EPIC | Effort | Priority | Status |
|---------|-------|----|----|--------|----------|--------|
| TASK-0001 | Project Setup | — | EPIC-1 | 2h | ★★★ CRITICAL | Ready |
| TASK-0002 | DB Migrations | US-001 | EPIC-1 | 2h | ★★★ CRITICAL | Ready |
| TASK-0003 | RLS Policies | US-002 | EPIC-1 | 1.5h | ★★★ CRITICAL | Ready |
| TASK-0004 | pg_cron Setup | US-003 | EPIC-1 | 1h | ★★ HIGH | Ready |
| TASK-0005 | Stripe Webhook | US-004 | EPIC-2 | 4h | ★★★ CRITICAL | Ready |
| TASK-0006 | Create Checkout | US-005 | EPIC-3 | 2h | ★★ HIGH | Ready |
| TASK-0007 | Chat JWT Auth | US-006 | EPIC-4 | 3h | ★★★ CRITICAL | Ready |
| TASK-0008 | Magic Link Callback | US-007 | EPIC-5 | 2h | ★★ HIGH | Ready |
| TASK-0009 | Frontend JWT | US-008 | EPIC-5 | 2h | ★★ HIGH | Ready |
| TASK-0010 | Success Page | US-009 | EPIC-5 | 1.5h | ★ MEDIUM | Ready |

**Total**: 10 tasks, ~22-25 hours

---

## Dependency Graph

```
EPIC-1 (Database)
  ├── US-001 (Migrations)
  ├── US-002 (RLS)
  └── US-003 (pg_cron)
       ↓
EPIC-2 (Stripe Webhook) ← depends on EPIC-1
  └── US-004
       ↓
EPIC-3 (Checkout) ← depends on EPIC-2
  └── US-005
       ↓
EPIC-4 (Chat Auth) ← depends on EPIC-1, EPIC-2
  └── US-006

EPIC-5 (Frontend) ← depends on EPIC-3, EPIC-4
  ├── US-007 (Magic Link)
  ├── US-008 (JWT Storage)
  └── US-009 (Success Page)
```

---

## Implementation Sequence (Recommended)

### Phase 1: Foundation (EPIC-1)
```
Week 1, Days 1-2
├── TASK-0001: Project Setup (2h)
├── TASK-0002: DB Migrations (2h)
├── TASK-0003: RLS Policies (1.5h)
└── TASK-0004: pg_cron Setup (1h)

Subtotal: 6.5 hours
Blockers: None
```

### Phase 2: Backend Services (EPIC-2, EPIC-3)
```
Week 1, Days 3-4
├── TASK-0005: Stripe Webhook (4h)
└── TASK-0006: Create Checkout (2h)

Subtotal: 6 hours
Blockers: Foundation (EPIC-1) must be complete
```

### Phase 3: Chat Authorization (EPIC-4)
```
Week 2, Day 1
└── TASK-0007: Chat JWT Auth (3h)

Subtotal: 3 hours
Blockers: Foundation + Webhook (EPIC-1, EPIC-2)
```

### Phase 4: Frontend (EPIC-5)
```
Week 2, Days 2-3
├── TASK-0008: Magic Link Callback (2h)
├── TASK-0009: Frontend JWT Storage (2h)
└── TASK-0010: Success Page (1.5h)

Subtotal: 5.5 hours
Blockers: Chat Auth + Checkout (EPIC-4, EPIC-3)
```

### Phase 5: Integration & Testing
```
Week 2, Day 4 + Beyond
├── E2E Testing (Stripe → magic link → chat)
├── Security Audit (JWT, RLS, webhook signature)
├── Performance Testing
└── Deployment

Est: 4-6 hours
```

---

## Success Criteria

### Functional
- [ ] User completes Stripe payment
- [ ] Magic link sent to email
- [ ] User clicks link and is authenticated
- [ ] User can access /chat endpoint
- [ ] User cannot access other users' data (RLS)
- [ ] Old data deleted after 30 days (pg_cron)

### Security
- [ ] Webhook signature verified (HMAC-SHA256)
- [ ] JWT validated on every /chat request
- [ ] Payment status enforced (30-day retention)
- [ ] RLS prevents cross-user access
- [ ] No sensitive data in logs/errors
- [ ] No JWT in query params or console logs

### Performance
- [ ] Webhook processed <5 seconds (including retries)
- [ ] Magic link validation <1 second
- [ ] /chat request <2 seconds (with API call)
- [ ] Indexes on client_id and paid_at (query optimization)

### Reliability
- [ ] Webhook idempotence (no duplicate users)
- [ ] 3-retry logic for user creation
- [ ] 30-day cleanup job runs daily
- [ ] All errors logged with context
- [ ] Rollback plan documented per task

---

## Testing Strategy

### Unit Tests
- JWT validation logic
- Payment status check (30-day boundary)
- Email validation (create-checkout)
- RLS policy simulation

### Integration Tests
- Webhook → user creation → magic link flow
- JWT storage → Authorization header → chat request
- 401/403 error handling (logout, permission denied)

### E2E Tests
1. Complete Stripe checkout (test mode)
2. Receive magic link email
3. Click magic link
4. Auto-sign-in and redirect to /chat
5. Send chat message
6. Verify response
7. Test cross-user isolation (User A cannot see User B's data)
8. Verify cleanup (old rows deleted after 30 days)

---

## Security Checklist

Before Deployment:
- [ ] `STRIPE_SECRET_KEY` in env vars (not code)
- [ ] `STRIPE_WEBHOOK_SECRET` in env vars (not code)
- [ ] `SUPABASE_SERVICE_ROLE_KEY` in env vars (not code)
- [ ] RLS enabled on diagnostics table
- [ ] Webhook signature verification mandatory (not optional)
- [ ] JWT validation on every /chat request
- [ ] No JWT in query params or logs
- [ ] HTTPS enforced (browser requirement)
- [ ] Error messages generic (no leakage)
- [ ] Rollback plan tested

---

## Related Specifications

- **Brief**: `/docs/specs/auth-stripe/brief-auth-stripe.md`
- **Scope**: `/docs/specs/auth-stripe/scope-auth-stripe.md`
- **Acceptance**: `/docs/specs/auth-stripe/acceptance-auth-stripe.md`
- **Stack**: `/docs/specs/stack-reference.md`

---

## Glossary

| Term | Definition |
|------|-----------|
| JWT | JSON Web Token (signed access token) |
| RLS | Row-Level Security (database access control) |
| OTP | One-Time Password (magic link token) |
| HMAC | Hash-based Message Authentication Code (signature verification) |
| pg_cron | PostgreSQL cron job scheduler (automated cleanup) |
| Idempotence | Property that request can be applied multiple times safely |
| Webhook | HTTP callback from Stripe on payment completion |

---

## Notes for Developers

1. **Read the full docs**: Each TASK file is self-contained with full implementation details
2. **Follow the sequence**: Tasks have dependencies; don't skip ordering
3. **Test each task**: Run unit/integration tests before proceeding
4. **Log everything**: All operations logged with timestamp and context
5. **Never hardcode secrets**: Use environment variables for all credentials
6. **Document your changes**: Update TASK files if assumptions change

---

**Version**: Planning v2  
**Last Updated**: 2026-04-27  
**Ready for**: Build Phase (ACT — BUILD)
