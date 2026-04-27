# ADR-0002: JWT Authentication Strategy (1 Hour Expiry, Stateless, No Refresh)

**Status**: Accepted  
**Date**: 2026-04-27  
**Context**: Auth-Stripe integration (greenfield-auth)  
**Participants**: Product, Security, Engineering

---

## Problem Statement

User authentication requires:
1. **Persistent sign-in** (user doesn't re-authenticate on every page reload)
2. **Time-limited access** (invalid token after logout or inactivity)
3. **Secure credential transport** (no passwords in localStorage)
4. **Simple session management** (stateless, no server-side session table)

Trade-offs:
- **Long TTL** (24h+): User stays signed in longer, but more time for token theft
- **Short TTL** (1h): More secure, but user must re-authenticate frequently
- **Refresh tokens**: Extend TTL securely, but add complexity and server state
- **No refresh**: Simple, stateless, but user forced to re-auth on TTL expiry

---

## Decision

**We use JWT with 1-hour expiry, stored in localStorage, validated server-side on every /chat request. No refresh tokens.**

### Strategy

1. **Issuance**: Supabase issues JWT after magic link verification
   - TTL: 1 hour (3600 seconds)
   - Algorithm: HS256 (HMAC-SHA256)
   - Signature: Verified via Supabase secret

2. **Storage**: JWT stored in browser localStorage
   - Survives page reload (persistent)
   - Accessible to frontend code
   - Sent in Authorization header to backend

3. **Validation**: Server validates on every /chat request
   - Signature verified via Supabase secret
   - Expiry checked: `NOW() < exp`
   - User ID extracted: `user.id` from JWT
   - No caching: fresh validation on every request

4. **Payment Status**: Checked separately (NOT in JWT)
   - Query diagnostics table: `SELECT paid_at WHERE client_id = user.id`
   - Checked on every /chat request
   - Not cached in JWT (allows payment window updates)

5. **Expiry Behavior**: On 401 (JWT invalid)
   - Frontend clears localStorage
   - Redirects to `/pricing`
   - User must re-pay or request new magic link

---

## Rationale

### Why JWT (not session cookies)?

**Option A: Session Cookies** (❌ NOT CHOSEN)
```
Server: Set-Cookie: sessionId=abc123; HttpOnly; Secure; SameSite=Strict
Client: Browser auto-includes cookie
```

**Problems**:
- Requires session table on server (breaks stateless architecture)
- CSRF protection needed (CSRF tokens)
- Logout requires server-side session invalidation
- Cookie same-site policy complex for cross-origin

**Option B: JWT** (✓ CHOSEN)
```
Server: Authorization: Bearer <jwt>
Client: localStorage + manual header
```

**Benefits**:
- Stateless (no session table)
- No CSRF (explicit header, browsers block via CORS)
- Backend is simple (just verify signature)
- Works for SPAs and mobile

**Conclusion**: JWT is better for stateless, SPA architecture.

---

### Why 1 Hour (not 24h, 7d, or longer)?

**Option A: Long TTL (24h+)** (❌ NOT CHOSEN)
- Pros: User stays signed in longer
- Cons: Longer attack window if token stolen (XSS, network sniff)
- Risk: Compromised token allows access for full day

**Option B: Short TTL (1h)** (✓ CHOSEN)
- Pros: Attack window limited to 1h
- Cons: User must re-auth more frequently (minor UX friction)

**Recommendation** (from OAuth 2.0 / OpenID Connect):
- Access token (short-lived): 1h typical
- Refresh token (long-lived): 7d+ (extends access)

**Our choice**: 1h without refresh tokens (simplest, still acceptable for chat app)

**Reasoning**:
- Chat is interactive app (user doesn't leave for days)
- User re-authenticating every 1h for security-sensitive payment scenario is acceptable
- Avoids complexity of refresh token rotation + server state

**Exception**: If UX testing shows 1h too aggressive, can extend to 2-4h (still < typical day-long sessions).

---

### Why NO Refresh Tokens (not long-lived refresh)?

**Option A: With Refresh Tokens** (⚠️ More Complex)
```
Access Token (JWT): 1h, httpOnly cookie (secure)
Refresh Token (JWT): 7d, localStorage (can be stolen)

On 401 (access expired):
  POST /refresh {refresh_token} → new JWT
```

**Complexity**:
- 2 tokens to manage
- Refresh token rotation needed (security best practice)
- Requires refresh endpoint (server code)
- More moving parts = more bugs

**Option B: No Refresh (✓ CHOSEN)**
```
Access Token (JWT): 1h

On 401 (access expired):
  User redirected to /pricing
  Can re-purchase or request new magic link
```

**Simplicity**:
- 1 token
- No refresh endpoint
- Clear UX (user knows they must re-auth)

**Trade-off**:
- User might need to re-pay if JWT expires during long chat session
- Acceptable for this use case (diagnostic analysis, not long-running session)

---

### Why localStorage (not sessionStorage)?

**Option A: sessionStorage** (❌ NOT CHOSEN)
- Clears when browser tab closes
- Doesn't survive page reload
- User forced to re-auth on F5

**Option B: localStorage** (✓ CHOSEN)
- Survives page reload
- Persists across browser sessions
- User can close browser, return later, still signed in (until JWT expiry)

**Conclusion**: localStorage better for user experience (less friction).

---

### Why Server-Side Validation (not client-side decoding)?

**Option A: Client-Side Trust** (❌ SECURITY RISK)
```javascript
// Don't do this!
const decoded = jwt_decode(token);
if (decoded.exp > Date.now() / 1000) {
  // "Token valid", proceed
}
```

**Problems**:
- Client can't validate signature (secret key is server-only)
- Client can't trust claims (attacker forges token)
- Attacker can modify exp, user_id, etc.

**Option B: Server-Side Validation** (✓ CHOSEN)
```javascript
const { user, error } = await supabase.auth.getUser(jwt);
if (!error) {
  // Token valid, claims verified by server
}
```

**Benefits**:
- Signature verified with secret key (only server has it)
- Token expiry checked server-side (not client time)
- Claims trusted (not modified by client)

**Conclusion**: Always validate JWT server-side.

---

## Implementation

### Frontend: JWT Storage

```typescript
// After magic link sign-in
const { data, error } = await supabase.auth.verifyOtp({...});
if (!error) {
  const { data: { session } } = await supabase.auth.getSession();
  const jwt = session?.access_token;
  localStorage.setItem('jwt', jwt);  // Persist
  window.location.href = '/chat?onboarded=true';
}

// On page load
const jwt = localStorage.getItem('jwt');
if (!jwt) {
  window.location.href = '/pricing';  // No token, require sign-in
}
```

### Frontend: Sending JWT in /chat

```typescript
const jwt = localStorage.getItem('jwt');
const response = await fetch('/functions/v1/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${jwt}`
  },
  body: JSON.stringify({message: userInput})
});

if (response.status === 401) {
  // JWT expired or invalid
  localStorage.removeItem('jwt');
  window.location.href = '/pricing';
} else if (response.status === 403) {
  // User not paid or retention expired
  alert('You need to purchase to access this feature.');
} else if (response.ok) {
  // Success, process response
}
```

### Backend: JWT Validation

```typescript
export async function chat(req: Request) {
  const authHeader = req.headers.get('Authorization');
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return new Response(JSON.stringify({error: 'Unauthorized'}), {status: 401});
  }

  const jwt = authHeader.substring(7);

  // Validate JWT (signature + expiry)
  const { data: { user }, error } = await supabase.auth.getUser(jwt);
  if (error || !user) {
    return new Response(JSON.stringify({error: 'Unauthorized'}), {status: 401});
  }

  // JWT valid, proceed with request
  // ...
}
```

---

## JWT Claims Structure

**Example JWT** (decoded):
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "aud": "authenticated",
  "iat": 1234567890,
  "exp": 1234571490,
  "role": "authenticated",
  "iss": "https://xyz.supabase.co/auth/v1"
}
```

**Claims**:
- `sub`: User UUID (used for RLS)
- `email`: User email
- `aud`: Audience ("authenticated")
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp (iat + 3600)
- `role`: User role (for RLS policy, admin override)
- `iss`: Issuer (Supabase auth service)

**Important**: `exp` claim is sole source of truth for expiry (not checked client-side).

---

## Payment Status Validation

**NOT in JWT**: paid_at, payment_status, retention window

**WHY**: JWT is immutable until expiry. If we cached payment status in JWT:
- User pays, gets JWT without payment yet (race condition)
- User pays, JWT cached as "unpaid" (stale data)
- User must wait for new JWT to use paid status (poor UX)

**SOLUTION**: Check paid_at on every /chat request:
```sql
SELECT paid_at FROM diagnostics WHERE client_id = user.id
```
- Always fresh (real-time)
- User can pay once, immediately access /chat
- No stale data problems

---

## Logout & Session Invalidation

**No explicit logout in this phase** (out of scope)

**Session ends when**:
- JWT expires (1h) → 401 on /chat → frontend clears localStorage
- User closes browser → localStorage persists, but user manually logs out (future feature)
- User clears browser data → localStorage cleared

**Note**: If logout needed in future (force invalidation), add:
- Token blacklist table (JWT blacklist after logout)
- Check during validation: `SELECT 1 FROM jwt_blacklist WHERE jti = ?`
- Would break statelessness, but acceptable for logout feature

---

## Test Cases

### Test 1: Normal Sign-In & Access

1. User completes magic link flow
2. JWT stored in localStorage (exp = NOW + 3600)
3. User calls /chat with valid JWT
4. Server validates signature ✓
5. Server checks expiry: NOW < exp ✓
6. Request proceeds (200 OK)

**Result**: ✓ Access granted

---

### Test 2: Expired JWT

1. JWT stored (exp = NOW - 100, already expired)
2. User calls /chat with expired JWT
3. Server validates signature ✓
4. Server checks expiry: NOW > exp ✗
5. Server returns 401

**Result**: ✓ Rejected, user redirected to /pricing

---

### Test 3: Forged JWT

1. Attacker creates fake JWT (signs with wrong key)
2. Attacker calls /chat with forged JWT
3. Server validates signature ✗ (HMAC doesn't match)
4. Server returns 401

**Result**: ✓ Rejected

---

### Test 4: Modified JWT

1. User gets valid JWT
2. Attacker modifies JWT (changes user_id or exp)
3. Attacker sends modified JWT
4. Server validates signature ✗ (HMAC no longer matches)
5. Server returns 401

**Result**: ✓ Rejected

---

### Test 5: JWT Boundary (59m 59s)

1. JWT stored (exp = NOW + 3599)
2. User calls /chat
3. Server checks: NOW + 1s < exp ✓
4. Request proceeds

**Result**: ✓ Still valid (grace period)

---

### Test 6: JWT Boundary (1h 1s)

1. JWT stored (exp = NOW + 3600)
2. Wait 3601 seconds
3. User calls /chat
4. Server checks: NOW > exp ✗
5. Server returns 401

**Result**: ✓ Expired exactly at 1h + 1s

---

## Consequences

### Positive
- ✓ Stateless (no session table required)
- ✓ Secure (1h expiry limits attack window)
- ✓ Simple (no refresh token complexity)
- ✓ Scalable (no session lookup on every request, just verify signature)
- ✓ Durable (JWT survives server restart)

### Negative
- ✗ User must re-auth every 1h (minor UX friction)
- ✗ No forced logout (user can't invalidate token early)
- ✗ localStorage can be read by XSS (but only during attack window)

### Mitigations
- User re-auth every 1h is acceptable for security-sensitive payment scenario
- Logout feature can be added later (blacklist table)
- XSS mitigation: proper input sanitization, CSP headers

---

## Related Decisions

- **ADR-0001**: Webhook idempotence (payment → user → diagnostic)
- **ADR-0003**: RLS policy design (uses user UUID from JWT)
- **ADR-0004**: Data retention (separate from JWT lifetime)

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-27  
**Status**: Accepted & Ready for Implementation
