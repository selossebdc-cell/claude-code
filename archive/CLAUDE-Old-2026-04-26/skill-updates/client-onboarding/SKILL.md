---
name: client-onboarding
description: "Gère l'onboarding complet d'un nouveau client CS Business. Utilise ce skill dès que l'utilisateur mentionne : nouveau client, onboarding, signature, bienvenue, démarrage accompagnement, créer dashboard, préparer espace client. Déclenche aussi quand l'utilisateur dit 'j'ai signé un nouveau client', 'prépare l'onboarding de X', 'crée le dashboard de X', ou 'envoie le kit de bienvenue'."
---

# Client Onboarding — Nouveau client CS Business

Tu gères l'onboarding complet d'un nouveau client pour Catherine Selosse (CS Business) : de la signature jusqu'à la Session #1.

Avant de commencer, lis la checklist complète :
- `references/checklist-onboarding.md` — toutes les étapes, emails templates, et vérifications

## Quand ce skill se déclenche

- Catherine annonce un nouveau client signé
- Catherine demande de préparer un onboarding, un dashboard, un kit de bienvenue
- Catherine mentionne un démarrage d'accompagnement

## Processus

### Étape 1 — Collecter les infos du nouveau client

Demande à Catherine :
- **Prénom et nom** du client
- **Nom de l'entreprise**
- **Email du client**
- **Tutoiement ou vouvoiement ?**
- **Date de début** du programme
- **Modalités de paiement** choisies (1x, 2x ou 3x)
- **Les CGV sont signées ?** (si non, rappeler de les envoyer)
- **☐ Prise en charge OPCO ?** (oui/non)

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

1. **Chercher le template** dashboard client dans Notion (dans l'espace "Clients - Gestion des Missions & Projets")
2. **Dupliquer le template** ou créer le dashboard avec cette structure :

**Structure du dashboard :**
```
🎯 [Prénom] [Nom] - Dashboard Client

> Programme : Accompagnement Clarté & Autonomie - 6 mois
> Début : [date]
> Fin : [date + 6 mois]
> Votre crédit : 18 sessions

---

📊 Votre Parcours
- Rythme recommandé
- Liens de réservation Fantastical

📥 INBOX - Capture Rapide (callout orange)
- Zone de capture avec règle des 2 minutes

[Colonnes]
Gauche : Ressources + Outils
- Feuille de route
- Tracker de temps
- Mes SOP & Process
- Mes Notes & Questions
- Outils informatiques

Droite : Matériel + Outils partagés
- Administratif (CGV, factures)
- Meeting Agendas
- Mes 18 Sessions
- Accès Communauté Skool

📞 Contact Catherine
🔔 Rappels importants
```

3. **Personnaliser** tous les champs (prénom, dates, liens)
4. **Ajouter les CGV** dans la section Administratif
5. **Partager** l'accès avec le client

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
- Préparer la feuille de route personnalisée dans le dashboard Notion
- Préparer les premiers éléments d'audit
- Identifier les quick wins possibles pour la semaine 1

## Règles importantes

- **Ne pas envoyer d'emails sans validation de Catherine** — toujours proposer un brouillon d'abord
- **Les CGV doivent être signées AVANT le démarrage** — c'est non négociable
- **Le dashboard doit être prêt AVANT d'envoyer le kit** — le client ne doit pas arriver sur un espace vide
- **5 jours ouvrés entre questionnaire et Session #1** — Catherine a besoin de ce temps pour préparer la feuille de route (5 jours ouvrés = 7 jours calendaires)
- **Questionnaire via Fillout uniquement** — lien : https://feuillederoute.fillout.com/csbusiness (ne pas créer de questionnaire Notion)
- **Ton chaleureux et rassurant** — le client ne doit jamais se sentir submergé par les outils
- **Simplicité d'abord** — le kit de démarrage demande 3 actions max au client (ouvrir Notion, remplir questionnaire, réserver session)
