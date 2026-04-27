---
name: admin-billing
description: "Gère l'admin facturation complète : création factures, liens paiement Stripe, relances paiement, suivi budget client, accès Portail, setup initial. Utilise ce skill dès que : nouveau client signé, facture à créer, lien de paiement à générer, paiement en retard, setup accès client."
---

# Admin Billing — Gestion facturation & accès clients

Tu gères l'administration complète après signature client : création factures Shine, génération liens Stripe, setup accès Portail, suivi paiements, relances.

Ce skill est complémentaire à :
- `proposal-generator` — génère la proposition (avant signature)
- `invoice-generator` — calcule l'échéancier (calcul des montants)
- `admin-billing` — **TOI** — exécute et suit les paiements (après signature)

## Quand ce skill se déclenche

- Nouveau client signé : créer facture 1, lien Stripe, accès Portail
- Catherine demande : "fais la facture de X", "crée le lien Stripe", "envoie la relance paiement"
- Paiement en retard (> 5 jours après échéance)
- Mise à jour accès client (Portail V2/V3)

## Processus

### Étape 1 — Valider les infos du client signé

Avant de créer une facture, vérifier dans `/02-clients/[client]/STATUS.md` :

```markdown
✅ Vérifier :
- [ ] Montant total du contrat ✓
- [ ] Modalité de paiement (1x/2x/3x) ✓
- [ ] Dates d'échéance calculées ✓
- [ ] Coordonnées client complètes ✓
- [ ] Contact email principal ✓
```

Si infos manquantes → demander à Catherine.

### Étape 2 — Créer facture #1 dans Shine

Pour la **première facture** de l'échéancier :

1. **Aller dans Shine** (espace facturation)
2. **Créer facture** avec les infos :
   - Client : [Nom + Entreprise]
   - Montant HT : calculé par invoice-generator
   - Description : "Accompagnement Clarté & Autonomie - Échéance 1/[X]"
   - Date : date de signature
   - Échéance : date prévue (0j = paiement immédiat, ou +30j selon contrat)
3. **Générer le PDF** dans Shine (validation, envoi)
4. **Récupérer le n° de facture** (ex: FAC-2026-001)

**Après création** :
- Copier le lien direct vers la facture PDF
- Mettre à jour `/02-clients/[client]/STATUS.md` avec le n° Shine

### Étape 3 — Créer lien Stripe pour paiement

1. **Aller dans Stripe**
2. **Créer une "Payment Link"** :
   - Montant exact : montant facture 1 (TTC, sans oublier TVA)
   - Description : "[Client] — Facture [N°] — Échéance 1/[X]"
   - Email client : pré-remplir avec contact principal
   - Durée du lien : 60 jours (par défaut)
3. **Récupérer le lien** (partager → copier URL)

**Format du lien à copier** :
```
https://buy.stripe.com/...
```

### Étape 4 — Setup accès Portail Client

**Portail V2** (en attendant V3) :
- URL : espace.csbusiness.fr/app.html
- Accès : par email du client
- Contenu : dashboard des sessions, livrables, actions

**À noter dans STATUS.md** :
```markdown
## Portail Client
- **Version** : V2 (temporaire jusqu'à V3)
- **URL accès** : espace.csbusiness.fr/app.html
- **Email** : [contact client]
- **Statut accès** : ✅ Créé / ⏳ À créer / 🔴 À mettre à jour
- **Lien CR sessions** : [dossier partagé ou lien]
```

### Étape 5 — Envoyer email de confirmation

Après facture + lien Stripe + accès Portail, envoyer un email client :

```
Sujet : Facture [N°] — Accompagnement Clarté & Autonomie

[Prénom],

Merci d'avoir signé l'accompagnement 6 mois ! Voici les infos importantes :

📋 FACTURE #1
[Lien direct facture PDF Shine]

💳 PAIEMENT EN LIGNE
[Lien Stripe Payment Link]
Montant : [X] €
Échéance : [Date]

🚪 ACCÈS PORTAIL CLIENT
[Lien accès]
Vous trouverez là : calendrier des sessions, CRs, livrables, actions en cours

📅 PROCHAINE SESSION
[Date + Heure]

Des questions ? Répondez à cet email ou contactez Catherine directement.

À bientôt ! 🚀
```

**Avant d'envoyer** → proposer le brouillon à Catherine pour relecture.

### Étape 6 — Mettre à jour STATUS.md

Remplir la section "💰 Budget & Commercial" :

```markdown
## 💰 Budget & Commercial

| Élément | Montant | Statut |
|---------|---------|--------|
| **Prix total contrat** | [X] € TTC | ✅ Signé |
| **Encaissé** | [X] € | ✅ Reçu |
| **Reste dû** | [X] € | [Date] |

### Échéancier
- **Facture 1** : [X] € — [Date] — [Statut]
  Lien Stripe : [URL]
  N° Shine : FAC-2026-XXX
  
- **Facture 2** : [X] € — [Date] — ⏳ À la date
  Lien Stripe : [À créer]
  N° Shine : [À créer]
  
- **Facture 3** : [X] € — [Date] — ⏳ À la date
  Lien Stripe : [À créer]
  N° Shine : [À créer]
```

### Étape 7 — Suivi paiements (hebdomadaire)

**Chaque lundi matin** :
1. Vérifier **Stripe** : quels clients ont payé depuis lundi dernier
2. Mettre à jour le **STATUS.md** de chaque client (statut + date paiement reçu)
3. **Générer factures suivantes** si première est payée :
   - Créer facture 2 dans Shine
   - Créer lien Stripe pour facture 2
   - Ajouter dans STATUS.md

### Étape 8 — Relances paiement (si retard > 5 jours)

Si un paiement ne rentre pas 5 jours après l'échéance :

1. Vérifier dans Stripe que le lien Stripe a eu des tentatives
2. Si lien expiré (60j) → créer un nouveau lien Stripe
3. Envoyer email de relance doux :

```
Sujet : Petit rappel — Facture [N°] en attente

[Prénom],

Je remarque que la facture [N°] ([Montant] €) est toujours en attente.

Le lien de paiement est valide jusqu'au [Date] :
[Lien Stripe frais si besoin]

Ou vous pouvez faire un virement sur nos coordonnées (voir facture PDF).

Y a-t-il un souci ? N'hésitez pas à me contacter.

Merci ! 🙏
```

**Avant d'envoyer** → valider avec Catherine.

## Règles critiques

1. **Jamais d'email sans validation Catherine** — même un email "auto" de relance doit être révisé
2. **Montant exact dans Stripe** — vérifier TTC (montant HT + TVA calculée)
3. **Traçabilité complète** — chaque lien Stripe doit être lié à une facture Shine
4. **STATUS.md à jour** — c'est la source de vérité pour les paiements clients
5. **Timing factures** : facture 1 = jour signature, facture 2 = selon échéance, etc.
6. **Accès Portail = jour signature** — le client doit avoir accès le jour même (ou J+1 max)

## Checklist setup client signé

- [ ] Montants + modalités vérifiés
- [ ] Facture #1 créée dans Shine
- [ ] Lien Stripe #1 généré
- [ ] Accès Portail créé + testé
- [ ] Email de confirmation envoyé
- [ ] STATUS.md rempli complètement
- [ ] Client signé dans Airtable = marqué "✅ Onboarding start"

**Status** : ✅ Setup complet prêt à démarrer première session
