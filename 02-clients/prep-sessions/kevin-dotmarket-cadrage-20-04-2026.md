# RÉUNION CADRAGE — Kevin JOURDAN
**Mercredi 20/04/2026 — 14h00**  
**Participants** : Catherine, Kevin, Elsa

---

## CONTEXTE DU PROJET
**Commanditaire** : Kevin Jourdan  
**Entités** : 3 (Dot Market + Dot Advisory + School Dot Market)  
**Périmètre** : 3 dashboards dédiés par entité + pilotage données & stratégie opérationnelle  
**Devis** : 10 000 EUR HT | **Démarrage** : 22/04/2026 | **Durée** : 6 mois (avec marges congés)

---

## SYNTHÈSE COMPRÉHENSION ACTUELLE

### Entités & KPIs distincts
| Entité | Type | Volume | Besoin clé | Processus |
|--------|------|--------|-----------|-----------|
| **Dot Market** | Marketplace | 50-100 clients | Suivi ventes time-to-market | Cycles courts |
| **Dot Advisory** | M&A/Consulting | 100+ dossiers | Suivi deals time-to-cash | Cycles longs |
| **School Dot Market** | ? | ? | ? | ? |

### Points soulevés par Kevin (04/14)
✓ Propale OK sur vue d'ensemble  
⚠ Besoin : Dot Market & Dot Advisory **apparaissent distinctement** dans les dashboards  
⚠ KPIs différents = logique de navigation différente (pas un seul dashboard générique)

### Enjeu clé identifié
**Définition des données ≠ définition des dashboards**
- Exemple : "time-to-cash" — quand start ? (prospect nous contacte vs client signing) — quand stop ? (paiement reçu vs projet clos ?)
- Chaque entité aura sa propre interprétation → **standardiser avant build**

---

## OBJECTIF RÉUNION
Poser **les fondations de définition des données** avant d'aller interviewer l'équipe.
- Valider stratégie par entité
- Identifier gaps & priorités données
- Confirmer composition équipe (interview 1-to-1 après)
- Fixer timeline & jalons

---

## AGENDA PROPOSÉ (1h30)

| Temps | Sujet | Notes |
|-------|-------|-------|
| **14h00-14h15** | Intro & contexte | Kevin : résumé des 3 entités, org chart somme |
| **14h15-14h40** | Dot Market deep dive | KPIs clés, processus, outils sources |
| **14h40-15h05** | Dot Advisory deep dive | KPIs clés, processus, outils sources, différences vs Market |
| **15h05-15h20** | School Dot Market | À couvrir (jamais mentionné avant) |
| **15h20-15h30** | Next steps | Interview équipe, planning, questions |

---

## QUESTIONS CLÉS À CLARIFIER

### Structure & Équipe
- [ ] 5 personnes chez Kevin ou 5 par entité ? Qui fait quoi dans chaque entité ?
- [ ] School Dot Market : c'est quoi ? Lié à Dot Market ou separate business ?
- [ ] Gouvernance : qui pilot les données ? (CFO, COO, CEO ?)

### Dot Market (Marketplace)
- [ ] Volume réel (50-100 clients ?) et types (vendeurs/acheteurs/les deux ?)
- [ ] "Time to market" = définition exacte pour vous ? (listing live ? first sale ??)
- [ ] Outils actuels : Webflow, mais données ventes/clients où ? (CRM ? sheets ? base de données ?)
- [ ] Quels sont vos **problèmes aujourd'hui** avec les données ? (manquent des infos ? pas de visibilité ?)

### Dot Advisory (M&A)
- [ ] Distinction claire avec Dot Market : pourquoi "100+" vs "50-100" ?
- [ ] "Time to cash" = à partir de quand commence-t-on le comptage ? (first contact ? LOI signing ? closing ?)
- [ ] Processus M&A typique : combien d'étapes ? délai moyen ? (3 mois ? 12 mois ?)
- [ ] Outils : même infra que Dot Market ou séparé ?

### Infrastructures & Security
- [ ] Serveur dédié ? Webflow + Siteground suffisent ou besoin hardening ?
- [ ] Données sensibles (M&A, pricing) : quelles restrictions ?
- [ ] Backup / archiving policy ?

---

## POINTS À DÉMONTRER
1. **Approche data d'abord** — on ne build pas dashboard sans avoir défini les KPIs
2. **Séparation nette** — 3 dashboards indépendants (pas une vue unique générique)
3. **Interview équipe** — pour comprendre chaque personne = chaque vue possible
4. **Timeline réaliste** — 6 mois avec marges pour congés, décisions lentes, etc.

---

## LIVRABLES APRÈS RÉUNION
- [ ] Notes de cadrage (envoyées dans les 48h)
- [ ] Confirmation dates interviews 1-to-1 avec équipe
- [ ] Contrat + CGV à envoyer (à préparer avant mercredi)
- [ ] Calendrier 3 réunions Kevin+Elsa sur 3 semaines

---

## DOCUMENTS À PRÉPARER
- ✓ Contrat d'engagement
- ✓ Conditions générales
- ✓ Devis détaillé (10 000 EUR HT + scope 3 dashboards)
- ✓ Calendrier proposé (réunions semaines 1/2/3 de mai)