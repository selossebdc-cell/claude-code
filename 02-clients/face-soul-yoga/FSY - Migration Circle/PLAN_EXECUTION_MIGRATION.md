# Plan d'exécution : Migration FSY → Circle + Stripe

**Stratégie:** Utiliser le **service gratuit de migration Circle** pour les subscriptions Stripe + bulk import des membres

---

## 🎯 Vue d'ensemble

**Objectif:** Migrer ~78 clients actifs de YouScreen → Circle sans perte d'abonnements

**Clé:** Circle offre un service **gratuit** qui migre les subscriptions Stripe en 10 jours. Pas besoin de réinventer la roue.

```
Semaine 1    → Préparation données + demande migration Circle
Semaine 2-3  → Circle migre subscriptions en parallèle
Semaine 3    → Bulk import membres + activation accès paywalls
Semaine 4    → Communication clients + test
```

---

## 📋 PHASE 1 : Préparation (Jour 1-3)

### Étape 1.1 : Extraire la base de données YouScreen

**Michael / Laurie :**
```
1. Se connecter à YouScreen
2. Aller dans Settings → Customers (ou équivalent)
3. Exporter en CSV tous les clients actifs (78)
4. Vérifier colonnes minimales:
   - Email (OBLIGATOIRE pour Circle)
   - Nom
   - Statut abonnement (mensuel/annuel)
   - Date abonnement
   - Méthode de paiement (Stripe/PayPal/Apple/Google)
5. Envoyer le CSV à Catherine
```

**CSV attendu: format YouScreen-export.csv**
```
email,nom,type_abonnement,date_abonnement,methode_paiement
laurie@fsy.com,Laurie Fsy,mensuel,2025-06-15,stripe
client@example.com,Client Test,annuel,2025-01-01,paypal
...
```

---

### Étape 1.2 : Segmenter et nettoyer

**Catherine :**
```
1. Charger le CSV dans un script ou Excel
2. Segmenter en 3 fichiers:
   a) segment_stripe.csv (clients Stripe mensuel + annuel)
   b) segment_paypal.csv (clients PayPal)
   c) segment_apps.csv (clients Apple/Google)

3. Nettoyer:
   - Vérifier emails uniques (pas de doublons)
   - Vérifier format email valide
   - Remplir les noms manquants avec "Client [ID]"
   - Ajouter colonne "source" = "youscreen" (pour tracker)

4. Résultat = 3 CSV propres + 1 fichier de mapping des segments
```

---

### Étape 1.3 : Lancer la migration gratuite Circle

**Michael :**
```
1. Accéder à https://circle.so/migration/payments
2. Remplir le formulaire:
   - Indiquer: "Migrer de YouScreen (Stripe) à Circle"
   - Mentionner: ~78 clients actifs
   - Specifier: garder les dates de renouvellement intactes
   - Demander priorité si $250k+ revenue

3. Circle répondra en 48h avec:
   - Confirmation qu'ils peuvent le faire
   - Accès demandé (à Aurélia probablement pour les credentials YouScreen Stripe)
   - Timeline précis
   - Point de contact pour les questions

4. IMPORTANT: Demander lors du contact s'ils peuvent:
   a) Mapper l'historique de paiement (montants, dates)
   b) Mettre à jour le product ID sans re-auth
   c) Garder les customer tokens Stripe
```

**Timing:** Jour 1-2 (lancé immédiatement, réponse en 48h)

---

## 🔄 PHASE 2 : Migration Circle (Jour 5-14)

### Étape 2.1 : Circle migre les subscriptions Stripe (AUTO)

**Pendant que Circle travaille:**
- ✅ Vous ne faites rien — Circle s'en charge
- ⏱️ Timeline: ~10 jours ouvrables
- 📧 Vous recevrez un rapport final "migrations complete"

**Ce qui est migré:**
- ✅ Subscriptions Stripe
- ✅ Payment method data
- ✅ Unfinished installments
- ❌ Transaction history (pas possible)

---

### Étape 2.2 : Préparer Circle en parallèle (Pendant migration Stripe)

**Michael :**
```
1. Créer un compte Circle (ou se connecter à existant)
2. Aller dans Paywall settings
3. Créer les paywalls nécessaires:
   - Paywall "Accès Studio" (pour le contenu)
   - Vérifier que Stripe est bien connecté
   - Copier le product ID de Circle dans Stripe (important)

4. Tester une création de compte test:
   - Créer 1 membre test
   - Vérifier qu'il peut accéder au paywall
   - Vérifier que ça crée bien un customer dans Stripe

5. Documenter:
   - Circle community ID
   - Stripe product IDs (pour Circle)
   - Structure des espaces/accès
```

**Responsable:** Michael  
**Timing:** Jours 5-10 (en parallèle de la migration Stripe)

---

## 📤 PHASE 3 : Bulk Import des Membres (Jour 10-12)

### Étape 3.1 : Créer les fichiers CSV Circle

**Catherine :**

Circle accepte un CSV minimal avec juste:
```csv
email,name
laurie@fsy.com,Laurie
client@example.com,Client Test
```

Mais on peut aussi ajouter des custom fields pour tracker l'historique:
```csv
email,name,source,ancien_abonnement,ancien_type,ancien_renouvellement
laurie@fsy.com,Laurie,youscreen,actif,mensuel,2025-12-15
```

**Créer 3 fichiers (un par segment):**
1. `bulk_import_stripe.csv` (clients Stripe)
2. `bulk_import_paypal.csv` (clients PayPal)
3. `bulk_import_apps.csv` (clients Apple/Google)

---

### Étape 3.2 : Importer dans Circle

**Michael :**

**Option A: Via Dashboard (simple)**
```
1. Aller dans Circle → Settings → Members
2. Cliquer "Bulk import"
3. Upload bulk_import_stripe.csv
4. Circle affiche preview + mapping
5. Confirmer → import lancé
6. Attendre fin (quelques secondes à quelques minutes)
7. Répéter pour les 2 autres fichiers
```

**Option B: Via EasyCSV (plus flexible)**
```
1. Créer un Google Sheet avec les données
2. Connecter EasyCSV à Circle
3. Mapper les colonnes
4. Lancer l'import
→ Avantage: revérifier avant import, plus contrôlable
```

**Recommandation:** Option A si CSV clean, Option B si vous voulez vérifier.

---

## 🔐 PHASE 4 : Gérer les 3 segments clients

### SEGMENT 1 : Clients STRIPE (priorité haute)

**Status:** ✅ La migration Circle + Stripe est censée les couvrir

**Workflow après import:**
```
1. Client créé dans Circle (via bulk import)
2. Stripe migration a mis à jour son subscription
3. Client reçoit email Circle: "Votre compte est prêt"
4. Client se connecte à Circle
5. Client voit son accès paywall (depuis sa subscription Stripe)
6. Client peut se désabonner / gérer depuis Circle → Stripe
```

**À tester immédiatement:** 1 client Stripe → vérifier qu'il voit son accès

**Risque:** Si Circle migration échoue pour ceux-là, il faudra contacter Circle support

---

### SEGMENT 2 : Clients PAYPAL (impact modéré)

**Status:** ❌ Pas de migration directe (PayPal ≠ Stripe)

**2 options:**

**Option A: Accès gratuit initial (simple)**
```
1. Importer les clients PayPal dans Circle
2. Leur accorder accès gratuit au paywall (via API ou manual)
3. Envoyer email: "Vous avez un accès gratuit 30 jours, puis re-payer via Stripe"
4. Après 30j: accès révoqué, ils doivent payer via Stripe

Pro: Simple, aucune complexité
Con: Perte potentielle si clients ne repaient pas
```

**Option B: Demander re-subscription (direct)**
```
1. Importer les clients PayPal dans Circle
2. NE PAS leur donner d'accès
3. Envoyer email: "Compte créé, cliquez ici pour vous connecter + payer via Stripe"
4. Ils paient et obtiennent accès immédiatement

Pro: Aucune perte de revenue
Con: Plus d'étapes, risque de drop-off
```

**Recommandation:** Option A (accès gratuit 30j) car moins de perte client, relance email après

**Volume:** À récupérer du CSV (nombre de clients PayPal)

---

### SEGMENT 3 : Clients APPS (Apple/Google) (impact faible)

**Status:** ❌ Impossible de migrer (API Apple/Google restreinte)

**Unique option:**
```
1. Importer les clients Apps dans Circle
2. Leur accorder accès gratuit
3. Envoyer email: "Nouvelle plateforme Circle, paiement par Stripe désormais"
4. Lien vers paywall Circle
5. Ils repaient via Stripe

Pro: Pas de perte d'accès, transition simple
Con: Ils vont peut-être partir
```

**À clarifier:** Combien de clients apps au total? (Y'en a peu selon réunion)

---

## 📧 PHASE 5 : Communication Clients (Jour 13-14)

### Étape 5.1 : Préparation Brevo

**Laurie / Aurélia :**

Créer 3 campagnes d'email dans Brevo (une par segment):

**Email 1 : Clients Stripe**
```
Objet: Nous migrons vers Circle.so — votre accès continue

Body:
On bouge de plateforme! Votre abonnement Stripe continue sans interruption.
- Votre accès: [Date]
- Prochain paiement: [Date]
- Accédez ici: [lien Circle]

Vous pouvez gérer votre abonnement directement dans votre compte Circle.
Questions? → [support]
```

**Email 2 : Clients PayPal**
```
Objet: Nouvelle plateforme Circle — accès gratuit 30 jours

Body:
On migre vers Circle! Vous avez 30 jours d'accès gratuit.
Après, paiement par Stripe sur la nouvelle plateforme.
- Accédez: [lien Circle]
- Créez votre compte
- Vous verrez l'accès gratuit dans les paramètres

Dans 28j, email de rappel pour payer (ou garder l'accès).
```

**Email 3 : Clients Apps**
```
Objet: Circle.so — votre nouvelle communauté

Body:
Vous aviez accès via Apple/Google. 
Ça change! Nouveau paiement via Stripe sur Circle (meilleure plateforme).
- Créez votre compte: [lien]
- Accès gratuit les 7 premiers jours
- Puis paiement Stripe

[lien de paiement]
```

---

### Étape 5.2 : Envoyer les emails

**Timing:**
```
J-2 avant le go-live:  Email 1 (Stripe) — "Ça vient, rien à faire de votre côté"
J0 (jour du go-live):  Email 2 + 3 (PayPal + Apps) — "Créez compte + accès gratuit"
J+7:                   Email relance (Stripe + PayPal)
J+14:                  Rappel PayPal "Fin accès gratuit bientôt"
```

---

## ✅ PHASE 6 : Validation (Jour 15+)

### Checklist finale

**Avant d'annoncer "c'est bon":**

- [ ] **1 client Stripe importé** → vérifier il voit son accès Circle
- [ ] **Vérifier Stripe** → le product ID Circle est bien utilisé
- [ ] **1 client PayPal créé** → lui donner accès test (gratuit)
- [ ] **1 email reçu** → vérifier qu'il peut cliquer + se créer compte
- [ ] **Paywall test** → acheter comme un client PayPal → vérifier accès instant
- [ ] **Historique manquant** → confirmer avec clients que c'est OK (pas visible mais "c'est normal")

**Si un truc explose:**
- Contact Circle support immédiatement
- Michael revient vers Catherine/Laurie
- Pivot plan si nécessaire

---

## 💰 Accompagnement CS Digital — Scope réel

**INCLUS dans le plan:**
✅ Audit données + CSV clean  
✅ Préparation bulk import  
✅ Tester migration Circle (vérifier ça marche)  
✅ Setup emails Brevo (templates)  
✅ Checklist validation  

**NON INCLUS (mais discutable):**
❌ Contacter Circle pour toi (tu peux le faire directement, c'est gratuit)  
❌ Recréer historique de paiement (impossible + pas utile)  
❌ Support post-migration (à prévoir avec Circle)  

**Budget estimé:**
- Préparation + test = 1-2 jours Catherine
- À facturer: tarif forfaitaire ou horaire selon votre deal
- Après ça: facturation support/adjustments si besoin

---

## 🚀 Commencer MAINTENANT

**Action immédiate:**
1. Michael → Remplir https://circle.so/migration/payments
2. Michael → Préparer la structure Circle (paywalls, product IDs)
3. Laurie → Exporter CSV YouScreen

**Semaine prochaine:** Check statut Circle migration, commencer bulk import

---

## Notes techniques

### Si Circle migration échoue (worst case)

Si Circle ne peut pas migrer les subscriptions Stripe, plan B:

```
1. Créer un script qui:
   - Récupère les subscription IDs de YouScreen (via Stripe API)
   - Les mappe aux clients Circle
   - Ajoute un champ custom "old_stripe_id" dans Circle
   
2. Les clients continuent de payer sur Stripe (old product ID)
   → Aucune rupture de service
   
3. Après 1 mois:
   - Les renouvellements restent sur old ID (automatique)
   - Vous transférez manuellement les clients un par un vers new product ID
   → Coûteux mais safe
```

**Coût if B:** Développement custom (~3-5 jours)

### Custom product IDs à tracer

```
Stripe (prod) Account ID: [à demander à Michael]
YouScreen Product ID (old): [dans Stripe]
Circle Product ID (new): [à générer dans Circle/Stripe]
```

Une fois qu'on a ça, on peut tester les paiements.

---

**Prochaine étape:** Remplir le formulaire Circle migration + exporter CSV YouScreen
