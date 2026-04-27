# TASK-0007: Modify chat Function — JWT & Payment Validation

**Epic**: EPIC-4 (Chat Authorization & Validation)  
**User Story**: US-006 (Chat Function — JWT Validation & Payment Check)  
**Priority**: CRITICAL  
**Effort**: 3 hours

---

## Overview

Modify the existing `/chat` Edge Function to validate JWT and enforce payment status before allowing access.

---

## Acceptance Criteria

- [ ] Extract JWT from `Authorization: Bearer <token>` header
- [ ] Return 401 if header missing or malformed
- [ ] Validate JWT signature and expiry via `supabase.auth.getUser(jwt)`
- [ ] Return 401 if JWT invalid, expired, or signature mismatch
- [ ] Query diagnostics table for `paid_at` where `client_id = user.id`
- [ ] Return 403 if `paid_at` missing or NULL (never paid)
- [ ] Return 403 if `NOW() - paid_at > '30 days'::interval` (expired)
- [ ] Proceed to chat logic if JWT valid and payment current
- [ ] RLS enforced: user sees only own diagnostics
- [ ] Error messages generic (no leakage of internal details)

---

## Definition of Done

- [ ] Edge Function modified and deployed
- [ ] JWT validation works (valid/invalid/expired/missing)
- [ ] Payment status check works (present/missing/expired)
- [ ] RLS prevents user A from accessing user B's data
- [ ] Tests: 401 for no JWT, expired JWT, invalid signature
- [ ] Tests: 403 for unpaid user, retention expired
- [ ] All error messages generic (no "token expired" leakage)

---

## Implementation

### Step 1: Backup Existing Function

Before modifying, backup current `/chat` function:
```bash
cp supabase/functions/chat/index.ts supabase/functions/chat/index.ts.backup
```

### Step 2: Modify Chat Function

Update `supabase/functions/chat/index.ts` to add JWT/payment validation:

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.104.1";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL") || "",
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || ""
);

interface ChatRequest {
  message: string;
}

interface ChatResponse {
  response: string;
  diagnostic_id: string;
}

async function validateJWT(token: string): Promise<{ userId: string } | null> {
  const { data: { user }, error } = await supabase.auth.getUser(token);

  if (error || !user) {
    return null;
  }

  return { userId: user.id };
}

async function checkPaymentStatus(userId: string): Promise<boolean> {
  const { data: diagnostic, error } = await supabase
    .from("diagnostics")
    .select("paid_at")
    .eq("client_id", userId)
    .maybeSingle();

  if (error) {
    console.error(
      "Payment status query failed",
      { 
        userId, 
        error: error.message,
        timestamp: new Date().toISOString() 
      }
    );
    return false;
  }

  if (!diagnostic || !diagnostic.paid_at) {
    return false;
  }

  // Check 30-day retention
  const paidDate = new Date(diagnostic.paid_at);
  const now = new Date();
  const daysDiff = (now.getTime() - paidDate.getTime()) / (1000 * 60 * 60 * 24);

  if (daysDiff > 30) {
    return false;
  }

  return true;
}

async function processChatRequest(
  userId: string,
  message: string
): Promise<ChatResponse> {
  // Existing chat logic here
  // This is a placeholder; replace with actual implementation

  // Example: Query diagnostic data, call Claude API, store response
  const { data: diagnostic } = await supabase
    .from("diagnostics")
    .select("id")
    .eq("client_id", userId)
    .maybeSingle();

  const response = `Diagnostic response for: ${message}`;
  const diagnostic_id = diagnostic?.id || "unknown";

  return { response, diagnostic_id };
}

serve(async (req) => {
  // 1. Check method
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  // 2. Extract and validate JWT
  const authHeader = req.headers.get("Authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return new Response(
      JSON.stringify({ error: "Unauthorized" }),
      { status: 401, headers: { "Content-Type": "application/json" } }
    );
  }

  const jwt = authHeader.slice(7);
  const authResult = await validateJWT(jwt);

  if (!authResult) {
    return new Response(
      JSON.stringify({ error: "Unauthorized" }),
      { status: 401, headers: { "Content-Type": "application/json" } }
    );
  }

  const userId = authResult.userId;

  // 3. Check payment status
  const hasPaid = await checkPaymentStatus(userId);

  if (!hasPaid) {
    return new Response(
      JSON.stringify({ error: "Forbidden" }),
      { status: 403, headers: { "Content-Type": "application/json" } }
    );
  }

  // 4. Parse request body
  let body: ChatRequest = { message: "" };
  try {
    body = await req.json();
  } catch (_err) {
    return new Response(
      JSON.stringify({ error: "Invalid JSON" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  const { message } = body;

  if (!message || typeof message !== "string") {
    return new Response(
      JSON.stringify({ error: "Invalid message" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  // 5. Process chat (existing logic, now with user context)
  try {
    const result = await processChatRequest(userId, message);

    console.log(
      "Chat request processed",
      { 
        userId, 
        messageLength: message.length,
        timestamp: new Date().toISOString() 
      }
    );

    return new Response(
      JSON.stringify(result),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (err) {
    console.error(
      "Chat processing failed",
      { 
        userId,
        error: (err as Error).message,
        timestamp: new Date().toISOString() 
      }
    );

    return new Response(
      JSON.stringify({ error: "Processing failed" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
});
```

### Step 3: Deploy Modified Function

```bash
# Deploy updated chat function
supabase functions deploy chat

# Verify deployment
supabase functions list
```

---

## Testing

### Test 1: Missing Authorization Header

```bash
curl -X POST https://your-project.supabase.co/functions/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}'
```

Expected: 401 response with `"error": "Unauthorized"`

### Test 2: Invalid JWT

```bash
curl -X POST https://your-project.supabase.co/functions/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid-token" \
  -d '{"message": "Test"}'
```

Expected: 401 response

### Test 3: Expired JWT

```bash
# Generate JWT, wait for expiry (1 hour), then call
# (Simulated in unit test with mocked time)
```

### Test 4: Unpaid User (403)

```typescript
// Create user without diagnostics row
const user = await supabase.auth.admin.createUser({ email: 'unpaid@test.com' });
const jwt = /* token from user */;

const response = await fetch('/functions/v1/chat', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${jwt}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ message: 'Test' })
});

assert(response.status === 403, 'Unpaid user returns 403');
```

### Test 5: Expired Retention (403)

```typescript
// Create user with diagnostics row >30 days old
const user = await supabase.auth.admin.createUser({ email: 'expired@test.com' });
const oldDate = new Date();
oldDate.setDate(oldDate.getDate() - 31);
await supabaseAdmin
  .from('diagnostics')
  .insert({
    stripe_session_id: 'cs_old',
    client_id: user.id,
    paid_at: oldDate.toISOString()
  });

const jwt = /* token from user */;
const response = await fetch('/functions/v1/chat', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${jwt}` },
  body: JSON.stringify({ message: 'Test' })
});

assert(response.status === 403, 'Expired retention returns 403');
```

### Test 6: Valid User (200)

```typescript
// Create user with current payment
const user = await supabase.auth.admin.createUser({ email: 'paid@test.com' });
await supabaseAdmin
  .from('diagnostics')
  .insert({
    stripe_session_id: 'cs_new',
    client_id: user.id,
    paid_at: new Date().toISOString()
  });

const jwt = /* token from user */;
const response = await fetch('/functions/v1/chat', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${jwt}` },
  body: JSON.stringify({ message: 'Test' })
});

assert(response.status === 200, 'Valid user returns 200');
const data = await response.json();
assert(data.response && data.diagnostic_id, 'Response includes data');
```

---

## Rollback Plan

If deployment fails:
```bash
# Restore from backup
cp supabase/functions/chat/index.ts.backup supabase/functions/chat/index.ts
supabase functions deploy chat
```

---

## Integration Notes

**RLS Enforcement**:
- Query uses `WHERE client_id = userId` in code (since using service role key)
- Frontend calls with anon key would be auto-protected by RLS
- Server-side validation ensures only user's data accessible

**Error Message Generality**:
- All auth/payment errors return generic `"Unauthorized"` / `"Forbidden"`
- Prevents attackers from determining if user exists, if paid, or if token expired

---

## Deployment Sequence

1. Modify chat function
2. Test locally with `supabase start`
3. Deploy to Supabase
4. Run all test cases
5. Verify no errors in Edge Function logs
6. Proceed to next task

---

## Related Specs

- Scope: **Section 3** (chat Function — Modify for Authentication, Q-004, Q-005, Q-006)
- Brief: **Objective 2** (Enforce authentication on /chat function)
