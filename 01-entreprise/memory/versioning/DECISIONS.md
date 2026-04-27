---
name: Archived Decisions — Precedents & Rationale
description: Major decisions with WHY and impact — used by growth agent to understand philosophy
type: versioning
last_update: 2026-04-23
---

# Archived Decisions — Precedents & Rationale

This file captures **major decisions** with their reasoning. Used by growth agent + future team members to understand why we do things a certain way.

---

## Architecture & Infrastructure

### Decision 1: Google Drive = System of Record (2026-04-23)
**What**: Google Drive (OneDrive/CS - Consulting Stragégique) is the source of truth. GitHub is backup only.

**Why**:
- All client data, session notes, deliverables live in GDrive
- Real-time collaboration (can edit while other people are viewing)
- Compliance: RGPD data stays in EU datacenter (GDrive EU)
- GitHub can't be real-time source (too slow for daily updates)
- Client data never staged in GitHub (privacy)

**Impact**:
- Growth agent reads from GDrive files, not Git history
- All SKILL inputs/outputs reference GDrive paths
- When in doubt about "what's current," read GDrive (not GitHub)
- Backups go GDrive → GitHub (unidirectional, not sync)

**Precedent for**: Where to store client data, which system is authoritative, privacy/compliance

---

### Decision 2: Memory Persists in `/01-entreprise/memory/` Files (2026-04-23)
**What**: Persistent context across Claude sessions is stored in structured MARKDOWN files (not database, not proprietary format).

**Why**:
- Markdown is human-readable (Catherine can read/edit directly)
- Markdown is version-controllable (can see what changed)
- Markdown doesn't require external services (self-contained)
- Growth agent can parse MARKDOWN as easily as Claude can
- Future: can be read by other tools/scripts (not locked in)

**Impact**:
- Every MEMORY file has consistent frontmatter (name, description, type, date)
- Growth agent reads `/01-entreprise/memory/` directory weekly
- Client knowledge = `/memory/client/[name].md` (not Notion, not spreadsheet)
- Technical state = `/memory/technical/blockers.md` (not Jira, not tickets)
- Process knowledge = `/memory/process/[workflow].md` (not wiki, not docs)

**Precedent for**: How to store cross-session context, what format to use, where agent reads from

---

### Decision 3: Client Folder Structure = Single Source for Client (2026-04-23)
**What**: Everything about a client lives in `/02-clients/[client]/` — one folder per client.

**Why**:
- Single point of truth (no client data scattered across Notion/Airtable/Google Drive)
- Easy to back up (entire client = single folder)
- Easy to share (send folder link to client if needed)
- Easy to archive (one folder per client at end of engagement)
- Integrates with SKILL workflows (all paths reference `/02-clients/`)

**Impact**:
- Client structure: NOTES.md, SESSIONS.md, SUIVI.md, STATUS.md, feuille-de-route.md + CRs
- New client = create `/02-clients/[name]/` folder (in client-onboarding SKILL)
- Archive client = copy `/02-clients/[name]/` to `/archive/2026-[name]/` (when engagement ends)
- Growth agent reads all `/02-clients/*/[file].md` files weekly

**Precedent for**: How to organize client data, what structure to use, how to archive

---

## Process & Workflow

### Decision 4: Weekly Growth Agent with 3-5 Propositions (2026-04-23)
**What**: Every Monday 09:00 AM, growth agent reads memory → generates 3-5 actionable improvement propositions.

**Why**:
- Catherine said: "I keep starting from zero" — need recurring context
- Weekly rhythm aligns with business week (action-oriented)
- 3-5 propositions is right volume (not overwhelming, not useless)
- Propositions are immediately actionable (Catherine starts same day)
- Automation: scheduled task, no manual trigger needed

**Impact**:
- Propositions rank by Impact × Urgency × Effort
- Growth agent reads: blockers, client patterns, process workflows, recent changes
- Propositions focus: unblock revenue, fix client friction, automate manual work
- Must include reasoning + specific steps (not vague ideas)

**Precedent for**: How often to review improvements, what to optimize, how to prioritize

---

### Decision 5: Notion Sunset by EOY 2026 (2026-04-23)
**What**: All Notion references removed from SKILLs by May 2026; Notion account can be closed EOY 2026.

**Why**:
- Cost: Notion is expensive (vs free Google Drive)
- Consolidation: Google Drive is already system of record
- Compliance: Notion has weaker EU data residency (GDrive is EU)
- Maintenance: Notion creates extra work (sync multiple systems)

**Status**: 6/8 SKILLs done (75%), 2 in progress (session-report, client-onboarding), target: 100% by 2026-05-07

**Impact**:
- All new clients onboarded to GDrive (no Notion)
- Existing client data must be migrated before closure
- Growth agent won't see Notion as data source (all reads from GDrive)

**Precedent for**: When to sunsetting systems, why consolidation matters, data migration strategy

---

### Decision 6: All Client Deliverables = HTML (not PDF, not Word, not Markdown) (2026-04-23)
**What**: Proposals, reports, guides sent to clients are HTML (styled, professional, interactive).

**Why**:
- One format works everywhere (browser, mobile, print)
- Can include: styling, colors, branding, logos, interactive elements
- Version control: HTML files in GDrive show diffs
- Accessibility: can be converted to PDF as needed
- Consistency: all deliverables look professional

**Impact**:
- proposal-generator outputs HTML
- Session reports (if client-facing) are HTML
- Guides/training materials are HTML
- Customer can read on any device (no software needed)

**Precedent for**: What format to use for client deliverables, style standards, brand consistency

---

## Team & Collaboration

### Decision 7: Michael is Primary Integration Developer (2026-04-23)
**What**: Michael owns API integrations (Brevo, Stripe, Airtable, etc.). Catherine owns SKILLs + client delivery.

**Note**: Michael's name is spelled "Michael" (not "Mickaël").

**Why**:
- Specialization: Michael knows APIs, Catherine knows process
- Clear ownership: blockers have clear owners (no confusion)
- Reduces context-switching: each person stays in their domain

**Impact**:
- Blockers assigned to Michael (FSY Circle Brevo sync) = Michael owns unblocking
- Growth agent flags blockers owned by Michael → suggest actions for him
- Catherine doesn't debug APIs (asks Michael), Michael doesn't write SKILLs (asks Catherine)

**Precedent for**: Team structure, ownership model, how to assign blockers

---

## Data & Privacy

### Decision 8: Confidential Data in Private GitHub Repo (2026-04-23)
**What**: Client passwords, API keys, financial data, RGPD-sensitive content NOT in public GitHub. Moved to private repo.

**Why**:
- RGPD compliance: personal data can't be in public repos
- Security: credentials can't be searchable on GitHub
- Reputational: accidental leaks damage trust

**Impact**:
- Public GitHub repo: SKILLs, templates, processes, public content only
- Private repo: client credentials, financial spreadsheets, sensitive notes
- `.env.local.example` in public (shows structure, no secrets)
- Backups: private data syncs to OneDrive + private GitHub

**Precedent for**: What data is safe to version control, where sensitive data lives, RGPD compliance

---

### Decision 9: Security Risk Assessment Mandatory Before Coding (2026-04-26)
**What**: Every feature/integration/SKILL must have a security risk assessment BEFORE development starts. No assessment = no coding.

**Why**:
- Risk-based approach: only mitigate risks that matter (don't waste effort on non-issues)
- Informed decisions: Catherine knows risks + mitigations + effort → decides what's worth it
- RGPD compliance: decision documented for audit trail (why we did/didn't mitigate X)
- Secure-by-Design foundation: integrates Michael's security directives into workflow

**Process**:
1. Feature requested → Run security-assessment SKILL
2. Identify risks (realistic scenarios, not generic concerns)
3. Propose mitigations (concrete technical actions + effort estimates)
4. Catherine decides: include all/some mitigations/accept risk
5. Code (with agreed scope)
6. Michael reviews post-dev (verifies mitigations implemented correctly)

**Impact**:
- No feature development starts without security review
- Catherine controls security investment level (not dogmatic, pragmatic)
- All decisions documented (audit trail for RGPD)
- Growth agent flags new features → suggests security assessment if missing
- Secure-by-Design becomes operational (not just theory)

**Precedent for**: Mandatory checks, security workflow integration, decision documentation, risk-based vs dogmatic security

---

### Decision 10: Spec-to-Code Factory is Mandatory Methodology for ALL Development (2026-04-26)
**What**: Every feature, app, or integration development must follow Sylvain Chabaud's spec-to-code-factory methodology (5 phases + 5 validation gates). This methodology was created as a production-ready system in the chatbot-fsy project and is now made system-wide mandatory.

**Why**:
- Prevents scope creep: specs are locked before code starts
- Maintains audit trail: every change tracked to a task ID (no anonymous commits)
- Ensures quality: 5 validation gates catch issues early
- Industry proven: Sylvain Chabaud's battle-tested methodology, refined over multiple projects
- Prevents improvisation: clear separation between planning, building, and validation
- Supports RGPD compliance: all decisions documented with gate markers
- Auto-remediation: 3x retry per phase before requiring human decision
- Greenfield/brownfield support: auto-detects V1 vs VN evolution to apply correct workflow

**The 5 Phases** (orchestrated by `factory/` master SKILL):
1. **BREAK (factory-intake)**: Requirements analysis + security assessment → Gate 1 ✅
2. **MODEL (factory-spec)**: Technical specifications + security implementation plan → Gate 2 ✅
3. **PLAN (factory-plan)**: Epics, user stories, tasks with IDs → Gate 3 ✅
4. **BUILD (factory-build)**: Code implementation with task-referenced commits → Gate 4 ✅
5. **DEBRIEF (factory-qa)**: QA validation + release preparation → Gate 5 ✅

**Core Principles**: 
- "No Spec, No Code" — specifications must be validated before coding starts
- "No Task, No Commit" — every git commit must reference a task ID
- Sequential strict — phases MUST run in order, never parallel
- Gate failures → auto-remediation (3x), then human decision (retry / correct / abandon)

**Workflow with Security-Assessment**:
1. User requests feature/app
2. Run security-assessment SKILL → identify risks + estimate mitigation effort → Catherine approves scope
3. Invoke `factory` master (orchestrator)
4. BREAK → Gate 1 ✅ → MODEL → Gate 2 ✅ → PLAN → Gate 3 ✅ → BUILD → Gate 4 ✅ → DEBRIEF → Gate 5 ✅
5. Deploy to production

**Quick-Track Option** (`factory-quick`):
- For simple features: skip planning details, move faster through phases
- Still requires all 5 gates to pass

**Resume Option** (`factory-resume`):
- If pipeline interrupted: resume from current phase, don't restart from beginning

**Impact**:
- ALL future development (features, apps, integrations) uses unified factory pipeline
- Development is standardized across all projects (no more project-specific workflows)
- Memory system learns from DEBRIEF (Phase 5) outputs via growth agent
- Tech-watch monitors spec-to-code-factory repo for methodology updates
- Brownfield support: can evolve existing projects through versioning (V2, V3, etc.)

**History**:
- Methodology created by Sylvain Chabaud (https://github.com/SylvainChabaud/spec-to-code-factory)
- Implemented as production system in chatbot-fsy project
- Discovered 2026-04-26 during cloud consolidation audit
- Migrated to system-wide availability in `/01-entreprise/skills/factory*/` (8 SKILLs total)

**Precedent for**: Development methodology, mandatory workflow, quality gates, scope management, audit trails, greenfield/brownfield project versioning

---

## Archived Decisions (> 7 days old, from earlier periods)

*None yet — decisions created 2026-04-23/26*

---

## How This Document Works

### When to add a decision
- After a major architectural choice (where to store X, how to organize Y)
- After choosing between two approaches (memory files vs database, GDrive vs Notion)
- After resolving a blocker that required a policy decision
- NOT for: routine work, task decisions, small tweaks

### When growth agent reads this
- When analyzing memory files: "Why is data in GDrive and not GitHub?" → read Decision 1
- When generating propositions: "Should we automate this?" → check existing process decisions
- When seeing conflicts: "Should we use Notion or GDrive?" → reference Decision 2 + 5

### When to archive
- After 7 days: if decision is working well, keep in this file but mark as "established"
- After 30 days: if decision causes issues, move to "reversed" section with new decision
- Decisions never expire (historical precedent is useful for future choices)

---

## Format for New Decisions

When adding a new decision, use this template:

```markdown
### Decision [N]: [Concise title] ([date])
**What**: [One sentence: what was decided]

**Why**: [Bullet points: reasoning]

**Impact**: [Bullet points: what changes because of this]

**Precedent for**: [What future decisions should reference this]
```

---

**Last updated**: 2026-04-26  
**Next review**: 2026-05-03 (if new major decisions made)  
**Total decisions on record**: 10 (all from April 2026)
