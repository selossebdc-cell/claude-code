# US-002: RLS Policies & Access Control

**EPIC**: EPIC-1 (Database Schema & Security)  
**User Story**: As a security engineer, I need RLS policies enforced so that users cannot access another user's diagnostic data.

---

## Acceptance Criteria

- [ ] RLS enabled on `diagnostics` table
- [ ] SELECT policy: `(auth.uid()::uuid = diagnostics.client_id) OR (auth.role() = 'admin')`
- [ ] INSERT policy: `auth.uid()::uuid IS NOT NULL` (only authenticated users)
- [ ] UPDATE policy: `(auth.uid()::uuid = client_id) OR (auth.role() = 'admin')`
- [ ] DELETE policy: `(auth.uid()::uuid = client_id) OR (auth.role() = 'admin')`
- [ ] Admin role can bypass RLS and view all diagnostics
- [ ] Test verifies user A cannot read/write user B's rows

## Definition of Done

1. RLS enabled on diagnostics table
2. Policies created and tested
3. Cross-user access attempt returns 0 rows (silent failure, not error)
4. Admin account can view all diagnostics
5. Test data in place (user A row, user B row, admin verifies both visible to admin only)

## Technical Details

**SQL Policies**:
```sql
ALTER TABLE diagnostics ENABLE ROW LEVEL SECURITY;

-- SELECT: User sees only their own diagnostics, admin sees all
CREATE POLICY "Users see own diagnostics"
  ON diagnostics
  FOR SELECT
  USING ((auth.uid()::uuid = client_id) OR (auth.role() = 'admin'));

-- INSERT: Only authenticated users can insert
CREATE POLICY "Users can create diagnostics"
  ON diagnostics
  FOR INSERT
  WITH CHECK (auth.uid()::uuid IS NOT NULL);

-- UPDATE: User or admin can update
CREATE POLICY "Users update own diagnostics"
  ON diagnostics
  FOR UPDATE
  USING ((auth.uid()::uuid = client_id) OR (auth.role() = 'admin'))
  WITH CHECK ((auth.uid()::uuid = client_id) OR (auth.role() = 'admin'));

-- DELETE: User or admin can delete
CREATE POLICY "Users delete own diagnostics"
  ON diagnostics
  FOR DELETE
  USING ((auth.uid()::uuid = client_id) OR (auth.role() = 'admin'));
```

**Testing**:
- Insert row as user A (client_id = A's UUID)
- Insert row as user B (client_id = B's UUID)
- Query as user A → returns only A's row
- Query as user B → returns only B's row
- Query as admin → returns both rows

## Dependencies

Requires US-001 (diagnostics table columns exist).

## Related Specs

- Scope: **Section 4** (RLS Policies, Q-006)
- Brief: **Objective 3** (Secure-by-Design, cross-user access prevention)
