# TASK-0003: Implement RLS Policies

**Epic**: EPIC-1 (Database Schema & Security)  
**User Story**: US-002 (RLS Policies & Access Control)  
**Priority**: CRITICAL  
**Effort**: 1.5 hours

---

## Overview

Enable Row-Level Security (RLS) on diagnostics table and create SELECT/INSERT/UPDATE/DELETE policies.

---

## Acceptance Criteria

- [ ] RLS enabled on `diagnostics` table
- [ ] SELECT policy allows user to see own diagnostics + admin sees all
- [ ] INSERT policy allows only authenticated users
- [ ] UPDATE and DELETE policies allow user or admin
- [ ] Test verifies cross-user isolation (user A cannot read user B's data)
- [ ] Admin account can view all diagnostics

---

## Definition of Done

- [ ] All policies created and tested
- [ ] Cross-user access attempt returns 0 rows
- [ ] Admin account verified with elevated access
- [ ] Test data confirms RLS enforced

---

## Implementation

### Step 1: Enable RLS on diagnostics Table

```sql
ALTER TABLE diagnostics ENABLE ROW LEVEL SECURITY;
```

### Step 2: Create RLS Policies

Connect to Supabase and execute:

```sql
-- SELECT: User sees only their own diagnostics, admin sees all
CREATE POLICY "Users see own diagnostics"
  ON diagnostics
  FOR SELECT
  USING (
    (auth.uid()::uuid = client_id) 
    OR (auth.role() = 'admin')
  );

-- INSERT: Only authenticated users can insert
CREATE POLICY "Users can create diagnostics"
  ON diagnostics
  FOR INSERT
  WITH CHECK (auth.uid()::uuid IS NOT NULL);

-- UPDATE: User or admin can update
CREATE POLICY "Users update own diagnostics"
  ON diagnostics
  FOR UPDATE
  USING (
    (auth.uid()::uuid = client_id) 
    OR (auth.role() = 'admin')
  )
  WITH CHECK (
    (auth.uid()::uuid = client_id) 
    OR (auth.role() = 'admin')
  );

-- DELETE: User or admin can delete
CREATE POLICY "Users delete own diagnostics"
  ON diagnostics
  FOR DELETE
  USING (
    (auth.uid()::uuid = client_id) 
    OR (auth.role() = 'admin')
  );
```

### Step 3: Verify Policies Created

```sql
-- List all policies on diagnostics table
SELECT policyname, cmd, qual, with_check 
FROM pg_policies 
WHERE tablename = 'diagnostics';
```

Expected output: 4 policies listed.

---

## Testing

### Test 1: Verify User Isolation

```bash
# Create two test users and rows
# 1. Insert row as user A
# 2. Insert row as user B
# 3. Query as user A → should see only A's row
# 4. Query as user B → should see only B's row
```

**Test Script** (pseudocode):

```typescript
// 1. Create user A
const userA = await supabase.auth.admin.createUser({ email: 'a@test.com' });

// 2. Insert diagnostics row for user A
const jwtA = /* token from userA */;
const supabaseA = createClient(url, anonKey, { global: { headers: { Authorization: `Bearer ${jwtA}` } } });
await supabaseA.from('diagnostics').insert({ client_id: userA.id, paid_at: now, stripe_session_id: 'cs_a' });

// 3. Create user B
const userB = await supabase.auth.admin.createUser({ email: 'b@test.com' });

// 4. Insert diagnostics row for user B
const jwtB = /* token from userB */;
const supabaseB = createClient(url, anonKey, { global: { headers: { Authorization: `Bearer ${jwtB}` } } });
await supabaseB.from('diagnostics').insert({ client_id: userB.id, paid_at: now, stripe_session_id: 'cs_b' });

// 5. Query as user A → should return 1 row (only A's)
const rowsA = await supabaseA.from('diagnostics').select('*');
assert(rowsA.length === 1 && rowsA[0].client_id === userA.id, 'User A sees only own row');

// 6. Query as user B → should return 1 row (only B's)
const rowsB = await supabaseB.from('diagnostics').select('*');
assert(rowsB.length === 1 && rowsB[0].client_id === userB.id, 'User B sees only own row');
```

### Test 2: Verify Admin Access

```typescript
// Query as admin (using service role key)
const supabaseAdmin = createClient(url, serviceRoleKey);
const allRows = await supabaseAdmin.from('diagnostics').select('*');
assert(allRows.length === 2, 'Admin sees all rows');
```

---

## Deployment Sequence

1. Enable RLS on diagnostics table
2. Create SELECT policy
3. Create INSERT policy
4. Create UPDATE policy
5. Create DELETE policy
6. Run tests to verify RLS enforced
7. Proceed to next task

---

## Rollback Plan

If needed, disable RLS:

```sql
ALTER TABLE diagnostics DISABLE ROW LEVEL SECURITY;
```

(Note: Only in development; never disable RLS in production.)

---

## Security Rationale

**RLS Enforces Data Isolation**:
- Regular users cannot see other users' diagnostics
- Admin override allows support/debugging without direct database access
- Every query respects the policy (no exceptions)

**Policy Logic**:
- `(auth.uid()::uuid = client_id)`: User ID matches row's client_id
- `(auth.role() = 'admin')`: User assigned admin role in Supabase auth
- Policies combined with OR logic: user OR admin can access

---

## Related Specs

- Scope: **Section 4** (RLS Policies, Q-006)
- Brief: **Objective 3** (Secure-by-Design, cross-user access prevention)
