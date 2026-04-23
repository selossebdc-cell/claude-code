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

### Étape 2 — Analyser en profondeur (ANALYSE FINE)

**IMPORTANT** : Cette étape est critique. Ne fais pas une extraction rapide des faits — fais une VRAIE analyse fine avec compréhension métier.

**A) Lire ET analyser complètement les transcriptions** :
- Si l'utilisateur partage des transcripts d'appel (Plaud, Fathom, notes) : lis-les ENTIÈREMENT + plusieurs fois
- Construis une timeline chronologique des problèmes mentionnés
- Extrais les **données chiffrées exactes** : CA, heures/semaine, nombre de clients, taux de conversion, nombre de mails/jour, durée DES TÂCHES EN MINUTES, délais de livraison, croissance prévue, etc.
- Identifie les **citations clés du client** (frustration, objectifs, contraintes, peurs) — réutilise-les EXACTEMENT dans la propale pour montrer compréhension fine
- Détecte les **timings concrets et précis** (combien de MINUTES pour chaque étape, où se perdent les HEURES, effet cascadant)
- Repère les **avant/après potentiels** (metrics quantifiables : heures récupérées, CA supplémentaire, taux amélioration)
- Identifie les données sensibles (RGPD, sécurité) qui nécessitent justification architecturale

**B) Construire une grille Avant/Après visuelle (4 métriques max)** :
- Timings actuels vs timings avec automation (concrètement chiffrés)
- Taux conversion/satisfaction (avant → après)
- Dépendances du fondateur (avant tout passe par le client → après partiellement automatisé)
- Revenu/acquisition (avant variabilité → après pipeline récurrent)
- Afficher en rouge/vert pour clarté visuelle

**C) Identifier les VRAIES priorités** (du client, pas du consultant) :
1. Relis ce que dit EXACTEMENT le client sur ses objectifs et frustrations
2. Ordre d'importance = ordre d'URGENCE du client (pas du consultant)
3. Modules à proposer = modules qu'on peut faire SANS surcharger le client, qui ne demandent pas de travail massif de sa part
4. Clarifier le ROI/amortissement de chaque module (quand ça se paie tout seul)
5. Structure "à tiroir" : client choisit ce dont il a besoin NOW vs PLUS TARD
6. Identifier QUI CRÉE LE CONTENU vs QUI AUTOMATISE (rôles clairs = rôles clairs dans la propale)

**D) Formuler en langage client avec finesse** :
1. Utilise ses termes exacts, sa tonalité, son contexte métier
2. Montre compréhension fine de SON business, pas du consulting générique
3. Chiffre les gains concrets et réalistes (heures libérées/mois, CA supplémentaire chiffré, taux amélioration)
4. Insiste sur ce qu'elle garde de PRÉCIEUX ET IRREMPLAÇABLE (sa voix, sa valeur, son lien client)
5. Adresse aussi la dimension ÉMOTIONNELLE (charge mentale, stress, besoin de respirer)

### Étape 3 — Déterminer le format & Structure

**Model selection — CRITIQUE** :
- **Claude 4.7 (Opus) pour la génération de propositions** — C'est de la réflexion poussée, c'est high-ticket, ça reflète la qualité du consultant
- Les propositions demandent finesse tonale, cohérence narrative, compréhension fine du contexte client — utilise le meilleur modèle
- Oui, ça coûte plus cher, mais c'est JUSTIFIÉ pour du work qui compte vraiment

**Format (basé sur complexité client)** :
- Client simple (1 personne, 1 activité) → 6-8 pages, 1 formule
- Client moyen (petite équipe, croissance) → 8-10 pages, 2-3 formules
- Client complexe (équipe + multi-canal) → 10-14 pages, 3 formules modulables à tiroir

**Structure (ordre d'apparition)** :
1. **Page 1 : Couverture** — Impact visuel, accroche, objectifs chiffrés
2. **Page 2 : Diagnostic intro + KPIs** — Reconnaissance de ses forces + données clés
3. **Page 3 : Avant/Après visuelle** (grille rouge→vert avec 4 metrics : timings, taux, dépendances, revenu)
4. **Page 4 : Pain points détaillés** (citations EXACTES du client, causes, conséquences, coûts cachés)
5. **Page 5 : Approche & Priorités** — "Pas un accompagnement 6 mois" → modules à tiroir + 4 priorités identifiées
6. **Pages 6+ : Modules détaillés** — Avec rôles clairs (client crée CONTENU / consultant automatise INFRA)
7. **ROI chiffré & formules** — Gain en heures, CA supplémentaire, amortissement précis
8. **Timeline concrete** — Phases avec dates et actions concrètes (sans imposer absence du client)
9. **Clarifications** — Ce qu'on fait / ce qu'on ne fait pas (périmètre noir sur blanc)
10. **Résultats attendus & CTA** — Résultats concrets du point de vue du client, appel à l'action simple

**Ton et engagement** :
- Demande le style (tutoiement/vouvoiement) à Catherine
- Utilise Claude 4.7 (Opus) : finesse tonale, cohérence narrative, qualité qui reflète l'expertise du consultant

### Étape 4 — Générer la proposition avec Claude 4.7

**Délégation à Claude 4.7 — Réflexion poussée** :
- Après l'analyse fine (Étape 2), tu as les données, les priorités, les citations, les chiffres
- Crée un prompt pour Claude 4.7 (Opus) qui synthétise : **l'analyse (Étape 2) + la structure (Étape 3) + le style-guide de Catherine**
- Le prompt doit inclure : extraits du transcript, données chiffrées exactes, priorités client, style de Catherine, structure de propale
- Claude 4.7 génère la proposition HTML complète, prête à imprimer en PDF
- Oui c'est plus cher, mais c'est justifié : c'est du work qui reflète la qualité du consultant

**Output format** :
- Document HTML complet, prêt à imprimer en PDF (Calibri, 11pt, marges A4 18mm)
- Couleurs client (pas les couleurs de Catherine)
- Page breaks aux bons endroits (avant Programme/Investissement/Prochaines étapes)

**Structure narrative du style-guide** (lire **références/style-guide.md** en détail) :
1. **Page de couverture** — Gradient couleurs client, accroche puissante, KPIs clés
2. **Diagnostic + KPIs** — "Ce que j'ai entendu le X" → reconnaissance des forces + chiffres
3. **Avant/Après visuelle** — Grille 4 colonnes : métrique, aujourd'hui, cible, impact
4. **Pain points** — Structure : problème → conséquence → coût caché (avec citations)
5. **Approche & priorités** — "Pas un accompagnement 6 mois" → modules à tiroir
6. **Modules détaillés** — Avec rôles clairs (Julie crée | Catherine automatise), RGPD le cas échéant
7. **Formules & investissement** — ROI chiffré, amortissement, options paiement
8. **Timeline concrète** — Phases avec actions (sans imposer absence du client)
9. **Clarifications** — Ce qu'on fait / ce qu'on ne fait pas
10. **Résultats attendus & CTA** — Appel à l'action simple, contact clair

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

> Ce fichier sera enrichi par les skills `client-onboarding` (création NOTES.md) et `session-report` (historique SESSIONS.md) au fil de l'accompagnement.
