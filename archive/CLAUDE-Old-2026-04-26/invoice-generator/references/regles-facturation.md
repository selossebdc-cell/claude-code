# Règles de facturation — CS Business

## Informations entreprise

- **Raison sociale :** CS Business / Consulting Stratégique
- **Dirigeante :** Catherine Selosse
- **Email :** catherine@csbusiness.fr
- **Téléphone :** 0661864016
- **Outils :** Shine (facturation), Stripe (paiement CB), Notion (suivi)

## Offre principale

| Élément | Détail |
|---------|--------|
| Programme | Accompagnement Clarté & Autonomie - 6 mois |
| Durée | 6 mois |
| Sessions | 18 sessions (Phase 1 : hebdo, Phase 2 : espacé) |
| Tarif standard | 10 000 € TTC |
| Tarif préférentiel | 8 000 € TTC (-20%) |
| Tarif HT (si assujettie TVA) | 8 000 € HT |

## Échéanciers de paiement

### Paiement en 1x
- 100% à la signature
- Facture unique

### Paiement en 2x
| Échéance | % | Moment |
|----------|---|--------|
| Échéance 1 | 50% | À la signature |
| Échéance 2 | 50% | Mois 3 (mi-parcours) |

### Paiement en 3x
| Échéance | % | Moment |
|----------|---|--------|
| Échéance 1 | 40% | À la signature |
| Échéance 2 | 40% | Mois 2 |
| Échéance 3 | 20% | Mois 4 |

### Calcul des montants (exemples sur tarif préférentiel 8 000€)

**En 1x :** 8 000€
**En 2x :** 4 000€ + 4 000€
**En 3x :** 3 200€ + 3 200€ + 1 600€

## Mentions légales obligatoires sur les factures

### Mentions standard
- Numéro de facture (séquentiel, géré par Shine)
- Date d'émission
- Date d'échéance de paiement
- Identité du vendeur (CS Business, adresse, SIRET)
- Identité de l'acheteur (nom, entreprise, adresse)
- Description de la prestation
- Montant HT, TVA (ou mention d'exonération), montant TTC
- Conditions de paiement

### Mention TVA micro-entreprise
Si Catherine est en micro-entreprise (non assujettie TVA) :
> "TVA non applicable, article 293 B du Code Général des Impôts"

⚠️ **Attention :** Vérifier avec Catherine si elle a franchi le seuil de TVA. Si oui, TVA à 20% s'applique.

### Description de prestation type
```
Accompagnement Clarté & Autonomie — Programme 6 mois
Consulting stratégique et accompagnement à la transformation digitale
18 sessions personnalisées (visio/présentiel)
Période : [date début] — [date fin]
Échéance [X/Y]
```

## Process par étape

### Nouveau client → Première facture
1. Client signe la proposition (skill `proposal-generator`)
2. CGV signées (skill `client-onboarding`)
3. **Créer la facture dans Shine** avec :
   - Infos client (nom, entreprise, adresse, email)
   - Description prestation
   - Montant selon échéancier choisi
   - Mention "Échéance 1/X"
4. **Créer le lien Stripe** (si paiement CB)
5. **Mettre à jour Notion** → page "💰 Factures & Paiements" du dashboard client
6. **Envoyer** : facture Shine + lien Stripe au client

### Échéance suivante
1. Vérifier la date d'échéance
2. Créer la facture suivante dans Shine
3. Générer nouveau lien Stripe si besoin
4. Envoyer au client (5 jours avant l'échéance)
5. Mettre à jour Notion

### Relance impayé
1. J+5 après échéance : relance douce par email
2. J+15 : relance ferme par email
3. J+30 : appel téléphonique + email recommandé
4. Toujours informer Catherine avant chaque relance

## Suivi dans Notion

### Page client "💰 Factures & Paiements"
Chaque dashboard client a une page dédiée (voir template dans le SKILL.md).

### Statuts de paiement
| Emoji | Statut | Signification |
|-------|--------|---------------|
| ✅ | Payé | Paiement reçu et confirmé |
| ⏳ | En attente | Facture envoyée, paiement pas encore reçu |
| 🔴 | En retard | Date d'échéance dépassée |
| 📤 | Envoyé | Facture envoyée, dans le délai de paiement |

## Liens avec les autres skills

- **proposal-generator** → le montant et les modalités viennent de la proposition acceptée
- **client-onboarding** → la première facture est émise à l'étape 1 (Validation & engagement)
- **session-report** → pas de lien direct, mais le suivi des sessions peut déclencher les échéances suivantes
