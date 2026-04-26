---
name: "Dot Market"
description: "M&A broker. 4-mois projet data + Claude Team + agent amélioration continue."
type: "client"
---

# Dot Market

**Dirigeants**: Kévin Jourdan (CEO), Elsa Fanjul (COO)  
**Entreprise**: Dot Market (marketplace), Dot Advisory (M&A), School Dot Market  
**Secteur**: M&A / Conseil en acquisition / Formation entrepreneurs  
**Équipe**: ~8 personnes (CEO, COO, Commercial, Analystes M&A, CSM, DAF)  
**Status**: Client actif — Projet data + Claude Team (démarrage Phase 0 fin avril 2026)  
**Contrat**: 10 000 € HT — 1/3 signature, 1/3 fin Phase 1, 1/3 fin mission

## 🎯 Mission Essence

**Transformer data en décision.** Donner à Kévin + Elsa une visibilité temps réel sur la pipeline, identifier bottlenecks, autonomiser l'équipe avec Claude personnalisé, mettre en place amélioration continue systématique.

## 🏢 Métier

- **Volume** : 550+ exits traités, 80% succès
- **Typologies** : SaaS, e-commerce, contenu/média
- **Blocage opérationnel** : Data existe (Pipedrive, MemberStack, Pennylane) mais ne "parle pas" — vision toujours manuelle
- **Time-to-cash** : ~85j estimé, 38% temps en négociation (SaaS 62j vs Contenu 91j = 29j écart)

## 💡 Patterns Clés

| Pattern | Impact | Levier |
|---------|--------|--------|
| **Data existe mais éparpillée** | Décisions à l'aveugle | Dashboard centralisé |
| **Time-to-cash boîte noire** | Impossible d'agir précisément | KPI par étape + bottleneck visibility |
| **IA en silos** | 2 perso dev solo, équipe exclue | Claude Team + centralisation |
| **Processes documentés mais pas exécutés** | Inefficacités invisibles | Agent amélioration hebdo |

## 📊 Architecture Cible

```
Pipedrive ─┐
           ├─→ n8n (webhooks, syncs) ──→ Dashboard temps réel
MemberStack┤                              │
Pennylane──┘                              └─→ KPI : time-to-cash, pipeline, closing, CA moyen
                                          │   filtrable par entité + type

Claude Team ─ 6 profils : Kévin, Elsa, Matys, Analystes, CSM, DAF
             ├─ Chacun a instructions adaptées à son rôle
             └─ Accès au dashboard + données Pipedrive (sécurisé)

Agent Amélioration Continue ─ Lundi : analyse données + process Notion + usage Claude
                            ├─ Mardi 8h : rapport 3-5 propositions classées impact
                            └─ Suivi historique décisions (go/no-go)
```

## 📈 KPIs Suivi

| KPI | Avant | Cible | Gain |
|-----|-------|-------|------|
| Time-to-cash moyen | 85j | 70j | -15j (~18%) |
| Visibilité étapes | 0% | 100% | Décision précise |
| Heures équipe (tâches auto) | [X] | X-15h/sem | ~780h/an |
| % équipe using Claude | 0% | 100% | Autonomie |
| Optimisations/sem | 0 | 3-5 | +15-20% efficacité |

## 📅 Planning Détaillé

| Phase | Durée | Focus | Livrable |
|-------|-------|-------|----------|
| 0 | S1-4 (~12h) | Audit stack + KPI mapping + quick wins | Cahier charges |
| 1 | S4-12 (~28h) | Dashboard Pipedrive + MemberStack | Production + 2 itérations |
| 2 | S10-13 (~18h) | Claude Team setup + instructions | Équipe formée |
| 3 | S13-15 (~4h) | Agent amélioration continue | Rapport hebdo auto |
| 4 | S15-17 (~5h) | Stabilisation + transfert | Équipe autonome |

## ⚠️ Dépendances Critiques

- **Elsa** : Dashboard KPI existant, accès Pipedrive lecture
- **API Pipedrive** : Doit avoir connexion lecture/écriture + toutes étapes documentées
- **Data quality** : Si pas clean, Phase 0 prend plus temps

## 💬 Styles Direction

| Personne | Style | Attente |
|----------|-------|---------|
| **Kévin** (CEO) | Stratégique, aime chiffres, pressé | Solution pérenne, ROI clair |
| **Elsa** (COO) | Opérationnelle, frustration "tout manuel" | Autonomie équipe, clarté process |

## 🎯 Prochaines Actions

- [ ] Signature contrat (paiement 1/3)
- [ ] Planifier Phase 0 Audit (fin avril)
- [ ] Elsa envoie dashboard KPI existant + accès Pipedrive
- [ ] Appel kickoff Phase 0

---
**Dernière mise à jour**: 2026-04-26  
**Prochaine révision**: Après Phase 0 (fin avril/début mai 2026)  
**Proposition valable jusqu'à**: 14 mai 2026
