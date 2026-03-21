---
name: client-onboarding
description: "Gère l'onboarding complet d'un nouveau client CS Consulting Stratégique. Utilise ce skill dès que l'utilisateur mentionne : nouveau client, onboarding, signature, bienvenue, démarrage accompagnement, créer dashboard, préparer espace client. Déclenche aussi quand l'utilisateur dit 'j'ai signé un nouveau client', 'prépare l'onboarding de X', 'crée le dashboard de X', ou 'envoie le kit de bienvenue'."
---

# Client Onboarding — Nouveau client CS Consulting Stratégique

Tu gères l'onboarding complet d'un nouveau client pour Catherine Selosse (CS Consulting Stratégique) : de la signature jusqu'à la Session #1.

Avant de commencer, lis les références :
- `references/checklist-onboarding.md` — toutes les étapes, emails templates, et vérifications
- `references/questionnaire-onboarding.md` — contenu complet du questionnaire (9 sections, 43 questions, mapping vers le diagnostic)

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

#### J+1 : Créer le Portail Client V2 (Supabase) + Dashboard Notion

**Étape 2a — Créer le compte client dans Supabase**

1. Aller sur https://supabase.com/dashboard → projet Portail Client V2
2. **Authentication → Users → Add user** :
   - Email : [email client]
   - Mot de passe : [Prénom][Année] (ex: Fred2026, FSY2026)
3. **Copier l'UUID** généré automatiquement

**Étape 2b — Insérer les données dans Supabase SQL Editor**

Générer et exécuter un script SQL basé sur le modèle `03-developpement/portail-client-v2/docs/factory/migrate-fred.sql` ou `migrate-fsy.sql`.

Le script doit insérer :

| Table | Données | Obligatoire |
|-------|---------|-------------|
| `profiles` | id (UUID Auth), email, full_name, role='client', program, total_sessions, start_date, end_date, company, logo_url, booking_url, whatsapp_url | ✅ |
| `contracts` | client_id, program_name, total_amount, start_date, end_date, payment_schedule (JSON), documents (JSON), automations_included, automations (JSON) | ✅ |
| `sessions` | session 1 planifiée (status='planned', date, title) | ✅ |
| `actions` | actions initiales si déjà définies (sinon vide, à remplir après Session #1) | ☐ |
| `tutos` | guides/vidéos si déjà prêts (type='guide'/'video' pour l'onglet Tutos, type='dashboard'/'project'/'roadmap' pour l'onglet Mon projet) | ☐ |
| `tools` | outils du client si déjà identifiés (status: adopted/in_progress/planned/abandoned) | ☐ |

**Champs `profiles` importants :**
- `booking_url` : lien Fantastical pour prendre RDV (https://fantastical.app/consulting-strategique/rdv1h)
- `whatsapp_url` : lien WhatsApp Catherine (https://wa.me/33661864016)
- `objectives` : JSONB array, à remplir après 2-3 sessions (pas au démarrage)
- `logo_url` : URL publique du logo client (PNG/SVG, min 200x200px)

**Champs `contracts.payment_schedule` (JSONB array) :**
```json
[
  {"date": "2026-XX-XX", "amount": XXXX, "status": "paid", "label": "Acompte signature"},
  {"date": "2026-XX-XX", "amount": XXXX, "status": "pending", "label": "2e échéance"},
  {"date": "2026-XX-XX", "amount": XXXX, "status": "pending", "label": "3e échéance"}
]
```
Statuts possibles : `paid`, `pending`. Ajouter `status_label` pour un statut personnalisé (ex: "En attente attestation URSSAF").

**Étape 2c — Tester le portail**

1. Se connecter sur https://espace.csbusiness.fr avec les identifiants du client
2. Vérifier : header (nom, entreprise, logo), onglets visibles, contrat affiché
3. Le portail affiche automatiquement les données insérées

**Étape 2d — Dupliquer le dashboard Notion (en parallèle)**

```
Page modèle : 3a8c3a2f-4255-8374-a789-01e14de407fa
URL : https://www.notion.so/3a8c3a2f42558374a78901e14de407fa
```

→ Utiliser `notion-duplicate-page`
→ Attendre ~10 sec (duplication asynchrone)
→ Le dashboard Notion reste l'espace de travail interne Catherine (CR, actions Catherine, roadmap)
→ Le Portail V2 Supabase est l'espace client visible

**Étape 2e — Récupérer le logo du client**

- **Site web** : chercher dans header/footer/favicon
- **LinkedIn** : page entreprise → logo
- Format : carré, PNG/SVG, min 200x200px, URL publique
- Uploader sur Supabase Storage ou utiliser l'URL directe

**Étape 2f — Personnaliser le dashboard Notion**

- Titre : "[Entreprise] - Dashboard Client"
- Icône : logo client (manuellement dans Notion)
- Cover/bandeau : logo ou image de marque
- Personnaliser tous les champs (prénom, dates, liens Fantastical)
- Ajouter les CGV signées dans la section Administratif

**Étape 2g — Enrichir la mémoire client**

Lire le fichier `02-clients/[prenom-ou-entreprise]/[nom].md` (doit exister depuis le skill `proposal-generator`).
Si le fichier n'existe pas → le créer depuis `02-clients/_TEMPLATE.md`.

1. Remplir/mettre à jour les **Notion IDs** : dashboard, meeting agendas (data source), objectifs & actions (data source)
2. Ajouter le **Supabase UUID** du client
3. Remplir : programme, période, sessions, tutoiement/vouvoiement
4. Quand Catherine fournit les réponses du questionnaire → remplir la section **Questionnaire** (9 sections + 1 bonus). Voir `references/questionnaire-onboarding.md` pour le mapping complet.
5. Commit + push GitHub

#### J+3 : Envoyer le kit de démarrage

1. **Email kit de démarrage** : rédiger à partir du template dans la checklist
   - Inclure le lien du portail : https://espace.csbusiness.fr (email + mot de passe)
   - Inclure le lien du questionnaire : [URL_QUESTIONNAIRE]
   - Inclure le lien Fantastical pour réserver Session #1
   - ⚠️ Ne plus envoyer de lien Notion au client — le portail V2 remplace Notion côté client
2. **Questionnaire d'onboarding** : le client remplit le formulaire HTML auto-hébergé (03-developpement/questionnaire-onboarding/)

⚠️ **RÈGLE DES 5 JOURS :** Le client doit réserver sa Session #1 minimum **5 jours ouvrés (7 jours calendaires) après** avoir rempli le questionnaire. Catherine a besoin de ce temps pour analyser les réponses et préparer la feuille de route personnalisée.

### Étape 3 — Suivre et relancer

Après l'envoi du kit, vérifier avec Catherine :
- Le client a-t-il rempli le questionnaire ?
- A-t-il réservé sa Session #1 (min. 5 jours ouvrés après le questionnaire) ?
- A-t-il accédé au portail (espace.csbusiness.fr) ?

Si non, proposer un email de relance doux.

### Étape 4 — Préparer la Session #1 (entre le questionnaire et la session)

Catherine utilise les 5 jours ouvrés pour :
- Analyser les réponses du questionnaire Fillout
- **Construire la feuille de route** → utiliser le skill `roadmap-generator` (diagnostic, cartographie process, roadmap 4 phases, indicateurs)
- Préparer les premiers éléments d'audit
- Identifier les quick wins possibles pour la semaine 1

## Architecture des espaces client

### Portail Client V2 (Supabase) — espace visible par le client
- **URL** : https://espace.csbusiness.fr
- **Stack** : HTML/CSS/JS vanilla + Supabase (PostgreSQL + Auth + RLS)
- **Code source** : `03-developpement/portail-client-v2/`
- **9 onglets client** : Dashboard, Actions, Brain Dump, Mes outils, Sessions, Tutos & Guides, Mon projet, Automatisations, Mon contrat
- **Vue admin Catherine** : Mes clients, Récap semaine, Dashboards
- **Supabase URL** : https://dcynlifggjiqqihincbp.supabase.co
- **Tables** : profiles, actions, brain_dumps, brain_dump_replies, sessions, tutos, contracts, tools, weekly_recaps
- **Scripts de migration** : `03-developpement/portail-client-v2/docs/factory/migrate-*.sql`

### Dashboard Notion — espace interne Catherine
- **Usage** : CR de séances (via skill session-report), roadmap, actions Catherine
- Le client n'accède plus à Notion — tout passe par le portail V2

| Base | Contenu | Qui remplit |
|------|---------|-------------|
| Meeting Agendas | CR complet dans la PAGE (pas juste les propriétés) | Catherine |
| Objectifs & Actions | Actions CLIENT uniquement | Client suit via portail V2 |
| Mes Actions Consulting | Actions CATHERINE | Catherine (base centrale) |

## Data sources de référence

### Supabase — Clients actifs

| Client | UUID | Email |
|--------|------|-------|
| Fred | `83e6c2be-f9cc-47d8-9232-e80e1626fa62` | fu@fusolutions.fr |
| Catherine (admin) | `7e7afc6a-50fb-4db6-bdeb-2ac0712703ea` | catherine@csbusiness.fr |

### Notion — Modèles
- **Page modèle dashboard** : `3a8c3a2f-4255-8374-a789-01e14de407fa`
- **Meeting Agendas** : `75d0e693-4576-4ce6-9d54-21be4786ba50`
- **Objectifs & Actions** : `e538e486-13f9-4509-952e-077c0ba0d454`

### Notion — Fred
- **Meeting Agendas** : `304c3a2f-4255-8059-9cbe-e445f9811586`
- **Objectifs & Actions** : `304c3a2f-4255-80a6-829f-effcce9fa0d4`

### Notion — Face Soul Yoga
- **Meeting Agendas** : `304c3a2f-4255-815e-b1b9-000b7082a58d`
- **Objectifs & Actions** : `304c3a2f-4255-81c3-82a0-000b8faa3263`

### Notion — Mes Actions Consulting (base centrale Catherine)
- **Data source** : `08e6087f-bbdf-4e66-af88-396f22389c1c`

## Règles importantes

- **Ne pas envoyer d'emails sans validation de Catherine** — toujours proposer un brouillon d'abord
- **Les CGV doivent être signées AVANT le démarrage** — c'est non négociable
- **Le portail V2 ET le dashboard Notion doivent être prêts AVANT d'envoyer le kit** — le client ne doit pas arriver sur un espace vide
- **5 jours ouvrés entre questionnaire et Session #1** — Catherine a besoin de ce temps pour préparer la feuille de route (5 jours ouvrés = 7 jours calendaires)
- **Questionnaire via formulaire HTML auto-hébergé** — lien : [URL_QUESTIONNAIRE] (ne pas créer de questionnaire Notion ni utiliser Fillout)
- **Ton chaleureux et rassurant** — le client ne doit jamais se sentir submergé par les outils
- **Simplicité d'abord** — le kit de démarrage demande 3 actions max au client (accéder au portail, remplir questionnaire, réserver session)
- **Pas de financement OPCO** — ne plus proposer ni gérer le financement OPCO pour les nouveaux clients (trop complexe à gérer)
- **Portail V2 = standard** — tous les nouveaux clients passent par le portail Supabase (plus de portail HTML statique V1)
