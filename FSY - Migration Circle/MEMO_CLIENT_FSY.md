# Mémo : Migration FSY vers Circle
**Plateforme | Paiement | Communication**

---

## 📌 Résumé exécutif

**Objectif:** Migrer ~78 clients actifs de YouScreen vers **Circle.so** (plateforme communauté premium) avec maintien transparent des abonnements Stripe.

**Bonne nouvelle:** Circle offre un **service de migration GRATUIT** qui transfère automatiquement les subscriptions Stripe. Pas de perte d'abonnements, pas de réauthentification requise des clients.

**Timeline:** 15 jours (1er mai → 15 mai 2026)

---

## 🎯 Ce qui change pour vos clients

### ✅ Clients avec abonnement Stripe (priorité)
- **Aucune action requise** pendant la migration
- Leurs abonnements continuent sans interruption
- Ils reçoivent un email: "Nouvelle plateforme Circle, accès conservé"
- Accès + gestion abonnement directement dans Circle

### ⚠️ Clients avec PayPal  
- Accès GRATUIT pendant 30 jours sur Circle
- Après 30j: demande de passer à Stripe pour continuer
- Email d'invitation + lien de paiement

### ⚠️ Clients app (Apple/Google Pay)
- Accès GRATUIT pendant 7 jours sur Circle
- Après 7j: paiement Stripe obligatoire (plateforme unifiée)
- Email d'invitation + lien de paiement

---

## 📊 Les 3 segments clients

```
STRIPE (60-65 clients approx)
├─ Mensuel → migration auto
├─ Annuel → migration auto
└─ Pas d'action client requise ✅

PAYPAL (10-15 clients)
├─ Accès gratuit 30j
├─ Puis: re-subscription Stripe
└─ Communication adaptée nécessaire

APPS (0-5 clients)
├─ Accès gratuit 7j
├─ Puis: Stripe uniquement
└─ Communication adaptée nécessaire
```

---

## 🗓️ Timeline (15 jours)

| Phase | Dates | Quoi | Qui |
|-------|-------|------|-----|
| **Préparation** | J1-3 | Demande migration Circle + export données | Michael + Laurie |
| **Migration Circle** | J5-14 | Circle transfère subscriptions Stripe (AUTO) | Circle (on fait rien) |
| **Import membres** | J10-12 | Création comptes Circle + accès paywall | Michael + Catherine |
| **Communication** | J13-14 | Emails clients (3 campagnes Brevo) | Laurie + Aurélia |
| **Validation** | J15+ | Test clients + support | Michael + Catherine |

---

## 💰 Ce qui est INCLUS

✅ **CS Digital accompagne:**
- Audit des données clients (nettoyage CSV)
- Préparation bulk import Circle
- Test migration sur quelques clients
- Setup campagnes email Brevo
- Validation finale

---

## ⚠️ Ce qui change de votre côté

### Michael
- [ ] Jour 1-2: Soumettre demande migration Circle (https://circle.so/migration/payments)
  - Indiquer: ~78 clients, Stripe + YouScreen
- [ ] Jour 5-10: Configurer Circle (paywalls, structure communauté)
- [ ] Jour 10-12: Importer membres en masse (Circle dashboard)

### Laurie  
- [ ] Jour 1-3: Exporter liste clients YouScreen (CSV avec emails)
- [ ] Jour 13: Préparer + envoyer emails Brevo (3 campagnes)

### Catherine (CS Digital)
- [ ] Audit + nettoyage données
- [ ] Préparation CSV import Circle
- [ ] Test accès clients (vérifier abonnements visibles)

---

## 🚀 Actions immédiatement

### Michael (Priorité absolue)
```
1. Accéder à https://circle.so/migration/payments
2. Remplir le formulaire:
   - "Migrer de YouScreen (Stripe) vers Circle"
   - ~78 clients actifs
   - Demander si dates renouvellement peuvent être conservées
3. Attendre réponse Circle (48-72h)
   - Ils confirmeront timeline + processus exact
```

### Laurie
```
1. Ouvrir YouScreen settings
2. Exporter tous les clients actifs (CSV)
   Colonnes nécessaires:
   - Email (OBLIGATOIRE)
   - Nom
   - Type abonnement (mensuel/annuel)
   - Date abonnement
   - Méthode paiement (Stripe/PayPal/Apple/Google)
3. Envoyer le CSV à Catherine
```

### Catherine (CS Digital) — Reception
```
Dès réception CSV de Laurie:
1. Vérifier emails uniques + format valide
2. Créer 3 fichiers séparés (Stripe/PayPal/Apps)
3. Tester import 1-2 clients dans Circle
4. Préparer templates Brevo
```

---

## ❓ FAQ rapide

**Q: Les clients vont devoir se reconnecter?**  
A: NON (sauf PayPal/Apps qui changent de plateforme paiement). Stripe clients → accès identique.

**Q: On perd l'historique de paiement?**  
A: Oui, les anciennes factures ne seront pas visibles dans Circle. Mais c'est normal, les clients garderont leurs emails de reçus.

**Q: Qui paye Circle?**  
A: Circle c'est gratuit pour la community. Vous payez **Stripe** (0.3%) + Brevo (email).

**Q: Et si un client PayPal n'accepte pas de passer à Stripe?**  
A: Contact direct — proposer 30j pour décider, puis accès coupé. À gérer manuellement.

**Q: Risque d'interruption d'accès?**  
A: NON, si tout se passe bien. Circle garantit continuité subscriptions Stripe. PayPal/Apps: 30-7j gratuit avant changement.

---

## 📞 Points de contact

- **Michael:** Demande Circle + Setup technique
- **Laurie:** Données clients + Brevo communication
- **Catherine (CS Digital):** Lead accompagnement + troubleshooting

**Escalade:** Si problème technique → Catherine → Circle support

---

## ✅ Checklist avant J1

- [ ] Michael a accès Circle (ou crée compte)
- [ ] Laurie peut exporter données YouScreen
- [ ] Catherine a reçu invitation Drive shared (FSY - Migration Circle)
- [ ] Chacun a lu ce mémo + PLAN_EXECUTION_MIGRATION.md

---

**Prochaine étape:** Michael soumet formulaire Circle + réception CSV Laurie = Go pour phase 2.

**Questions?** Réunion checkpoint semaine du 28 avril (après réponse Circle).
