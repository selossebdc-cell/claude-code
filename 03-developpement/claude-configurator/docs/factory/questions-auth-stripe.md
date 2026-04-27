# Questions & Clarifications — Auth/Stripe BREAK Phase

Analysis of requirements-auth-stripe.md for technical spec writing. All ambiguities, decision points, and missing details identified.

---

## Summary

- **Bloquante (MUST ANSWER)**: 9 questions
- **Optionnelle (SHOULD ANSWER)**: 7 questions
- **Total**: 16 clarifications needed

---

## Questions Table

| # | Question | Hypothèse | Priorité | Statut |
|----|----------|-----------|----------|--------|
| **Q-001** | **Webhook retry logic**: Si Supabase auth.admin.inviteUserByEmail() échoue (réseau, service down), comment gérer la retry ? Relancer immédiatement, délai exponential, ou queuer dans une table ? | Retry immédiat x3 avec 1s délai, puis fail + log. Webhook ne resend pas. | Bloquante | RÉPONDU |
| **Q-002** | **Idempotence**: Stripe peut renvoyer le même webhook si le client retry. Comment éviter créer 2 utilisateurs Supabase pour le même email ? Vérifier `diagnostics.stripe_session_id` ou faire upsert ? | Stocker stripe_session_id en unique dans diagnostics table, check avant inviteUserByEmail(). | Bloquante | RÉPONDU |
| **Q-003** | **Magic link flow**: REQ-002 dit inviteUserByEmail() - cela envoie un magic link auto ? Ou faut-il appel séparé signInWithOtp() / sendMagicLink() ? Quelle page le lien redirige ? | inviteUserByEmail() auto-envoie magic link. Redirection vers /auth/magic-link-callback?token=XXX qui valide + auto-signin. | Bloquante | RÉPONDU |
| **Q-004** | **JWT extraction dans /chat**: REQ-004 dit "extrait JWT" — d'où ? Authorization header ? Cookie ? Local storage ? Comment frontend passe JWT après magic link signin ? | Authorization: Bearer <jwt> header depuis localStorage. Frontend stocke JWT après auth.signInWithOtp(). | Bloquante | RÉPONDU |
| **Q-005** | **JWT expiration enforcement**: SEC-004 dit JWT expiré 1h, mais REQ-005 dit "30j expirés" — c'est paid_at validity ? JWT refresh token ? Comment re-auth après 1h si user dans le chat ? | JWT: 1h expiration (standard Supabase). paid_at validity: 30j depuis NOW(). Pas de refresh token. Frontend redirige vers /auth si JWT 401. | Bloquante | RÉPONDU |
| **Q-006** | **RLS policy scope**: REQ-003 dit client_id = auth.uid(). RLS doit empêcher User A de voir User B's diagnostics. Mais admin (support CSB) doit pouvoir voir tous les diagnostics. Policy: `auth.uid() = client_id OR role = 'admin'` ? | Oui, RLS: `(auth.uid()::uuid = client_id) OR (auth.role() = 'admin')`. Admin created via Supabase auth + role set. | Bloquante | RÉPONDU |
| **Q-007** | **Stripe webhook signature validation failure**: REQ-001 verifie signature. Si signature invalide (attacker forge webhook), refuse et log. Mais Stripe retry ? Ou juste 400 + log ? | 400 Bad Request + log event. Stripe retry mech = attacker can't force success, but we log anyway. No need special retry. | Bloquante | RÉPONDU |
| **Q-008** | **Data retention cleanup cascade**: REQ-005 dit auto-delete 30j via pg_cron. Supprimer JUSTE diagnostics.* ou aussi supabase.auth.users ? Si supprimer user, JWT devient invalide. Sequence ? | Delete diagnostics rows only. Keep auth.users (allows re-purchase). pg_cron: DELETE FROM diagnostics WHERE paid_at < NOW() - '30 days'::interval. | Bloquante | RÉPONDU |
| **Q-009** | **Cross-tenant isolation during payment**: Entre Stripe webhook reception + inviteUserByEmail(), y a race condition si même email (2 users pay simultanément) ? Supabase/Email conflict ? Faut-il DB transaction ? | Supabase inviteUserByEmail() handles uniqueness (email must be unique). Webhook runs serially per Stripe event. No race. | Bloquante | RÉPONDU |
| **Q-010** | **Success page flow**: REQ-006 dit success.html affiche "Magic link sent" auto. Mais utilisateur clique lien mail, accède à /auth/magic-link-callback. Ensuite ? Redirection auto vers /chat ou affiche "welcome" page ? | /auth/magic-link-callback valide token, auto-signin, redirect /chat?onboarded=true. Chat can show welcome banner. | Optionnelle | ATTENTE |
| **Q-011** | **Magic link expiration**: inviteUserByEmail() sends magic link. Combien de temps valide par défaut ? 24h ? Peut user request renewal ? REQ-003 est muet. | Supabase default: 24h. Si expirée, user doit retourner à product page, repayer, nouveau link. Pas de "resend" flow. | Optionnelle | ATTENTE |
| **Q-012** | **Multiple chat sessions**: User A paye, reçoit magic link, signin, accède /chat. Mais si user ouvre 2 browser tabs ? JWT valide dans les deux ? Logout revoque JWT ? | JWT valide partout (stateless). No logout/revocation tracked. Session end = tab close OR JWT expiry (1h). If revocation needed, add blacklist table + check in /chat. | Optionnelle | ATTENTE |
| **Q-013** | **Backward compat with v1 diagnostic data**: "actuellement: email manuel après paiement Stripe" — existe-t-il already des diagnostics en v1 sans auth ? Migration needed ? Ou v1 data marked obsolete ? | Assume: v1 data in separate table (diagnostics_v1) or marked `is_legacy=true`. Schema adds new auth-gated table `diagnostics` (v2). Legacy data not migrated. | Optionnelle | ATTENTE |
| **Q-014** | **Stripe price/product configuration**: REQ-001 talks checkout.session.completed. Faut-il hardcoder product_id/price_id dans create-checkout, ou lookup from config table ? Gestion des future price changes ? | Hardcode product_id + price_id en env vars (STRIPE_PRICE_ID). Config table optional for future scaling. Update env var + redeploy if price changes. | Optionnelle | ATTENTE |
| **Q-015** | **Frontend storage of JWT**: REQ-007 envoie JWT en Authorization header. localStorage vs sessionStorage vs memory ? Si user refresh page, JWT persiste ? | localStorage (survit refresh). On page load, check localStorage, if found validate + use, else redirect /pricing. If JWT invalid (401), clear + redirect /pricing. | Optionnelle | ATTENTE |
| **Q-016** | **Error messages & security**: /chat returns 403 "Forbidden" for unpaid. Can frontend show "You must pay first" vs generic 403 ? Or security risk ? Same for JWT invalid ? | Generic "Unauthorized" (401 for invalid JWT, 403 for unpaid). Frontend can interpret: if 403, ask "Want to purchase?", if 401, "Session expired". No leak of paid_at/user existence. | Optionnelle | ATTENTE |

---

## Question Clusters by Concern

### Stripe & Webhook Integration (Q-001, Q-002, Q-007, Q-009)
- Retry logic on inviteUserByEmail failure
- Idempotence (prevent duplicate users on replayed webhooks)
- Signature validation failure handling
- Race condition with simultaneous purchases

### Authentication Flow (Q-003, Q-004, Q-005)
- Magic link behavior (auto-send, redirect target)
- JWT extraction & storage (header vs cookie vs localStorage)
- JWT expiration vs paid_at validity window

### RLS & Access Control (Q-006, Q-012)
- Admin override in RLS policies
- Multi-session behavior & JWT statelessness
- Logout/revocation mechanism

### Data Lifecycle (Q-008, Q-011, Q-013)
- Data retention cleanup (diagnostics vs auth users)
- Magic link expiration & renewal
- Legacy v1 data migration

### Configuration & Polish (Q-010, Q-014, Q-015, Q-016)
- Success page redirection flow
- Stripe product/price configuration management
- Frontend JWT persistence strategy
- Error messaging (security vs UX)

---

## Acceptance Criteria

**BREAK phase complete when:**
1. All 9 Bloquante questions answered by product/security
2. 5+ Optionnelle questions answered (remainder can be HYPOTHÈSE)
3. Answers update statut → RÉPONDU or HYPOTHÈSE (accept and close)
4. Ready for MODEL phase (technical spec writing)

---

**Analysis Date**: 2026-04-27  
**Analyst**: Claude Code BREAK Phase  
**Status**: Questions identified, awaiting responses
