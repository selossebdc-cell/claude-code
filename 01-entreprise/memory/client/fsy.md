---
name: "FSY (Face Soul Yoga)"
description: "Plateforme vidéo yoga/bien-être. Projet data + automations livraison critique 23/04/2026."
type: "client"
---

# FSY — Face Soul Yoga

**Contact Principal**: Aurélia (fondatrice/propriétaire, validation seule)  
**Équipe Opérationnelle**: Aurélia + nouveau bras droit opérations (recrutement en cours)  
**Status**: Client actif — Projet Data/KPI/Automations **LIVRÉ 23/04/2026** → Phase post-livraison  
**Contrat**: Sprint 17 jours (audit 06/04 → livraison 23/04) ✓ COMPLÉTÉ

## 🎯 Mission Essence

Construire infrastructure data **sans dépendance Catherine** — tracker source → conversion → rétention en temps réel. Automations complètes (Brevo, n8n, chatbots).

## 🏢 Métier

- **Produits** : FSY Studio (mass-market 17€), MTM (premium), Aurélia Del Sol (coaching)
- **Base** : 13K+ contacts Brevo, migration Uscreen → Circle (2 membres initiale)
- **Architecture** : Brevo (CRM), Circle (communauté), n8n (workflows), Stripe (paiements), Telegram/WhatsApp (chatbots)

## 💡 Patterns Clés

| Pattern | Implication |
|---------|------------|
| **Aurélia = validation, pas opérationnel** | Tous les process doivent être déléguables au nouveau bras droit |
| **Nouveau binôme à installer** | Prioriser process simples + SOP claires pour autonomie rapide |
| **Data blind** | 13K contacts sans visibility conversions. Veut rapports hebdo auto. |
| **Sprint serré** | 23/04 deadline critique — tolérance zéro sur glissements |

## 📊 KPIs Tracking

- **Tracking** : source → conversion → rétention temps réel
- **Reporting** : hebdomadaire validé + envoyé (automatisé)
- **Segmentation** : par offre + intérêt + statut

## ⚠️ Dépendances Critiques

- **Laurie** : connexions Stripe↔Circle + UTM links
- **Aurélia** : validation templates + contenu
- **Mickaël** : chatbots (timeline très serrée)

## 🔴 Risques

- **DEADLINE 23/04 18h CRITIQUE** — Sprint final en cours
- **Chatbots blocage** : timeline très serrée si Mickaël en retard
- **Migration Uscreen** : data clean-up requis avant migration Circle

## 📅 Sessions (RDV)

| Num | Date | Étape | Décision | Livrables |
|-----|------|-------|----------|-----------|
| 1 | 06/04 | Audit initial | Brevo core 9 attrs, 22 templates, 9 n8n workflows | Audit report |
| 2 | 20/04 | Livraison + test | Validation tests, Stripe webhook, migration | Planning interactif |
| 3 | 23/04 | Livraison finale | Chatbots + formation équipe | Checklist validation ✓ |

## 📦 Livrables Post-Livraison (Documents Restaurés)

**Runbooks & Documentation Technique**
- `runbook-automatisations-fsy.html` (56KB) — Guide complet des automations (Brevo, n8n, Stripe)
- `schemas-tous-workflows.html` — Diagrammes de tous les workflows
- `schema-parcours-client-fsy.html` — Parcours client complet (visuel)
- `brief-michael-chatbots.html` — Brief chatbots Telegram/WhatsApp

**Planning & Checklists**
- `planning-livraison-jeudi.html` — Timeline livraison (20/04)
- `checklist-dimanche-validation.html` — Checklist validation Aurélia (23/04)
- `test-plan-automatisations.html` — Plan de test exhaustif

**Status**: Tous les runbooks documentés pour délégation à Laurie/Anam

## 🎯 Prochaines Actions

- [ ] Finaliser templates Brevo + validation Aurélia
- [ ] Webhook Stripe → Brevo actif + testé
- [ ] Migration Uscreen → Circle en place
- [ ] Chatbots Telegram + WhatsApp déployés
- [ ] Intégration du nouveau bras droit opérations (prise en main process + automatisations)

## 📝 Session de clôture — 2026-04-29

### Context
- Consolidation documentaire FSY pour livraison client immédiate.
- Focus recrutement: cadrer le rôle "bras droit opérations" et l'évaluation des candidatures.

### Decisions
- Unifier le client sous un seul dossier actif: `02-clients/fsy` (suppression du doublon `face-soul-yoga`).
- Structurer les livrables recrutement et onboarding communauté en format HTML/PDF-ready.
- Ajouter un dossier `transcripts/` pour conserver les verbatims source et améliorer les livrables sur-mesure.

### Execution (safe)
- Création livrables: fiches de poste, grille d'entretien (MD+HTML), script Loom Circle, guide "3 premières actions".
- Harmonisation visuelle: branding FSY (logo + palette), optimisation impression A4.
- Regroupement livraison client: `02-clients/fsy/documents/espace-client/livrables-2026-04-29/`.

### Secret handling
- Aucun secret stocké dans cette note.
- Rappel: si des tokens/keys apparaissent dans des terminaux historiques, rotation requise.

### Next actions
- Déposer les livrables dans le Portail Client V2 dès que le chemin cible exact est confirmé.
- Finaliser recrutement du bras droit (annonce + entretiens via la grille).
- Démarrer l'onboarding du bras droit sur les SOP/priorités FSY.

---
**Dernière mise à jour**: 2026-04-29  
**Prochaine révision**: Après publication des livrables dans Portail Client V2
