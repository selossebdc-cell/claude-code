---
name: Claude Configurator v2 — Deployment Status & Next Actions
description: Current deployment status (2026-04-27). Backend ready for Supabase, frontend changes deferred.
type: project
---

## Status: ✅ READY FOR SUPABASE DEPLOYMENT

**Date**: 2026-04-27 (afternoon)  
**Next Session**: Resume Supabase deployment

---

## Current State

### ✅ Backend (EPIC-1-5): COMPLETE & COMMITTED
- All 5 edge functions implemented in TypeScript
- Code committed to GitHub (26 April recover commit)
- Located: `supabase/functions/chat/`
- Files: `index.ts`, `pattern-detector.ts`, `opportunity-detector.ts`, `metadata-manager.ts`, `synthesis-generator.ts`
- Migration: `supabase/migrations/20260427_create_diagnostics_table.sql`
- **Status**: Ready for `supabase functions deploy chat`

### ⚠️ Frontend (unrelated to backend deploy)
- File: `frontend/js/config-display.js` — uncommitted changes (SSE streaming for `/generate-config` function)
- `.DS_Store` — untracked (macOS noise)
- **Decision**: These changes are NOT critical for backend deployment
- **Why**: Changes call a different Edge Function (`/generate-config`), not the `/chat` function being deployed
- **Action**: Ignore for now, handle as separate commit after backend validation

### ✅ Git Status
- Main branch clean (frontend submodule has working tree changes, not blocking)
- All backend code tracked and committed
- Ready to push any further changes

---

## Next Steps (In Order)

### Session 2: Deploy Backend to Supabase (DEPLOYMENT.md)

**Prerequisites** (verify before starting):
- [ ] Supabase CLI installed: `brew install supabase`
- [ ] Authenticated: `supabase login`
- [ ] ANTHROPIC_API_KEY ready (from https://console.anthropic.com/)
- [ ] Project ref: `ptksijwyvecufcvcpntp` (pre-configured in DEPLOYMENT.md)

**Steps** (exact commands in `/03-developpement/claude-configurator/DEPLOYMENT.md`):
1. **Apply migration**: `supabase db push --project-ref ptksijwyvecufcvcpntp`
   - Creates `diagnostics` table with RLS + indexes
   - Takes ~30 seconds
   
2. **Deploy chat function**: `supabase functions deploy chat --project-ref ptksijwyvecufcvcpntp`
   - Pushes all 5 integrated TypeScript files
   - Takes ~20 seconds
   
3. **Set secrets**: `supabase secrets set ANTHROPIC_API_KEY=sk-ant-... --project-ref ptksijwyvecufcvcpntp`
   - Replace with actual API key
   
4. **Test via curl** (Step 4 in DEPLOYMENT.md)
   - Confirms backend works in isolation
   - Should return SSE stream of Claude response

### Session 3+: Frontend Handling (separate task)
- Inside `frontend/` submodule: commit `config-display.js` with Factory-compliant task ID
- Add `.DS_Store` to `.gitignore`
- Update parent repo's submodule pointer
- Test E2E in browser (optional after backend validation)

### Session 4+: EPIC-6 & EPIC-7 (after validation)
- **EPIC-6**: Agent & Routine Configuration (generate 6 agent prompts from metadata)
- **EPIC-7**: Generate-Config Integration (feed synthesis to config generator)

---

## Key Files

| File | Purpose | Status |
|------|---------|--------|
| `DEPLOYMENT.md` | Step-by-step Supabase deploy guide | ✅ Use this for Session 2 |
| `DEPLOYMENT-READY.md` | Acceptance criteria + validation tests | ✅ Reference after deploy |
| `supabase/functions/chat/index.ts` | Main edge function | ✅ Ready |
| `supabase/migrations/20260427_*` | DB migration | ✅ Ready |

---

## Decision Log

**Opus 4.7 Analysis (2026-04-27 afternoon)**:
- Q: Is frontend critical for backend deployment?
- A: No. Frontend changes are iteration (SSE UI), call different function (`/generate-config` ≠ `/chat`)
- Action: Deploy backend first, handle frontend as separate commit after

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| ANTHROPIC_API_KEY missing | Have ready before Step 3 |
| Supabase project not found | Verify project ref: `ptksijwyvecufcvcpntp` in Supabase dashboard |
| Function already exists | Script handles overwrite; no manual cleanup needed |
| CORS errors in browser | Post-backend-validation concern; not blocking curl test |

---

**Last Updated**: 2026-04-27 afternoon  
**Next Action**: Session 2 — Run DEPLOYMENT.md Steps 1-4 (migration + deploy + secret + curl test)  
**Time Estimate**: 5-10 minutes for all 4 steps + verification
