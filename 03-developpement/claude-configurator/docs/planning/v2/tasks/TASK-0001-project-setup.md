# TASK-0001: Project Setup & Configuration

**Epic**: EPIC-1 (Database Schema & Security)  
**User Story**: Prerequisite  
**Priority**: CRITICAL (must complete before other tasks)  
**Effort**: 2 hours

---

## Overview

Initialize the auth-stripe project by installing all dependencies, configuring environment variables, and verifying the build/test setup.

## Objective

Ensure project environment is ready for all subsequent tasks by installing exact package versions from stack-reference.md and verifying build/test pipelines.

---

## Acceptance Criteria

- [ ] All packages from stack-reference.md installed with exact versions
- [ ] Environment variables configured (both `.env.local` and Supabase secrets)
- [ ] Build passes without errors (`pnpm build`)
- [ ] Tests pass without errors (`pnpm test`)
- [ ] Supabase project initialized and accessible
- [ ] Stripe API keys configured in Supabase secrets

## Definition of Done

All developers can clone the repo, run setup, and have a functional dev environment.

---

## Implementation Steps

### 1. Install Runtime Dependencies

From stack-reference.md, install exact versions:

```bash
pnpm install stripe@22.1.0 @supabase/supabase-js@2.104.1
```

Verify installation:
```bash
pnpm ls stripe @supabase/supabase-js
```

### 2. Configure Environment Variables

Create `.env.local` in project root:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xyz.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_PRICE_ID=price_...
STRIPE_WEBHOOK_SECRET=whsec_...

# App
APP_URL=http://localhost:3000  # Local dev
# APP_URL=https://app.com  # Production
```

### 3. Configure Supabase Secrets

Via Supabase dashboard, set Edge Function secrets:

```bash
STRIPE_SECRET_KEY: sk_test_...
STRIPE_WEBHOOK_SECRET: whsec_...
SUPABASE_SERVICE_ROLE_KEY: eyJ...  (usually already set)
```

### 4. Verify Build

```bash
pnpm build
```

Expected output: Build completes without errors (0 exit code).

### 5. Verify Tests

```bash
pnpm test
```

Expected output: All tests pass (0 exit code).

### 6. Verify Supabase Connection

```bash
pnpm exec supabase status
```

Expected output: Project status shows connected, no errors.

---

## Technical Context

**Stack Reference Source**: `/docs/specs/stack-reference.md`

**Key Dependencies**:
- `stripe@22.1.0`: Webhook verification, checkout session creation
- `@supabase/supabase-js@2.104.1`: Auth, database queries, RLS
- Build tools: `pnpm` (package manager)
- Test framework: `jest` or `vitest` (existing setup)

**Environment Scopes**:
- Development: `.env.local` (local testing, ngrok for webhooks)
- Staging: Supabase preview branch (optional)
- Production: Environment variables in deployment platform (Vercel, etc.)

---

## Verification Checklist

- [ ] `pnpm ls` shows all packages installed
- [ ] `.env.local` exists with all keys populated
- [ ] `pnpm build` exits with code 0
- [ ] `pnpm test` exits with code 0 (or skipped if no tests yet)
- [ ] Supabase CLI shows project status connected
- [ ] Stripe keys verified in Supabase secrets dashboard

---

## Blockers / Dependencies

None (prerequisite task).

---

## Notes

**Webhook Testing Locally**:
- Use ngrok to expose localhost to Stripe webhooks:
  ```bash
  ngrok http 3000
  # Copy forwarding URL: https://abc123.ngrok.io
  # Configure Stripe dashboard webhook endpoint: https://abc123.ngrok.io/functions/v1/stripe-webhook
  ```

**Package Version Pinning**:
- Do NOT use `^` or `~` in package.json for auth-stripe dependencies.
- Pin exact versions to match stack-reference.md (prevents surprises in builds).

---

## Related Specs

- Stack Reference: `/docs/specs/stack-reference.md` (source of truth for versions)
