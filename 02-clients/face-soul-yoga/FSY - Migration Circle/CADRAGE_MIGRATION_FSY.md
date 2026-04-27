# Cadrage Migration FSY : YouScreen → Circle + Stripe + Brevo

**Date réunion:** 23 avril 2026  
**Participants:** Laurie (FSY), Michael (collaborateur), Catherine (CS Digital)  
**Status:** ⚠️ **BLOQUÉ sur import des membres** — hors périmètre initial

---

## 🔴 BLOCAGE PRINCIPAL : Import des Membres

### Le problème
L'import des membres (base client depuis YouScreen) **n'était PAS inclus dans l'accompagnement initial**. C'était annoncé comme "vraiment le côté" — mais s'avère être une complexité majeure.

**Citation de Michael:**
> "cette partie-là d'import des membres, c'était pas c'était pas inclus si tu veux dans le projet, c'était vraiment le côté. Donc il va falloir effectivement qu'on prenne le temps de bien [comprendre]"

### Ce qui BLOQUE concrètement
✅ Créer un CSV depuis YouScreen → faisable  
✅ Créer des comptes dans Circle → faisable  
❌ **Créer/importer les liens avec les informations critiques:**
- Statut abonnement (mensuel vs annuel)
- Dates d'initialisation des paiements
- Dates d'échéance de renouvellement
- Lien vers Stripe (payment subscription history)
- Plateforme d'accès (app vs web app)
- Méthode de paiement initiale (Stripe/PayPal/Apple/Google)

**Problème technique core:**
> "c'est comment on les rentre dans Circle... les dates d'invoice, c'est là où ça bloque"

Les dates de facturation et les liens d'abonnement Stripe doivent être transférés depuis la base YouScreen, mais **Circle ne dispose pas de champ pour importer ces données en masse**.

---

## 📊 SANGLES D'ATTAQUE (Ordre de priorité)

### 1️⃣ IMPORT DES MEMBRES (CRITIQUE — Hors périmètre actuellement)

**Ce qu'on a:** CSV avec ~78 clients actifs + statut paiement  
**Ce qu'on doit faire:**

```
FLUX 1 : Stripe (Priorité absolue)
├─ Extraire clients Stripe mensuel + annuel → tagguer dans Brevo
├─ Créer comptes Circle
├─ Changer Product ID Stripe vers Circle product ID (via Stripe API)
├─ Préserver dates de renouvellement (automatique si Product ID change)
└─ Vérifier historique paiements visible dans Circle

FLUX 2 : PayPal (Impact limité)
├─ Clients qui payent via PayPal ≠ pas sur Stripe
├─ Solution = les réinscrire avec lien PayPal custom
└─ Besoin d'identifier ces clients dans le CSV

FLUX 3 : Apps (Apple/Google Pay)
├─ Clients sur apps younscreen ≠ pas sur Stripe
├─ Pas de migration possible (pas d'API Apple/Google)
└─ Solution = réinscrire avec accès Stripe pour la plateforme
```

**CE QU'ON PEUT FAIRE (Trouvé dans la doc Circle):**

✅ **Circle a un service de migration GRATUIT** pour les paiements Stripe
- Inclus: memberships, subscriptions, unfinished installments, payment method data
- **MAIS:** transaction history ❌ ne peut pas être migré (pas de date d'échéance visible dans Circle a priori)
- Timeline: ~10 jours ouvrables une fois lancé
- Éligibilité: $250k+ revenue annuel (MAIS: à demander si vous rentrez dedans)

✅ **Bulk import de membres via CSV** (3 méthodes)
1. Dashboard native (upload CSV)
2. API Members endpoint (programmatic)
3. EasyCSV (via Zapier / Google Sheets)

✅ **Accorder accès paywall sans paiement** (workaround possible)
- Via form + Zapier automation = donner accès à espace paywall sans transaction

❌ **MAIS les limitationsidentifiées:**
1. Circle ne peut pas importer l'historique de paiement (dates d'échéance, montants historiques)
2. Les produits Circle n'apparaissent pas dans Stripe dashboard (bug ou design?)
3. Pas de visibilité directe sur le lien Circle ↔ Stripe dans l'UI Circle

**Approche pragmatique à proposer à Laurie/Michael:**
```
OPTION A: Faire la migration gratuite Circle
├─ Circle transfère les subscriptions Stripe automatiquement (gratuit)
├─ Créer des comptes Circle avec bulk import CSV
├─ Accorder accès paywall aux clients existants (via form + Zapier)
└─ Les clients voient leur abonnement continuer sur Circle/Stripe (sans ré-auth)

OPTION B: Import manuel + migration
├─ Export CSV YouScreen
├─ Identifier les 3 segments (Stripe/PayPal/Apps)
├─ Créer comptes Circle manuellement ou bulk
├─ Utiliser Circle migration service pour les subscriptions Stripe
└─ Gérer PayPal/Apps à part (re-subscription ou accès offert)

OPTION C: Demander à Circle s'ils peuvent faire plus
├─ Est-ce qu'on peut importer subscription ID + dates via API?
├─ Est-ce qu'on peut créer des "virtual subscriptions" dans Circle?
└─ Contact: Circle support (mentions free migration service)
```

**Accompagnement CS Digital — Version ajustée:**
- ✅ Audit données + structuration CSV (3 segments)
- ✅ Tester bulk import Circle (1 test + valider les champs acceptés)
- ✅ Tester accès paywall sans paiement (form/Zapier)
- ✅ Documenter le flux de migration
- ⏸️ **Pause ici** — Décider OPTION A/B/C
- 💰 Au-delà (ex: custom script import, reconciliation Stripe) = **facturation supplémentaire**

---

### 2️⃣ STRIPE : Changement Product ID

**Le défi:** Tous les abonnements existants pointent vers YouScreen product ID → faut changer vers Circle product ID sans perdre les abonnements.

**Approche:**
- Via Stripe API = changement atomique si possible
- Sinon = changement manuel + vérifier que dates renouvellement se transfert bien
- **Risque:** Si les clients doivent se réautoriser = perte d'abonnements

**Blocage actuellement:**
Circle n'affiche pas ses produits Stripe ni le lien vers Stripe → visibility problem pour tester/valider

---

### 3️⃣ BREVO : 3 campagnes de migration

**Besoin:** Pré-informer clients avant import Circle (éviter surprise + bouncing)

**Segmentation (3 flux):**
1. **Stripe mensuel + annuel** → "Migration plateforme, votre abonnement continue"
2. **PayPal** → "Migration plateforme + changement méthode de paiement"
3. **Apps** → "Migration plateforme + nouveau lien de paiement Stripe"

**Responsibility:**
- Laurie / Aurélia → créer les campaigns dans Brevo
- CS Digital → segmenter + tagguer les clients dans Brevo avant import

**Timing:** Campagnes AVANT import Circle (préparation client)

---

### 4️⃣ CIRCLE → STRIPE : Vérifier la liaison

**Questions non tranchées:**
- ✅ Circle est connecté à Stripe (confirmé)
- ❌ Mais les produits Circle **n'apparaissent pas dans Stripe dashboard** — pourquoi?
- ❌ Possible que ce soit un délai de sync ou un bug Circle

**À tester:**
- Créer un paywall test → vérifier apparition dans Stripe
- Vérifier lien dans direction inverse (Circle → Stripe payment history visible?)

---

### 5️⃣ BUNNY.NET + Vidéos

**Contexte:** Toutes les vidéos YouScreen → Bunny.net (indépendance plateforme)  
**Status:** ✅ Fait — les clients auront juste des liens Bunny  
**No blocage** mais veille : vérifier les liens dans Circle

---

### 6️⃣ ZAPs et Integrations

**Contexte:** Certains clients sur automations YouScreen (ZAPs) → pas d'équivalent sur Circle actuellement

**Plan:**
- Michael → mail à YouScreen pour clarifier quoi garder actif
- Identifier clients affectés
- Impact limité (moins d'utilisateurs que avant)

---

## 🎯 PROCHAINES ÉTAPES

### Semaine du 23 avril

- [ ] **Michael/Aurélia:** Clarifier via Circle support = Est-ce que **on peut importer subscription IDs ou au moins dates d'échéance?**
- [ ] **Michael:** Définir le **Circle product ID exact dans Stripe** (et vérifier visibilité)
- [ ] **Laurie/Aurélia:** Préparer segmentation Brevo (3 campagnes) + tagging clients
- [ ] **Michael/Aurélia:** Tester Stripe API pour changement product ID (si possible)
- [ ] **CS Digital:** Analyser CSV YouScreen → documenter structure données

### Après clarifications Stripe/Circle

**Si possible = import technique:**
- Scénario 1 : Circle API accepte les données → à mettre en place
- Scénario 2 : Pas d'API → import manuel par batch (peut être long)

**Si IMPOSSIBLE = revoir scope:**
- Solution alternative = **créer les comptes Circle sans historique**, laisser les abonnements Stripe indépendants
- Clients auraient le lien Stripe visible dans Circle pour se désabonner/modifier
- Moins élégant mais pragmatique

---

## 💰 Accompagnement CS Digital — Clarification

### INCLUS (initial)
✅ Configuration Circle de base  
✅ Setup Stripe + Brevo  
✅ Validation des 3 flux clients  

### NON INCLUS (découvert réunion)
❌ **Import des membres en masse avec historique**
❌ Changement product ID batch Stripe
❌ Tests exhaustifs liaison Circle ↔ Stripe

### À FACTURER après triage

Une fois qu'on aura les réponses Circle/Stripe, évaluer:
- Complexité technique effective
- Temps d'exécution pour l'import
- Tests/validation nécessaires
- Support post-migration

**Approche proposée:** Accompagner jusqu'au point de décision (semaine prochaine), puis **facturer la complexité réelle** au-delà du périmètre initial.

---

## 📋 Notes techniques supplémentaires

### Structure CSV YouScreen à récupérer
```
client_id | email | nom | type_abonnement (mensuel/annuel) | date_abonnement | date_renouvellement | methode_paiement (Stripe/PayPal/Apple/Google) | app_vs_web
```

### Stripe → Circle mapping
```
YouScreen Product ID → Circle Product ID (?)
Subscription ID → ? (à clarifier si importable)
Customer metadata → Tags Circle?
```

### Risques identifiés
1. **Perte d'abonnements** si re-auth demandée aux clients → à éviter coûte que coûte
2. **PayPal + Apps** = pas de migration directe, besoin de communication client
3. **Visibilité Stripe** = Circle ne monte pas ses produits Stripe → bug ou design?
4. **Dates d'échéance** = donnée critique pour reconduire les abonnements

---

**Prochaine réunion:** Après réponses Circle + Stripe (début mai?)
