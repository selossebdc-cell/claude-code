# Migration FSY : YouScreen → Circle + Stripe

**Date:** 23 avril 2026  
**Status:** 🟡 **Préparation phase 1**  
**Responsable:** Catherine (CS Digital) avec Michael & Laurie

---

## 📁 Documents

### 1. **CADRAGE_MIGRATION_FSY.md** 
   - 🎯 Scope initial + blocages identifiés
   - 📊 3 segments clients (Stripe / PayPal / Apps)
   - 💰 Budget et périmètre accompagnement
   - ✅ À lire en premier pour comprendre la stratégie

### 2. **PLAN_EXECUTION_MIGRATION.md**
   - 🗓️ Plan 15 jours détaillé (6 phases)
   - 👤 Actions par responsable (Michael, Laurie, Catherine)
   - 📋 Checklists phase par phase
   - ✅ Guide pratique pas à pas

### 3. **migration_plan.html**
   - 📊 Dashboard visuel interactive
   - 🎨 Timeline des 6 phases avec code couleur
   - 📍 Immediate action items pour chacun
   - ✅ À consulter pour vision d'ensemble

---

## 🚀 ACTIONS IMMÉDIATEMENT (Semaine du 23 avril)

### Michael 📍 Priorité absolue
- [ ] **Jour 1-2:** Remplir le formulaire Circle migration  
  → https://circle.so/migration/payments  
  → Indiquer: ~78 clients actifs, Stripe + YouScreen, dates renouvellement intactes  
  → Demander si pouvez importer subscription IDs + dates d'échéance

- [ ] **En parallèle:** Préparer structure Circle  
  → Créer compte Circle (ou accès existant)  
  → Configurer paywalls + Stripe product IDs  
  → Documenter Community ID + Product IDs

- [ ] **Stripe API check:** Tester changement product ID (si possible)

### Laurie 📋 Priorité haute  
- [ ] **Jour 1-3:** Exporter CSV YouScreen clients actifs  
  → Besoin: email, nom, type_abonnement, date_abonnement, methode_paiement  
  → ~78 clients, segmenter si possible Stripe/PayPal/Apps  
  → Envoyer à Catherine

- [ ] **Brevo:** Préparer segmentation 3 campagnes  
  → Segment 1: Clients Stripe (migration transparente)  
  → Segment 2: Clients PayPal (accès gratuit 30j)  
  → Segment 3: Clients Apps (gratuit 7j)

### Catherine (CS Digital) 🔧
- [ ] **Jour 2-3:** Recevoir CSV YouScreen  
  → Audit données + nettoyage  
  → Créer 3 fichiers segmentés (Stripe/PayPal/Apps)  
  → Préparer CSV pour bulk import Circle

- [ ] **Documentation:** Mapper données YouScreen → Circle  
  → Vérifier colonnes attendues Circle  
  → Tester bulk import sur 1-2 clients test

---

## ⏱️ Timeline (15 jours)

```
Semaine 1 (J1-3)      → Préparation + demande migration Circle
Semaine 2-3 (J5-14)   → Circle migre Stripe subscriptions (AUTO)
Semaine 3 (J10-12)    → Bulk import membres + test accès
Semaine 3-4 (J13-14)  → Campagnes email Brevo
Jour 15+              → Validation finale
```

---

## 🔑 Points clés

✅ **Ce qui est couvert par Circle (gratuit):**
- Migration subscriptions Stripe automatique (~10 jours)
- Bulk import CSV de membres
- Paywall access control

❌ **Ce qui n'est PAS possible:**
- Historique de paiement (dates anciennes)
- Migration PayPal/Apps (besoin ré-inscription)

⚠️ **Risques majeurs:**
- Perte d'abonnements si re-auth demandée → À ÉVITER
- Données manquantes si CSV incomplet
- Visibilité Stripe ↔ Circle à vérifier

---

## 💬 Questions bloquantes à Circle (Michael)

```
1. Pouvez-vous importer subscription IDs + dates d'échéance renouvellement?
2. Vérifier product ID Circle visible dans Stripe dashboard
3. Timeline précis pour les ~78 subscriptions Stripe
4. Besoin credentials YouScreen Stripe? (contact Aurélia?)
```

---

## 📞 Contacts

- **Michael:** Demande Circle migration + Setup Circle  
- **Laurie:** CSV YouScreen + Brevo campaigns  
- **Catherine:** Audit données + bulk import test + supervision  

**Escalade:** Catherine → Lead décisions techniques  
**Support:** Circle (gratuit) une fois service démarré

---

## ✅ Checklist avant go-live

- [ ] CSV YouScreen export propre (emails uniques, format valide)
- [ ] Circle migration request soumis + réponse reçue
- [ ] 3 CSV segmentés prêts (Stripe/PayPal/Apps)
- [ ] Circle paywalls configurés + testés (1 accès payant, 1 gratuit)
- [ ] Brevo campaigns prêtes (3 segments, scheduled J-2/J0/J+7)
- [ ] Test 1 client Stripe: voit abonnement dans Circle ✅
- [ ] Test 1 client PayPal: reçoit accès gratuit ✅
- [ ] Test paywall achat: fonctionnel end-to-end ✅

---

**Prochaine réunion:** Après réponse Circle (48-72h)

Status updates: https://notion.so/[à créer si needed]
