---
name: session-report
description: "Génère un compte-rendu de séance client et le pousse dans Notion. Utilise ce skill dès que l'utilisateur mentionne : compte-rendu, CR, session, séance, transcript, Plaud, Fathom, récap de réunion, ou partage un transcript d'appel. Déclenche aussi quand l'utilisateur dit 'fais le CR de la séance', 'récap session Fred', 'mets le CR dans Notion', ou colle un transcript de réunion."
---

# Session Report — Compte-rendu de séance client

Tu génères des comptes-rendus de séance pour Catherine Selosse (CS Consulting Stratégique) et tu les publies directement dans le Notion du client.

Avant de rédiger, lis le template de référence :
- `references/template-cr.md` — la structure exacte du CR avec tous les emojis, sections et formatage

## Quand ce skill se déclenche

- "CR session [Client]"
- "Compte-rendu [Client] du [date]"
- "Report session [N] avec [Client]"
- Après réception d'un transcript Fathom
- L'utilisateur colle ou partage un transcript de séance (Plaud, Fathom, notes)
- L'utilisateur demande de faire un CR, un récap, un compte-rendu
- L'utilisateur mentionne une séance qui vient d'avoir lieu

## Input attendu

1. **Nom du client**
2. **Numéro de session**
3. **Date**
4. **Notes brutes / transcript Fathom / résumé oral**
5. (Optionnel) **Lien Fathom**

Si des infos manquent, demande à Catherine.

## Processus

### Étape 1 — Identifier les bases du client

→ Chercher le dashboard du client dans Notion
→ Récupérer les `data_source_id` de **Meeting Agendas** et **Objectifs & Actions**

#### Data sources de référence

| Client | Meeting Agendas | Objectifs & Actions |
|--------|----------------|---------------------|
| **Modèle (template)** | `75d0e693-4576-4ce6-9d54-21be4786ba50` | `551ab0d9-4525-45a2-a55a-e81913d062c6` |
| **Fred** | `304c3a2f-4255-8059-9cbe-e445f9811586` | `304c3a2f-4255-80a6-829f-effcce9fa0d4` |
| **Face Soul Yoga** | `304c3a2f-4255-815e-b1b9-000b7082a58d` | `304c3a2f-4255-8105-939a-cc224a563a66` |

**Mes Actions Consulting (base centrale Catherine)** : `7b0e4d79-18c3-4efd-97af-a28b21ac2ab6`

### Étape 2 — Créer l'entrée Meeting Agendas

Créer une nouvelle entrée dans la base **Meeting Agendas** du client.

#### Propriétés de l'entrée

| Champ | Valeur |
|-------|--------|
| Session | "Session [N] - [Titre thématique]" |
| N° | [Numéro] |
| Date | [YYYY-MM-DD] |
| Statut | ✅ Réalisée |
| Phase | Mois 1-3 (Hebdo) ou Mois 4-6 (Bi-mensuel) |
| Thème | Résumé 1 ligne |
| Notes CR | Résumé 2-3 phrases |
| Prochaines étapes | Priorités prochaine session |
| Lien Visio | URL Fathom |

#### Contenu de la page (CR COMPLET)

⚠️ **Le CR complet va dans le CONTENU de la page**, pas juste dans les propriétés.

Formate le CR exactement comme décrit dans `references/template-cr.md`. Structure :

```markdown
**🎥 Enregistrement :** [Lien Fathom]

## 🎯 SESSION [N] - [Titre]

### ✅ CÉLÉBRATIONS
- [Ce qui a fonctionné]

### 🔄 BLOCAGES IDENTIFIÉS
- [Problèmes soulevés]

---

## 🛠️ DÉCISIONS PRISES

### 1️⃣ [Décision]
- Détails et justification

---

## 🎯 ACTIONS CLIENT (Semaine du [dates])

### ⚡ Priorité 1 : [Titre] 🔴
- [ ] Action

### ⚡ Priorité 2 : [Titre] 🟠
- [ ] Action

---

## 📝 ACTIONS CATHERINE
- [ ] [Listées ici pour référence, créées dans base centrale]

---

## 🧘 MINDSET & INSIGHTS
[Prises de conscience]

---

## 📅 PROCHAINE SESSION
**Date :** [Date]
**Focus :** [Thème prévu]
```

### Étape 3 — Créer les actions CLIENT dans Objectifs & Actions

Pour **chaque action client** identifiée dans le CR, créer une entrée dans la base **Objectifs & Actions** du client.

| Champ | Valeur |
|-------|--------|
| Objectif / Action | [Titre] |
| Type | ✅ Action (ou 🎯 Objectif ou 📈 Progression) |
| Statut | ⏳ À faire |
| Responsable | 👤 Client |
| Priorité | 🔴 Haute / 🟠 Moyenne / 🟢 Basse |
| Catégorie | 📊 Organisation / 💻 Outils/Digital / 💰 Commercial / 👥 Management / 🧠 Mindset |
| Notes | Contexte |

### Étape 4 — Créer les actions CATHERINE dans Objectifs & Actions du client

Pour **chaque action Catherine** identifiée dans le CR, créer une entrée dans la base **Objectifs & Actions** du client avec **Responsable = 🎯 Catherine**.

→ Tout est dans UNE seule base par client. Quand Catherine marque "✅ Fait", le dashboard client est à jour automatiquement.

**Cycle de vie des actions :**
- À la création d'un CR → créer les nouvelles actions (⏳ À faire)
- Les actions terminées des sessions précédentes → passer en ✅ Fait (PAS supprimer, PAS abandonner)
- Les actions "Fait" restent visibles dans une vue "Historique/Fait" — elles servent de preuve de travail à montrer au client
- La vue "À faire" reste propre avec uniquement les actions en cours

| Champ | Valeur |
|-------|--------|
| Objectif / Action | [Titre] |
| Type | ✅ Action |
| Statut | ⏳ À faire |
| Responsable | 🎯 Catherine |
| Priorité | 🔴 Haute / 🟠 Moyenne / 🟢 Basse |
| Catégorie | 📊 Organisation / 💻 Outils/Digital / 💰 Commercial / 👥 Management / 🧠 Mindset |
| Session N° | [Numéro] |
| Notes | [Contexte] |

### Étape 5 — Mettre à jour la fiche client

- Sessions utilisées : +1
- Dernière session : [Date]
- Rappeler la date et l'objectif de la prochaine séance

### Étape 6 — Mettre à jour la mémoire client

Lire le fichier `clients/[prenom-nom].md` et le mettre à jour :

1. **Sessions** : incrémenter le compteur (ex: "3 / 18" → "4 / 18")
2. **Historique Sessions** : ajouter une ligne au tableau (numéro, date, thème, décision clé, avancée notable)
3. **Patterns Observés** — enrichir si le transcript révèle :
   - Un nouveau pattern (positif ou négatif) → ajouter dans "Ce qui marche" ou "Blocages récurrents"
   - Un thème qui revient → ajouter dans "Thèmes qui reviennent"
   - Une citation marquante du client → ajouter dans "Citations clés" (entre guillemets, avec contexte)
4. Commit + push GitHub

> **Instruction** : Avant de commencer le CR, toujours lire `clients/[prenom-nom].md` pour avoir le contexte complet du client. Utiliser ce contexte pour mieux analyser le transcript et personnaliser le CR.

## Analyse du transcript

À partir du transcript brut, extrais et organise :

**Célébrations (✅)** :
- Qu'est-ce qui a bien marché depuis la dernière séance ?
- Quelles victoires, même petites ?
- Quelle bonne pratique est validée et à reproduire ?

**Blocages identifiés (🔄)** :
- Qu'est-ce qui bloque ou ralentit le client ?
- Quels outils posent problème ?
- Quels process sont inefficaces ?

**Décisions prises (🛠️)** :
- Quelles décisions concrètes ont été actées pendant la séance ?
- Numéroter chaque décision (1️⃣, 2️⃣, 3️⃣)

**Actions client (🎯)** :
- Lister TOUTES les actions pour le client, avec checkboxes
- Classer par priorité : 🔴 Priorité 1, 🟠 Priorité 2, 🟡 Priorité 3
- Chaque action doit être concrète et actionnable

**Actions Catherine (📝)** :
- Lister ce que Catherine doit préparer pour la prochaine séance
- Inclure : setup technique, contenus à créer, outils à configurer

**Mindset & Insights (🧘)** :
- Ce qui fonctionne (bonnes pratiques validées)
- Prises de conscience (utiliser les CITATIONS EXACTES du client entre guillemets)

**Prochaine séance (📅)** :
- Date et heure
- Objectif principal

### Étape 7 — Extraire les pépites LinkedIn

Après chaque CR, extraire les **pépites** : phrases, situations ou transformations réutilisables pour du contenu LinkedIn (anonymisé).

Pour chaque pépite, noter :

| Champ | Valeur |
|-------|--------|
| Citation ou situation | La phrase exacte ou le résumé de la situation |
| Angle LinkedIn | Expertise / Témoignage / Coulisses / Éducatif |
| Hook potentiel | Une accroche possible pour un post |
| Anonymisable ? | Oui / Non (si non, demander l'accord du client) |

**Où les stocker :**
1. Dans le fichier mémoire client `clients/[prenom].md` → section `## Pépites LinkedIn`
2. Proposer immédiatement à Catherine : « J'ai extrait [N] pépites de cette session. Tu veux que j'en fasse un post LinkedIn ? »

**Ce qui fait une bonne pépite :**
- Une citation client qui résonne avec la cible (dirigeants TPE)
- Un avant/après concret et chiffré
- Une prise de conscience exprimée par le client
- Une situation universelle (tout dirigeant TPE s'y reconnaît)
- Un résultat inattendu ou contre-intuitif

**Ce qui n'est PAS une pépite :**
- Du jargon technique
- Des détails personnels non anonymisables
- Des décisions internes sans valeur pour l'audience

## Règles importantes

1. **CR complet = dans le CONTENU de la page Meeting Agendas** (pas juste les propriétés)
2. **Actions Catherine = dans Objectifs & Actions client** avec Responsable = 🎯 Catherine (même base que les actions client, une seule source de vérité)
3. **Le client ET Catherine voient toutes les actions** dans Objectifs & Actions — filtrables par Responsable
4. **TOUJOURS taguer toutes les propriétés** (Type, Statut, Responsable, Priorité, Catégorie, Session N°) — ne jamais créer d'entrée vide
5. **Toujours commencer par les célébrations** — c'est le ton positif de Catherine
6. **Citations exactes du client** — entre guillemets, ça rend le CR vivant et personnel
7. **Actions concrètes uniquement** — pas de "réfléchir à..." mais "créer X", "configurer Y", "lister Z"
8. **Ne pas inventer** — si une info n'est pas dans le transcript, ne la fabrique pas
9. **Respecter le format Notion** — emojis, checkboxes, toggle headings, c'est la signature Catherine
