# ADR-0001: Webhook Idempotence & Duplicate User Prevention

**Status**: Accepted  
**Date**: 2026-04-27  
**Context**: Auth-Stripe integration (greenfield-auth)  
**Participants**: Product, Security, Engineering

---

## Problem Statement

Stripe can retry webhook delivery if the endpoint doesn't acknowledge (5 retries with exponential backoff). If CS Business doesn't handle replay idempotently, the same webhook can trigger:
1. **Duplicate user creation** (same email, multiple auth.users entries)
2. **Duplicate diagnostic records** (multiple rows for same payment)
3. **Duplicate magic links** (email spam)

This creates security and UX issues:
- User gets multiple magic link emails
- Application logic breaks if expecting 1:1 mapping (payment → user → diagnostic)
- Database integrity violated
- RLS policy assumptions break

---

## Decision

**We use Stripe session ID (stripe_session_id) as an idempotence key with a UNIQUE database constraint.**

### Mechanism

1. **Stripe provides immutable session ID** (`checkout.session.completed.data.object.id`)
   - Each checkout session is globally unique (e.g., `cs_live_xyz...`)
   - Never reused, never modified by Stripe
   - Survives webhook retries

2. **Database constraint enforces uniqueness**
   ```sql
   ALTER TABLE diagnostics ADD COLUMN stripe_session_id VARCHAR UNIQUE NOT NULL;
   ```

3. **Webhook handler checks before user creation**
   ```sql
   SELECT 1 FROM diagnostics WHERE stripe_session_id = 'cs_xyz' LIMIT 1
   ```
   - If exists: return 200 OK (already processed)
   - If new: create user + diagnostic

4. **Database handles race conditions**
   - Postgres UNIQUE constraint is atomic
   - If 2 parallel webhooks try to insert same session_id:
     - First wins, second fails with UNIQUE violation
     - Second webhook catches exception, returns 500 (Stripe retries)
     - On next retry, first check finds existing row, returns 200

---

## Rationale

### Why UNIQUE constraint (not application-level check)?

**Option A: Application-level check** (❌ NOT CHOSEN)
```typescript
const existing = await db.select('SELECT 1 FROM diagnostics WHERE stripe_session_id = ?', sessionId);
if (existing.length > 0) { return 200; }
// Create user...
const inserted = await db.insert('INSERT INTO diagnostics (stripe_session_id, ...) VALUES (?, ...)', sessionId);
```

**Problems**:
- Check-then-act is racy (between SELECT and INSERT, another webhook inserts)
- 2 webhooks can both pass the SELECT, both create users
- Requires application to catch INSERT errors and recover

**Option B: UNIQUE constraint** (✓ CHOSEN)
```sql
CREATE TABLE diagnostics (
  ...
  stripe_session_id VARCHAR UNIQUE NOT NULL,
  ...
);
```

**Benefits**:
- Database enforces atomicity (Postgres is source of truth)
- No race condition (UNIQUE constraint checked at INSERT time)
- Simple application logic: check → create → INSERT (constraint guarantees)
- If INSERT fails due to UNIQUE violation, Stripe retries (idempotent)

**Conclusion**: UNIQUE constraint is more robust, database-native, and guarantees correctness.

---

### Why NOT use stripe_events table for deduplication?

**Option A: stripe_events table** (alternative, rejected)
```sql
CREATE TABLE stripe_events (
  stripe_event_id VARCHAR UNIQUE NOT NULL,
  processed BOOLEAN
);
```

**Problems**:
- Adds complexity (check 2 tables instead of 1)
- Stripe event_id ≠ session_id (different lifecycle)
- Event can be received multiple times, but session_id is what matters for user creation

**Conclusion**: stripe_session_id in diagnostics is sufficient and simpler.

---

### Why stripe_session_id (not email)?

**Option A: Email as key** (❌ NOT CHOSEN)
```sql
UNIQUE(email)  -- in diagnostics table
```

**Problems**:
- User might pay twice with same email (legitimate use case)
- Only 1 diagnostic per email (limitation)
- Email could be updated/normalized differently

**Option B: stripe_session_id** (✓ CHOSEN)
- 1:1 mapping to payment
- Global uniqueness guaranteed by Stripe
- Session never reused

**Conclusion**: stripe_session_id is the correct idempotence key.

---

## Implementation

### Database Schema

```sql
-- Add column to existing diagnostics table
ALTER TABLE diagnostics ADD COLUMN stripe_session_id VARCHAR UNIQUE NOT NULL;

-- Add index for fast idempotence check
CREATE INDEX idx_diagnostics_stripe_session_id ON diagnostics(stripe_session_id);

-- Foreign key to auth.users
ALTER TABLE diagnostics ADD COLUMN client_id UUID NOT NULL REFERENCES auth.users(id);

-- Retention marker
ALTER TABLE diagnostics ADD COLUMN paid_at TIMESTAMP WITH TIME ZONE NOT NULL;
```

### Webhook Handler Logic

```typescript
export async function stripeWebhook(req: Request) {
  const event = stripe.webhooks.constructEvent(...);  // Signature verified

  if (event.type !== 'checkout.session.completed') {
    return { status: 200 };
  }

  const sessionId = event.data.object.id;
  const email = event.data.object.customer_email;

  // Step 1: Idempotence check
  const existing = await db.select(
    'SELECT id FROM diagnostics WHERE stripe_session_id = ?',
    sessionId
  );
  if (existing.length > 0) {
    // Already processed, return success
    return { status: 200, body: {received: true} };
  }

  // Step 2: Create user (with retries)
  let user;
  for (let i = 0; i < 3; i++) {
    try {
      user = await supabase.auth.admin.inviteUserByEmail(email, {...});
      break;
    } catch (e) {
      if (i === 2) throw e;
      await sleep(1000);  // 1s delay before retry
    }
  }

  // Step 3: Insert diagnostic (UNIQUE constraint will catch duplicates)
  try {
    await db.insert(
      `INSERT INTO diagnostics (stripe_session_id, client_id, paid_at, created_at)
       VALUES (?, ?, NOW(), NOW())`,
      sessionId,
      user.id
    );
  } catch (e) {
    if (e.code === 'UNIQUE_VIOLATION') {
      // Another webhook already inserted this session_id
      // Return success (idempotent response)
      return { status: 200, body: {received: true} };
    }
    throw e;
  }

  return { status: 200, body: {received: true} };
}
```

---

## Test Cases

### Test 1: Normal Flow (Single Webhook)

**Setup**: Stripe sends webhook with session_id = `cs_test_1`

**Steps**:
1. Webhook received
2. Idempotence check: 0 rows in diagnostics
3. User created via inviteUserByEmail()
4. INSERT into diagnostics succeeds
5. Return 200 OK

**Expected**: 1 user, 1 diagnostic row

---

### Test 2: Webhook Replay (Same Event)

**Setup**: Stripe retries same webhook with session_id = `cs_test_1`

**Steps (first webhook)**:
1. Idempotence check: 0 rows
2. User created
3. INSERT succeeds
4. Return 200

**Steps (replay webhook)**:
1. Idempotence check: 1 row found (already inserted)
2. Return 200 immediately
3. No user creation attempted

**Expected**: Still 1 user, 1 diagnostic row (no duplicates)

---

### Test 3: Parallel Webhooks (Race Condition)

**Setup**: 2 webhooks for same session_id = `cs_test_1` arrive simultaneously

**Timeline**:
- T0: Webhook A checks idempotence → 0 rows
- T0: Webhook B checks idempotence → 0 rows
- T1: Webhook A creates user → success
- T1: Webhook B creates user → SUCCESS (Supabase creates 2 users with same email? → FAIL)
  - Actually: Supabase email is UNIQUE, so second inviteUserByEmail fails
- T2: Webhook A tries INSERT diagnostics → success
- T2: Webhook B tries INSERT diagnostics → UNIQUE constraint violation
- Webhook B catches exception, returns 500
- Stripe retries Webhook B
- On retry: Idempotence check finds row, returns 200

**Expected**: 1 user, 1 diagnostic row, both webhooks return success (Stripe happy)

**Note**: Supabase's email UNIQUE constraint also provides safety for Step T1 failure case.

---

### Test 4: Stale Webhook Delayed

**Setup**: Webhook 1 (session_id = `cs_test_1`) gets delayed and arrives after Webhook 2 (session_id = `cs_test_2`)

**Timeline**:
- T0: Session 1 completed (user pays)
- T0: Session 2 completed (different user pays)
- T0: Webhook 2 received → Insert session_id = `cs_test_2`
- T1: Webhook 1 finally received (delayed)
- Webhook 1 checks idempotence → 0 rows for `cs_test_1`
- Webhook 1 creates user + inserts diagnostic
- Result: 2 users, 2 diagnostics

**Expected**: Correct (different sessions, no interference)

---

## Consequences

### Positive
- ✓ Webhook replays handled automatically (idempotent)
- ✓ No duplicate users (UNIQUE constraint prevents)
- ✓ No duplicate diagnostics (UNIQUE constraint prevents)
- ✓ Application doesn't need complex retry/recovery logic
- ✓ Database is source of truth (not application memory)
- ✓ Simple to test and reason about

### Negative
- ✗ If stripe_session_id somehow duplicated, constraint will fail (but Stripe guarantees uniqueness)
- ✗ If inviteUserByEmail() succeeds but INSERT fails (network error), user created but no diagnostic (can be manually recovered)

### Mitigation for Negative #2
- Log all INSERT failures (webhook returns 500)
- Stripe will retry
- On retry, idempotence check finds the row, returns 200
- User gets magic link (from inviteUserByEmail call), can sign in

---

## Alternatives Considered

### Alternative 1: No Idempotence Check (❌)
- Risk: Duplicate users on replay
- Not acceptable for security/UX reasons

### Alternative 2: Webhook Deduplication Table (⚠️ More Complex)
```sql
CREATE TABLE stripe_webhooks (
  stripe_event_id VARCHAR UNIQUE,
  processed_at TIMESTAMP
);
```
- Pros: Separates concern
- Cons: Adds complexity, still need UNIQUE on diagnostics anyway

### Alternative 3: Soft Delete + Temporal Keys (⚠️ Overkill)
- Not needed for this use case
- Session ID already provides uniqueness

---

## Related Decisions

- **ADR-0002**: JWT validation strategy (1h expiry, no refresh)
- **ADR-0003**: RLS policy design (client_id ownership)
- **ADR-0004**: Data retention (30-day cleanup via pg_cron)

---

## Sign-Off

- **Product**: Approves idempotent behavior (user sees same flow on replay)
- **Security**: Accepts UNIQUE constraint as database-enforced control
- **Engineering**: Commits to implementing with UNIQUE constraint

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-27  
**Status**: Accepted & Ready for Implementation
