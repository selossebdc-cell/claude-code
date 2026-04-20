# Compte-rendu reunion FEEDUC — Mars 2026

**Date** : Mars 2026
**Participants** : Dirigeante FEEDUC (Speaker 1), Catherine Selosse, Jean-Francois (Speaker 4)
**Duree** : ~53 minutes
**Type** : Point de suivi + nouveaux projets

---

## Sujets abordes

### 1. Google Form — Feedback equipe (reunion juin Madrid)

**Contexte** : Reunion d'equipe debut juin a Madrid (semaine du 1-5 juin). La dirigeante souhaite sonder les 7 prestataires en amont.

**Objectif du Google Form** :
- Quels outils utilisez-vous ?
- Qu'est-ce qui vous plait ?
- Qu'est-ce que vous voulez faire evoluer ?
- Qu'est-ce que vous n'utilisez pas et pourquoi ?

**Decision** : Catherine peut intervenir a la reunion (en ligne ou en presentiel a Madrid) pour presenter les resultats et proposer des pistes d'amelioration.

### 2. Vente de l'entreprise

- FEEDUC est officiellement en vente
- Plusieurs acheteurs potentiels :
  - 2 jeunes investisseurs tech (pourraient faire evoluer rapidement les outils)
  - 1 acteur existant (GEDS) qui a deja sa propre plateforme
- La dirigeante continue d'operer normalement pendant la vente ("je veux que les acheteurs voient une boite active")
- Catherine sera presentee aux futurs acheteurs comme prestataire tech

### 3. Contrat de maintenance & facturation

- Les automatisations (n8n) tournent deja
- Catherine n'a pas encore envoye le contrat de maintenance
- **Decision** : Facture annuelle 2026 plutot que mensuelle
- Montant : 150 EUR HT / mois = **1 800 EUR HT / an**

### 4. Nouveau projet : Automatisation leads partenaires

**Probleme actuel** :
- Les formulaires de contact WordPress (partenaires : ecoles de langue, residences, etc.) ont ete supprimes
- Remplaces par des pages avec adresse mail du partenaire + demande de mise en copie
- Resultats : moins de leads pour les partenaires, et manip manuelle pour la dirigeante (transfert des copies a Lucia, etc.)

**Solution prevue (deploiement aout 2026)** :
1. Remettre les formulaires de contact sur WordPress (Gravity Forms)
2. 2 niveaux de service :
   - Formulaire WordPress = leads non qualifies (acces direct, pas d'avantages)
   - Mini-site = leads qualifies (avec avantages etudiants)
3. Automatisation a construire :
   - Formulaire WordPress → mail automatique au partenaire concerne
   - + Alimentation d'un tableau de suivi avec 4 colonnes :
     - Nom du partenaire
     - Nom de l'etudiant
     - Prenom de l'etudiant
     - Email de l'etudiant
   - Prefixer le sujet du mail : "Lead Partenaire — [Nom]" pour qualification
   - Source : boite info@

**Timeline** :
- Preparation technique : maintenant
- Remise en place des formulaires sur le site : aout (Chloe/Agnes)
- Lancement automatisation : aout

**Note** : Catherine a suggere "Lead Partenaire" comme prefix dans le titre du mail pour qualifier automatiquement.

---

## Actions Catherine

| # | Action | Echeance | Statut |
|---|--------|----------|--------|
| 1 | Envoyer facture annuelle maintenance 2026 (1 800 EUR HT) | ASAP | A faire |
| 2 | Rediger et envoyer le contrat de maintenance | ASAP | A faire |
| 3 | Creer le Google Form feedback equipe FEEDUC | Avant fin mai | A faire |
| 4 | Verifier dispo semaine du 1-5 juin (reunion Madrid, en ligne ou presentiel) | Avant fin avril | A faire |
| 5 | Preparer spec technique automatisation leads partenaires (WordPress → n8n → tableau) | Juin-juillet | A faire |
| 6 | Construire l'automatisation n8n leads partenaires | Aout | A faire |

## Actions Dirigeante FEEDUC

| # | Action | Echeance |
|---|--------|----------|
| 1 | Confirmer dates exactes reunion juin Madrid | A venir |
| 2 | Briefer Chloe/Agnes sur remise en place des formulaires WordPress | Juillet |
| 3 | Fournir la liste des partenaires (noms + emails) pour le routing | Avant aout |

---

## Notes

- La dirigeante est sereine sur la vente, bien accompagnee
- L'equipe a 2 profils proactifs sur 7, les autres ont besoin d'etre plus pousses
- Variable individuelle : 2 personnes ont atteint le 1er palier
- Le site web est en francais (base), aussi en anglais et italien
- Chloe/Agnes gere bien le site WordPress
