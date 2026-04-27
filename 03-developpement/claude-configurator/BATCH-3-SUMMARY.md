# BUILD Phase — Batch 3 Summary

**Status**: ✅ COMPLETE  
**Date**: 2026-04-27  
**Tasks**: TASK-0007  
**Effort**: 3 hours (planned)

---

## Deliverables

### TASK-0007: Modify `/chat` Function — JWT Validation + Payment Check

**File**: `supabase/functions/chat/index.ts`

Added security gates to prevent unauthorized access to the diagnostic chat:

#### 1. **JWT Validation**
- Extracts `Authorization: Bearer <token>` header
- Validates JWT against Supabase Auth using `supabase.auth.getUser(token)`
- Extracts `userId` from JWT claims
- Returns **401** if missing, invalid, or expired

```typescript
const authHeader = req.headers.get("authorization");
if (!authHeader || !authHeader.startsWith("Bearer ")) {
  return 401: "Missing or invalid Authorization header"
}

const jwtValidation = await validateJWT(token);
if (!jwtValidation.valid) {
  return 401: jwtValidation.error
}
```

#### 2. **Payment Status Check**
- Queries `diagnostics` table for user's payment record
- **Condition**: `paid_at IS NOT NULL AND paid_at >= NOW() - interval '30 days'`
- Meaning: User purchased access within the last 30 days
- Returns **403** if no active payment

```typescript
const paymentCheck = await checkPaymentStatus(userId);
if (!paymentCheck.hasPaid) {
  return 403: {
    error: "No active payment. Please purchase access.",
    code: "PAYMENT_REQUIRED"
  }
}
```

#### 3. **RLS Isolation**
- Metadata now includes `client_id = userId` (authenticated user)
- All subsequent queries via metadata-manager enforce RLS (row-level security)
- User can only see/modify their own diagnostic session

#### 4. **Implementation Details**
- Added `validateJWT()` helper → validates token + extracts user ID
- Added `checkPaymentStatus()` helper → queries diagnostics table with payment window
- Integrated checks into handler **before** processing chat request
- Fallback metadata includes authenticated `client_id` for RLS

---

## Security Guarantees

### ✅ Authentication (JWT)
- Only valid Supabase Auth tokens accepted
- Invalid/expired JWTs blocked with 401
- User identity extracted from JWT `sub` claim

### ✅ Payment Verification
- Verifies `paid_at` timestamp (30-day retention window)
- Prevents access if no payment or payment expired
- Returns 403 with clear error message

### ✅ RLS Enforcement
- Every diagnostic session linked to authenticated `client_id`
- Metadata manager enforces row-level visibility
- Admin users (with `auth.role() = 'admin'`) can override via service_role

### ✅ Access Control Flow
```
Request → Check JWT → Extract userId
→ Check payment (paid_at >= NOW() - 30 days)
→ Load metadata (client_id = userId)
→ Process chat with RLS isolation
```

---

## HTTP Status Codes

| Status | Meaning | Example |
|--------|---------|---------|
| **200** | Chat succeeds (streaming) | Access granted, diagnostic continues |
| **400** | Bad request | Missing message, invalid JSON |
| **401** | Unauthorized | Missing JWT or signature invalid |
| **403** | Forbidden | Payment required (paid_at expired) |
| **405** | Method not allowed | GET instead of POST |
| **500** | Server error | Supabase down, Anthropic API error |

---

## Testing Checklist

### Unit Tests
- [ ] `validateJWT()` accepts valid token → returns `{ valid: true, userId }`
- [ ] `validateJWT()` rejects invalid token → returns `{ valid: false, error }`
- [ ] `checkPaymentStatus()` finds active payment → returns `{ hasPaid: true, paidAt }`
- [ ] `checkPaymentStatus()` finds expired payment → returns `{ hasPaid: false }`

### Integration Tests
- [ ] POST to `/chat` without Authorization header → 401
- [ ] POST with expired JWT → 401
- [ ] POST with valid JWT but no payment → 403
- [ ] POST with valid JWT + active payment → 200 (streaming)
- [ ] RLS: User A cannot see User B's diagnostics (Supabase RLS policy)

### E2E Test Flow
1. User clicks "Purchase" → redirects to Stripe
2. Stripe → webhook → creates auth.users + sends magic link
3. User opens magic link → redirects to `/auth/callback` → sets localStorage JWT
4. User calls POST `/chat` with `Authorization: Bearer <jwt>`
5. Server validates JWT + checks payment
6. If valid: Stream diagnostic chat
7. If expired/no payment: Return 403

---

## Next Steps

### Immediate (Before Batch 4)
1. **Deploy modified `/chat` function**:
   ```bash
   supabase functions deploy chat
   ```

2. **Test with Stripe webhook flow** (ensure payment status persists):
   ```bash
   # Simulate checkout completion
   stripe trigger checkout.session.completed
   
   # Verify diagnostics table has paid_at timestamp
   SELECT * FROM diagnostics WHERE client_email = 'test@example.com';
   ```

3. **Test JWT + payment check**:
   ```bash
   # After magic link created, test chat access
   curl -X POST http://localhost:3000/chat \
     -H "Authorization: Bearer <jwt_from_magic_link>" \
     -H "Content-Type: application/json" \
     -d '{"session_id": "...", "message": "..."}'
   ```

### Batch 4 (Next) — Frontend Integration
- TASK-0008: Magic Link Callback Handler (`/auth/callback`)
- TASK-0009: Frontend JWT Management (localStorage + Authorization header)
- TASK-0010: Update Success Page (confirmation UI)
- Effort: 5.5 hours

### Timeline
- **Batch 1**: Database foundation (6.5h) ✅
- **Batch 2**: Backend webhooks (5h) ✅
- **Batch 3**: Chat authorization (3h) ✅
- **Batch 4**: Frontend integration (5.5h) → Next
- **Total**: ~20.5 hours

---

## Security Notes

**30-Day Access Window**:
- User pays on Day 0 → `paid_at = NOW()`
- User can access diagnostic until Day 30
- On Day 31: `paid_at < NOW() - 30 days` → access denied
- This window is **independent of JWT expiration** (JWT can be 1h, access window is 30 days)

**RLS Isolation**:
- `diagnostics` table RLS policy: `auth.uid() = client_id OR auth.role() = 'admin'`
- Service role key (backend) bypasses RLS for webhook processing
- Client-side JWT (frontend) enforces row-level isolation

**Payment Verification Flow**:
1. Webhook invites user → creates `auth.users` row
2. Magic link sent → user signs in
3. Frontend calls `/chat` with JWT
4. Server checks: `SELECT paid_at FROM diagnostics WHERE client_id = userId AND paid_at IS NOT NULL`
5. If found and recent: ✅ Access granted
6. If not found or expired: ❌ Access denied (403)

---

**Ready for Batch 4 once `/chat` function deployed.**
