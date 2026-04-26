---
name: "Dot Market"
type: "client"
status: "active"
program: "Accompagnement Projet — Data & Claude Team"
contract_value: "10000"
contract_date: "2026-04-14"
end_date: "2026-10-XX"
sessions_planned: 15
sessions_completed: 1
---

# Dot Market — Mémoire Client

## 👤 Identité

- **Dirigeants**: Kévin Jourdan, Elsa Fanjul
- **Entreprise**: Dot Market (marketplace), Dot Advisory (M&A), School Dot Market
- **Secteur**: M&A / Conseil / Formations pour entrepreneurs
- **Équipe**: ~8 personnes (CEO, COO, Commercial, Analystes M&A, CSM, DAF)
- **Contacts**: Kévin (CEO) + Elsa (COO)

## 🎯 Objectifs Contrat

**Construire une infrastructure data complète + déployer Claude Team pour autonomiser l'équipe.**

1. Dashboard temps réel connecté Pipedrive + MemberStack (KPIs, time-to-cash par étape, pipeline, conversion)
2. Claude Team avec instructions par rôle (CEO, COO, Commercial, Analystes, CSM, DAF)
3. Agent d'amélioration continue (rapport hebdo Monday, 3-5 optimisations proposées)
4. Formation équipe + stabilisation

## 📊 État Actuel

### Sessions
- Planifiées: 15 (phases 0-4 sur 4 mois)
- Complétées: 1 (validation proposition)
- Prochaine: Phase 0 Audit (fin avril)

### Progression Diagnostic
- Phase 0 (Cadrage & Audit): 0% — démarrage fin avril
- Phase 1 (Dashboard pilotage): 0% — semaines 4-12
- Phase 2 (Claude Team): 0% — semaines 10-13
- Phase 3 (Agent amélioration): 0% — semaines 13-15
- Phase 4 (Stabilisation): 0% — semaines 15-17

### Architecture Cible
- **CRM** : Pipedrive (deals, pipeline, étapes, KPIs, UTM)
- **Base investisseurs** : MemberStack
- **IA** : Claude Team (6 profils : Kévin, Elsa, Matys, Analystes, CSM, DAF)
- **Automations** : n8n (webhooks, syncs, rapports)
- **Dashboard** : Temps réel, filtrable par entité + type de dossier

## 🔴 Blocages Actuels / Risques

🟠 **Data quality** — Pipedrive propre ? Toutes les étapes documentées ? Dépend de la Phase 0.
🟠 **Accès API** — Pipedrive + MemberStack doivent avoir connexion API en lecture/écriture.
🟠 **Timeline serrée** — 4 mois pour tout (Phase 0 peut décaler selon les données).

## 💬 Patterns Observés

### Style Direction
- **Kévin** (CEO) : Stratégique, aime les chiffres clairs, pressé mais veut une solution pérenne
- **Elsa** (COO) : Opérationnelle, frustration "tout est manuel", veut autonomiser l'équipe

### Contexte Métier

#### Les 3 Entités (clarification Session 1)

**Dot Market**
- Marketplace pour acheter/vendre petites businesses
- Petit deal saisonnier, haute volumétrie, commission rapide
- Parcours client: contact → qualification → annonce → négociation → closing
- KPI vendeur: visites, messages reçus, temps en ligne avant vente
- KPI acheteur: time-to-cash (85j estimé actuel)

**Dot Advisory** 
- M&A advisory pour deals > €1M (cabinet approach)
- Client: grandes entreprises / entrepreneurs en croissance
- Process: audit profond, valorisation complexe, négociation longue
- Time-to-cash: ~120j+ (plus long que Market)

**School Dot Market**
- Formation/coaching pour entrepreneurs
- KPI: visites → leads → leads engagés → formations vendues
- Acquisition: Google, site, partenaires touristiques
- UTM tagging = critical (tracer source acquisition)

#### Observations Phase 0
- **550+ exits traités** → besoin d'une vision globale de la pipeline
- **+80% de succès** → process qui fonctionne, mais non-documenté = perte de propriété intellectuelle
- **Time-to-cash est une boîte noire** → "85j en moyenne" estimé mais où ça bloque ? Phase négociation = 38% du temps
  - Besoin: mesurer en jours **calendrier client** (pas ETP), car délai perçu ≠ effort interne
  - Exemple: "4 jours travail ≠ 2 mois pour client" → c'est 2 mois qui compte
- **IA en silos** → 2 personnes développent des solutions perso, pas partagé avec équipe
- **Data quality concerns** : Pipedrive bien structuré mais ajustements récents post-process
- **Besoin de data pour décider** → pas de vision croisée Pipedrive/MemberStack/Pennylane

#### Structure Dashboard (Session 1 decision)
- **Vue "Acheteur-Vendeur"** plutôt que "Par entité"
  - Raison: parcours client centralisé (même logique chez Market/Advisory/School)
  - Drill-down possible par entité après
- **Accès**: Kévin, Elsa, Abdel Nasser (3 users)
- **Refresh**: à définir par KPI (real-time vs 1x/jour vs 1x/semaine)
- **Historique**: 1 semaine (certains KPI), 1 mois (autres), 1 année (trends)
- **Priority metrics**: 
  - Time-to-cash par étape (pipeline visibility)
  - Taux de conversion (visites → messages → closing)
  - Commission tracking (CA moyen par type dossier)
  - Panier moyen vs volume

### Moteurs
- Scalabilité (viser 1M+ CA)
- Autonomie équipe (pas de dépendance "2 IA specialists")
- Clarté opérationnelle (savoir où agir)
- Process documentés (éventuellement passer à un tier pour traiter plus de dossiers)

## 📈 KPIs Suivi

| Métrique | Avant | Cible | Actuel |
|----------|-------|-------|--------|
| Time-to-cash moyen | 85j (estimé) | 70j | - |
| Visibilité time-to-cash | 0% | 100% | - |
| Heures équipe (tâches auto) | [X] | X-15h/sem | - |
| % equipe utilisant Claude | 0% | 100% | - |
| Optimisations/semaine | 0 | 3-5 | - |
| Taux closing | 34% | 35%+ | - |

## 💡 Pépites LinkedIn

À extraire après livraison dashboard : patterns de décision uniques à Dot Market, time-to-cash insights par secteur, etc.

## 📝 Livrables en Préparation

### Première Ébauche Macro (Catherine → Avant Session 2)
- **But**: Validation que Catherine a bien compris le parcours client + articulation
- **Contenu**: 
  - Parcours client par entité (visuel simplifié)
  - Étapes clés identifiées
  - Premiers KPI proposés avec définitions
  - Questions en suspens
- **Format**: Document Google Sheet / Figma / Notion (à proposer à Kévin/Elsa)
- **Révision**: Session 2 (validation + ajustements)

### Document Définition Data (Catherine → Avant Session 2)
- **But**: Single source of truth pour toute la data
- **Contenu**:
  - Chaque KPI: définition, source (Pipedrive/MemberStack/Pennylane), corrélations
  - Règles de calcul (ex: "time-to-cash = date closing - date création dossier")
  - Format/unités (jours, €, %, nombres)
  - Historique retention rules
- **Validation**: Kévin + Elsa doivent approuver les règles
- **Impact**: Anything not defined = risk de mauvaise interprétation en Phase 1

### Vision Document (Kévin → envoyer à Catherine)
- Stratégie Dot Market 3 ans (partage Kévin)
- Format: PDF (vision document via Elsa)

## 📝 Notes Internes

- **Langage technique** : Kévin parle IA, pipeline, KPIs. Elsa parle process, équipe, timing.
- **Communication style**: Directe, orientée décision. Questions posées = attends réponse.
- **Décision** : Contrat signé 2026-04-14, projet approuvé. Paiement reçu 1/3 signature.
- **Vision** : Scaler 3x-5x CA sans proportionnel sur coûts (équipe 80% complète)
- **Maintenance post-projet** : Optionnelle. 3 premiers mois support inclus, puis ~50€/mois hébergement.

---

**Créé**: 2026-04-26  
**Dernière mise à jour**: 2026-04-26 (Session 1 intégration)  
**Proposition date**: 14 avril 2026  
**Valable jusqu'à**: 14 mai 2026
