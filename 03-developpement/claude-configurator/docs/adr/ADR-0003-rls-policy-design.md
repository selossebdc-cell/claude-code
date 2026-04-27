# ADR-0003: Row-Level Security (RLS) Policy Design & Admin Override

**Status**: Accepted  
**Date**: 2026-04-27  
**Context**: Auth-Stripe integration (greenfield-auth)  
**Participants**: Product, Security, Engineering

---

## Problem Statement

The diagnostics table stores user data:
- Each user can have multiple diagnostic records
- Users should see **only their own** records
- Support/admin should see **all** records (for troubleshooting)
- Data filtering must happen at **database layer**, not application layer (defense in depth)

Options:
1. **Application-level filtering**: Backend code checks `user_id` before returning data (❌ brittle, can be bypassed if logic error)
2. **RLS policies**: Postgres enforces data filtering regardless of query (✓ robust, database-native)

---

## Decision

**We use Postgres Row-Level Security (RLS) with policies enforcing:**
```sql
(auth.uid()::uuid = client_id) OR (auth.role() = 'admin')
```

This ensures:
- Regular users see only their own diagnostics
- Admin role can see all diagnostics
- Enforcement happens at SQL query layer (cannot be bypassed by app logic)

---

## RLS Policy Design

### Policy 1: SELECT (Read)

```sql
CREATE POLICY "users_select_own_diagnostics" ON diagnostics
  FOR SELECT USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );
```

**Effect**:
- Query: `SELECT * FROM diagnostics` → returns only rows where `client_id = auth.uid()`
- Query by admin: Same query → returns all rows (role = 'admin' matches)
- Postgres applies USING clause as WHERE filter automatically

**Example**:
```sql
-- User A (UUID = abc123)
SELECT * FROM diagnostics;
-- Returns: rows where client_id = 'abc123'

-- Admin user (role = 'admin')
SELECT * FROM diagnostics;
-- Returns: all rows
```

---

### Policy 2: INSERT (Create)

```sql
CREATE POLICY "users_insert_diagnostics" ON diagnostics
  FOR INSERT WITH CHECK (
    auth.uid()::uuid IS NOT NULL
  );
```

**Effect**:
- Only authenticated users can insert (auth.uid() must be non-null)
- User can insert ANY row, but will be owned by them after /chat request

**Note**: We don't restrict `client_id` in INSERT CHECK because:
- Edge Function (server-side) sets `client_id` to current user (not request-controlled)
- Frontend never sends `client_id`
- Stripe webhook sets `client_id` to created user

---

### Policy 3: UPDATE (Modify)

```sql
CREATE POLICY "users_update_own_diagnostics" ON diagnostics
  FOR UPDATE USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );
```

**Effect**:
- User can update only their own rows
- Admin can update any row

**Example**:
```sql
-- User A tries to update User B's row
UPDATE diagnostics SET content = '...' WHERE id = 'user_b_row_id';
-- RLS filters: no rows match (client_id != User A's uuid)
-- Result: 0 rows updated (no error, just silently filtered)
```

---

### Policy 4: DELETE (Remove)

```sql
CREATE POLICY "users_delete_own_diagnostics" ON diagnostics
  FOR DELETE USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );
```

**Effect**:
- User can delete only their own rows
- Admin can delete any row

---

## Admin Override Design

### What is "Admin Role"?

**In Supabase**:
- `auth.role()` returns value from JWT's `role` claim
- Default: `'authenticated'` for all signed-in users
- Admin: `'admin'` (set manually in Supabase dashboard or via admin API)

### Creating Admin User

```sql
-- Via Supabase dashboard:
1. Sign in as admin (with SUPABASE_SERVICE_ROLE_KEY)
2. Go to Authentication > Users
3. Select user
4. Click "Edit user"
5. Set custom claim: `{"role": "admin"}`
6. Save

-- Or via admin API:
const { data, error } = await supabase.auth.admin.updateUserById(
  'user-uuid',
  {
    user_metadata: {role: 'admin'}
  }
);
```

### Admin JWT Token

```json
{
  "sub": "admin-uuid",
  "email": "admin@csbusiness.fr",
  "role": "admin",  // <-- This matters for RLS
  "aud": "authenticated",
  "iat": 1234567890,
  "exp": 1234571490
}
```

When admin calls `/chat` with this JWT:
```sql
SELECT * FROM diagnostics;
-- RLS evaluates: auth.role() = 'admin' → TRUE
-- Result: all rows returned
```

---

## Implementation Checklist

### Step 1: Enable RLS on diagnostics table

```sql
ALTER TABLE diagnostics ENABLE ROW LEVEL SECURITY;
```

**Verification**:
```sql
SELECT relrowsecurity FROM pg_class WHERE relname='diagnostics';
-- Should return: true
```

---

### Step 2: Create policies

```sql
-- SELECT policy
CREATE POLICY "users_select_own_diagnostics" ON diagnostics
  FOR SELECT USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );

-- INSERT policy
CREATE POLICY "users_insert_diagnostics" ON diagnostics
  FOR INSERT WITH CHECK (
    auth.uid()::uuid IS NOT NULL
  );

-- UPDATE policy
CREATE POLICY "users_update_own_diagnostics" ON diagnostics
  FOR UPDATE USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );

-- DELETE policy
CREATE POLICY "users_delete_own_diagnostics" ON diagnostics
  FOR DELETE USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );
```

---

### Step 3: Verify policies

```sql
-- List all policies
SELECT * FROM pg_policies WHERE tablename='diagnostics';

-- Should show 4 policies (SELECT, INSERT, UPDATE, DELETE)
```

---

## Test Cases

### Test 1: User A Cannot See User B's Data

**Setup**:
- User A: UUID = `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa`
- User B: UUID = `bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb`
- Diagnostic row: `client_id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'` (belongs to B)

**Test**:
```sql
-- Execute as User A (auth.uid() = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')
SELECT * FROM diagnostics WHERE id = 'b_diagnostic_id';

-- RLS evaluates: (auth.uid() = 'aaaaaaaa...') OR (auth.role() = 'admin')
--                → FALSE OR FALSE
-- Result: 0 rows (filtered out)
```

**Expected**: ✓ User A sees 0 rows (cannot access User B's data)

---

### Test 2: User A Can See Own Data

**Setup**:
- User A: UUID = `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa`
- Diagnostic row: `client_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'` (belongs to A)

**Test**:
```sql
-- Execute as User A
SELECT * FROM diagnostics WHERE id = 'a_diagnostic_id';

-- RLS evaluates: (auth.uid() = 'aaaaaaaa...') OR (auth.role() = 'admin')
--                → TRUE OR FALSE
-- Result: row returned
```

**Expected**: ✓ User A sees 1 row (own diagnostic)

---

### Test 3: Admin Sees All Data

**Setup**:
- Admin user: UUID = `cccccccc-cccc-cccc-cccc-cccccccccccc`, role = 'admin'
- Diagnostic rows: Multiple, with various client_ids

**Test**:
```sql
-- Execute as Admin (auth.role() = 'admin')
SELECT * FROM diagnostics;

-- RLS evaluates for each row: (auth.uid() = client_id) OR (auth.role() = 'admin')
--                              → FALSE OR TRUE (for any row)
-- Result: all rows returned
```

**Expected**: ✓ Admin sees all rows

---

### Test 4: Update Isolation

**Setup**:
- User A: UUID = `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa`
- Diagnostic row X: `client_id = 'aaaaaaaa...'` (A's row)
- Diagnostic row Y: `client_id = 'bbbbbbbb...'` (B's row)

**Test**:
```sql
-- User A tries to update User B's row
UPDATE diagnostics SET content = '...' WHERE id = 'y_id';

-- RLS evaluates for each candidate row:
-- Row Y: (auth.uid() = 'bbbbbbbb') OR (auth.role() = 'admin')
--        → FALSE OR FALSE
-- Result: 0 rows updated
```

**Expected**: ✓ Update silently filtered (0 rows affected)

---

### Test 5: Insert by Authenticated User

**Setup**:
- User A: UUID = `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa` (authenticated)

**Test**:
```sql
-- User A inserts new row (backend sets client_id automatically)
INSERT INTO diagnostics (stripe_session_id, client_id, paid_at, created_at)
  VALUES ('cs_test_1', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW(), NOW());

-- RLS evaluates: auth.uid() IS NOT NULL
--                → TRUE (User A is authenticated)
-- Result: row inserted
```

**Expected**: ✓ Insert succeeds

---

### Test 6: Insert by Anonymous User (Future)

**Setup**:
- Anonymous session (no auth.uid())

**Test**:
```sql
-- Anonymous tries to insert
INSERT INTO diagnostics (stripe_session_id, client_id, paid_at, created_at)
  VALUES ('cs_test_2', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', NOW(), NOW());

-- RLS evaluates: auth.uid() IS NOT NULL
--                → FALSE (no authenticated user)
-- Result: insert rejected
```

**Expected**: ✓ Insert fails (policy blocks)

---

## Why NOT Other Approaches

### Approach A: No RLS, Application-Level Filtering (❌)

```typescript
// Backend code
async function getChat(userId) {
  const rows = await db.query('SELECT * FROM diagnostics WHERE client_id = ?', userId);
  return rows;
}
```

**Problems**:
- Single point of failure (if logic error, data leaks)
- Possible bugs in filtering code
- Hard to audit (scattered across application)
- Cannot prevent direct SQL queries bypassing code

**Conclusion**: Not sufficient for security-sensitive data.

---

### Approach B: RLS Only, No Application Check (✓ Better)

```sql
ALTER TABLE diagnostics ENABLE ROW LEVEL SECURITY;
CREATE POLICY ... USING (auth.uid() = client_id);
```

**Benefits**:
- Database enforces filtering (cannot be bypassed)
- Consistent across all queries
- Easy to audit (policies are explicit)
- Protection from indirect queries (ORM, raw SQL, etc.)

**Conclusion**: Database-native RLS is more robust.

---

### Approach C: RLS + Application Check (✓ Best Practice)

```typescript
// Backend code
async function getChat(userId) {
  // Application-level check (defense in depth)
  if (!authenticatedUserId || authenticatedUserId !== userId) {
    throw new Error('Unauthorized');
  }
  
  const rows = await db.query('SELECT * FROM diagnostics WHERE client_id = ?', userId);
  // RLS also filters, provides additional safety
  return rows;
}
```

**Benefits**:
- Defense in depth (2 layers of protection)
- Fail-fast (app rejects before DB query)
- Better error messages to client

**Conclusion**: Best practice, but RLS alone is minimum acceptable.

---

## Consequences

### Positive
- ✓ Data isolation enforced at database layer (robust)
- ✓ Cannot be bypassed by application logic errors
- ✓ Automatic filtering (no manual WHERE clauses needed)
- ✓ Admin override simple (just set role = 'admin')
- ✓ Audit trail clear (policies are explicit)

### Negative
- ✗ Debugging harder (RLS filters silently, 0 rows vs error)
- ✗ Performance impact negligible (but worth monitoring)
- ✗ Admin role setup manual (no UI, requires dashboard or API)

### Mitigations
- Logging on sensitive queries (e.g., admin viewing users)
- Clear error messages to frontend (not "0 rows", but "access denied")
- Admin role automation (script or terraform)

---

## Test Queries

### Verify RLS Enabled

```sql
SELECT relname, relrowsecurity
FROM pg_class
WHERE relname = 'diagnostics';

-- Output: relrowsecurity = true
```

---

### List All Policies

```sql
SELECT schemaname, tablename, policyname, permissive, roles, qual, with_check
FROM pg_policies
WHERE tablename = 'diagnostics'
ORDER BY policyname;
```

---

### Simulate User Query

```sql
-- As User A, query own diagnostics
SELECT * FROM diagnostics WHERE client_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

-- RLS filters automatically (should return own rows)
```

---

### Audit Admin Access

```sql
-- Check if user has admin role
SELECT id, email, (raw_user_meta_data->>'role') as role
FROM auth.users
WHERE raw_user_meta_data->>'role' = 'admin';

-- Verify admin users
```

---

## Related Decisions

- **ADR-0001**: Webhook idempotence (sets client_id)
- **ADR-0002**: JWT strategy (extracts auth.uid() for RLS)
- **ADR-0004**: Data retention (pg_cron runs as service role, RLS bypassed)

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-27  
**Status**: Accepted & Ready for Implementation
