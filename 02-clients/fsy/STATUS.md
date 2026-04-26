---
name: Status — Face Soul Yoga
description: Santé du projet, KPIs, satisfaction client, risques et monitoring
---

# Status — Face Soul Yoga

Tableau de bord du projet. Vue d'ensemble santé et progression.

**Dernière mise à jour** : 23/04/2026

---

## 📊 KPIs Projet

| Métrique | Valeur | Cible | Status |
|----------|--------|-------|--------|
| **Étapes complétées** | 3 / 4 | 4 / 4 | 🟠 À suivre (75%) |
| **Rendez-vous effectués** | 3 | 4-5 | 🟠 En cours |
| **Livrables prêts** | 7 / 8 | 8 / 8 | 🟠 À suivre (87%) |
| **Budget consommé** | $X | $Y | À confirmer |
| **Jours projet restants** | 4 jours | 0 | 🔴 CRITIQUE (deadline 23/04 18h) |

---

## 💰 Budget & Commercial

| Élément | Montant | Statut |
|---------|---------|--------|
| **Prix total contrat** | 8 000€ TTC | ✅ Signé |
| **Encaissé** | 5 250€ (2 500€ + 2 750€) | ✅ Reçu |
| **Reste dû** | 2 750€ | 📅 Dû 17/04/2026 |
| **Dépenses variables (outils)** | Brevo (~40€/mois) + Circle (199€/mois) + Telegram (free) + WhatsApp (~1.25€/mois) + eSignatures (0.49€/contrat) | 📋 À tracker |
| **Statut paiement** | 65% encaissé, 35% en attente | 🟠 À suivre |

---

## 🎯 Objectifs & Livrables

| Livrable | Statut | Deadline | Notes |
|----------|--------|----------|-------|
| Audit Brevo + architecture | ✅ Complété | 06/04/2026 | 13K contacts audités, 9 attributes définis |
| 22 templates Brevo + 9 workflows n8n | ✅ Complété | 06/04/2026 | Prêts en JSON, en attente déploiement |
| Automations Brevo en prod | 🔄 En cours | 23/04/2026 | Tests webhook en cours, 70% avancement |
| Migration Uscreen → Circle (5K vidéos) | 🔄 En cours | 23/04/2026 | CSV export done, import 50% |
| Chatbots (Telegram MTM + WhatsApp FSY) | 🔄 En cours | 23/04/2026 | Mickaël en dev, timeline serrée |
| Documentation + formation équipe | ⏳ À faire | 27/04/2026 | 6 sections guide, après livraison |
| Monitoring + reporting post-go | ⏳ À faire | 27/04 + mai-juin | Check-in 3 mois après |

---

## 😊 Satisfaction Client

**Satisfaction générale** : ⭐⭐⭐⭐ (Satisfait — audit initial positif)

**Retours positifs** :
- Architecture data comprise et approuvée
- Processus automatisé réduit charge opérationnelle
- Reporting hebdo fonctionnel et utile

**Points à améliorer** :
- Timeline livraison très serrée (ven-dim pour chatbots = stress)
- Aurélia souhaite plus de visibilité sur étapes (demandes de status checks réguliers)
- Laurie débordée = besoin d'automations plus robustes

**Dernier feedback** : 20/04/2026 — "Bravo la structure. On a enfin une vraie visibilité sur les conversions. Impatiente de voir les chatbots dimanche."

---

## ⚠️ Santé du projet

| Domaine | Statut | Commentaire |
|---------|--------|------------|
| **Planning** | 🔴 En retard | Deadline 23/04 18h = critique, buffer très faible |
| **Qualité livrables** | ✅ On track | Automations testées, architecture solide |
| **Communication** | ✅ On track | Planning transparent, status updates réguliers |
| **Équipe** | 🟠 À surveiller | Laurie débordée (ops), Mickaël timeline serrée (chatbots) |
| **Risques** | 🔴 Critiques | Webhooks Stripe dimanche = peu de buffer post-deployment |

**Indicateurs d'alerte** :
- 🔴 = Action urgente requise
- 🟠 = À suivre de près
- 🟢 = Tout va bien

---

## 🚩 Risques & Blocages

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|-----------|
| Laurie ne livre pas connexions Stripe lundi | Moyen (50%) | 🔴 Critique | Catherine peut faire backup (mais timeline?) |
| Aurélia n'approuve pas templates à temps | Faible (20%) | 🟠 Important | Catherine peut deployer + corriger après |
| Mickaël ne livre pas chatbots dimanche | Moyen (40%) | 🔴 Critique | Réduire scope (1 chatbot seulement) ou retarder |
| Webhooks Stripe causent bugs dimanche soir | Faible (25%) | 🔴 Critique | Avoir rollback plan + support dimanche |
| Anam ne termine pas migration vidéos | Faible (15%) | 🟠 Important | Migration peut être progressive (7 jours après) |

**Mitigation** : Avoir backup plan pour chaque dépendance externe.

---

## 📅 Timeline restante

```
Audit (06/04)  → Tests (20/04)  → Livraison (23/04)  → Debrief (27/04)  → Monitoring (mai-juin)
   ✅ Done         ✅ Done          🔄 En cours            ⏳ Planned           📋 À venir
  Scope OK      Prêt             Go/No-Go               Handoff          Check-in 3m
```

**Jalons critiques** :
- 🔴 Webhooks Stripe : 23/04 lundi matin (URGENT)
- 🔴 Chatbots dimanche : 23/04 dimanche 18h (final call)
- 🔴 Livraison finale : 23/04 jeudi 18h (deadline absolue)
- 🟠 Debrief + documentation : 27/04 (post-livraison)
- 🟢 Monitoring 3 mois : 27/05/2026 (check-in pour optimisations)

---

## 📝 Notes de gestion

**Contexte stratégique** :
- Aurélia voulait tracker conversions (13K contacts, taux unknown) → infrastructure data complète
- Objectif = zéro dépendance Catherine après livraison (Laurie + Anam autonomes)
- Deux marques parallèles : FSY mass-market (17€) vs Aurélia Del Sol premium → même infrastructure, segmentation claire

**Communication** :
- Status updates weekly (lundi + jeudi)
- Brief Mickaël envoyé, timeline extrême (ven-dim pour 2 chatbots)
- Planning livraison en HTML interactif (partagé avec équipe)

**Leçons pour projets futurs** :
- Timeline 17 jours pour infrastructure complète = trop tight
- Avoir backup plan pour dépendances externes (ex: Laurie = single point of failure)
- Chatbots = toujours ajouter +50% buffer sur timeline (imprevisibilité)

---

## ✅ Checklist Clôture

- [ ] Webhooks Stripe validés en production
- [ ] 9 automations Brevo actives et testées
- [ ] Migration Uscreen → Circle complète
- [ ] Chatbots déployés et testés
- [ ] Équipe Laurie/Anam formée
- [ ] Documentation maintenance livrée
- [ ] Aurélia satisfaction confirmée (retour positif)
- [ ] Monitoring 3 mois planifié
- [ ] Pépites LinkedIn extraites
- [ ] Contrat clôturé

**Statut clôture** : 🔄 En cours (40% complete)
