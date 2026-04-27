# US-006: Chat Function — JWT Validation & Payment Check

**EPIC**: EPIC-4 (Chat Authorization & Validation)  
**User Story**: As a security engineer, I need the /chat function to validate JWT and enforce payment so that only authorized, paid users can access the diagnostic.

---

## Acceptance Criteria

- [ ] Edge Function: modify existing `/functions/v1/chat`
- [ ] Extract JWT from `Authorization: Bearer <token>` header
- [ ] Return 401 if header missing or malformed
- [ ] Validate JWT signature and expiry (1-hour TTL) via `supabase.auth.getUser(jwt)`
- [ ] Return 401 if JWT invalid, expired, or signature mismatch
- [ ] Query `diagnostics` table for `paid_at` where `client_id = user.id`
- [ ] Return 403 if `paid_at` is NULL or missing (user never paid)
- [ ] Return 403 if `NOW() - paid_at > '30 days'::interval` (retention expired)
- [ ] Proceed to chat logic if JWT valid and payment current
- [ ] RLS enforced: user sees only own diagnostics
- [ ] Error messages are generic (no "token expired" vs "invalid signature")

## Definition of Done

1. JWT extraction and validation implemented
2. Payment status query works correctly
3. 401 and 403 status codes returned appropriately
4. RLS prevents user A from accessing user B's data
5. Test with valid JWT, expired JWT, no JWT, unpaid user, expired retention
6. Error messages do not leak sensitive information

## Technical Details

**Modified Handler**:
```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.104.1";

const supabase = createClient(
  Deno.env.get('SUPABASE_URL'),
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
);

serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 });

  // 1. Extract JWT
  const authHeader = req.headers.get('Authorization');
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return new Response(
      JSON.stringify({ error: 'Unauthorized' }),
      { status: 401, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const jwt = authHeader.slice(7);

  // 2. Validate JWT
  const { data: { user }, error: userErr } = await supabase.auth.getUser(jwt);
  if (userErr || !user) {
    return new Response(
      JSON.stringify({ error: 'Unauthorized' }),
      { status: 401, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const userId = user.id;

  // 3. Check payment status
  const { data: diagnostic, error: queryErr } = await supabase
    .from('diagnostics')
    .select('paid_at')
    .eq('client_id', userId)
    .maybeSingle();

  if (queryErr) {
    console.error('Payment status query failed:', { userId, error: queryErr.message });
    return new Response(
      JSON.stringify({ error: 'Forbidden' }),
      { status: 403, headers: { 'Content-Type': 'application/json' } }
    );
  }

  if (!diagnostic || !diagnostic.paid_at) {
    return new Response(
      JSON.stringify({ error: 'Forbidden' }),
      { status: 403, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // 4. Check retention (30 days)
  const paidDate = new Date(diagnostic.paid_at);
  const now = new Date();
  const daysDiff = (now.getTime() - paidDate.getTime()) / (1000 * 60 * 60 * 24);
  
  if (daysDiff > 30) {
    return new Response(
      JSON.stringify({ error: 'Forbidden' }),
      { status: 403, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // 5. Proceed to existing chat logic
  // (existing diagnostic processing code here)
  const { message } = await req.json();
  
  // Chat implementation (existing code)
  const response = 'Chat response from diagnostic...';

  return new Response(
    JSON.stringify({ response, diagnostic_id: diagnostic.id }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
});
```

**Environment Variables Required**:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Admin API key for querying with RLS

**RLS Note**:
- When using `SUPABASE_SERVICE_ROLE_KEY`, RLS is bypassed by design (server-side operation).
- However, the query `WHERE client_id = userId` enforces the security boundary in code.
- Frontend calls (with client key) would be protected by RLS automatically.

## Dependencies

Requires:
- US-001 (diagnostics table with `paid_at` column)
- US-002 (RLS policies in place)
- Existing `/chat` Edge Function implementation

## Related Specs

- Scope: **Section 3** (chat Function — Modify for Authentication, Q-004, Q-005, Q-006)
- Brief: **Objective 2** (Enforce authentication on /chat function)
