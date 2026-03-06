# Template SOP & Méthode de collecte

## Qu'est-ce qu'un SOP

SOP = Standard Operating Procedure = "Comment on fait les choses ici."
Un SOP documente un process de manière suffisamment claire pour que quelqu'un d'autre puisse le reproduire sans poser de question.

Pour les dirigeants TPE de Catherine : un SOP n'a PAS besoin d'être un document de 10 pages. C'est une fiche simple, visuelle, actionnable.

## Template SOP (à créer dans la database "MES SOP & PROCESS")

Chaque SOP = une entrée dans la database avec ses propriétés + du contenu dans la page.

### Propriétés de l'entrée

| Champ | Valeur |
|-------|--------|
| Name | Nom du process (ex: "Facturation client BtoC") |
| Catégorie | Finance/Compta, Commercial, RH/Équipe, Opérations, Tech/Outils |
| Fréquence | Quotidien, Hebdomadaire, Mensuel, Ponctuel |
| Statut | À documenter → En cours → Terminé |

### Contenu de la page (template)

```
## [Nom du process]

**Fréquence** : [Quand et combien de fois ?]
**Temps actuel** : [Combien de temps ça prend aujourd'hui ?]
**Temps cible** : [Combien de temps ça devrait prendre ?]

---

### RACI — Qui fait quoi ?

| Étape | R (Réalise) | A (Approuve) | C (Consulté) | I (Informé) |
|-------|-------------|--------------|--------------|-------------|
| [Étape 1] | [Qui] | [Qui] | [Qui] | [Qui] |
| [Étape 2] | [Qui] | [Qui] | — | [Qui] |
| ... | | | | |

> **R** = fait le travail. **A** = responsable final (1 seul par étape). **C** = on lui demande son avis. **I** = on le tient au courant.
> Le dirigeant doit être **A** sur le moins d'étapes possible. Objectif : le mettre en **I** sur un maximum de process.

---

### Déclencheur
> Qu'est-ce qui fait qu'on lance ce process ?
> Ex: "Un client passe commande", "C'est le 1er du mois", "Un email arrive de..."

[Décrire]

---

### Étapes

1. [Étape 1 — action concrète] → Outil : [quel outil]
2. [Étape 2] → Outil : [quel outil]
3. [Étape 3] → Outil : [quel outil]
4. ...

---

### C'est terminé quand... (Definition of Done)

- [ ] [Critère 1 — résultat vérifiable]
- [ ] [Critère 2]
- [ ] [Critère 3]

> Tant que TOUS les critères ne sont pas cochés, le process n'est pas terminé.

---

### Points d'attention
- [Ce qui peut mal tourner]
- [Les erreurs fréquentes]
- [Ce qu'il ne faut surtout pas oublier]

---

### Automatisable ?
- [ ] Oui, totalement
- [ ] Oui, partiellement (quelles étapes ?)
- [ ] Non, nécessite du jugement humain

**Si oui, quelle automatisation ?** : [Décrire]
```

## Matrice RACI — Mode d'emploi simplifié pour TPE

### Les 4 rôles

| Lettre | Rôle | En clair | Règle |
|--------|------|----------|-------|
| **R** | Réalisateur | Fait le travail | Au moins 1 par tâche |
| **A** | Approbateur | Responsable final, rend des comptes | **1 seul par tâche** (obligatoire) |
| **C** | Consulté | On lui demande son avis avant | Optionnel |
| **I** | Informé | On le prévient après | Optionnel |

### Règles fondamentales

1. **1 seul A par tâche** — si tout le monde est responsable, personne n'est responsable
2. **Le A peut aussi être R** — dans une TPE c'est fréquent, mais l'objectif est de les séparer
3. **Le A organise les R** — si les R ne font pas le travail, c'est le A qui assume
4. **Moins de A pour le dirigeant = plus de liberté** — l'objectif est de déplacer le dirigeant du A vers le I

### Comment utiliser le RACI en séance

1. **Lister les étapes du process** (depuis l'interview)
2. **Lister les personnes** impliquées (dirigeant, équipe, prestataire, client, outil/automatisation)
3. **Remplir la matrice** étape par étape : "Qui fait ? Qui valide ? Qui est consulté ? Qui est informé ?"
4. **Identifier les déséquilibres** :
   - Dirigeant = A sur tout ? → Problème de délégation
   - Personne n'est R ? → Process qui tombe entre les mailles
   - Trop de C ? → Process trop lent (trop de consultation)
   - Personne en I ? → Risque de surprise / mauvaise communication

### Exemple : SOP "Facturation client"

| Étape | Dirigeant | Assistante | Comptable | Client |
|-------|-----------|------------|-----------|--------|
| Créer le devis | R | — | — | I |
| Valider le devis | A | — | — | R |
| Émettre la facture | I | R | C | I |
| Envoyer la facture | I | R | — | I |
| Suivre le paiement | I | R | — | — |
| Relancer si impayé | I | R | — | — |
| Clôture comptable | I | — | A/R | — |

> **Lecture** : Le dirigeant est R sur 1 seule étape (créer le devis) et A sur 1 seule (valider). Tout le reste est délégué. C'est la cible.

## Évaluation des compétences pour la délégation

### Matrice Maîtrise × Intérêt (inspirée de la matrice de compétences)

Avant de déléguer un process, évaluer la personne cible sur 2 axes :

| Niveau | Maîtrise | Intérêt |
|--------|----------|---------|
| 0 | Aucune connaissance | Aucun intérêt |
| 1 | Connaissance théorique | Intérêt faible |
| 2 | Première expérience | Intérêt moyen |
| 3 | Bonne expérience | Intérêt élevé |
| 4 | Expert | Passion |

### Grille de décision délégation

| Maîtrise | Intérêt élevé (3-4) | Intérêt faible (0-2) |
|----------|--------------------|--------------------|
| **Élevée (3-4)** | Déléguer immédiatement | Déléguer avec suivi (risque de lassitude) |
| **Moyenne (2)** | Former puis déléguer (motivation = moteur) | Envisager un autre candidat |
| **Faible (0-1)** | Former si le process est clé | Ne pas déléguer (trouver quelqu'un d'autre) |

> En TPE, souvent il n'y a qu'1 personne disponible. Dans ce cas : **former + documenter le SOP** = la personne apprend avec le guide sous les yeux.

## Méthode de collecte — L'interview "Raconte-moi ta semaine"

### Principe

On ne demande PAS au dirigeant de "lister ses process" (il ne saura pas). On lui demande de **raconter** ce qu'il fait. C'est Catherine qui transforme le récit en SOP.

### Les 5 questions clés

**Question 1 — La semaine type**
> "Décris-moi ta semaine type, du lundi matin au vendredi soir. Raconte-moi tout ce que tu fais, même les petites choses."

→ Permet d'identifier les process quotidiens et hebdomadaires
→ Noter tout, même "je regarde mes emails" (c'est un process)

**Question 2 — Le début de mois**
> "Qu'est-ce qui se passe en début de mois ? Qu'est-ce que tu fais systématiquement ?"

→ Permet d'identifier les process mensuels (compta, facturation, reporting)

**Question 3 — Le client arrive**
> "Un nouveau client te contacte. Raconte-moi tout ce qui se passe, du premier message jusqu'à ce qu'il soit pleinement accompagné."

→ Permet de cartographier le parcours client complet
→ Identifier les trous (étapes où le client est "perdu")

**Question 4 — Le pompier**
> "Qu'est-ce qui te fait arrêter ce que tu fais pour gérer une urgence ? Donne-moi 3 exemples récents."

→ Permet d'identifier les process de crise / SAV
→ Souvent les process les plus chronophages et les moins documentés

**Question 5 — Si je n'étais pas là**
> "Si demain tu étais absente 2 semaines, qu'est-ce que personne d'autre ne pourrait faire ?"

→ Permet d'identifier les process critiques non-délégables
→ Ce sont les premiers SOP à documenter (risque maximum)

### Question bonus — La décomposition (inspirée du WBS)

> "Ce process que tu viens de décrire, est-ce qu'on peut le découper en sous-étapes ? Par exemple, 'facturation' c'est : créer le devis, l'envoyer, suivre le paiement, relancer... Qu'est-ce que j'oublie ?"

→ Permet de décomposer un macro-process en tâches élémentaires (méthode WBS)
→ Chaque tâche élémentaire = 1 ligne dans le RACI

### Comment conduire l'interview

1. **Poser la question et ÉCOUTER** — ne pas interrompre, noter
2. **Relancer sur les détails** — "Et après ?", "Tu fais ça comment ?", "Quel outil tu utilises ?"
3. **Identifier les patterns** — si le dirigeant dit "ça dépend", creuser les scénarios
4. **Utiliser les mots du client** — nommer le SOP comme le client le nomme
5. **Valider à la fin** — "Donc si je résume, pour [process], tu fais 1, 2, 3... c'est bien ça ?"
6. **Remplir le RACI ensemble** — "Pour cette étape, c'est toi qui fais ? Qui devrait faire ?"

### Après l'interview

1. Transformer les notes en SOP structurés (template ci-dessus)
2. Remplir le RACI pour chaque SOP — identifier où le dirigeant est trop présent
3. Évaluer les compétences de l'équipe (matrice Maîtrise × Intérêt) pour planifier la délégation
4. Prioriser : commencer par les process qui sont à la fois **fréquents** et **chronophages**
5. Ajouter la Definition of Done pour chaque SOP — "c'est terminé quand..."
6. Limiter à 5 SOP pour commencer — ne pas submerger le client
7. Faire valider chaque SOP par le client : "Est-ce que c'est bien comme ça que tu fais ?"

## Priorisation des 5 premiers SOP

### Matrice de sélection

| Critère | Poids |
|---------|-------|
| Fréquence (plus c'est fréquent, plus on gagne) | x3 |
| Temps consommé (plus c'est long, plus on gagne) | x3 |
| Douleur client (plus c'est pénible, plus on gagne en satisfaction) | x2 |
| Automatisable (si oui, le ROI est immédiat) | x2 |
| Délégable (si oui, on libère le dirigeant) | x1 |

### Process typiques à documenter en premier (par catégorie)

**Finance/Compta** (presque toujours dans le top 5) :
- Facturation / émission de devis
- Clôture mensuelle / transmission comptable
- Relance impayés

**Commercial** (si le parcours client est un point de douleur) :
- Onboarding nouveau client
- Relance prospects
- Gestion des demandes entrantes

**Opérations** (si le dirigeant est "dans le guidon") :
- Planning hebdomadaire
- Process de production / livraison
- Gestion SAV / réclamations

**RH/Équipe** (si délégation = objectif) :
- Brief équipe hebdomadaire
- Attribution et suivi des tâches

**Tech/Outils** (si migration en cours) :
- Workflow de sauvegarde
- Process de publication (RS, newsletter)

## Suivi du déploiement des SOP

### Tableau de suivi (pour Catherine, pas pour le client)

| SOP | Statut | Priorité | RACI fait ? | DoD défini ? | Délégation | % avancement | Échéance |
|-----|--------|----------|-------------|--------------|------------|-------------|----------|
| [Nom] | À documenter / En cours / Terminé | P1-P4 | Oui/Non | Oui/Non | [À qui] | 0-100% | [Date] |

### Définition des priorités

| Priorité | Description | Timing |
|----------|-------------|--------|
| P1 | Critique — bloque le business ou le dirigeant | Phase 1 (Mois 1) |
| P2 | Important — gain de temps significatif | Phase 2 (Mois 2-3) |
| P3 | Utile — amélioration de confort | Phase 3 (Mois 4-6) |
| P4 | Nice to have — quand tout le reste est en place | Post-accompagnement |

### Cycle de vie d'un SOP

1. **Identifier** (interview) → Statut : À documenter
2. **Documenter** (template + RACI + DoD) → Statut : En cours
3. **Valider** (le client confirme que c'est correct) → Statut : En cours
4. **Déployer** (former l'équipe, mettre en place) → Statut : En cours
5. **Contrôler** (vérifier que ça tourne, ajuster) → Statut : Terminé
6. **Réviser** (tous les 3-6 mois, le SOP est-il toujours d'actualité ?) → retour à Documenter si besoin
