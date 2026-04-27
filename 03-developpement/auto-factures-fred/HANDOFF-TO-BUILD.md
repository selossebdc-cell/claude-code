# Handoff to BUILD Phase

**From**: PLAN Phase (2026-04-27)  
**To**: BUILD Phase (2026-04-28+)  
**Status**: Ready ✓

---

## Quick Start for Build Orchestrator

You are receiving a complete planning package from the PLAN phase. Here's what you need to do:

### 1. Review the Planning Artifacts (15 minutes)

Start with this order:

1. **docs/planning/v1/INDEX.md** ← Start here for overview
2. **PLAN-PHASE-SUMMARY.md** ← High-level summary
3. **docs/planning/v1/epics.md** ← Full epic breakdown

### 2. Assign TASK-0001 (Today)

**TASK-0001**: Project Configuration & Setup

- **Path**: docs/planning/v1/tasks/TASK-0001-project-config.md
- **Duration**: 2 days
- **Complexity**: Foundation (no dependencies)
- **Prerequisites**: Node.js 20+, pnpm
- **Who**: Assign to most senior developer (this is the foundation)
- **Status**: Ready to implement immediately

**Developer instructions**:
1. Read the entire TASK-0001 document
2. Follow Step 1-11 exactly
3. Verify the Definition of Done (all checkboxes)
4. Run the verification checklist at the end
5. Report when complete

### 3. Queue TASK-0002 (While TASK-0001 is in progress)

**TASK-0002**: Database Configuration & Migrations

- **Path**: docs/planning/v1/tasks/TASK-0002-database-config.md
- **Duration**: 1-2 days
- **Complexity**: Database setup (depends on TASK-0001)
- **Prerequisites**: PostgreSQL 14+, TASK-0001 complete
- **Who**: Can assign to same developer or second one
- **Status**: Ready to queue

**Implementation order**: Start TASK-0002 once TASK-0001 is 80% complete

### 4. Plan Sprint 1 (By 2026-04-28)

Epic 1 is complete. For Sprint 1 (Weeks 1-2):

**Immediate tasks** (Weeks 1-2):
- TASK-0001: Project config (2 days)
- TASK-0002: Database setup (1-2 days)
- Epic 2 domain entities (begin after DB setup)

**Remaining Sprint 1**: Domain modeling tasks

See docs/planning/v1/INDEX.md (Sprint Planning section) for details.

---

## Planning Package Contents

### Core Planning Documents

| Document | Purpose | Location |
|----------|---------|----------|
| **epics.md** | 8 strategic epics with scope/priority/effort | docs/planning/v1/epics.md |
| **User Stories (Epic 1)** | Detailed requirements for 2 stories | docs/planning/v1/us/ |
| **Tasks (Epic 1)** | Fully specified tasks with code examples | docs/planning/v1/tasks/ |
| **INDEX.md** | Planning overview and cross-references | docs/planning/v1/INDEX.md |

### Phase Reports

| Document | Purpose | Location |
|----------|---------|----------|
| **PLAN-PHASE-SUMMARY.md** | High-level phase summary | This directory |
| **PLAN-PHASE-COMPLETION.txt** | Detailed completion report | This directory |
| **PLAN-PHASE-LOG.txt** | Execution log | This directory |

### Model Phase Reference

These are available for context (don't re-read, just reference):

- docs/specs/system.md ← System architecture
- docs/specs/domain.md ← Entity models
- docs/specs/api.md ← REST endpoints
- docs/specs/stack-reference.md ← Exact versions
- docs/adr/ ← Technology decisions

---

## Important Files for BUILD Phase

### Configuration & Rules

These define how to implement tasks:

- **.claude/rules/architecture.md** ← Coding standards
- **.claude/rules/testing.md** ← Test requirements
- **.env.example** ← Environment variables template

### Task Template Reference

Each task follows this structure:

```
# TASK-XXXX: [Title]

## Overview
[What this task does]

## Context
[Why this is needed, what specs it derives from]

## Prerequisites
[What must be done first]

## Requirements
[R1, R2, R3... detailed specifications]

## Implementation Steps
[Step 1, 2, 3... copy-paste ready code]

## Definition of Done
[Checklist of completion criteria]

## Testing
[Manual and automated tests]

## References
[Links to specs, ADRs, rules]
```

---

## Dependency Graph

```
TASK-0001 (Project Config)
    ↓ (depends on)
TASK-0002 (Database Setup)
    ↓ (depends on)
Epic 2 Domain Tasks (TASK-0003+)
    ↓
Epic 3 Generation Tasks
    ↓
Epic 4 API Tasks
    ↓
Epic 5 Auth Tasks (can parallel with Epic 3)
    ↓
Epic 6 Email Tasks
    ↓
Epic 7 Monitoring Tasks (parallel)
    ↓
Epic 8 Testing Tasks (ongoing throughout)
```

---

## Build Phase Workflow

### Daily Standup Checklist

1. **What tasks are in progress?**
   - Check docs/planning/v1/tasks/ for details
   - Verify DoD criteria

2. **Are tasks blocked?**
   - Review TASK-XXXX "Prerequisites" section
   - Check "References" for blocked dependencies

3. **Did task complete?**
   - Verify all DoD checkboxes
   - Run testing procedures
   - Check code examples were properly applied

4. **Ready for next task?**
   - Queue next task from dependency graph
   - Ensure prerequisites met

### Sprint Retrospective

After each sprint:

1. **Actual vs. Estimated Effort**
   - Compare actual duration to "Effort" field in task
   - Track velocity for sprint planning

2. **Quality Metrics**
   - Did all DoD criteria pass?
   - Were all tests run?
   - Were code examples helpful?

3. **Blockers & Improvements**
   - Any tasks harder than expected?
   - Missing information?
   - Suggested improvements to planning?

---

## Quick Reference: Reading a Task

### Essential Sections

Every TASK-XXXX file has these sections (in order):

1. **Header** (top of file)
   - Epic, User Story, Status, Priority, Effort
   - Dependencies (what must be done first)

2. **Overview** (one paragraph)
   - What this task does
   - Start here for quick understanding

3. **Context** (background)
   - Why this is needed
   - What specs it implements
   - How it connects to architecture

4. **Requirements** (R1, R2, R3...)
   - Detailed specifications
   - What code to write
   - Exact configurations needed

5. **Implementation Steps** (numbered)
   - Exact steps to follow
   - Code examples (copy-paste ready)
   - File paths provided

6. **Definition of Done** (checklist)
   - All items must be ✓ when task is complete
   - Use this to verify completion

7. **Testing** (how to verify)
   - Manual tests
   - Automated tests
   - Expected output

8. **References** (links)
   - Specs: docs/specs/xxxx.md
   - ADRs: docs/adr/ADR-XXXX.md
   - Rules: .claude/rules/xxxx.md

---

## FAQ for Developers

**Q: Can I skip steps in a TASK?**  
A: No. Each step builds on previous ones. Follow them in order.

**Q: Do I need to read the other tasks?**  
A: No. Each task is 100% self-contained. Read only the task assigned to you.

**Q: What if I encounter an error?**  
A: Check the "Testing" section for troubleshooting. If still blocked, escalate to team lead.

**Q: Can I modify the code examples?**  
A: Yes, use them as a starting point, but stick to the patterns and conventions defined in .claude/rules/

**Q: What if the effort estimate is wrong?**  
A: Log it. In retrospectives, we adjust estimates for future tasks.

**Q: Can I parallelize tasks?**  
A: Only if dependencies are met. Check the "Prerequisites" section of each task.

---

## Success Criteria for Sprint 1

Sprint 1 is successful when:

- [x] TASK-0001 complete (project setup)
- [x] TASK-0002 complete (database)
- [x] First domain entities implemented
- [x] All tests passing
- [x] Project builds without errors
- [x] Health check endpoint working

---

## Timeline

| Date | Milestone | Status |
|------|-----------|--------|
| 2026-04-27 | PLAN phase complete | ✓ Done |
| 2026-04-28 | Sprint 1 starts | Next |
| 2026-05-02 | TASK-0001 & TASK-0002 due | Target |
| 2026-05-11 | Sprint 1 complete | Target |
| 2026-05-12 | Sprint 2 starts | Planned |
| 2026-06-30 | V1 release | Target |

---

## Contact

**Planning Orchestrator**: Factory Plan Skill  
**Phase Completed**: 2026-04-27 01:00 UTC  

Questions about planning?
→ Review docs/planning/v1/INDEX.md  
→ Check PLAN-PHASE-SUMMARY.md  

Technical issues?
→ Check .claude/rules/architecture.md  
→ Reference docs/specs/

---

## Next Steps

1. **Now**: Review PLAN-PHASE-SUMMARY.md
2. **Today**: Assign TASK-0001 to developer
3. **Tomorrow**: Begin Sprint 1 kick-off
4. **By 2026-05-02**: TASK-0001 & TASK-0002 complete

---

**Prepared by**: Factory Plan Skill  
**Ready for**: factory-build (BUILD Phase)  
**Date**: 2026-04-27  
**Status**: ✓ READY

---

*Welcome to the BUILD phase! The hard work is about to begin.*
