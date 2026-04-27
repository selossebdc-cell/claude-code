---
name: RLS Testing & Debugging Methodology (Confirmed)
description: Effective approach for testing PostgreSQL RLS isolation bugs when frontend code uses JWT-authenticated queries
type: feedback
---

## Testing RLS Issues: What Works

**Why**: When users report data isolation problems, you need to verify whether the issue is at the RLS layer (database enforcement) or the frontend layer (JavaScript logic).

**How to Apply**: 
1. Verify RLS policies exist and are correctly configured in Supabase (check with `pg_policies` query)
2. Query the data directly in Supabase SQL editor to confirm RLS is working (test both users)
3. **Always check what values are being passed to the query** — inspect `appState` or session variables
4. If RLS works in SQL editor but fails in JavaScript, the bug is in the frontend code, not the database

## This Session's Learnings

**Problem**: Taïna saw Aurélia's templates despite RLS policies existing and being correct.

**Debugging Path**:
- ❌ First assumption: RLS policies broken
- ✅ Actual issue: `appState.currentClientId` contained user ID instead of client_id

**Solution**: Inspect what the frontend is actually passing to Supabase queries, not just whether RLS exists.

## Confirmed Best Practices

**RLS Testing Checklist**:
- [ ] RLS enabled on table? (`pg_tables.rowsecurity = true`)
- [ ] Policies exist? (`pg_policies` query shows them)
- [ ] Policies correct? Check `qual` column (USING clause)
- [ ] Test as different users in SQL editor: do they get different results?
- [ ] Frontend values correct? (`appState.currentClientId` = actual client_id, not user_id)
- [ ] End-to-end test: Login as User A → verify data isolated from User B

## When to Deep-Dive into Frontend

If SQL editor tests pass (RLS working) but browser tests fail, focus on:
1. Session/storage variables holding wrong values
2. Hard refresh needed (browser cache)
3. Deployment lag (local changes not live on server)

## Co-Author Feedback

User prefers: "Correct the code directly" rather than reporting and asking for confirmation. This applies to bugs with clear root cause and simple fixes.

---

**Last Updated**: 2026-04-27  
**Applied to**: Portail Client V2 template isolation bug
