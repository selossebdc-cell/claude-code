# PLAN Phase — Index & Timeline

## Phase Status
✅ **PLAN Phase Ready**

---

## Documents Created

### Planning Artifacts
- **epics.md** — 8 strategic epics (EPIC-1 through EPIC-8), effort estimate, dependencies, sprint allocation
- **PLAN-INDEX.md** (this file) — Overview + timeline

### Ready for BUILD Phase
- Detailed user stories (by epic)
- Task breakdowns with estimates (coming next)
- Code implementation guidance (in BUILD phase)

---

## Sprint Timeline

### Sprint 1 (Weeks 1-2): Foundation
**Epics**: EPIC-1, EPIC-2, EPIC-4

| Epic | Effort | Status |
|------|--------|--------|
| EPIC-1: Diagnostic Prompt Refactor | 4 days | Ready to start |
| EPIC-2: Pattern Detection Engine | 3 days | Blocked on EPIC-1 |
| EPIC-4: Metadata Enrichment System | 3 days | Parallel with EPIC-1/2 |

**Output**: New diagnostic prompt, metadata schema, pattern detection logic

---

### Sprint 2 (Week 3): Intelligence
**Epics**: EPIC-3, EPIC-5, EPIC-6

| Epic | Effort | Status |
|------|--------|--------|
| EPIC-3: Claude Opportunities | 3.5 days | Blocked on EPIC-2 |
| EPIC-5: Strategic Synthesis | 3.5 days | Blocked on EPIC-1/2/3 |
| EPIC-6: Agent & Routine Config | 3.5 days | Ready to start |

**Output**: Opportunities logic, synthesis generator, agent selection logic

---

### Sprint 3 (Week 4): Integration
**Epics**: EPIC-7

| Epic | Effort | Status |
|------|--------|--------|
| EPIC-7: Generate-Config v20+ Integration | 4.5 days | Blocked on EPIC-1..6 |

**Output**: Updated generate-config Edge Function

---

### Sprint 4 (Weeks 5-6): Validation
**Epics**: EPIC-8

| Epic | Effort | Status |
|------|--------|--------|
| EPIC-8: E2E Testing & Validation | 5 days | Blocked on EPIC-7 |

**Output**: Test suite, comparison report vs Fred, production readiness

---

## Estimated Timeline

| Phase | Duration | End Date |
|-------|----------|----------|
| PLAN phase (current) | ~1 day | 2026-04-27 |
| Sprint 1 (EPIC-1, 2, 4) | 2 weeks | 2026-05-11 |
| Sprint 2 (EPIC-3, 5, 6) | 1 week | 2026-05-18 |
| Sprint 3 (EPIC-7) | 1 week | 2026-05-25 |
| Sprint 4 (EPIC-8) | 2 weeks | 2026-06-08 |
| **Total** | **~6 weeks** | **2026-06-08** |

---

## Key Dependencies

```
EPIC-1 (Prompt Refactor)
  ↓
EPIC-2 (Pattern Detection)
  ├─→ EPIC-3 (Opportunities)
  │    ├─→ EPIC-5 (Synthesis)
  │    └─→ EPIC-6 (Agents)
  │
  └─→ EPIC-4 (Metadata)
  
EPIC-6 (Agents) ──→ EPIC-7 (Gen-Config v20+) ──→ EPIC-8 (Testing)
```

---

## Next Steps (BUILD Phase)

1. **Create detailed user stories** (per epic)
2. **Break down into tasks** (with estimates in days)
3. **Assign tasks** (to developer)
4. **Create pull requests** (with task ID references)
5. **Merge to production** (after DEBRIEF phase)

---

## Notes

- All epics are P0 (critical)
- No blockers identified (all dependencies available)
- Single developer can execute serially or parallel where dependencies allow
- Compression + chunking from v18-19 stay in place (no regression)

---

**Created**: 2026-04-27 (PLAN phase)  
**Status**: Ready for BUILD phase  
**Next Phase**: factory-build (Implementation)
