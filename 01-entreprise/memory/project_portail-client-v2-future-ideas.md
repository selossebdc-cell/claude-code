---
name: Portail Client V2 — Future Evolution Ideas
description: Enhancement opportunities for Portail Client V2 discovered during development
type: project
---

## Idea 1: AI-Assisted Process Step Generation (2026-04-27)

**Vision**: When creating a new process/playbook, user only needs to describe what they want to do. Claude (or another LLM) automatically generates optimized step proposals.

**Current Flow**:
1. User selects a template (manual)
2. User creates steps manually (tedious)
3. Result: Steps might be incomplete or suboptimal

**Proposed Flow**:
1. User dictates goal: "Je veux lancer un challenge recrutement" 
2. AI analyzes goal + domain context (Face Soul Yoga, MTM program, etc.)
3. AI generates step proposals based on:
   - Historical best practices (existing processes in DB)
   - Domain-specific knowledge (training program specifics)
   - Industry standards (recruitment challenge patterns)
4. User reviews/edits proposals
5. Result: Steps are "nickel" (perfect) with minimal manual effort

**Implementation Approach**:
- Add "Generate Steps" button in process creation flow
- Call Edge Function with:
  - Process goal/description (user input)
  - Client context (Face Soul Yoga, Guadeloupe Explor, etc.)
  - Similar past processes (search playbook_processes by similarity)
- Edge Function calls Claude API to generate steps
- Return proposals for user approval/editing

**Dependencies**:
- Edge Function infrastructure (Supabase)
- LLM API integration (Claude via Anthropic SDK)
- Vector similarity search (find similar processes for context)
- RLS policy for generated content (tie to client_id)

**Status**: Future enhancement — capture for planning phase of Epic 5

**Priority**: Medium (nice-to-have, improves UX but not critical path)

**Effort Estimate**: 8-12 hours (Edge Function + LLM integration + UI + testing)

---

## Technical Considerations

### Data Context for Better Proposals
- Existing processes for this client (what's worked before)
- Process categories/templates (patterns to follow)
- Step sequences from similar processes (copy structure)
- Historical outcomes (which steps correlate with success)

### Quality Safeguards
- User must review + approve before saving
- Generated steps can be edited inline
- Flag AI-generated content for audit trail
- Track which processes used AI generation (for metrics)

### RLS Implications
- Generated steps must respect client_id isolation
- Only users from the client can see AI-generated steps for their processes
- Audit log: who generated, when, what was edited

---

**Created**: 2026-04-27  
**Status**: Idea (not yet in Factory pipeline)

---

## Idea 2: Portail V3 — Integrated CRM (2026-04-27)

**Vision**: Portail Client V2 evolves into V3 as unified CRM + client workspace. Catherine & Michaël get complete client relationship visibility.

**Current State**: V2 is client-focused (playbooks, processes, templates, training)

**Proposed Evolution (V3)**:
- **CRM Core**: Client master data, interaction history, pipeline, opportunities
- **Sales Visibility**: Proposal pipeline, deal status, forecast
- **Service Delivery**: Playbooks, processes, progress tracking (current V2 features)
- **Analytics**: Client health, engagement metrics, revenue impact
- **Unified Client View**: 360° profile combining CRM + service delivery data

**Data Model Additions**:
```
playbook_clients (already exists)
  ├── interactions (calls, emails, meetings)
  ├── opportunities (deals in pipeline)
  ├── proposals (sent & status)
  ├── contracts (active & archived)
  ├── health_metrics (engagement score, churn risk)
  └── revenue (actual + forecast)
```

**User Personas**:
- **Catherine (Owner)**: Full visibility, strategic decisions, pipeline management
- **Michaël (Partner)**: Client relationship management, proposal oversight, deal tracking
- **Client Users**: Playbooks, training, documentation (unchanged from V2)

**Benefits**:
- No context-switching between tools (Airtable, spreadsheets, etc.)
- Real-time client health dashboard
- Automated insights ("Client X at risk", "Opportunity Y closing soon")
- Historical context for better decisions

**Phase Timeline**:
- Phase 1 (V2 current): Playbooks + RLS isolation ✅
- Phase 2 (Epic 4-5): Frontend refactoring + AI step generation
- Phase 3 (V3): CRM integration (new epic)

**Status**: Strategic vision — capture for planning Q3 2026

**Effort Estimate**: 20-30 hours (significant refactor + new features)

**Priority**: High (aligns with business needs, improves decision-making)

---

**Created**: 2026-04-27  
**Status**: Strategic idea (ready for roadmap planning)
