---
name: roadmap-generator
description: "Construit la feuille de route stratégique personnalisée d'un client. Utilise ce skill dès que l'utilisateur mentionne : feuille de route, roadmap, plan d'action 6 mois, construire le parcours, ou demande de préparer la stratégie d'accompagnement d'un client. Déclenche aussi quand l'utilisateur dit 'crée la feuille de route de X', 'prépare la roadmap', 'construis le plan d'action', ou partage un CSV d'audit stratégique."
---

# Roadmap Generator — Feuille de Route Stratégique Client

Tu construis la feuille de route personnalisée des clients de Catherine Selosse (CS Consulting Stratégique). La feuille de route est le livrable central de l'accompagnement : elle traduit le diagnostic en actions concrètes, phasées et réalistes.

Avant de commencer, lis les références :
- `references/structure-feuille-de-route.md` — schéma Notion, phases, propriétés
- `references/guide-cartographie-process.md` — méthodologie de cartographie des process
- `references/template-sop.md` — template SOP, méthode d'interview "Raconte-moi ta semaine", priorisation
- `../client-onboarding/references/questionnaire-onboarding.md` — contenu complet du questionnaire (9 sections, mapping questions → diagnostic)

## Quand ce skill se déclenche

- "Feuille de route [Client]"
- "Roadmap [Client]"
- "Crée le plan d'action de [Client]"
- "Prépare la stratégie d'accompagnement de [Client]"
- Catherine partage les réponses au questionnaire d'onboarding (CSV ou données brutes)
- Catherine demande de construire ou mettre à jour une feuille de route
- Après réception des réponses au questionnaire d'un client

## Input attendu

1. **Nom du client**
2. **Réponses au questionnaire d'onboarding** (CSV, JSON webhook ou données brutes)
3. **CR d'appel découverte / échanges initiaux** (transcripts ou notes)
4. **Contrat signé** (pour vérifier les engagements spécifiques)
5. (Optionnel) **CR de sessions précédentes** si le programme a déjà démarré

Si des infos manquent, demande à Catherine.

## Processus

### Étape 1 — Lire le contexte complet

> **Règle** : Ne JAMAIS commencer une feuille de route sans avoir lu TOUS les documents disponibles.

1. Lire `clients/[prenom-nom].md` — mémoire projet du client
2. Lire le **contrat signé** dans Notion (page "Contrat & Conditions" du dashboard client)
3. Lire les **réponses au questionnaire** (section Questionnaire de la mémoire client ou données brutes)
4. Lire les **CR d'échanges initiaux** (appel découverte, session de lancement)
5. Identifier le dashboard Notion du client et ses databases (Feuille de Route, SOP & Process)

### Étape 2 — Diagnostic de départ

À partir du questionnaire d'onboarding et de l'appel découverte, extraire et structurer :

| Dimension | Source questionnaire | Ce qu'on extrait |
|-----------|---------------|------------------|
| Répartition temps | Heures ops / stratégie / gestion | % de chaque + total heures/semaine |
| Stratégie structurée | "Échelle 1-10 stratégie" | Score + description qualitative |
| Documentation process | "Niveau documentation 1-5" | Score + implications |
| Automatisation | "% parcours client automatisé" | Niveau actuel + marge de progression |
| Autonomie équipe | "Autonomie globale 1-5" | Score + freins identifiés |

**Compléter avec :**
- Blocages principaux (question "PLUS GROS blocage")
- Points de friction parcours client
- Outils actuels et leur niveau d'intégration (score 1-5)
- Vision à 3 ans et priorités 12 mois

**Livrable** : Remplir la section "DIAGNOSTIC DE DÉPART" de la page "Feuille de Route Stratégique" dans Notion.

Présenter le diagnostic à Catherine pour validation avant de continuer.

### Étape 3 — Cartographie des process

> **⚠️ ÉTAPE OBLIGATOIRE — NE JAMAIS SAUTER**
> La cartographie des process est le socle de la feuille de route.
> On ne peut pas optimiser ce qu'on n'a pas cartographié.

#### 3a — Identifier les process existants

Sources pour identifier les process :
- Questionnaire : "3 tâches qui prennent le PLUS de temps" (Q3.3)
- Questionnaire : "3 tâches à automatiser" (Q3.4)
- Questionnaire : "Point de friction parcours client" (Q4.4)
- Questionnaire : "Tâches à déléguer DÈS MAINTENANT" (Q6.3)
- Questionnaire : "Tâches gérées faute de temps/process/confiance" (Q3.5)
- Appel découverte : problématiques identifiées
- Contrat : objectifs spécifiques du programme

#### 3b — Structurer dans la database "MES SOP & PROCESS"

Pour chaque process identifié, créer une entrée :

| Champ | Valeur |
|-------|--------|
| Name | Nom du process (ex: "Clôture comptable mensuelle") |
| Catégorie | Finance/Compta, Commercial, RH/Équipe, Opérations, Tech/Outils |
| Fréquence | Quotidien, Hebdomadaire, Mensuel, Ponctuel |
| Statut | À documenter |

#### 3c — Identifier les process manquants

Comparer avec les process essentiels pour une TPE :
- **Finance** : facturation, suivi trésorerie, clôture mensuelle
- **Commercial** : prospection, devis, suivi clients, relances
- **Opérations** : production, livraison, SAV
- **RH/Équipe** : onboarding, communication interne, suivi tâches
- **Tech/Outils** : sauvegarde, sécurité, maintenance

#### 3d — Validation Catherine

Présenter la cartographie complète à Catherine. Elle valide, ajuste, priorise AVANT de construire la feuille de route.

### Étape 4 — Construire la feuille de route

> **⚠️ RÈGLE ANTI-SURCHARGE** : Maximum **20 actions** au total.
> La première feuille de route de Fred était trop pleine (30 actions).
> Mieux vaut 15 actions bien exécutées qu'une roadmap décourageante.
> Le client doit regarder sa feuille de route et se sentir **capable**, pas **submergé**.

#### Principes de construction

1. **Partir des process cartographiés** (étape 3), pas d'une liste théorique
2. **Prioriser impitoyablement** : seules les actions à fort impact passent
3. **Respecter la capacité du client** : vérifier les heures disponibles (questionnaire Q9.4)
4. **Chaque action = 1 résultat concret** (pas de "réfléchir à..." mais "créer X", "configurer Y")
5. **Les phases sont progressives** : on ne passe à la suivante que quand la précédente est solide

#### Structure en 4 phases

| Phase | Nom | Focus | Timing | Max actions |
|-------|-----|-------|--------|-------------|
| 0 | Fondations | Quick wins + mise en place essentiels | Semaines 1-2 | 5 |
| 1 | Clarté | Comprendre, cartographier, décider | Mois 1-2 | 5 |
| 2 | Automatiser | Systématiser les process prioritaires | Mois 3-4 | 5 |
| 3 | Consolider | Autonomie, délégation, pérennisation | Mois 5-6 | 5 |

> Les noms de phases peuvent être adaptés au contexte du client (ex: "Nettoyage", "Systématisation", "Vision & Scale" pour un profil plus avancé).

#### Peupler la database "FEUILLE DE ROUTE"

Pour chaque action, créer une entrée :

| Champ | Valeur |
|-------|--------|
| Name | Titre clair et actionnable |
| Phase | Phase 0 / 1 / 2 / 3 |
| Priorité | Haute / Moyenne / Basse |
| Type | À remplir / À uploader / À lire / À réfléchir / À valider |
| Temps estimé | 5 min / 15 min / 30 min / 1h / 2h+ |
| Ordre | Séquence dans la phase (1, 2, 3...) |
| Fait | Non (checkbox décochée) |

**Présenter la feuille de route complète à Catherine pour validation avant de pousser dans Notion.**

### Étape 5 — Remplir la page stratégique

Compléter la page "Feuille de Route Stratégique" dans Notion :

1. **En-tête** : dates début/fin, objectif global
2. **Diagnostic de départ** : tableau des 5 dimensions (état actuel → objectif 6 mois)
3. **Blocages identifiés** : liste des freins principaux (depuis questionnaire + découverte)
4. **Roadmap 6 mois** : résumé narratif des 4 phases (2-3 lignes par phase)
5. **Indicateurs de succès** : 3-5 KPIs mesurables (ex: "Passer de 5h/sem à 15h/sem de stratégie")
6. **Engagement client** : objectif 6 mois en une phrase (citation du client depuis questionnaire Q9.2)

### Étape 6 — Mettre à jour la mémoire client

1. Lire `clients/[prenom-nom].md`
2. Mettre à jour la section **Questionnaire d'onboarding** (9 sections + 1 bonus) si pas encore fait
3. Ajouter les Notion IDs des databases Feuille de Route et SOP & Process si manquants
4. Commit + push GitHub

## Data sources de référence

### Modèle (template)
- **Feuille de Route (database)** : voir le dashboard template
- **SOP & Process (database)** : voir le dashboard template

### Fred
- **Dashboard** : `2efc3a2f-4255-81c0-8c3a-fd9a5b39c6c0`
- **Feuille de Route** : (database intégrée au dashboard)

### Face Soul Yoga
- **Dashboard** : `304c3a2f-4255-80da-b8b2-fef4e17f7243`
- **Feuille de Route (database)** : `304c3a2f-4255-8126-a334-000bb2fe5505`
- **SOP & Process (database)** : `304c3a2f-4255-81ae-8bae-000bef8717d0`
- **Page stratégique** : `304c3a2f-4255-814d-a857-d766711d8825`

## Sections du questionnaire d'onboarding (référence)

> Référence complète : `../client-onboarding/references/questionnaire-onboarding.md` (43 questions, mapping vers diagnostic)
> Formulaire HTML : `03-developpement/questionnaire-onboarding/index.html`

Le questionnaire d'onboarding contient ces sections :

1. **Vision** (Q1.1→Q1.5) : pourquoi l'entreprise, description 1 phrase, vision 3 ans, 3 priorités 12 mois, valeurs
2. **Stratégie** (Q2.1→Q2.4) : score structuration (1-10), description organisation, client idéal, offres & tarifs
3. **Productivité** (Q3.1→Q3.5) : heures/semaine, répartition ops/stratégie/gestion (3 curseurs), 3 tâches chronophages, 3 tâches à automatiser, tâches faute de temps/process
4. **Parcours client** (Q4.1→Q4.5) : description parcours complet, perte prospects (où/pourquoi), % automatisation (0-100), friction principale, canaux d'acquisition
5. **Outils** (Q5.1→Q5.4) : liste outils quotidiens, intégration (1-5), doublons/outils inutilisés, automatisations existantes
6. **Équipe & Délégation** (Q6.1→Q6.5) : taille équipe, rôles, tâches à déléguer immédiatement, autonomie (1-5), freins à la délégation
7. **Pilotage** (Q7.1→Q7.4) : KPIs suivis, outils de suivi, fréquence consultation, fiabilité données (1-5)
8. **Mindset & Blocages** (Q8.1→Q8.4) : % dirigeant vs opérationnel, PLUS GROS blocage, tentatives passées, baguette magique
9. **Engagement & Objectifs** (Q9.1→Q9.5) : priorités classées (drag&drop), objectif 6 mois (citation), prêt au changement (1-10), heures disponibles/semaine, CA actuel & objectif
10. **Documentation process** (Q10.1→Q10.2) : score documentation (1-5), scénario absence 2 semaines

## Règles importantes

1. **NE JAMAIS sauter la cartographie des process** (étape 3) — c'est le socle de tout
2. **Maximum 20 actions** dans la feuille de route — less is more
3. **Toujours lire le contrat signé** pour les engagements spécifiques
4. **Catherine valide chaque étape** avant de pousser dans Notion
5. **Actions concrètes uniquement** — pas de "réfléchir à..." mais "créer X", "lister Y", "configurer Z"
6. **Adapter les phases au profil du client** — les noms et le contenu varient selon le diagnostic
7. **Le client doit se sentir capable** en regardant sa feuille de route, jamais submergé
8. **Commencer par les quick wins** — Phase 0 = victoires rapides pour créer la dynamique
9. **Ne pas inventer** — chaque action doit être justifiée par le diagnostic, le questionnaire ou le contrat
10. **Respecter la capacité du client** — vérifier les heures disponibles déclarées dans le questionnaire (Q9.4)
