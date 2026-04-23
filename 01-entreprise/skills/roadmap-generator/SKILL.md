---
name: roadmap-generator
description: "Construit la feuille de route stratégique personnalisée d'un client. Utilise ce skill dès que l'utilisateur mentionne : feuille de route, roadmap, plan d'action 6 mois, construire le parcours, ou demande de préparer la stratégie d'accompagnement d'un client. Déclenche aussi quand l'utilisateur dit 'crée la feuille de route de X', 'prépare la roadmap', 'construis le plan d'action', ou partage un CSV d'audit stratégique."
---

# Roadmap Generator — Feuille de Route Stratégique Client

Tu construis la feuille de route personnalisée des clients de Catherine Selosse (CS Consulting Stratégique). La feuille de route est le livrable central de l'accompagnement : elle traduit le diagnostic en actions concrètes, phasées et réalistes.

Avant de commencer, lis les références :
- `references/template-feuille-de-route.md` — schéma feuille de route, phases, propriétés
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

1. Lire `/02-clients/[prenom-nom]/NOTES.md` — mémoire projet du client
2. Lire le **contrat signé** depuis le dossier client (fichier contrat ou STATUS.md)
3. Lire les **réponses Fillout** (CSV ou section Questionnaire de NOTES.md)
4. Lire les **CR d'échanges initiaux** (dans SESSIONS.md ou CR dossier client)
5. Identifier les fichiers Google Drive du client (NOTES.md, SESSIONS.md, SUIVI.md, STATUS.md)

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

**Livrable** : Remplir la section "DIAGNOSTIC DE DÉPART" dans `/02-clients/[client]/feuille-de-route.md`.

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

#### 3b — Structurer dans `/02-clients/[client]/feuille-de-route.md`

Pour chaque process identifié, documenter dans la section "PROCESS & SOP À DOCUMENTER" (Phase 1-2) :

| Champ | Valeur |
|-------|--------|
| Process | Nom du process (ex: "Clôture comptable mensuelle") |
| Fréquence | Quotidien, Hebdomadaire, Mensuel, Ponctuel |
| Propriétaire | Qui en est responsable |
| Status | À documenter |

#### 3c — Identifier les process manquants

Comparer avec les process essentiels pour une TPE :
- **Finance** : facturation, suivi trésorerie, clôture mensuelle
- **Commercial** : prospection, devis, suivi clients, relances
- **Opérations** : production, livraison, SAV
- **RH/Équipe** : onboarding, communication interne, suivi tâches
- **Tech/Outils** : sauvegarde, sécurité, maintenance

#### 3d — Validation Catherine

Présenter la cartographie complète à Catherine dans `/02-clients/[client]/feuille-de-route.md`. Elle valide, ajuste, priorise AVANT de construire les phases d'action.

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

#### Peupler la section "PHASES DÉTAILLÉES"

Pour chaque action, structurer dans `/02-clients/[client]/feuille-de-route.md` :

| Champ | Valeur |
|-------|--------|
| Titre | Titre clair et actionnable |
| Phase | Phase 1 / 2 / 3 (ou 0 pour quick wins) |
| Priorité | Haute / Moyenne / Basse |
| Type | À documenter / À automatiser / À déléguer / À valider |
| Temps estimé | 5 min / 15 min / 30 min / 1h / 2h+ |
| Ordre | Séquence dans la phase (1, 2, 3...) |
| Statut | À faire / En cours / Fait |

**Présenter la feuille de route complète à Catherine pour validation avant de démarrer l'accompagnement.**

### Étape 5 — Finaliser la feuille de route Google Drive

Compléter `/02-clients/[client]/feuille-de-route.md` :

1. **En-tête** : dates début/fin (création + validation), objectif global
2. **Diagnostic de départ** : tableau des 5 dimensions (état actuel → objectif 6 mois)
3. **Problèmes principaux** : liste des freins principaux (depuis Fillout + découverte)
4. **Phases détaillées** : actions concrètes pour chaque phase (avec timing et responsabilité)
5. **Indicateurs de succès** : 3-5 KPIs mesurables (ex: "Passer de 5h/sem à 15h/sem de stratégie")
6. **Hypothèses & Risques** : identifiés durant l'audit, mitigation prévue

### Étape 6 — Mettre à jour NOTES.md du client

1. Lire `/02-clients/[prenom-nom]/NOTES.md`
2. Mettre à jour la section **Audit Découverte** avec les résultats du diagnostic
3. Ajouter lien vers `/02-clients/[client]/feuille-de-route.md` dans les références du dossier client
4. Commit + push GitHub

## Data sources de référence

### Templates Google Drive
- **template-feuille-de-route.md** : `/01-entreprise/references/template-feuille-de-route.md`
- **template-NOTES.md** : `/01-entreprise/references/template-NOTES.md`

### Exemples de feuilles de route complètes
- **Fred** : `/02-clients/fred-andre/feuille-de-route.md` (exemple accompagnement classique)
- **Face Soul Yoga** : `/02-clients/face-soul-yoga/feuille-de-route.md` (exemple DAta/KPI)

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
4. **Catherine valide chaque étape** avant de finaliser la feuille de route
5. **Actions concrètes uniquement** — pas de "réfléchir à..." mais "créer X", "lister Y", "configurer Z"
6. **Adapter les phases au profil du client** — les noms et le contenu varient selon le diagnostic
7. **Le client doit se sentir capable** en regardant sa feuille de route, jamais submergé
8. **Commencer par les quick wins** — Phase 0 = victoires rapides pour créer la dynamique
9. **Ne pas inventer** — chaque action doit être justifiée par le diagnostic, le Fillout ou le contrat
10. **Respecter la capacité du client** — vérifier les heures disponibles déclarées dans le Fillout
