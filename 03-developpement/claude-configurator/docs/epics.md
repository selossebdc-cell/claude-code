# Epics — Claude Configurator v2: Diagnostic Intelligent

## Overview
Décomposition du MODEL phase en 8 épics pour la phase ACT (Planning + Build).

---

## EPIC-1: Diagnostic Prompt Refactor
**Priority**: P0 (Critical)  
**Scope**: Refactor du système prompt diagnostique pour Sonnet 4.6

### Description
Créer le nouveau prompt système qui implémente l'exploration intelligente et adaptative (vs questionnaire linéaire). Cela inclut:
- System prompt architecture (5 parts: role, mental model, metadata instructions, adaptive logic, synthesis)
- Integration du modèle Sonnet 4.6
- Message compression fallback
- Pattern detection directives

### Features Covered
- F-001 (Adaptive Question Generation)
- F-002 (Pattern Detection)
- F-003 (Claude Opportunities)
- F-006 (Guide Client)

### Acceptance Criteria
- [ ] New system prompt written (based on DIAGNOSTIC-SPEC.md)
- [ ] Tested with 5+ diverse test cases
- [ ] Questions adapt based on responses (3+ examples)
- [ ] No generic/robotic language
- [ ] Message compression active (fallback)

### Effort Estimate
- **Design**: 1 day
- **Prompt iteration**: 2-3 days (testing + refinement)
- **Documentation**: 0.5 day
- **Total**: 3.5-4.5 days

### Dependencies
- AGENTS-ROUTINES-SPEC.md (finalized)
- DIAGNOSTIC-SPEC.md (finalized)

---

## EPIC-2: Pattern Detection Engine
**Priority**: P0 (Critical)  
**Scope**: Implement pattern detection logic in diagnostic agent

### Description
Implémente la détection de patterns en temps réel:
- Recurring blocages
- Work style traits
- Strength signals
- Risk indicators

Chaque pattern doit être:
- Spécifique au client (pas générique)
- Evidence-based (avec quotes/références)
- Actionnable (peut générer une opportunity)

### Features Covered
- F-002 (Pattern Detection in Real-Time)
- F-004 (Enriched Metadata)

### Acceptance Criteria
- [ ] Pattern detection logic implemented in prompt
- [ ] Metadata: patterns_detected[] populated (≥2 per diagnostic)
- [ ] Each pattern has evidence + consequence
- [ ] Patterns inform subsequent questions (adaptive loop)
- [ ] Test: 5+ diagnostics, ≥2 patterns each

### Effort Estimate
- **Logic design**: 1 day
- **Prompt integration**: 1 day
- **Testing**: 1 day
- **Total**: 3 days

### Dependencies
- EPIC-1 (Diagnostic Prompt)

---

## EPIC-3: Claude Opportunities Identification
**Priority**: P0 (Critical)  
**Scope**: Detect where Claude truly transforms client's daily work

### Description
Implémente la détection d'opportunités (où Claude devient vraiment game-changer):
- Linked to pain_points (why it matters)
- Linked to patterns (what context enables it)
- Justifie pourquoi c'est une opportunity (pas generic)
- Influence la config generation downstream

### Features Covered
- F-003 (Claude Opportunities Identification)
- F-004 (Enriched Metadata)

### Acceptance Criteria
- [ ] Metadata: claude_opportunities[] populated (≥3 per diagnostic)
- [ ] Each opportunity has: description, linked_pain_point, why_it_matters
- [ ] Opportunities are passed to generate-config
- [ ] Test: 5+ diagnostics, ≥3 opportunities each, review for quality

### Effort Estimate
- **Logic design**: 1 day
- **Prompt integration**: 1.5 days
- **Testing**: 1 day
- **Total**: 3.5 days

### Dependencies
- EPIC-2 (Pattern Detection)

---

## EPIC-4: Metadata Enrichment System
**Priority**: P0 (Critical)  
**Scope**: Implement enriched metadata schema and persistence

### Description
Implémente le système de métadonnées enrichies:
- JSON schema (pain_points, patterns_detected, work_style_traits, claude_opportunities, assumptions_validated, coverage_tracking)
- Real-time updates during diagnostic
- Persistence in Supabase (diagnostics table)
- Pass to generate-config v20+

### Features Covered
- F-004 (Enriched Metadata Schema)

### Acceptance Criteria
- [ ] Metadata schema JSON valid + size < 2KB
- [ ] Auto-updated after each response
- [ ] Stored in Supabase.diagnostics.metadata
- [ ] Passed to generate-config (check logs)
- [ ] Frontend displays metadata (optional: debug view)
- [ ] Test: 5+ diagnostics, metadata extracted successfully

### Effort Estimate
- **Schema design**: 0.5 day
- **Database changes**: 0.5 day
- **Chat Edge Function update**: 1 day
- **Testing**: 1 day
- **Total**: 3 days

### Dependencies
- EPIC-1, EPIC-2, EPIC-3 (all populate metadata)

---

## EPIC-5: Strategic Synthesis Generator
**Priority**: P0 (Critical)  
**Scope**: Generate strategic synthesis (not just summary) at end of diagnostic

### Description
Implémente la génération de synthèse stratégique:
- "Ce que j'ai compris de vous" (blocages + forces)
- "Où Claude devient vraiment game-changer" (linked to opportunities)
- "Votre config sera centrée sur" (preview de config future)
- Justifie le 149€ pricing
- Comparable to Fred's config density

### Features Covered
- F-005 (Strategic Synthesis Generator)

### Acceptance Criteria
- [ ] Synthesis generated when diagnostic concludes
- [ ] Not a summary (different structure)
- [ ] Includes 3 sections (what understood, where transforms, config focus)
- [ ] Reads naturally (narrative logic)
- [ ] References Fred's config as analogy (where applicable)
- [ ] Reviewed by Catherine: justifies 149€?
- [ ] Test: 5+ diagnostics, synthesis quality reviewed

### Effort Estimate
- **Prompt engineering**: 1.5 days
- **Template definition**: 0.5 day
- **Testing + iteration**: 1.5 days
- **Total**: 3.5 days

### Dependencies
- EPIC-1, EPIC-2, EPIC-3 (synthesis uses all metadata)

---

## EPIC-6: Agent & Routine Configuration Logic
**Priority**: P0 (Critical)  
**Scope**: Implement agent selection + routine suggestion logic

### Description
Implémente la logique pour proposer agents et routines:
- 6 agents obligatoires (Miroir, Garde-Fou, Admin, Stratégie, Planif, Amélioration Continue)
- 2 agents contextuels (Coach, Ingénieur) avec triggers
- Ma Mémoire project (toujours)
- Custom Instructions (toujours, spécifique)
- Au min 1 routine, proposer les 3 (Daily, Weekly, Monthly)

### Features Covered
- AGENTS-ROUTINES-SPEC.md (full implementation)

### Acceptance Criteria
- [ ] 6 mandatory agents in every config
- [ ] Coach agent proposed if pain_point("progress tracking")
- [ ] Ingénieur agent proposed if pain_point("compliance") OR complexity
- [ ] Ma Mémoire project always created + populated
- [ ] Custom Instructions always generated (2000+ chars)
- [ ] At least 1 routine scheduled (suggest all 3)
- [ ] Test: 5+ configs, validate mandatory agents present

### Effort Estimate
- **Logic design**: 1 day
- **Config template updates**: 1.5 days
- **Testing**: 1 day
- **Total**: 3.5 days

### Dependencies
- AGENTS-ROUTINES-SPEC.md (finalized)
- EPIC-3 (opportunities trigger agent selection)

---

## EPIC-7: Generate-Config v20+ Integration
**Priority**: P0 (Critical)  
**Scope**: Update generate-config to consume enriched metadata

### Description
Upgrade generate-config Edge Function:
- Accept enriched metadata from diagnostic
- Use metadata to inform agent instructions
- Use opportunities to prioritize/deepen agent roles
- Pass Custom Instructions correctly
- Validate agents + routines configuration

### Features Covered
- All (downstream consumption of diagnostic output)

### Acceptance Criteria
- [ ] generate-config v20+ accepts metadata parameter
- [ ] Metadata consumed in generation logic
- [ ] Config reflects client-specific opportunities
- [ ] 6 mandatory agents always generated
- [ ] Conditional agents (Coach, Ingénieur) generated when appropriate
- [ ] Test: 5+ configs generated, metadata visible in output

### Effort Estimate
- **Design**: 1 day
- **Implementation**: 2 days
- **Testing**: 1.5 days
- **Total**: 4.5 days

### Dependencies
- EPIC-1, EPIC-2, EPIC-3, EPIC-4, EPIC-5, EPIC-6

---

## EPIC-8: End-to-End Testing & Validation
**Priority**: P0 (Critical)  
**Scope**: E2E testing, Fred's config comparison, acceptance validation

### Description
Validation complète:
- E2E test: 1.5h diagnostic + config gen without crash
- Compare generated config vs Fred's reference (density, pertinence)
- Validate metadata integrity
- Performance benchmarks (compression, timeouts)
- Quality gates passed

### Features Covered
- All acceptance criteria (AC-001 through AC-007)

### Acceptance Criteria
- [ ] E2E test: diagnostic + config gen completes < 90s
- [ ] No timeouts, API errors, frontend hangs
- [ ] Generated config comparable to Fred's
- [ ] Metadata extracted correctly (schema valid)
- [ ] Strategic synthesis reviewed by Catherine
- [ ] 5+ test runs, all criteria PASS
- [ ] Ready for production deployment

### Effort Estimate
- **Test setup**: 1 day
- **Test execution**: 2 days
- **Iteration/fixes**: 1.5 days
- **Documentation**: 0.5 day
- **Total**: 5 days

### Dependencies
- All other epics (integration test)

---

## Epic Summary Table

| Epic | Priority | Effort | Dependencies | Status |
|------|----------|--------|--------------|--------|
| EPIC-1: Prompt Refactor | P0 | 4 days | specs | Ready |
| EPIC-2: Pattern Detection | P0 | 3 days | EPIC-1 | Ready |
| EPIC-3: Opportunities | P0 | 3.5 days | EPIC-2 | Ready |
| EPIC-4: Metadata System | P0 | 3 days | EPIC-1,2,3 | Ready |
| EPIC-5: Synthesis | P0 | 3.5 days | EPIC-1,2,3 | Ready |
| EPIC-6: Agents & Routines | P0 | 3.5 days | AGENTS-SPEC | Ready |
| EPIC-7: Gen-Config v20+ | P0 | 4.5 days | EPIC-1..6 | Ready |
| EPIC-8: E2E Testing | P0 | 5 days | All | Ready |

**Total Effort**: ~30 days (6-week sprint, 1 dev)

---

## Sprint Planning

### Sprint 1 (Weeks 1-2): Foundation
- EPIC-1: Diagnostic Prompt Refactor
- EPIC-2: Pattern Detection Engine
- EPIC-4: Metadata Enrichment (schema + persistence)

### Sprint 2 (Week 3): Intelligence
- EPIC-3: Claude Opportunities
- EPIC-5: Strategic Synthesis
- EPIC-6: Agent & Routine Config

### Sprint 3 (Week 4): Integration
- EPIC-7: Generate-Config v20+ Integration

### Sprint 4 (Week 5-6): Validation
- EPIC-8: E2E Testing & Validation
- Fixes + iteration based on test results
- Production deployment readiness

---

**Created**: 2026-04-27 (PLAN phase)  
**Status**: Ready for BUILD phase  
**Next**: User stories + detailed tasks (separate documents)
