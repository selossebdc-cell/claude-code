# Deployment Guide — EPIC-1 & EPIC-4

## Prerequisites

1. **Supabase CLI installed**
   ```bash
   brew install supabase
   ```

2. **Authentication** (required for remote deployment)
   ```bash
   supabase login
   ```
   This will open a browser window to authenticate and generate an access token.

3. **ANTHROPIC_API_KEY** ready
   - Get from your Anthropic account (https://console.anthropic.com/)

## Quick Start Secrets (1Password)

Use this workflow before any local dev, deploy, or function test.

1. Store secrets in 1Password vault `APIs` with standardized items:
   - `Claude Configurator - Anthropic - Prod`
   - `Claude Configurator - Supabase - Prod`
   - `Claude Configurator - Stripe - Prod`
2. Keep `.env.local` with `op://...` references only (no raw keys).
3. Run commands through 1Password env resolution:

```bash
op run --env-file=.env.local -- <command>
```

Example checks:

```bash
op run --env-file=.env.local -- env | grep -E "ANTHROPIC|SUPABASE|STRIPE"
op run --env-file=.env.local -- supabase functions list --project-ref ptksijwyvecufcvcpntp
```

Rules:
- `.env.example` must contain placeholders only.
- If a secret was exposed in plain text, rotate it immediately.

## Deployment Steps

### Step 1: Apply Database Migration (EPIC-4)

```bash
cd /Users/cath/Library/CloudStorage/GoogleDrive-catherine@csbusiness.fr/Drive\ partagés/CS\ -\ Consulting\ Stragégique/03-developpement/claude-configurator

# Apply migration to create diagnostics table
supabase db push --project-ref ptksijwyvecufcvcpntp
```

This will:
- Create the `diagnostics` table with JSONB fields for metadata and conversation history
- Set up indexes on session_id, client_id, and metadata fields
- Configure RLS policies for security
- Create automatic updated_at timestamp trigger

### Step 2: Deploy Chat Edge Function (EPIC-1)

```bash
# Deploy the chat function
supabase functions deploy chat --project-ref ptksijwyvecufcvcpntp
```

Verify deployment:
```bash
supabase functions list --project-ref ptksijwyvecufcvcpntp
# Should show: chat (public)
```

### Step 2b: Deploy Generate-Config Edge Function (EPIC-7)

```bash
supabase functions deploy generate-config --project-ref ptksijwyvecufcvcpntp
```

Same auth rules as `chat` (JWT + paiement actif). Call after diagnostic metadata contains `synthesis` and `living_proposal`:

```bash
curl -X POST https://ptksijwyvecufcvcpntp.supabase.co/functions/v1/generate-config \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer <YOUR_SUPABASE_USER_JWT>" \
  -d '{"session_id":"<SESSION_UUID>"}'
```

Réponse JSON : pack complet (`markdown_bundle`, `structured`, `validation`). Sans `Accept: application/json`, la réponse est un flux SSE avec événements `progress` puis `complete`.

### Step 3: Set Environment Secrets

```bash
# Set the Anthropic API key
supabase secrets set ANTHROPIC_API_KEY=sk-ant-... --project-ref ptksijwyvecufcvcpntp
```

### Step 4: Test the Deployment

The `chat` function expects a **paid** diagnostic row (`paid_at` within 30 days) and a valid **JWT**:

```bash
curl -X POST https://ptksijwyvecufcvcpntp.supabase.co/functions/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_SUPABASE_USER_JWT>" \
  -d '{
    "session_id": "test-session-001",
    "message": "Hello, I am an engineer managing electronics export.",
    "conversation_history": [],
    "client_name": "Test Client"
  }'
```

Expected response: SSE stream (text/event-stream). Without `Authorization` or payment, expect `401` / `403`.

---

## Liens application (production)

| Page | URL |
|------|-----|
| Setup / tunnel principal | **https://setup.csbusiness.fr** |
| Chat diagnostic | **https://setup.csbusiness.fr/chat.html** |

`APP_URL` en prod doit être `https://setup.csbusiness.fr` (Stripe success/cancel + magic links).

---

## Tester sans payer ni ouvrir le navigateur (QA interne)

Pour éviter `Invalid JWT` ou `PAYMENT_REQUIRED` pendant les tests :

### A — Bypass paiement (Edge secrets)

Dans Supabase → Project Settings → Edge Functions → Secrets (ou CLI) :

```bash
supabase secrets set SKIP_PAYMENT_CHECK=true --project-ref ptksijwyvecufcvcpntp
```

Ou, plus contrôlé : définir une clé opaque puis envoyer un header sur **chaque** requête `chat` / `generate-config` :

```bash
supabase secrets set CONFIGURATOR_DEV_KEY='une-longue-chaine-secrete' --project-ref ptksijwyvecufcvcpntp
```

```bash
curl ... -H "X-Configurator-Dev-Key: une-longue-chaine-secrete"
```

**À retirer en production** (`SKIP_PAYMENT_CHECK` vide ou `false`, secret rotation si exposé).

### B — Obtenir un vrai JWT depuis le terminal (`dev-mint-token`)

1. Définir un mot de passe partagé pour les comptes mintés :

```bash
supabase secrets set DEV_LOGIN_PASSWORD='MotDePasseFortPourQAUniquement' --project-ref ptksijwyvecufcvcpntp
```

`CONFIGURATOR_DEV_KEY` doit être défini (même valeur que ci-dessus pour la section A).

2. Déployer la fonction :

```bash
supabase functions deploy dev-mint-token --project-ref ptksijwyvecufcvcpntp
```

3. Mint :

```bash
curl -s -X POST "https://ptksijwyvecufcvcpntp.supabase.co/functions/v1/dev-mint-token" \
  -H "Content-Type: application/json" \
  -H "X-Configurator-Dev-Key: une-longue-chaine-secrete" \
  -d '{"email":"ton-email@csbusiness.fr"}'
```

La réponse JSON contient :
- **`access_token`** (JWT à utiliser dans `Authorization: Bearer ...`)
- **`latest_sessions`** (5 dernières sessions diagnostics)
- **`preferred_session_id`** (session la plus récente quand disponible)

Utilise `preferred_session_id` pour ton premier test `generate-config`.

`Authorization: Bearer <access_token>`

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Access token not provided" | Run `supabase login` |
| "Cannot connect to Docker" | Not needed for remote deployment |
| "Function not found after deploy" | Wait 30s and try again, or check Supabase dashboard |
| "CORS errors from frontend" | Verify `SUPABASE_FUNCTIONS_URL` in frontend/js/chat.js |

---

## Post-Deployment Verification Checklist

- [ ] Migration applied successfully (check Supabase dashboard → SQL Editor)
- [ ] Chat function deployed (check Supabase dashboard → Edge Functions)
- [ ] ANTHROPIC_API_KEY set (check Supabase dashboard → Settings → Secrets)
- [ ] Test curl request returns SSE stream
- [ ] Frontend can call `/functions/v1/chat` (CORS working)

---

## Rollback (if needed)

```bash
# Remove the chat function
supabase functions delete chat --project-ref ptksijwyvecufcvcpntp

# Rollback migration (drop diagnostics table)
# Note: This requires manual SQL execution in Supabase dashboard
# Go to SQL Editor and run: DROP TABLE IF EXISTS diagnostics CASCADE;
```

---

## Next Steps After Deployment

Once deployment is verified:
1. Test E2E with frontend (open configurator in browser)
2. Run diagnostic conversation test (10+ turns)
3. Verify message compression and metadata persistence in Supabase dashboard
4. Proceed to EPIC-2: Pattern Detection Engine
