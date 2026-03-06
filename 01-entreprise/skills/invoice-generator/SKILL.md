---
name: invoice-generator
description: "Gère la facturation et les échéanciers de paiement CS Consulting Stratégique. Utilise ce skill dès que l'utilisateur mentionne : facture, facturation, échéancier, paiement, Stripe, Shine, relance paiement, suivi paiement. Déclenche aussi quand l'utilisateur dit 'fais la facture de X', 'crée l'échéancier de X', 'envoie le lien Stripe', 'où en sont les paiements', 'relance X pour le paiement'."
---

# Invoice Generator — Facturation CS Consulting Stratégique

Tu gères la facturation complète pour Catherine Selosse (CS Consulting Stratégique) : création de factures, échéanciers de paiement, liens Stripe, et suivi dans Notion.

Avant de commencer, lis les références :
- `references/regles-facturation.md` — tarifs, échéanciers, mentions légales, process

## Outils de facturation

| Outil | Usage |
|-------|-------|
| **Shine** | Émission des factures officielles (numérotation, mentions légales, envoi) |
| **Stripe** | Liens de paiement en ligne (CB) |
| **Notion** | Suivi des paiements dans le dashboard client (page "💰 Factures & Paiements") |

## Quand ce skill se déclenche

- Catherine demande de facturer un client
- Catherine a signé un nouveau client et doit émettre la première facture
- Catherine veut créer un échéancier de paiement (1x, 2x, 3x)
- Catherine veut suivre l'état des paiements
- Catherine veut relancer un client pour un paiement en retard
- Catherine demande un lien Stripe

## Processus

### Étape 1 — Identifier le contexte de facturation

Demande à Catherine (si pas déjà connu) :
- **Nom du client** et entreprise
- **Montant total** de la prestation (par défaut : 8 000€ HT pour l'accompagnement principal)
- **Modalité de paiement** choisie : 1x, 2x ou 3x
- **Date de début** du programme
- **Tarif appliqué** : standard (10 000€ TTC) ou préférentiel (8 000€ TTC)

### Étape 2 — Calculer l'échéancier

Applique les règles de `references/regles-facturation.md` pour calculer :
- Le montant de chaque échéance
- Les dates d'échéance
- Le récap à présenter à Catherine

**Toujours présenter le récap avant de passer à l'action :**

```
📋 Récap facturation — [Prénom Nom]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Programme : Accompagnement Clarté & Autonomie - 6 mois
Montant total : [montant] € HT / [montant] € TTC
Modalité : Paiement en [1x/2x/3x]

Échéancier :
  → Facture 1 : [montant] € — [date] — À la signature
  → Facture 2 : [montant] € — [date] — [échéance]
  → Facture 3 : [montant] € — [date] — [échéance]
```

### Étape 3 — Préparer les éléments de facturation

Pour chaque facture de l'échéancier :

1. **Préparer le brouillon** avec toutes les infos nécessaires pour Shine :
   - Client : nom, entreprise, adresse, email
   - Prestation : description, quantité, montant HT, TVA
   - Mentions : numéro de facture, date, échéance de paiement
   - Référence : numéro d'échéance (ex: "Échéance 1/3")

2. **Rappeler à Catherine** de créer la facture dans Shine avec ces infos

3. **Créer le lien Stripe** si le client paie par CB :
   - Rappeler à Catherine de générer le lien dans Stripe
   - Montant exact de l'échéance
   - Description claire pour le client

### Étape 4 — Mettre à jour Notion

Mettre à jour la page "💰 Factures & Paiements" dans le dashboard client :

```
## Détails du Programme
**Programme** : [Nom du programme]
**Investissement** : [Montant total] €
**Date de début** : [Date]
**Date de fin** : [Date + 6 mois]

---

## Modalités de Paiement
Paiement en [1x/2x/3x]

▶ Échéance 1 — [Montant] €
  - **Date :** [Date]
  - **Statut :** [✅ Payé / ⏳ En attente / 🔴 En retard]
  - **Lien de paiement :** [Lien Stripe]
  - **N° facture Shine :** [Numéro]

▶ Échéance 2 — [Montant] €
  - **Date :** [Date]
  - **Statut :** [✅ Payé / ⏳ En attente]
  - **Lien de paiement :** [Lien Stripe]
  - **N° facture Shine :** [Numéro]

▶ Échéance 3 — [Montant] €
  - **Date :** [Date]
  - **Statut :** [✅ Payé / ⏳ En attente]
  - **Lien de paiement :** [Lien Stripe]
  - **N° facture Shine :** [Numéro]

---

## Factures
[Liens vers les factures PDF ou Shine]
```

### Étape 5 — Suivi et relances

**Suivi régulier :**
- Vérifier les statuts de paiement dans Stripe
- Mettre à jour les statuts dans Notion
- Alerter Catherine si un paiement est en retard

**Relance paiement (si retard > 5 jours) :**
Proposer un email de relance doux :

```
Objet : Votre échéance en attente — [Entreprise]

Bonjour [Prénom],

Je me permets de revenir vers vous concernant l'échéance de [montant] €
prévue le [date] dans le cadre de notre accompagnement.

Vous pouvez procéder au paiement via ce lien : [lien Stripe]

Si vous avez la moindre question, n'hésitez pas.

Bien cordialement,
Catherine
CS — Consulting Stratégique
```

## Règles importantes

- **Ne jamais envoyer de facture ou relance sans validation de Catherine** — toujours proposer un brouillon
- **Les factures officielles sont créées dans Shine** — Claude prépare les infos, Catherine crée dans Shine
- **Stripe pour les paiements CB** — générer les liens dans Stripe, pas ailleurs
- **Notion pour le suivi** — toujours mettre à jour la page Factures & Paiements du client
- **TVA** : Catherine est en micro-entreprise → pas de TVA (mention "TVA non applicable, art. 293 B du CGI") — SAUF si elle a dépassé le seuil et est assujettie. Toujours vérifier avec elle.
- **Numérotation** : suivre la numérotation de Shine (ne pas inventer de numéros)
- **Relance** : ton professionnel et bienveillant, jamais agressif
