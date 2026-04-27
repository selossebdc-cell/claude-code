---
name: "Fred"
description: "Nouveau client, accompagnement classique. À compléter après premier RDV."
type: "client"
---

# Fred

**Contact Principal**: Fred (dirigeant)  
**Entreprise**: [À identifier] — Activité facturation/accounting related  
**Secteur**: Transformation digitale / Optimisation facturation  
**Status**: Client actif — Accompagnement Classique (sessions 1-10+ complétées)  

## 🎯 Mission Essence

Transformation digitale & optimisation système facturation. Sessions intensives sur structuration workflow, outillage (Dashlane, Outlook, n8n), automatisations.

## 🏢 Contexte Métier

- **Focus** : Facturation, structure financière, expatriation/onboarding complexe
- **Outils clés** : Facturations tests (PDF), Dashlane (password mgmt), Outlook (gestion catégories)
- **Enjeu** : Workflow facturation structuré + délégation possible

## 💡 Patterns Observés (Sessions 1-10)

- Workflow facturation en évolution (schéma en place)
- Besoin fort en automatisations (n8n workflows)
- Structuration progressive (arborescence OneDrive, catégories Outlook, etc.)
- Retro-planning expatriation identifié

## 📦 Documents Livrés & Livrables

**Dashboards & Schémas**
- `dashboard-fred.html` (16KB) — Dashboard de facturation
- `schema-facturation-fred.html` (59KB) — Workflow facturation détaillé

**Tutoriels & Guides**
- `tuto-dashlane-fred.html` (28KB) — Guide Dashlane (password mgmt)
- `tuto-outlook-categories-fred.html` (28KB) — Guide Outlook (gestion catégories)
- `retro-planning-expatriation.html` — Timeline expatriation

**CRs & Preps Sessions**
- Sessions 5-10 documentées (CRs + preps)
- Arborescence OneDrive schématisée
- Checklists de sessions

## 📅 Historique Sessions

| Num | Étape | Documents |
|-----|-------|-----------|
| 5-8 | Workflows facturation | CRs + schémas |
| 9-10 | Dashlane + Outlook | Tutoriels + retro-planning |
| TBD | Prochaines étapes | À planifier |

## 🎯 Configuration Claude pour Fred (Implémentation)

**Status**: ✅ Corrigé (pas de UI "Instructions personnalisées")  
**Reference**: `/01-entreprise/memory/reference/fred-config-standard.md`

**À livrer à Fred:**
- [ ] CLAUDE.md project (fichier texte dans `.claude/CLAUDE.md`)
- [ ] .claude/settings.json (fichier config, pas d'UI)
- [ ] ~/claude/memory/client/fred.md (operational memory)

**⚠️ CORRECTION IMPORTANTE**: 
- ❌ Il N'Y A PAS de "Paramètres → Instructions personnalisées" dans Claude
- ✅ Tout se configure via des fichiers: CLAUDE.md + settings.json
- ✅ C'est 100% code-based, pas d'interface UI

Configuration réelle:
- CLAUDE.md → system prompt + style guide (fichier texte)
- settings.json → hooks + permissions (fichier JSON)
- ~/claude/memory/ → centralized knowledge base (fichier markdown)
- schedule skill → tâches programmées (daily briefing, weekly debrief, monthly alerts)

---

## 🎯 Prochaines Actions

- [ ] Livrer fred_claude_setup.md avec implémentation concrète (CLAUDE.md template)
- [ ] Configurer scheduled tasks (daily 6h30, weekly Thursday 17h, monthly 1st)
- [ ] Valider que Fred peut charger /client/fred.md dans ~/.claude/memory
- [ ] Tester les workflows spécialisés (Engineer, Admin, Coach, Security)
- [ ] Planifier Session 11+ (selon objectifs restants)
- [ ] Documenter prochaines automations (n8n)

---
**Dernière mise à jour**: 2026-04-27 (clarification Claude implementation)  
**Sessions Complétées**: 5-10+  
**Config Status**: Claude-native implementation ready  
**Prochaine révision**: Après déploiement config Claude pour Fred
