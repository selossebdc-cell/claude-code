# Plan d'Onboarding — Dot Market × Dot Advisory
**Catherine Selosse — CS Consulting Stratégique**

---

## Vue d'ensemble
- **Projet** : Pilotage opérationnel & stratégie données
- **Durée** : 6 mois (4 mois projet + 2 mois ajustements)
- **Démarrage** : 15 avril 2026 (mercredi 14h)
- **Contacts clés** : Kévin Jourdan (CEO, vision stratégique) + Elsa (COO, opérationnel)
- **Équipe** : ~5 personnes (interviews 1:1 après)

---

## Phase 1 : Onboarding collectif (3 semaines)

### RDV 1 — Semaine 1 (15 avril 2026, mercredi 14h)
**Durée** : 1h30 | **Participants** : Kévin + Elsa + Catherine

**Objectif** : Cadrage complet, définir la stratégie données par entité

**Agenda**
1. **Contexte & vision** (20 min)
   - Rappel contexte : 2 entités (Marketplace 50-100K + M&A, dossiers différents)
   - Objectif final : dashboards multi-niveaux clairs

2. **Stratégie Kévin** (25 min)
   - Quels KPI stratégiques cherche-tu ?
   - Comment tu piloterais Dot Market vs Dot Advisory différemment ?
   - Quelles données te manquent en ce moment ?

3. **Réalités opérationnelles Elsa** (25 min)
   - Outils actuels : Webflow (site), Siteground (domaine), où la data est-elle stockée ?
   - Champs manquants ? Processus peu documentés ?
   - Que faudrait-il changer demain ?

4. **Prochaines étapes** (10 min)
   - Planning interviews équipe
   - Audit sécurité/hébergement : dans le scope ?

**À envoyer avant** : Proposition + CGV + accès outils actuels (GSheets, CRM, etc.)

---

### RDV 2 — Semaine 2 (22 avril 2026, mercredi 14h)
**Durée** : 1h30 | **Participants** : Kévin + Elsa + Catherine

**Objectif** : Approfondir, définir les KPI exacts, valider architecture données

**Agenda**
1. **Approfondissement KPI** (30 min)
   - **Time to cash** : à quel moment débute le calcul ? Prospect contacté ? Contrat signé ?
   - **Marketplace KPI** : volume, GMV, CA, marge, churn
   - **M&A KPI** : time to deal, valorisation, deal pipeline, taux de closing
   - Qui pilote quoi ? Qui voit quoi dans les dashboards ?

2. **Cartographie données** (30 min)
   - Où vit chaque donnée ? (CRM, GSheets, Webflow,…)
   - Quelle data est fiable, quelle data doit être validée ?
   - Data qu'il faudrait créer (formules, calculs) ?

3. **Architecture hébergement & sécurité** (20 min)
   - État actuel : Webflow + Siteground + ?
   - Audit sécurité nécessaire ? (Catherine proposera devis avec dev)
   - Serveur dédié pour centraliser les dashboards ?

4. **Valider le reste** (10 min)
   - OK sur les interviews équipe (S3) ?
   - Questions avant S3 ?

**À préparer** : Doc cartographie données (draft Catherine)

---

### RDV 3 — Semaine 3 (29 avril 2026, mercredi 14h)
**Durée** : 1h30 | **Participants** : Kévin + Elsa + Catherine

**Objectif** : Valider le plan, bloquer les décisions, kick-off interviews

**Agenda**
1. **Recap définitions** (20 min)
   - KPI validés Marketplace + M&A
   - Périmètre data = exactement ça
   - Dashboards L1 (Elsa) vs L2 (Kévin) = c'est bon

2. **Synthèse interviews équipe** (20 min)
   - Qui a dit quoi (vue macro)
   - Problèmes identifiés, opportunités
   - Rien de surprenant ? Ajustements à faire ?

3. **Prochaines étapes & livrables** (30 min)
   - **Livrable 1 (S4)** : Schéma cartographie données (qui collecte quoi)
   - **Livrable 2 (S6)** : Dashboard Marketplace MVP (Elsa)
   - **Livrable 3 (S7)** : Dashboard M&A MVP (Kévin)
   - Audit sécurité : timing et devis dev
   - Support maintenance : 50 €/mois (ok ?)

4. **Gouvernance** (10 min)
   - Feedback loops : comment on valide les dashboards ?
   - Fréquence des points (tous les 2 semaines ?)
   - Qui approuve les évolutions ?

---

## Phase 2 : Interviews équipe (semaines 2-3)

### Format
- **1h par personne**, visio
- **Timing** : étalé sur S2-S3 (entre RDV 1 et 3)
- **But** : Comprendre les besoins opérationnels fine-grained

### Personnes à interviewer (~5)
1. **[Nom]** — Commercial/Sales → KPI : pipeline, conversion, délai closewin
2. **[Nom]** — Opérationnel → KPI : livraison, quality, délai
3. **[Nom]** — Finances → KPI : cash flow, invoicing, AR aging
4. **[Nom]** → [Rôle] → [Données critiques]
5. **[Nom]** → [Rôle] → [Données critiques]

### Questions template
- Quels sont les 3 chiffres que tu regardes tous les jours/semaines ?
- Qu'est-ce que tu dois demander à Elsa/Kévin quand tu as besoin de info ?
- Si tu avais un outil magique, qu'est-ce que tu verrais dedans ?
- Comment tu sais si vous êtes sur track vs. off track ?

---

## Phase 3 : Construction & itération (semaines 4-20)

### Livrable 1 — Cartographie données (S4, ~40 mai)
**Ce que tu reçois**
- Schéma (Figma ou PDF) : qui collecte quelle donnée, où elle vit, qui la valide
- Doc KPI définitions : "Time to cash = du prospect contacté au CA encaissé"
- Audit sécurité (optionnel) : devis + recommandations

**Ton travail**
- Valider les définitions auprès de l'équipe
- Approuver la cartographie
- Décider : audit sécurité y/n ?

### Livrable 2 — Dashboard Marketplace (S6)
**Ce que tu reçois**
- Dashboard opérationnel Elsa (Marketplace focus)
- KPI : volume, GMV, CA, churn, pipeline
- Filtres : par période, par marché, par produit

**Ton travail**
- Tester avec l'équipe
- Feedback : données manquantes ? Mauvaises formules ?
- OK pour passer en prod ?

### Livrable 3 — Dashboard M&A (S7)
**Ce que tu reçois**
- Dashboard stratégique Kévin (M&A focus)
- KPI : deal pipeline, time to deal, valuation, taux closing
- Liens avec Marketplace (si pertinent)

**Ton travail**
- Valider que ça te dit ce que tu veux savoir
- Questions pour Elsa ?
- OK pour passer en prod ?

### Itérations (S8-S20)
- Allers-retours : "Ce KPI n'est pas bon, faut le recalculer"
- Évolutions : "Ajoute ce filtre"
- Stabilisation : tout fonctionne en solo, sans Catherine

---

## Scope & non-scope

### ✅ Inclus
- Interviews (Catherine)
- Cartographie données
- Dashboards itératifs jusqu'à stable
- Audit sécurité/hébergement (diagnostic) — **devis dev séparé pour implémentation**
- Support & maintenance (3 mois inclus, après 50 €/mois)
- Documentation pour autonomie

### ❌ Hors scope (devis à part)
- Migration données (si serveur dédié nécessaire)
- Intégration API tiers
- Formation préstataire tech
- Agrandissement équipe (hiring)

---

## Récapitulatif timeline

| Semaine | Quoi | Durée |
|---------|------|-------|
| S1 (15 avril) | RDV 1 — Cadrage | 1h30 |
| S2 (22 avril) | RDV 2 + interviews start | 1h30 + ~5h interviews |
| S3 (29 avril) | RDV 3 + interviews end | 1h30 + ~5h interviews |
| S4 (6 mai) | Livrable 1 (Cartographie) | — |
| S5-6 (13-20 mai) | Livrable 2 (Dashboard Marketplace) | — |
| S7 (27 mai) | Livrable 3 (Dashboard M&A) | — |
| S8-20 (juin-juillet) | Itérations, stabilisation | Allers-retours |
| S21-26 (août-septembre) | Support, ajustements, maintenance | Final polish |

**Total** : ~30h Catherine + ~5h interviews = ~35h sur 6 mois

---

## Points de vigilance

1. **Data quality** : Si les data sources ne sont pas fiables, les dashboards ne serviront à rien → insister sur "garbage in = garbage out"
2. **Décisions** : À chaque RDV, valider les choix → pas de "on réfléchit et on revient"
3. **Vacances** : Juillet-août = slack, prévoir les livrables plus tôt
4. **Audit sécurité** : Peut bloquer l'hébergement → à décider vite (S1 idéalement)
5. **Équipe** : L'équipe doit être impliquée (interviews) sinon dashboards = déconnectés de la réalité

---

## Prochaine étape

✅ Signature bon de commande (mercredi 15 avril avant 14h)
✅ Accès outils : CRM, GSheets, Webflow, etc. → envoyer à catherine@csbusiness.fr
✅ Rendez-vous S1 : 15 avril 14h (lien Zoom envoyé)