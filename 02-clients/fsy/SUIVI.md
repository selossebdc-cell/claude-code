---
name: Suivi Projet — Face Soul Yoga
description: État actuel du projet, étapes en cours, actions ouvertes, blocages
---

# Suivi Projet — Face Soul Yoga

État **ACTUEL** du projet. À jour au 23/04/2026.

**Dernière mise à jour** : 23/04/2026 (RDV 3 — Livraison finale)  
**Prochaine session** : À planifier après clôture (ex: 27/04 debrief, 15/05 monitoring 3 mois)

---

## État du projet

**Phase actuelle** : Livraison finale (sprint critique)

**% Avancement** : 75% (3 étapes complétées / 4 totales)

---

## Étapes du projet

### ✅ Complétées

- [x] **Audit initial** (RDV 1, 06/04/2026)
  - Analyse Brevo 13,302 contacts
  - Définition 9 attributes cœur
  - Architecture data validée

- [x] **Conception automations** (RDV 1, 06/04/2026)
  - 22 templates Brevo créés
  - 9 workflows n8n prêts
  - Parcours client mappé

- [x] **Tests + préparation livraison** (RDV 2, 20/04/2026)
  - Tests parcours FSY Studio + MTM
  - Webhooks endpoint validé
  - Planning interactif livraison

### 🔄 En cours

- [ ] **Déploiement + go-live automations** (RDV 3, depuis 23/04)
  - Responsable : Catherine + Laurie
  - Deadline : 23/04 18h
  - Blocage : Laurie doit connecter Stripe↔Circle
  - Avancement : 70% (9 workflows prêts, webhooks en test)

- [ ] **Migration Uscreen → Circle + subscriptions** (RDV 3, 23-26/04)
  - Responsable : Lori (subscription update) + Anam (CSV export) + Catherine (supervision)
  - Deadline : Lundi 26/04 matin (go-live Circle)
  - Étapes :
    - Étape 2 : Export CSV Uscreen (email, statut abo, date renouvellement)
    - Étape 3 : Import en masse dans Circle (invitation bulk)
    - Étape 4 : Subscription update Stripe via Claude/n8n Edge (preserve dates + payment methods)
  - Blocage : Étapes 2-3 en attente de démarrage
  - Avancement : 30% (Stripe connecté, étapes 2-4 en queue)

- [ ] **Déploiement chatbots** (RDV 3, ven-dim)
  - Responsable : Mickaël (dev) + Laurie (modération)
  - Deadline : 23/04 18h (dimanche validation)
  - Telegram MTM : ven 3-4h + sam 2h = 6h total
  - WhatsApp FSY : ven 3h + sam 4h = 7h total
  - Avancement : 40% (brief envoyé, dev en cours)

### 📋 À venir

- [ ] **Formation équipe + handoff** (après 23/04)
  - Responsable : Catherine
  - Deadline : 27/04 (debrief + documentation)
  - Contenu : 6 sections guide maintenance (emails, UTMs, automations, Circle, chatbots, escalade)

- [ ] **Monitoring 3 mois post-go** (mai-juin 2026)
  - Responsable : Catherine (check-in)
  - Contenu : Reporting automations OK? Churn rate? Revenue impact?
  - Décision après : optimisations ou clôture?

---

## Actions ouvertes

### 🔴 Priorité 1 — URGENT (bloque livraison)

- [ ] **Laurie : Connecter Stripe ↔ Circle** (Client)
  - Créée : RDV 1
  - Deadline : Lundi 23/04 avant 18h (CRITIQUE)
  - Description : Webhook Stripe → Circle subscription sync. Dépend du "Authenticate with Stripe" + Circle API token
  - Dépendance : Catherine a fourni les endpoints

- [ ] **Laurie : Fournir 3 liens UTM Stripe** (Client)
  - Créée : RDV 2
  - Deadline : Lundi 23/04 avant 18h
  - Description : FSY Studio + MTM + Licence. Pour tester parcours complets.
  - Dépendance : Utile pour tests webhook lundi

- [ ] **Catherine : Valider webhooks Stripe → n8n** (Catherine)
  - Créée : RDV 2
  - Deadline : 23/04 lundi matin
  - Description : Test paiement FSY Studio → Brevo active + Circle invite
  - Blocage : Attend liens Stripe de Laurie

- [ ] **Aurélia : Relire + valider 22 templates Brevo** (Client)
  - Créée : RDV 1
  - Deadline : 23/04 (idéalement avant tests)
  - Description : Contenu, ton, personnalisation. 22 templates nurture+onboarding+rétention
  - Avancement : Templates prêts, en attente validation contenu

### 🟠 Priorité 2 — Important (livraison + jour)

- [ ] **Anam : Migrer 5K vidéos Uscreen → Circle** (Client)
  - Créée : RDV 1
  - Deadline : 23/04 mercredi
  - Description : Export CSV Uscreen → import Circle. Préserver métadonnées (durée, tags, etc.)
  - Blocage : CSV export en cours
  - Avancement : 50%

- [ ] **Catherine : Activer 8 automations Brevo** (Catherine)
  - Créée : RDV 1
  - Deadline : 23/04 mercredi-jeudi
  - Description : Créer dans l'UI Brevo (Laurie fera le ménage après si besoin)
  - Automations : Nurture (3), Onboarding (2), Rétention (2), Anti-churn (1)
  - Avancement : 80% (workflows prêts, UI steps à faire)

- [ ] **Chatbots (reporter semaine prochaine)** (External)
  - Créée : RDV 2
  - Deadline : Reporter lun 26/04 (ne pas tout démarrer en même temps)
  - Telegram MTM : commandes, logic, intégration Circle
  - WhatsApp FSY : commandes, logic, intégration Circle
  - Matière prête, déploiement + tests = semaine prochaine
  - Avancement : 40% (brief prêt, dev peut démarrer lun)

### 🟡 Priorité 2.5 — Transition Circle (lundi-mardi)

- [ ] **Email onboarding Circle aux clientes** (Catherine)
  - Créée : RDV 3
  - Deadline : Lundi 26/04 avec migration
  - Description : "Dorénavant vous vous connectez à Circle. Lien accès. Vous serez accompagnées."
  - Statut : Template à rédiger

- [ ] **Connecter n8n workflows + UTMs dynamiques** (Catherine)
  - Créée : RDV 3
  - Deadline : Mardi 27/04 (after Circle migration go-live)
  - Description : 9 workflows en attente de data flow. Quand client arrive mardi avec UTM → n8n tourne. UTMs hardcodés d'abord, puis système dynamique après.
  - Statut : Workflows prêts, data flow à connecter

### 🟢 Priorité 3 — Après livraison

- [ ] **Catherine : Documentation maintenance 6 sections** (Catherine)
  - Créée : RDV 2
  - Deadline : 27/04 (debrief)
  - Description : Guide pour Laurie + Anam (emails | UTMs | automations | Circle | chatbots | escalade)
  - Format : HTML + markdown

- [ ] **Extraire pépites LinkedIn** (Catherine)
  - Créée : RDV 1
  - Deadline : Après clôture projet (27/04)
  - Description : 3-5 pépites (automation ROI, tracking impact, team autonomy story)

---

## Blocages actuels

| Blocage | Impact | Responsable | Statut |
|---------|--------|-------------|--------|
| Laurie — Connexions Stripe↔Circle | 🔴 Critique | Laurie | À faire (lun) |
| Laurie — 3 liens UTM | 🔴 Critique | Laurie | À faire (lun) |
| Aurélia — Validation templates | 🟠 Important | Aurélia | En attente (validation, pas blocage) |
| Mickaël — Chatbots | 🟠 Important | Mickaël | En développement (timeline serrée) |

---

## Prochaine session

**Date** : À planifier après 23/04 (ex: 27/04 ou 30/04)  
**Durée estimée** : 1h (debrief + handoff)

**Focus** :
- Debrief livraison : qu'est-ce qui s'est bien passé / à améliorer
- Validation équipe sur automations + chatbots
- Handoff documentation à Laurie/Anam
- Planning monitoring 3 mois

**À préparer** :
- [ ] Catherine : Guide maintenance final
- [ ] Laurie/Anam : Feedback utilisation outils
- [ ] Aurélia : Feedback satisfaction + direction future

---

## Notes internes

**Dépendances critiques** :
- Laurie = single point of failure pour Stripe/Circle (pas de backup)
- Aurélia = validation bottleneck (besoin de processus d'approval rapide)
- Mickaël = timeline extrêmement serrée (ven-dim pour 2 chatbots complets)

**Pattern observé** :
- Aurélia décide mais ne fait pas → Laurie/Anam exécutent → Catherine supervise
- Processus décidé au départ, bien suivi jusqu'à 23/04
- Besoin de rôles clairs : Aurélia (PM), Laurie (ops), Anam (VA), Catherine (infra)

**Risques à surveiller** :
- 🟠 Webhook Stripe en prod dimanche (mêmes de la deadline) = peu de buffer
- 🟠 Chatbots Go/No-Go dimanche 18h (final call, peu de temps pour pivots)
- 🟢 Monitoring post-go = important pour justifier ROI aux yeux d'Aurélia
