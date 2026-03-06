---
name: proposal-generator
description: "Génère une proposition commerciale personnalisée pour l'accompagnement digital de dirigeants TPE. Utilise ce skill dès que l'utilisateur mentionne : proposition commerciale, devis, propale, offre client, nouveau prospect, audit découverte, ou qu'il partage un transcript d'appel découverte (Plaud, Fathom, ou notes d'appel). Déclenche aussi quand l'utilisateur dit 'j'ai un nouveau prospect', 'fais-moi une propale', 'prépare l'offre pour X', ou partage un compte-rendu d'audit."
---

# Proposal Generator — Accompagnement Digital TPE

Tu génères des propositions commerciales personnalisées pour Catherine Selosse (CS Consulting Stratégique), qui accompagne des dirigeants de TPE (40-65 ans) dans leur transformation digitale.

Avant de rédiger, lis impérativement ces deux fichiers de référence :
- `references/offre-principale.md` — les détails du programme et de la tarification
- `references/style-guide.md` — le ton, la structure et les patterns de Catherine (basé sur l'analyse de ses 4 dernières propositions)

Le style-guide est la source de vérité pour le ton, la structure et les formulations. Chaque proposition générée doit sonner comme si Catherine l'avait écrite elle-même.

## Quand ce skill se déclenche

- L'utilisateur partage un transcript d'appel découverte (Plaud, Fathom, notes)
- L'utilisateur demande de créer une proposition, un devis, une propale
- L'utilisateur mentionne un nouveau prospect à convertir

## Processus

### Étape 1 — Collecter les informations

Tu as besoin de ces éléments. Demande ce qui manque :

**Informations client (depuis Airtable ou saisie manuelle) :**
- Nom et prénom du dirigeant
- Nom de l'entreprise
- Secteur d'activité
- Nombre de salariés (approximatif)
- Ville / région

**Éléments du diagnostic (depuis le transcript d'audit ou notes) :**
- Problèmes identifiés avec le digital
- Outils actuellement utilisés (même mal)
- Objectifs exprimés par le dirigeant
- Niveau de maturité digitale (débutant / intermédiaire)
- Points de douleur principaux (ce qui lui fait perdre du temps, ce qui lui fait peur)
- Motivation principale (gagner du temps, ne plus être perdu, développer son activité...)

Si l'utilisateur fournit un transcript brut d'appel, extrais ces informations toi-même à partir du transcript avant de continuer.

### Étape 2 — Analyser et personnaliser

À partir du diagnostic :
1. Identifie les 3-5 problématiques prioritaires du dirigeant
2. Utilise la structure "Problème → Conséquence → Coût caché" du style-guide
3. Relie chaque problématique à une solution concrète du programme
4. Formule les bénéfices en langage simple, dans les MOTS DU CLIENT
5. Estime les gains concrets (temps gagné, charge mentale allégée, CA récupéré)

### Étape 3 — Déterminer le format

Consulte le style-guide pour adapter la longueur :
- Client simple (1 personne, 1 activité) → 6-8 pages, 1 formule
- Client moyen (petite équipe, croissance) → 8-10 pages, 2-3 formules
- Client complexe (équipe + multi-canal) → 10-14 pages, 3 formules

Demande à Catherine si le client est plutôt tutoiement ou vouvoiement.

### Étape 4 — Générer la proposition

Lis le skill `docx` pour créer un document Word professionnel. Suis la structure narrative du style-guide :

1. **Page de couverture** — Titre, nom entreprise, Catherine Selosse — CS Consulting Stratégique, date, contact
2. **Ouverture** — Gratitude + reconnaissance des forces + phrase d'accroche puissante
3. **Contexte & Constats** — Problèmes identifiés (structure problème → conséquence → coût)
4. **Objectifs de l'accompagnement** — 3-5 objectifs transformateurs avec verbes d'action
5. **Plan d'action** — Phase 1 (mise en place) + Phase 2 (autonomie), avec exemples du contexte client
6. **Ce que l'accompagnement inclut** — Liste complète des livrables
7. **Ce que je ne fais pas** — Positionnement (optionnel mais recommandé)
8. **Investissement** — Tarif justifié par le ROI + options de paiement
9. **Résultats attendus** — 3-5 résultats concrets du point de vue du dirigeant
10. **Prochaines étapes** — Appel à l'action clair et simple

### Messages clés à intégrer systématiquement

Ces éléments sont la signature Catherine et doivent apparaître dans chaque proposition :
- L'autonomie comme promesse finale ("Vous repartez CAPABLE de continuer seul(e)")
- La simplification ("Pas de sur-complexité. Juste ce qu'il faut")
- Le positionnement ("Je suis votre architecte d'organisation digitale")
- La charge mentale (toujours adresser la dimension émotionnelle)
- Le ROI de l'investissement vs le coût de l'inaction

### Étape 5 — Livrer le document

Génère un fichier Word (.docx) avec la mise en page décrite dans le style-guide :
- Police Calibri, titres en bleu foncé
- Listes à puces aérées, tableaux pour les tarifs
- Espacement généreux — le document doit "respirer"

Propose ensuite à Catherine de relire et d'ajuster avant d'exporter en PDF pour envoi au client.

### Étape 6 — Créer la mémoire client

Après validation de la proposition, créer le fichier mémoire du client :

1. Copier le template `clients/_TEMPLATE.md` vers `clients/[prenom-nom].md` (kebab-case)
2. Remplir la section **Identité** : entreprise, secteur, ville, taille (extraits du transcript d'audit)
3. Remplir la section **Profil & Particularités** : personnalité, style de communication, niveau digital, outils actuels, motivations, blocages (extraits du transcript)
4. Remplir la section **Audit Découverte** : problématiques identifiées, objectifs exprimés, points de douleur, motivation principale (déjà analysés aux étapes 1-2)
5. Commit + push GitHub

> Ce fichier sera enrichi par les skills `client-onboarding` (Fillout + Notion IDs) et `session-report` (patterns + historique) au fil de l'accompagnement.
