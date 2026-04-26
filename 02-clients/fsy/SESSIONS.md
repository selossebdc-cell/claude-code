---
name: Sessions — Face Soul Yoga
description: Historique rendez-vous clients, étapes du projet, décisions et livrables
---

# Sessions — Face Soul Yoga

Historique de tous les rendez-vous depuis le démarrage du projet (audit initial → livraison).

| RDV | Date | Étape | Décisions clés | Actions complétées | Statut |
|-----|------|-------|---|---|---|
| 1 | 06/04/2026 | Audit initial | Scope data/KPI + automations validé; Brevo core architecture décidée | Audit 13K contacts; 9 attributes Brevo; 22 templates; 9 workflows n8n prêts | ✅ Complétée |
| 2 | 20/04/2026 | Livraison + Test | Tests Stripe webhook; validation templates Aurélia; planning livraison interactif | Tests parcours 1 & 2; migration Uscreen planifiée; chatbot brief Mickaël | ✅ Complétée |
| 3 | 23/04/2026 | Livraison finale | Configuration webhooks GO; chatbots déployés; équipe formation | Chatbots live; équipe formée; reporting hebdo en prod | 🔄 En cours |

---

## Notes par session

### RDV 1 — 06/04/2026
**Étape** : Audit initial

**Décisions actées** :
- Scope complet : automations Brevo + migration Uscreen → Circle + chatbots + eSignatures
- Architecture : Brevo CRM central (listes = déclencheurs temps réel) + n8n orchestration
- GHL rejeté (trop cher) → rester sur Brevo + n8n + Manychat + Circle

**Livrables produits** :
- Audit Brevo : 13,302 contacts, 19 listes, 35 templates existants, 62% taux ouverture
- 9 attributes Brevo : SOURCE, INTERET, OFFRE, DATE_ACHAT, STATUT_MEMBRE, CIRCLE_ID, UTM_SOURCE, UTM_MEDIUM, UTM_CAMPAIGN
- 22 templates email (nurture + onboarding + rétention + anti-churn)
- 9 workflows n8n prêts (Stripe → Brevo, Circle sync, reporting, etc.)
- Rapport hebdo testé et fonctionnel

**Prochaine session** : 20/04 — Tests complets et validation templates

---

### RDV 2 — 20/04/2026
**Étape** : Tests + Livraison préparation

**Décisions actées** :
- Stripe webhook endpoint validé : https://n8n.srv921609.hstgr.cloud/webhook/stripe-fsy-01
- Tests lun-mer sur parcours FSY Studio (17€) et MTM
- Mickaël pour chatbots (Timeline ven-dim = très serrée)

**Actions complétées** :
- Tests parcours 1 & 2 en cours
- Migration Uscreen → Circle planifiée mercredi
- Checklist validation dimanche 18h préparée
- Brief Mickaël chatbots envoyé

**Blocages identifiés** :
- 🔴 CRITIQUE : Laurie doit fournir liens UTM/Stripe connexion avant lundi soir (bloque tout)
- 🟠 Mickaël timeline très serrée (ven-dim pour 2 chatbots + guide)
- 🟠 Migration Uscreen = 5K vidéos, test 5 contacts mercredi

**Prochaine session** : 23/04 18h — Livraison finale + validation

---

### RDV 3 — 23/04/2026
**Étape** : Livraison finale (EN COURS)

**Décisions à acter** :
- Go/no-go chatbots dimanche 18h
- Go/no-go webhooks Stripe si tests ok
- Formation équipe Laurie + Anam sur maintenance

**Livrables à livrer** :
- ✅ Automations Brevo en prod (9 workflows actifs)
- ✅ Migration Uscreen → Circle (5K vidéos + subscriptions préservées)
- ✅ Chatbots Telegram MTM + WhatsApp FSY
- ✅ Guide maintenance (6 sections : emails, UTMs, automations, Circle, chatbots, escalade)
- ✅ Rapport hebdo live en prod

**Dépendances critiques** :
- Laurie : Stripe↔Circle connexion + 3 UTM links
- Aurélia : Validation templates + commandes chatbots
- Mickaël : Livraison chatbots dimanche 18h
- Catherine : Validation webhooks + infrastructure

**Prochaine session** : À planifier après clôture projet (ex: monitoring 3 mois après, feedback, optimisations)

---

## Résumé progression

- **Rendez-vous effectués** : 2 / 3
- **Étapes complétées** : Audit (100%) → Tests (90%) → Livraison (70%)
- **Blocages actuels** : Webhooks Stripe en attente; Laurie sur connexions
- **À faire critique** : Tests finaux; validation Aurélia; déploiement chatbots dimanche

**Status** : 🔴 CRITIQUE — Deadline 23/04 18h en cours
