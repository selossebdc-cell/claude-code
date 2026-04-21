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

## Quand ce skill se déclenche

- "Feuille de route [Client]"
- "Roadmap [Client]"
- "Crée le plan d'action de [Client]"
- "Prépare la stratégie d'accompagnement de [Client]"
- Catherine partage un CSV d'audit stratégique Fillout
- Catherine demande de construire ou mettre à jour une feuille de route
- Après réception des réponses au questionnaire Fillout d'un client

## Input attendu

1. **Nom du client**
2. **Réponses au questionnaire Fillout** (CSV ou données brutes)
3. **CR d'appel découverte / échanges initiaux** (transcripts ou notes)
4. **Contrat signé** (pour vérifier les engagements spécifiques)
5. (Optionnel) **CR de sessions précédentes** si le programme a déjà démarré

Si des infos manquent, demande à Catherine.

## Processus

### Étape 1 — Lire le contexte complet

> **Règle** : Ne JAMAIS commencer une feuille de route sans avoir lu TOUS les documents disponibles.

1. Lire `clients/[prenom-nom].md` — mémoire projet du client
2. Lire le **contrat signé** dans Notion (page "Contrat & Conditions" du dashboard client)
3. Lire les **réponses Fillout** (CSV ou section Questionnaire de la mémoire client)
4. Lire les **CR d'échanges initiaux** (appel découverte, session de lancement)
5. Identifier le dashboard Notion du client et ses databases (Feuille de Route, SOP & Process)

### Étape 2 — Diagnostic de départ

À partir du questionnaire Fillout et de l'appel découverte, extraire et structurer :

| Dimension | Source Fillout | Ce qu'on extrait |
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
- Fillout : "3 tâches qui prennent le PLUS de temps"
- Fillout : "3 tâches à automatiser"
- Fillout : "Point de friction parcours client"
- Fillout : "Tâches à déléguer DÈS MAINTENANT"
- Fillout : "Tâches gérées faute de temps/process/confiance"
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
3. **Respecter la capacité du client** : vérifier les heures disponibles (Fillout)
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
3. **Blocages identifiés** : liste des freins principaux (depuis Fillout + découverte)
4. **Roadmap 6 mois** : résumé narratif des 4 phases (2-3 lignes par phase)
5. **Indicateurs de succès** : 3-5 KPIs mesurables (ex: "Passer de 5h/sem à 15h/sem de stratégie")
6. **Engagement client** : objectif 6 mois en une phrase (citation du client depuis Fillout)

### Étape 6 — Mettre à jour la mémoire client

1. Lire `clients/[prenom-nom].md`
2. Mettre à jour la section **Questionnaire Fillout** (7 sections) si pas encore fait
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

## Colonnes du questionnaire Fillout (référence CSV)

Le CSV d'audit stratégique contient ces catégories :
1. **Vision** : mission, vision 3 ans, priorités 12 mois, valeurs
2. **Stratégie** : score structuration (1-10), description organisation
3. **Productivité** : heures/semaine, répartition ops/stratégie/gestion, tâches chronophages
4. **Parcours client** : connaissance parcours, perte prospects, % automatisation, friction principale
5. **Outils** : liste outils, intégration (1-5), doublons, automatisations existantes
6. **Équipe & Délégation** : taille, tâches à déléguer, autonomie (1-5), freins délégation
7. **Pilotage** : KPIs suivis, outils de suivi, fiabilité données, fréquence consultation
8. **Mindset** : dirigeant vs opérationnel, légitimité, blocages, baguette magique
9. **Engagement** : priorités classées, prêt au changement (1-10), heures disponibles

## Règles importantes

1. **NE JAMAIS sauter la cartographie des process** (étape 3) — c'est le socle de tout
2. **Maximum 20 actions** dans la feuille de route — less is more
3. **Toujours lire le contrat signé** pour les engagements spécifiques
4. **Catherine valide chaque étape** avant de pousser dans Notion
5. **Actions concrètes uniquement** — pas de "réfléchir à..." mais "créer X", "lister Y", "configurer Z"
6. **Adapter les phases au profil du client** — les noms et le contenu varient selon le diagnostic
7. **Le client doit se sentir capable** en regardant sa feuille de route, jamais submergé
8. **Commencer par les quick wins** — Phase 0 = victoires rapides pour créer la dynamique
9. **Ne pas inventer** — chaque action doit être justifiée par le diagnostic, le Fillout ou le contrat
10. **Respecter la capacité du client** — vérifier les heures disponibles déclarées dans le Fillout
