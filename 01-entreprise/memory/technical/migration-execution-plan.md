---
name: Migration Execution Plan — Spec-to-Code Factory Adoption
description: Step-by-step execution plan for migrating all 10 projects to spec-to-code-factory, respecting dependencies
type: technical
last_update: 2026-04-26
---

# Migration Execution Plan — Spec-to-Code Factory Adoption

**Mandate**: All projects must adopt spec-to-code-factory by 2026-06-30. This plan respects project dependencies and prioritizes revenue-critical projects.

---

## Dependency Map

### Cross-Project References Found
- **playbook-fsy** → references **portail-client-v2** as architectural precedent (ADR-0001)
- No npm/package dependencies between projects
- All projects are technically independent

### Conclusion
✅ Safe to migrate in priority order without breaking dependencies.

---

## Migration Sequence

### Phase 1: URGENT (Before May 1, 2026)

#### 1. **portail-client-v2** (Revenue-critical)
- **Priority**: CRITICAL
- **Reason**: Design blocker #2 (scope creep) — factory specs would prevent this
- **Current State**: 
  - Has CLAUDE.md mentioning factory methodology
  - Has `.claude/phases/` with 4 phase summaries (01-INTAKE, 02-SPEC, 03-PLAN, 04-QA)
  - MISSING: `.claude/skills/factory*/` directory (8 factory SKILLs)
  - MISSING: Full factory docs structure (brief, scope, acceptance, planning vN/, ADR, etc.)

- **Migration Steps**:
  1. Copy factory skills: `cp -r /01-entreprise/skills/factory* /03-developpement/portail-client-v2/.claude/skills/`
  2. Create factory structure: `mkdir -p docs/{brief,scope,acceptance,specs,planning,adr}`
  3. Document existing architecture as spec ADRs (migrate `phases/` notes → `docs/adr/ADR-*.md`)
  4. Create initial requirements.md from design blocker context (V3 scope creep issue)
  5. Run `/factory` to validate structure and establish baseline
  6. Invoke `/factory-intake` on next feature request

- **Effort**: 2-3 hours (setup + structure creation)
- **Blockers**: None identified
- **Owner**: Catherine (with design feedback for portail V3 scope)

---

#### 2. **auto-factures-fred** (Revenue-critical invoicing)
- **Priority**: MEDIUM (client-facing, but less urgent than portail-client-v2)
- **Reason**: Invoicing integration needs audit trail for financial compliance
- **Current State**: Standalone project, no factory structure detected
- **Estimated Complexity**: Low (single-purpose integration)

- **Migration Steps**:
  1. Copy factory skills
  2. Create factory structure
  3. Document current invoicing logic as spec ADRs
  4. Create requirements.md from existing integration specs
  5. Run `/factory` baseline validation

- **Effort**: 1-2 hours (simple project)
- **Blockers**: None identified
- **Owner**: Catherine (with Fred input for requirements validation)

---

### Phase 2: HIGH (By May 15, 2026)

#### 3. **questionnaire-onboarding** (Sales pipeline)
- **Priority**: MEDIUM
- **Reason**: Part of prospect intake flow; good factory-quick candidate
- **Estimated Complexity**: Low (simple form)

- **Migration Steps**:
  1. Copy factory skills
  2. Create factory structure
  3. Document current form logic
  4. Create requirements.md
  5. Use `/factory-quick` for future enhancements (BMAD Quick Flow)

- **Effort**: 1 hour (straightforward)
- **Owner**: Catherine

---

#### 4. **claude-configurator** (Internal tool)
- **Priority**: LOW (non-customer-facing)
- **Reason**: Good candidate for factory-quick; internal tool for Claude setup
- **Estimated Complexity**: Low (psychology axes configuration)

- **Migration Steps**:
  1. Copy factory skills
  2. Create factory structure
  3. Use `/factory-quick` as default workflow (no complex phases needed)

- **Effort**: 30 minutes (minimal setup)
- **Owner**: Catherine

---

### Phase 3: MEDIUM (By June 1, 2026)

#### 5. **playbook-fsy** (Compliance verification)
- **Priority**: MEDIUM
- **Reason**: Already using factory; verify active adoption and document it
- **Current State**: ✅ Using factory (8 SKILLs present)

- **Verification Steps**:
  1. Run `/gate-check [0-5]` to validate all gates
  2. Review `docs/factory/instrumentation.json` for active phase execution
  3. Verify recent commits follow `TASK-XXXX: description` format
  4. Check if DEBRIEF outputs are feeding growth agent
  5. Document findings in project-factory-status.md

- **Effort**: 1 hour (audit only, no changes expected)
- **Owner**: Catherine

---

#### 6. **site-csbusiness** (Optional)
- **Priority**: LOW (marketing website, low-tech)
- **Reason**: Optional review; only if actively developing
- **Decision Gate**: If no active development expected, skip factory adoption

- **Action**: Catherine decides based on roadmap (archive if static, migrate if developing)

---

### Phase 4: ARCHIVE (By June 15, 2026)

#### 7. **portail-client** (V1 Legacy)
- **Priority**: ARCHIVE
- **Reason**: Legacy; being replaced by portail-client-v2
- **Action**: 
  1. Verify all users/clients migrated to V2
  2. Move to `/archive/2026-portail-client-v1/`
  3. Add redirect notice in repo README

- **Effort**: 30 minutes
- **Owner**: Catherine

---

#### 8. **uscreen-comments-scraper** (Status unclear)
- **Priority**: ARCHIVE/DECISION
- **Reason**: Utility script; unclear if still maintained
- **Action**:
  1. Determine: Still in active use?
  2. If YES → Migrate to factory, add to Phase 2
  3. If NO → Move to `/archive/` folder

- **Effort**: 15 minutes (decision) + 1 hour (migration if needed)
- **Owner**: Catherine

---

## Execution Checklist

### Before Each Migration
- [ ] Security Risk Assessment SKILL run (new features required only)
- [ ] Identify key stakeholders (client, team members)
- [ ] Prepare initial requirements.md
- [ ] Review existing architecture/code for ADR candidates

### During Each Migration
- [ ] Copy factory skills to `.claude/skills/factory*/`
- [ ] Create factory documentation structure
- [ ] Run `/factory` to validate baseline
- [ ] Document any project-specific ADRs
- [ ] Update CLAUDE.md with factory workflow confirmation

### After Each Migration
- [ ] Gate 0 (Intake) validation passing
- [ ] Gate 1 (Structure) validation passing
- [ ] Commit with message: `TASK-001: Initialize spec-to-code-factory structure`
- [ ] Update project-factory-status.md (move project from ❌ to ✅)
- [ ] Update 2026-04.md changelog with migration date

---

## Timeline Summary

```
Week of 2026-04-28    Phase 1: portail-client-v2, auto-factures-fred
Week of 2026-05-05    Phase 2: questionnaire-onboarding, claude-configurator
Week of 2026-06-01    Phase 3: playbook-fsy compliance check, site-csbusiness decision
Week of 2026-06-15    Phase 4: Archive portail-client V1, clarify uscreen-comments-scraper
```

**Target**: 100% compliance by 2026-06-30

---

## Compliance Metrics

### Baseline (2026-04-26)
- Projects with factory: 2/10 (20%)
- Projects migrated: 0/8 (0%)

### Target (2026-05-31)
- Projects with factory: 6/10 (60%)
- Projects migrated: 4/8 (50%)

### Final (2026-06-30)
- Projects with factory: 8/10 (80%) + 2 archived = 100% of active projects
- All active projects follow spec-to-code-factory mandatory

---

## How to Migrate a Project (Template)

### Step 1: Copy Factory Skills
```bash
cp -r /01-entreprise/skills/factory* \
      /03-developpement/[PROJECT]/.claude/skills/
```

### Step 2: Create Documentation Structure
```bash
mkdir -p /03-developpement/[PROJECT]/docs/{brief,scope,acceptance,specs,planning,adr,factory}
```

### Step 3: Initialize Factory Files
```bash
# Create initial brief
touch docs/brief/brief-v1.md

# Create scope
touch docs/scope/scope-v1.md

# Create acceptance criteria
touch docs/acceptance/acceptance-v1.md

# Create requirements
touch input/requirements.md
```

### Step 4: Populate Requirements
Edit `input/requirements.md` with:
- Overview (1-2 paragraphs)
- Requirements (2-3 key requirements)
- Data types (if applicable)
- Constraints
- Blockers (if any)
- Assumptions
- Success criteria

### Step 5: Validate Structure
```bash
cd /03-developpement/[PROJECT]
node .claude/skills/factory/factory.js validate
```

### Step 6: Run Factory Baseline
```bash
# Invoke factory to generate baseline documentation
/factory-intake

# Then proceed through phases as needed
/factory-spec
/factory-plan
/factory-build
/factory-qa
```

---

## Risk Mitigation

### Risk 1: Breaking existing workflows
**Mitigation**: All migrations are additive (add factory structure without removing existing code). Existing CLAUDE.md files updated, not replaced.

### Risk 2: Team unfamiliar with factory
**Mitigation**: Start with simplest projects (factory-quick for configurator, questionnaire). Learn from portail-client-v2 (URGENT) as first "full" migration.

### Risk 3: Dependencies between projects
**Mitigation**: Dependency audit complete. All projects independent (no breaking changes). playbook-fsy only references portail-client-v2 architecturally (documentation, not code).

### Risk 4: Portal V3 design blocker
**Mitigation**: Factory specs-locking mechanism specifically addresses this. First feature request after factory setup should use factory to prevent recurrence.

---

## Related Documents

- [project-factory-status.md](project-factory-status.md) — Compliance tracking per project
- [DECISIONS.md](../versioning/DECISIONS.md) — Decision 10: Spec-to-Code Factory is Mandatory
- [2026-04.md](../versioning/2026-04.md) — Changelog with factory discovery and audit
- [MEMORY.md](../MEMORY.md) — Mandatory checks section lists factory requirements
- [`/01-entreprise/skills/factory/SKILL.md`](../../skills/factory/SKILL.md) — Master orchestrator

---

**Created**: 2026-04-26  
**Last Updated**: 2026-04-26  
**Next Review**: 2026-04-28 (phase 1 start date)  
**Target Completion**: 2026-06-30 (100% compliance)
