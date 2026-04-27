---
name: Project Factory Status — Spec-to-Code Factory Adoption
description: Track which projects use spec-to-code-factory methodology. Mandatory for all new development. See migration-execution-plan.md for step-by-step sequence.
type: technical
last_update: 2026-04-26
---

# Project Factory Status — Spec-to-Code Factory Adoption

**Mandate**: As of 2026-04-26, ALL development projects MUST use spec-to-code-factory methodology (5 phases + 5 validation gates).

---

## Dependency Map

### Cross-Project References
- **playbook-fsy** → references **portail-client-v2** as architectural precedent (ADR-0001: "same approach")
- No npm/package dependencies found between projects
- All projects technically independent — safe to migrate in priority order

### Audit Results (2026-04-26)
- Audited all 10 projects for CLAUDE.md, package.json, cross-references
- No breaking dependencies identified
- Migration order determined: portail-client-v2 → auto-factures-fred → questionnaire-onboarding → claude-configurator

---

## Summary

| Status | Count | Projects |
|--------|-------|----------|
| ✅ **Using factory** | 2 | chatbot-fsy, playbook-fsy |
| ❌ **NOT using factory** | 8 | auto-factures-fred, claude-configurator, portail-client, portail-client-v2, questionnaire-onboarding, site-csbusiness, uscreen-comments-scraper |
| 🔄 **In progress** | 0 | — |

**Adoption Rate**: 2/10 (20%) ❌ **Below target. Action needed.**

---

## Projects WITH Factory (✅ Compliant)

### 1. **chatbot-fsy**
- **Status**: ✅ ACTIVE
- **Factory Skills**: 8 (factory, factory-intake, factory-spec, factory-plan, factory-build, factory-qa, factory-quick, factory-resume)
- **Location**: `/03-developpement/chatbot-fsy/.claude/skills/factory*/`
- **Migrated to Google Drive**: ✅ Yes (2026-04-26)
- **Phase**: In production, actively using factory pipeline
- **Last Updated**: 2026-04-26 (migrated from backup)

### 2. **playbook-fsy**
- **Status**: ✅ ACTIVE
- **Factory Skills**: 8 (identical to chatbot-fsy)
- **Location**: `/03-developpement/playbook-fsy/.claude/skills/factory*/`
- **Note**: Copy of chatbot-fsy factory (same implementation)
- **Phase**: In production
- **Last Updated**: 2026-04-26 (verified identical to chatbot-fsy)

---

## Projects WITHOUT Factory (❌ Non-Compliant)

### 1. **auto-factures-fred**
- **Status**: ❌ NO FACTORY
- **Type**: Integration (Fred's invoicing automation)
- **Action Required**: Migrate to factory workflow
- **Priority**: MEDIUM (client-facing, revenue-critical)
- **Target**: Before next development iteration
- **Notes**: Should follow factory for any new features

### 2. **claude-configurator**
- **Status**: ❌ NO FACTORY
- **Type**: Internal tool (Claude setup/psychology axes configuration)
- **Action Required**: Integrate factory workflow (can use factory-quick for simple features)
- **Priority**: LOW (internal tool, non-customer-facing)
- **Target**: Next maintenance cycle
- **Notes**: Simple app, good candidate for factory-quick

### 3. **portail-client** (V1 - Legacy)
- **Status**: ❌ NO FACTORY
- **Type**: Legacy API (being replaced by V2)
- **Action Required**: NONE (legacy, in sunset mode)
- **Priority**: ARCHIVE (deprecated, maintenance mode only)
- **Notes**: Do not add new features. Archive after V2 migration complete.

### 4. **portail-client-v2**
- **Status**: ❌ NO FACTORY (but PARTIAL: has CLAUDE.md mentioning factory)
- **Type**: Main client portal (in active development)
- **Action Required**: URGENT — Complete factory migration (setup + skills)
- **Priority**: CRITICAL (revenue-critical, active development)
- **Target**: Week of 2026-04-28 (Phase 1 of migration plan)
- **Current Blockers**: "Portail V3 Design scope creep" (blocker #2) — factory specs-locking will prevent recurrence
- **Current State**: 
  - ✅ Has CLAUDE.md mentioning "Méthode obligatoire: Spec-to-Code Factory"
  - ✅ Has `.claude/phases/` with phase summaries (01-INTAKE, 02-SPEC, 03-PLAN, 04-QA)
  - ❌ MISSING: `.claude/skills/factory*/` (8 SKILLs required)
  - ❌ MISSING: Full factory structure (brief/, scope/, acceptance/, planning/vN/, adr/, etc.)
- **Migration Path**: Copy factory skills + create factory docs structure + run `/factory` baseline
- **Notes**: Partial setup suggests previous alignment attempt. Complete setup will establish proper spec-locking.

### 5. **questionnaire-onboarding**
- **Status**: ❌ NO FACTORY
- **Type**: Prospect intake form
- **Action Required**: Integrate factory workflow
- **Priority**: MEDIUM (part of sales pipeline)
- **Target**: Before next prospect cycle
- **Notes**: Simple form, good candidate for factory-quick

### 6. **site-csbusiness**
- **Status**: ❌ NO FACTORY
- **Type**: Marketing website
- **Action Required**: Optional (low-tech, mostly static content)
- **Priority**: LOW (not development-intensive)
- **Notes**: Can use simplified workflow if changes needed

### 7. **uscreen-comments-scraper**
- **Status**: ❌ NO FACTORY
- **Type**: Utility script (UScreen integration)
- **Action Required**: Integrate factory if maintained as ongoing project
- **Priority**: LOW (utility, maintenance)
- **Target**: If extending functionality
- **Notes**: Verify if still in active use; archive if deprecated

---

## Adoption Plan

**See detailed step-by-step migration plan**: [`migration-execution-plan.md`](migration-execution-plan.md)

### Timeline at a Glance

| Phase | Timeline | Projects | Status |
|-------|----------|----------|--------|
| **1. URGENT** | Week of 2026-04-28 | portail-client-v2, auto-factures-fred | 🔴 PENDING |
| **2. HIGH** | Week of 2026-05-05 | questionnaire-onboarding, claude-configurator | 🔴 PENDING |
| **3. MEDIUM** | Week of 2026-06-01 | playbook-fsy compliance audit, site-csbusiness decision | 🔴 PENDING |
| **4. ARCHIVE** | Week of 2026-06-15 | portail-client (V1), uscreen-comments-scraper | 🔴 PENDING |

### Phase 1: URGENT (Week of 2026-04-28)

**1. portail-client-v2** (3 hours)
- Rationale: Revenue-critical, active development, design blocker #2 shows specs need
- Action: Copy factory skills + create factory structure + run `/factory` baseline
- Effort: 2-3 hours

**2. auto-factures-fred** (2 hours)
- Rationale: Client-facing invoicing, needs audit trail for compliance
- Action: Copy factory skills + create structure + validate
- Effort: 1-2 hours

### Phase 2: HIGH (Week of 2026-05-05)

**3. questionnaire-onboarding** (1 hour)
- Rationale: Part of sales pipeline, good factory-quick candidate
- Effort: ~1 hour

**4. claude-configurator** (0.5 hour)
- Rationale: Internal tool, minimal setup required
- Effort: ~30 minutes

### Phase 3: MEDIUM (Week of 2026-06-01)

**5. playbook-fsy** (1 hour audit)
- Action: Verify active factory usage, validate all gates, check instrumentation
- Effort: ~1 hour (audit only)

**6. site-csbusiness** (decision gate)
- Action: Determine if actively developing → migrate, or archive
- Effort: 15 minutes decision

### Phase 4: ARCHIVE (Week of 2026-06-15)

**7. portail-client** (V1)
- Action: Move to `/archive/2026-portail-client-v1/`
- Effort: ~30 minutes

**8. uscreen-comments-scraper**
- Action: Determine if still in use
- Effort: 15 min decision + 1 hour migration if YES

---

## How to Migrate a Project to Factory

### Step 1: Copy Factory Skills
```bash
cp -r /01-entreprise/skills/factory* /03-developpement/[project]/.claude/skills/
```

### Step 2: Create Initial Files
```bash
# Create requirements structure
mkdir -p docs/brief docs/scope docs/acceptance docs/specs docs/planning docs/adr

# Create input file
touch input/requirements.md
```

### Step 3: Prepare Requirements
- Write `/requirements.md` following spec-to-code-factory format
- Include: overview, requirements, data types, constraints, blockers, assumptions

### Step 4: Invoke Master Orchestrator
```
/factory
```

The factory will:
- Auto-detect greenfield (V1) vs brownfield (VN)
- Run all 5 phases sequentially
- Apply validation gates
- Auto-remediate failures (3x per phase)
- Produce release artifacts

---

## Enforcement

**Starting 2026-04-26**:
- ✅ **All NEW projects** must use factory from day 1
- ✅ **All NEW features** in existing projects must follow factory
- ✅ **security-assessment SKILL** must run BEFORE factory phase 1 (BREAK)
- ❌ **No coding** without validated specs from factory phase 2 (MODEL)
- ❌ **No commits** without task ID references from factory phase 3 (PLAN)

**Growth Agent Role**:
- Every Monday: Check project status
- Flag projects not following factory
- Propose migration for high-priority projects
- Alert on phase failures

---

## Metrics & Health Checks

### Compliance Timeline
- **Week of 2026-04-28**: portail-client-v2 migration starts
- **Week of 2026-05-05**: 50% of projects using factory (target)
- **June 1, 2026**: 80% compliance target
- **June 30, 2026**: 100% compliance (all active projects)

### Success Indicators
- ✅ No scope creep (specs locked before code)
- ✅ Complete audit trail (every commit has task ID)
- ✅ Validation gates pass (no GATE_FAIL recurring)
- ✅ Phase 4 DEBRIEF outputs inform growth agent propositions

---

## Related Documents

- [migration-execution-plan.md](migration-execution-plan.md) — **Detailed step-by-step migration sequence** (see this for implementation)
- [MEMORY.md](../MEMORY.md) — Mandatory checks section lists factory as required
- [DECISIONS.md](DECISIONS.md) — Decision 10 documents factory as mandatory
- [2026-04.md](2026-04.md) — Changelog entry for factory discovery and audit
- [`/01-entreprise/skills/factory/`](../../skills/factory/SKILL.md) — Master orchestrator SKILL

---

**Created**: 2026-04-26  
**Last Updated**: 2026-04-26  
**Next Review**: 2026-05-03 (progress check on portail-client-v2 migration)  
**Target Adoption**: 100% by 2026-06-30
