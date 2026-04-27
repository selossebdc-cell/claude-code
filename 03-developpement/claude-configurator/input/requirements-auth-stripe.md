# Requirements — Authentification Secure (Stripe → Magic Link → RLS)

## Overview

Ajouter une couche d'authentification sécurisée au produit CS Digital Setup (149€). Actuellement : email manuel après paiement Stripe. Objectif : flux automatisé Stripe payment → Supabase auth (magic link) → JWT validation → /chat function avec RLS + rétention 30j des données diagnostiques.

Menace couverte (Secure-by-Design) : Attaquant forge JWT ou modifie requête HTTP pour accéder au /chat sans payer.

## Scope & Objectives

- **OBJ-001**: Implémenter intégration Stripe webhook pour capturer paiements
- **OBJ-002**: Créer automatiquement utilisateur Supabase auth + envoyer magic link
- **OBJ-003**: Valider JWT dans /chat function + vérifier paid_at status
- **OBJ-004**: Ajouter RLS policies sur table diagnostics
- **OBJ-005**: Implémenter auto-delete 30j via pg_cron
- **OBJ-006**: Intégrer frontend pour envoyer JWT

## Functional Requirements

- **REQ-001**: Stripe webhook reçoit checkout.session.completed + vérifie signature
- **REQ-002**: Sur webhook : supabase.auth.admin.inviteUserByEmail(email)
- **REQ-003**: Insertion diagnostics avec paid_at = NOW() + client_id = auth.uid()
- **REQ-004**: /chat extrait JWT + appel supabase.auth.getUser(jwt)
- **REQ-005**: /chat refuse accès si JWT invalide OU paid_at IS NULL OU 30j expirés
- **REQ-006**: success.html affiche "Magic link sent" (auto, pas manuel)
- **REQ-007**: chat.html envoie JWT dans Authorization: Bearer header

## Security Requirements (Secure-by-Design)

- **SEC-001**: Stripe signature vérifiée (Stripe.webhooks.constructEvent)
- **SEC-002**: Validation côté serveur (pas confiance frontend)
- **SEC-003**: RLS obligatoire sur diagnostics
- **SEC-004**: JWT signé par Supabase, expiré 1h
- **SEC-005**: STRIPE_WEBHOOK_SECRET via env var
- **SEC-006**: Pas d'API key Stripe au frontend

## Edge Functions

1. **create-checkout** (NEW) - POST /functions/v1/create-checkout
2. **stripe-webhook** (NEW) - POST /functions/v1/stripe-webhook
3. **chat** (MODIFY) - require Authorization header + validate JWT + enforce RLS

## Success Criteria

- [ ] Webhook receives & verifies payment
- [ ] Supabase user created automatically
- [ ] Magic link sent (automatic)
- [ ] /chat rejects unauthenticated (403)
- [ ] /chat rejects unpaid (403)
- [ ] RLS prevents cross-user access
- [ ] pg_cron cleanup verified
- [ ] E2E: payment → diagnostic chat (working)

---
**Created**: 2026-04-27  
**Status**: Ready for BREAK phase  
**Decision**: Full Secure-by-Design (Opus 4.7 approach)
