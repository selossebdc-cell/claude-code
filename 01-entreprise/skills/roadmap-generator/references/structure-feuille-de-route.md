# Structure Feuille de Route — Référence Notion

## Schéma de la database "FEUILLE DE ROUTE"

| Propriété | Type | Valeurs possibles |
|-----------|------|-------------------|
| **Name** | title | Titre de l'action (clair, actionnable) |
| **Fait** | checkbox | Oui / Non |
| **Phase** | select | Phase 0 - Fondations, Phase 1 - Clarté, Phase 2 - Automatiser, Phase 3 - Consolider |
| **Priorité** | select | Haute, Moyenne, Basse |
| **Type** | select | À remplir, À uploader, À lire, À réfléchir, À valider |
| **Temps estimé** | select | 5 min, 15 min, 30 min, 1h, 2h+ |
| **Ordre** | number | Séquence dans la phase (1, 2, 3...) |

> Les noms de phases peuvent être adaptés au profil du client. Exemples :
> - TPE débutant digital : Fondations / Clarté / Automatiser / Consolider
> - Entrepreneur en croissance : Nettoyage / Systématisation / Délégation / Vision & Scale
> - Client technique avancé : Audit / Migration / Optimisation / Autonomie

## Structure de la page "Feuille de Route Stratégique"

```
(construite suite aux réponses aux questionnaires) — Transformation Dirigeant

Début : [date]
Fin : [date + 6 mois]
Objectif : [phrase du client depuis Fillout "où voulez-vous être dans 6 mois ?"]

---

## DIAGNOSTIC DE DÉPART

| Dimension | État actuel | Objectif 6 mois |
|-----------|------------|-----------------|
| Temps stratégie | [X]% → [X]h/sem | [objectif] |
| Autonomie équipe | [score]/5 | [objectif] |
| Automatisation | [X]% | [objectif] |
| Stratégie structurée | [score]/10 | [objectif] |
| Documentation process | [score]/5 | [objectif] |

## BLOCAGES IDENTIFIÉS
- [Blocage 1 — depuis Fillout "PLUS GROS blocage"]
- [Blocage 2 — depuis découverte]
- [Blocage 3]

---

## ROADMAP 6 MOIS

### Phase 0 — Fondations (Semaines 1-2)
[2-3 lignes : quick wins pour créer la dynamique]

### Phase 1 — Clarté (Mois 1-2)
[2-3 lignes : comprendre, cartographier, décider]

### Phase 2 — Automatiser (Mois 3-4)
[2-3 lignes : systématiser les process prioritaires]

### Phase 3 — Consolider (Mois 5-6)
[2-3 lignes : autonomie, délégation, pérennisation]

---

## INDICATEURS DE SUCCÈS
- [KPI 1 : mesurable, avec cible]
- [KPI 2]
- [KPI 3]

---

## RESSOURCES HUB
- [Liens vers outils, guides, templates pertinents]

---

## TON ENGAGEMENT
Ton objectif 6 mois : "[citation exacte du client depuis Fillout]"
```

## Schéma de la database "MES SOP & PROCESS"

| Propriété | Type | Valeurs possibles |
|-----------|------|-------------------|
| **Name** | title | Nom du process |
| **Catégorie** | select | Finance/Compta, Commercial, RH/Équipe, Opérations, Tech/Outils |
| **Fréquence** | select | Quotidien, Hebdomadaire, Mensuel, Ponctuel |
| **Statut** | select | À documenter, En cours, Terminé |

## Phases détaillées

### Phase 0 — Fondations (max 5 actions)

**Objectif** : Poser les bases, victoires rapides, créer la confiance.

Actions typiques :
- Remplir le questionnaire d'audit (si pas encore fait)
- Installer les outils essentiels (gestionnaire MDP, cloud)
- Time-blocking : bloquer les créneaux "dirigeant" dans l'agenda
- Premier tri/nettoyage (emails, fichiers, outils)
- Onboarding équipe sur Notion (si applicable)

**Critère de passage** : Le client a ses fondations digitales en place et une routine installée.

### Phase 1 — Clarté (max 5 actions)

**Objectif** : Comprendre l'existant, cartographier, prendre les décisions structurantes.

Actions typiques :
- Cartographier le parcours client actuel
- Documenter les process existants (SOP)
- Audit des outils : garder / remplacer / supprimer
- Choisir la stack technique définitive
- Définir les KPIs de pilotage

**Critère de passage** : Le client sait exactement où il en est et a une vision claire de la cible.

### Phase 2 — Automatiser (max 5 actions)

**Objectif** : Systématiser les process prioritaires, mettre en place les outils choisis.

Actions typiques :
- Configurer les outils choisis
- Créer les automatisations prioritaires
- Mettre en place les workflows équipe
- Documenter les SOP finalisés
- Former l'équipe sur les nouveaux outils

**Critère de passage** : Les process prioritaires tournent, l'équipe est formée.

### Phase 3 — Consolider (max 5 actions)

**Objectif** : Autonomie totale, délégation, vision long terme.

Actions typiques :
- Valider l'autonomie sur chaque outil
- Transférer les responsabilités (délégation)
- Optimiser les KPIs de pilotage
- Bilan de fin d'accompagnement
- Plan de continuité post-accompagnement

**Critère de passage** : Le client est autonome et sait maintenir ses systèmes seul.

## Exemples de feuilles de route par profil

### Profil "Débutant digital" (type Fred)
- Phase 0 : Cloud, MDP, time-blocking
- Phase 1 : Tri fichiers, migration outils, arborescence
- Phase 2 : Automatisations simples, agent IA, workflows
- Phase 3 : Autonomie outils, routines consolidées

### Profil "Entrepreneur en croissance" (type Face Soul Yoga)
- Phase 0 : Questionnaire audit, outils essentiels, routines
- Phase 1 : Cartographie process, audit technique, décisions stack
- Phase 2 : Migration plateforme, workflows équipe, SOP
- Phase 3 : Délégation, posture CEO, pilotage KPIs

### Profil "Stratégique avancé" (type Aurélia)
- Phase 0 : Quick wins, gel des coûts, onboarding équipe
- Phase 1 : Audit technique, benchmark, cartographie parcours client
- Phase 2 : Migration, automatisations, montée en compétence équipe
- Phase 3 : Vision croissance, posture CEO, modèle économique
