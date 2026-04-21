---
name: client-onboarding
description: "Gère l'onboarding complet d'un nouveau client CS Consulting Stratégique. Utilise ce skill dès que l'utilisateur mentionne : nouveau client, onboarding, signature, bienvenue, démarrage accompagnement, créer dashboard, préparer espace client. Déclenche aussi quand l'utilisateur dit 'j'ai signé un nouveau client', 'prépare l'onboarding de X', 'crée le dashboard de X', ou 'envoie le kit de bienvenue'."
---

# Client Onboarding — Nouveau client CS Consulting Stratégique

Tu gères l'onboarding complet d'un nouveau client pour Catherine Selosse (CS Consulting Stratégique) : de la signature jusqu'à la Session #1.

Avant de commencer, lis la checklist complète :
- `references/checklist-onboarding.md` — toutes les étapes, emails templates, et vérifications

## Quand ce skill se déclenche

- "Crée le dashboard pour [Client]"
- "Onboarding [Entreprise]"
- "Nouveau client : [Nom]"
- Catherine annonce un nouveau client signé
- Catherine demande de préparer un onboarding, un dashboard, un kit de bienvenue
- Catherine mentionne un démarrage d'accompagnement

## Processus

### Étape 1 — Collecter les infos du nouveau client

Demande à Catherine :
1. **Nom de l'entreprise**
2. **Nom du contact principal** (prénom et nom)
3. **URL du logo** (site web ou LinkedIn de l'entreprise)
4. **Email du client**
5. **Tutoiement ou vouvoiement ?**
6. **Date de début** du programme
7. **Nombre de sessions** (défaut : 18)
8. **Modalités de paiement** choisies (1x, 2x ou 3x)
9. **Les CGV sont signées ?** (si non, rappeler de les envoyer)
10. **☐ Prise en charge OPCO ?** (oui/non)

#### Si OPCO = oui :
Le client doit fournir **sous 10 jours** :
1. **Attestation de cotisation de formation** — disponible sur leur profil URSSAF (site URSSAF > Mon profil)
2. **Nom de l'OPCO** et coordonnées
3. **Montant estimé de prise en charge** (si déjà connu)

⚠️ **RÈGLE OPCO :** Un premier versement est demandé au client dès la signature (sans attendre l'OPCO). Une fois le montant de prise en charge OPCO confirmé, le solde restant est calculé et facturé. Voir le skill `invoice-generator` pour le détail du flux de facturation avec OPCO.

### Étape 2 — Lancer la séquence d'onboarding

Suivre la checklist dans `references/checklist-onboarding.md` étape par étape.

#### J-0 : Administratif + Email de bienvenue

1. **Vérifier CGV** : rappeler à Catherine d'envoyer les CGV si pas encore fait
2. **Facture** : rappeler d'émettre la facture avec les bonnes modalités
3. **Email de bienvenue** : rédiger l'email personnalisé à partir du template dans la checklist
   - Adapter les dates (début/fin programme = date début + 6 mois)
   - Personnaliser le ton (tutoiement/vouvoiement)
   - Proposer à Catherine de relire avant envoi

#### J+1 : Créer le dashboard Notion

**Étape 2a — Dupliquer le modèle de dashboard**

```
Page modèle : 3a8c3a2f-4255-8374-a789-01e14de407fa
URL : https://www.notion.so/3a8c3a2f42558374a78901e14de407fa
```

→ Utiliser `notion-duplicate-page`
→ Attendre ~10 sec (duplication asynchrone)

**Étape 2b — Récupérer le logo du client**

- **Site web** : chercher dans header/footer/favicon
- **LinkedIn** : page entreprise → logo
- Format : carré, PNG/SVG, min 200x200px, URL publique

**Étape 2c — Personnaliser le dashboard**

- Titre : "[Entreprise] - Dashboard Client"
- Icône : logo client (manuellement dans Notion)
- Cover/bandeau : logo ou image de marque (manuellement dans Notion)
- Header : mettre à jour dates début/fin et nombre de sessions
- Personnaliser tous les champs (prénom, dates, liens Fantastical)
- Ajouter les CGV signées dans la section Administratif
- Partager l'accès Notion au client

**Étape 2d — Mettre à jour la fiche client**

- Sessions achetées : [nombre]
- Sessions utilisées : 0
- Début programme : [date]
- Statut : 🟢 Actif

**Étape 2e — Enrichir la mémoire client**

Lire le fichier `clients/[prenom-nom].md` (doit exister depuis le skill `proposal-generator`).
Si le fichier n'existe pas → le créer depuis `clients/_TEMPLATE.md`.

1. Remplir/mettre à jour les **Notion IDs** : dashboard, meeting agendas (data source), objectifs & actions (data source), fiche client
2. Remplir : programme, période, sessions, tutoiement/vouvoiement
3. Quand Catherine fournit les réponses Fillout du client → remplir la section **Questionnaire Fillout** (7 sections : Vision, Stratégie, Parcours client, Productivité, Problématiques, Objectifs, Revenus)
4. Commit + push GitHub

#### J+3 : Envoyer le kit de démarrage

1. **Email kit de démarrage** : rédiger à partir du template dans la checklist
   - Inclure le lien Notion
   - Inclure le lien du questionnaire Fillout : https://feuillederoute.fillout.com/csbusiness
   - Inclure le lien Fantastical pour réserver Session #1
2. **Questionnaire d'onboarding** : le client remplit le formulaire Fillout (pas besoin de le créer, il existe déjà)

⚠️ **RÈGLE DES 5 JOURS :** Le client doit réserver sa Session #1 minimum **5 jours ouvrés (7 jours calendaires) après** avoir rempli le questionnaire. Catherine a besoin de ce temps pour analyser les réponses et préparer la feuille de route personnalisée.

### Étape 3 — Suivre et relancer

Après l'envoi du kit, vérifier avec Catherine :
- Le client a-t-il rempli le questionnaire Fillout ?
- A-t-il réservé sa Session #1 (min. 5 jours ouvrés après le questionnaire) ?
- A-t-il ouvert Notion ?

Si non, proposer un email de relance doux.

### Étape 4 — Préparer la Session #1 (entre le questionnaire et la session)

Catherine utilise les 5 jours ouvrés pour :
- Analyser les réponses du questionnaire Fillout
- **Construire la feuille de route** → utiliser le skill `roadmap-generator` (diagnostic, cartographie process, roadmap 4 phases, indicateurs)
- Préparer les premiers éléments d'audit
- Identifier les quick wins possibles pour la semaine 1

## Structure des bases de données du dashboard

| Base | Contenu | Qui remplit |
|------|---------|-------------|
| Meeting Agendas | CR complet dans la PAGE (pas juste les propriétés) | Catherine |
| Objectifs & Actions | Actions CLIENT uniquement | Client suit |
| Mes Actions Consulting | Actions CATHERINE | Catherine (base centrale) |

## Data sources de référence

### Modèle (template)
- **Page modèle dashboard** : `3a8c3a2f-4255-8374-a789-01e14de407fa`
- **Meeting Agendas** : `75d0e693-4576-4ce6-9d54-21be4786ba50`
- **Objectifs & Actions** : `e538e486-13f9-4509-952e-077c0ba0d454`

### Fred
- **Meeting Agendas** : `304c3a2f-4255-8059-9cbe-e445f9811586`
- **Objectifs & Actions** : `304c3a2f-4255-80a6-829f-effcce9fa0d4`

### Face Soul Yoga
- **Meeting Agendas** : `304c3a2f-4255-815e-b1b9-000b7082a58d`
- **Objectifs & Actions** : `304c3a2f-4255-81c3-82a0-000b8faa3263`

### Mes Actions Consulting (base centrale Catherine)
- **Data source** : `08e6087f-bbdf-4e66-af88-396f22389c1c`

## Règles importantes

- **Ne pas envoyer d'emails sans validation de Catherine** — toujours proposer un brouillon d'abord
- **Les CGV doivent être signées AVANT le démarrage** — c'est non négociable
- **Le dashboard doit être prêt AVANT d'envoyer le kit** — le client ne doit pas arriver sur un espace vide
- **5 jours ouvrés entre questionnaire et Session #1** — Catherine a besoin de ce temps pour préparer la feuille de route (5 jours ouvrés = 7 jours calendaires)
- **Questionnaire via Fillout uniquement** — lien : https://feuillederoute.fillout.com/csbusiness (ne pas créer de questionnaire Notion)
- **Ton chaleureux et rassurant** — le client ne doit jamais se sentir submergé par les outils
- **Simplicité d'abord** — le kit de démarrage demande 3 actions max au client (ouvrir Notion, remplir questionnaire, réserver session)
