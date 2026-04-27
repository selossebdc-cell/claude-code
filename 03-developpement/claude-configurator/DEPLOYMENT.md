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

### Step 3: Set Environment Secrets

```bash
# Set the Anthropic API key
supabase secrets set ANTHROPIC_API_KEY=sk-ant-... --project-ref ptksijwyvecufcvcpntp
```

### Step 4: Test the Deployment

```bash
curl -X POST https://ptksijwyvecufcvcpntp.supabase.co/functions/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-001",
    "message": "Hello, I am an engineer managing electronics export.",
    "conversation_history": [],
    "client_name": "Test Client"
  }'
```

Expected response: SSE stream of Claude's response

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
