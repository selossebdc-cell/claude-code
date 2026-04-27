---
name: MEMORY Index — Growth Agent Knowledge Base
description: Central index for all client, technical, and process memory. Read by growth agent every Monday.
last_update: 2026-04-26
location: Google Drive (source of truth) — /Drive partagés/CS - Consulting Stragégique/01-entreprise/memory/
---

# MEMORY — Source de Vérité Persistante

This is the unified knowledge base that **survives across Claude sessions** and feeds the weekly improvement agent.

## 📊 Index Rapide

### Client Memory
- **Actifs** : Fred, Taïna, Aurélia, Face Soul Yoga
- **Prospects** : Julie Aymé, Massens Group
- **Modules** : Accompagnement classique (18 sessions), Data/KPI, Cloud Team

### Technical Stack
- **API**: Portail Client V2 (RLS complete), Portail V3 (strategic planning phase)
- **Integrations**: Stripe, Shine, Brevo, Airtable, Google Drive, Google Calendar
- **Apps**: Playbook FSY (Circle migration), Questionnaire onboarding, Claude Configurator (v2 diagnostic refactor in progress)
- **Blockers**: 3 (see `/technical/blockers.md`)
- **Factory Status**: 2/10 projects compliant (see `/technical/project-factory-status.md`)
- **Portail V2 — Template Isolation**: Fixed RLS bug (2026-04-27) — see `project_portail-client-v2-template-isolation.md`
- **Portail V3 Vision**: Integrated CRM + client workspace for Catherine & Michaël — see `project_portail-client-v2-future-ideas.md`

### Claude Configurator — v2 Development (2026-04-27)
- **EPIC-1 to EPIC-5: COMPLETE** ✅ All core diagnostic components implemented + integrated + documented — see `project_claude-configurator-v2-epics-complete.md`
- **Diagnostic Refactor**: Intelligent + adaptive (vs linear 9-block) — 9 implicit blocks as internal checklist, not visible order — see `/technical/claude-configurator-diagnostic-refactor.md`
- **Model Choice**: Sonnet 4.6 for diagnostic — confirmed as best quality/cost balance — see `/technical/model-selection-decisions.md`
- **Quality Reference**: Fred's config standard (Claude-native implementation) — see `/reference/fred-config-standard.md` + `/reference/fred-claude-implementation-guide.md`
- **Fred Config Deployment**: Concrete implementation guide ready — NO Custom Instructions (OpenAI feature) — use CLAUDE.md + settings.json + memory system instead
- **Methodology**: Factory BREAK > MODEL > ACT > DEBRIEF — see `/technical/factory-methodology-adoption.md`
- **Security**: Passed Secure-by-Design audit (RLS policies, no hardcoded secrets, server-side validation)
- **Status**: ✅ CODE COMMITTED + PUSHED (2026-04-27) — 305 files recovered from GitHub + cleaned phantom worktree
- **Deployment Status** (2026-04-27 afternoon): Backend ready for Supabase (DEPLOYMENT.md Steps 1-4) — see `project_claude-configurator-v2-deployment-status.md`
- **Frontend**: Deferred (non-critical SSE streaming changes for separate commit after backend validation)

### Git & Workspace Recovery (2026-04-27)
- **Problem**: Phantom worktree phantom broke `git status` after Claude Code exit
- **Solution**: Deleted `.claude/worktrees/adoring-ramanujan`, recovered all files from GitHub — see `project_git-recovery-2026-04-27.md`
- **Result**: All 305 project files now tracked, committed, and pushed — **Nothing can be lost now**
- **Process**: Repeatable workflow documented for future incidents — see `feedback_claude-code-worktree-solution.md`

### Process Memory & Automation
- **Skill Workflow**: 8 refactored SKILL.md (Notion → Google Drive complete)
- **Client Onboarding**: Manual (no automation yet)
- **Proposal Generation**: HTML-based (not Word/PDF)
- **Session Reporting**: 🚀 **Automation in progress** — see `project_session-report-automation-v2.md`
  - **Problem**: Manual CR generation post-session (multiple transcript sources: Plaud, Fireflies, Fathom, notes)
  - **Goal**: Auto-generate CR + extract actions + send proposal via WhatsApp/Telegram for validation
  - **Status**: Requirements gathering (awaiting: validation channel choice, Portail V2 API, LinkedIn storage location)

---

## 🔄 Rules for Updates

**When to update MEMORY:**
- After every client session (update `/client/[client].md`)
- When a decision is made (update `/process/[workflow].md`)
- When a blocker is resolved (update `/technical/blockers.md`)
- Every time something changes that affects "how we work"

**Agent reads MEMORY every Monday** at 9am and generates improvement propositions.

---

## 📁 File Structure

```
01-entreprise/memory/
├── MEMORY.md (this file - index + rules)
├── growth-agent-system-prompt.md (optimized agent prompt for weekly runs)
├── feedback_claude-code-worktree-solution.md (worktree isolation + recovery)
├── feedback_rls-testing-methodology.md (RLS testing patterns)
├── project_git-recovery-2026-04-27.md (phantom worktree fix — repeatable process)
├── project_claude-configurator-v2-epics-complete.md (diagnostic v2 complete)
├── project_portail-client-v2-future-ideas.md (V3 vision + CRM integration)
├── project_portail-client-v2-template-isolation.md (RLS bug fixed)
├── technical_claude-configurator-v2-architecture-decisions.md (design decisions)
├── reference/
│   ├── fred-config-standard.md (Fred's quality baseline — Claude-native implem)
│   └── fred-claude-implementation-guide.md (⭐ CONCRETE steps for Fred to deploy)
├── client/
│   ├── fred.md (Accompagnement 6 mois, état courant + config deployment status)
│   ├── taïna.md [TBD]
│   ├── aurélia.md [TBD]
│   ├── face-soul-yoga.md [TBD]
│   └── template.md (blueprint for client-[name].md)
├── technical/
│   ├── blockers.md (3 current issues: Brevo sync, V3 design, Notion refs)
│   ├── security-risk-assessment.md (template + 3 examples for risk evaluation)
│   ├── project-factory-status.md (adoption tracking: 2/10 projects compliant)
│   ├── migration-execution-plan.md (step-by-step sequence to 100% compliance)
│   ├── portail-client.md (V2/V3 strategy) [TBD]
│   ├── integrations.md (Stripe, Shine, Brevo status) [TBD]
│   └── dependencies.md (cross-project impacts) [TBD]
├── process/
│   ├── skill-workflow.md (how to build/refactor SKILLs — 5 phases + standards)
│   ├── client-onboarding.md (sales → delivery — 5 stages + checklists)
│   ├── session-reporting.md (CRs + memory enrichment — 4 phases)
│   ├── proposal-generation.md (audit → proposal → contract — 6 phases)
│   └── consolidation-protocol.md (cloud sync conflict resolution rules)
└── versioning/
    ├── 2026-04.md (changelog: structural changes, decisions, blockers)
    └── DECISIONS.md (archived decisions with WHY + precedents)
```

---

## ☁️ Cloud Sync Protocol (Source of Truth)

**Location**: Google Drive (this folder)  
**Archive**: OneDrive (`/Claude Code/01-entreprise/memory/`) — read-only reference  
**Backup**: GitHub — monthly backup of critical files

**Rules**:
- **Edit only in Google Drive** — OneDrive is archive only (no editing)
- **If files differ** between clouds: See `/process/consolidation-protocol.md` for decision rules
- **Monthly audit** (first Monday): Spot-check 3-5 files for divergence
- **All edits documented** in `/versioning/2026-04.md` (changelog)

See `/process/consolidation-protocol.md` for complete conflict resolution procedures.

---

## 🔒 MANDATORY CHECKS (Before Any Coding)

**All of these must be executed BEFORE development starts. In this order:**

### 1. Security Risk Assessment
- **SKILL**: `/01-entreprise/skills/security-assessment/SKILL.md`
- **Template**: `/01-entreprise/memory/technical/security-risk-assessment.md`
- **Process**: Identify risks → propose mitigations → estimate effort → Catherine decides
- **Outcome**: Risk assessment + approved scope + documented decision
- **Status**: ✅ ACTIVE (mandatory for all features)

### 2. Spec-to-Code Factory Methodology
- **MASTER SKILL**: `/01-entreprise/skills/factory/SKILL.md` (orchestrates entire pipeline)
- **Phase Skills**: 
  - `factory-intake` (BREAK: requirements analysis)
  - `factory-spec` (MODEL: technical specifications)
  - `factory-plan` (ACT planning: epics/user stories/tasks)
  - `factory-build` (ACT building: code implementation)
  - `factory-qa` (DEBRIEF: QA & release validation)
  - `factory-quick` (fast-track for simple features)
  - `factory-resume` (resume interrupted pipeline)
- **Reference**: https://github.com/SylvainChabaud/spec-to-code-factory
- **Phases**: BREAK (intake) → MODEL (specs) → PLAN (planning) → BUILD (code) → DEBRIEF (QA) = 5 phases, 5 validation gates
- **Core Principles**: 
  - "No Spec, No Code" — specs locked before coding
  - "No Task, No Commit" — every commit references task ID
  - Auto-detection: greenfield (V1) vs brownfield (V2+)
  - Auto-remediation: 3x retry per phase before human intervention
- **Status**: ✅ ACTIVE & MANDATORY (recovered from chatbot-fsy project, now centralized for ALL development)

### Workflow: How They Work Together
```
[Feature request]
  ↓
[Security-Assessment SKILL] → risk assessment + approved scope
  ↓
[Spec-to-Code-Factory Phase 1: BREAK] (requirements + security assessment)
  ↓
[Gate 1 validation] → scope agreed?
  ↓
[Phase 2: MODEL] (technical specs + security implementation plan)
  ↓
[Gate 2 validation] → specs complete?
  ↓
[Phase 3: ACT] (build with task-referenced commits)
  ↓
[Gates 3 & 4 validation] → code quality + acceptance criteria?
  ↓
[Phase 4: DEBRIEF] (QA + release validation)
  ↓
[Gate 5 validation] → ready to deploy?
  ↓
[Deploy to production]
```

---

## 🤖 Growth Agent Schedule

**Mondays 9:00 AM**
1. Read all files in `/client/`, `/technical/`, `/process/`
2. Parse `/versioning/2026-04.md` for recent changes
3. Detect: blockers, dependencies, patterns, automation opportunities
4. Generate: 3-5 actionable propositions
5. **Include security check**: "Does this feature need security assessment?"
6. Send notification: "Rapport Amélioration — Semaine [N]"

---

## 📌 Current Focus (2026-04-27)

- [x] Git consolidation (GitHub = primary backup, source of truth established)
- [x] Memory architecture (client/, technical/, process/, versioning/)
- [x] Growth agent system prompt (optimized with chain-of-thought)
- [x] Process documentation (all 4 workflows documented)
- [x] **Cloud consolidation** (11 memory files copied OneDrive → Google Drive; consolidation-protocol.md created)
- [x] Security Risk Assessment SKILL (mandatory before feature development)
- [x] **Git recovery + worktree cleanup** (2026-04-27 — recovered all project files from GitHub, cleaned phantom worktree, committed 305 files + pushed)
- [ ] Populate client memory files (extract from existing data)
- 🟡 **Refactor session-report SKILL + build automation** (see `project_session-report-automation-v2.md` — awaiting Catherine's clarifications)
- [ ] Refactor client-onboarding SKILL (Notion → GDrive folders)
- [ ] **Portail V2 — Future: AI-assisted process step generation** (see `project_portail-client-v2-future-ideas.md`)
- [ ] First growth agent run (Monday 2026-04-28 @ 09:00)

**Status Summary:**
- ✅ Memory infrastructure ready (14 files: 12 original + 1 consolidation-protocol + 1 session-report-automation)
- ✅ Growth agent prompt optimized for quality
- ✅ All process workflows documented with phases + checklists
- ✅ Cloud consolidation complete (Google Drive = source of truth, OneDrive archived)
- ✅ Security assessment system active (mandatory before all features)
- 🟡 Client memories need population (templates ready)
- 🟡 Session Report Automation: In discovery phase (awaiting clarifications on validation channel, Portail V2 API, LinkedIn storage)
- 🟡 2 SKILLs need Notion→GDrive refactor (target: 2026-04-30)

**Modified:** 2026-04-27 by Claude  
**Next Agent Run:** Monday 2026-04-28 @ 09:00 (reads MEMORY files from Google Drive, generates 3-5 propositions)
- [Config as Living Proposal](product_claude-configurator-v2-config-living-proposal.md) — Config must be customizable, updatable with Claude features (EPIC-6/7 requirement)
