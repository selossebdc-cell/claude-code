---
name: Claude Configurator v2 — Architecture & Technical Decisions
description: Key architectural choices for diagnostic system. 9 implicit blocks, Sonnet 4.6, message compression, synthesis readiness criteria, RLS security.
type: reference
---

## Architecture Overview

**System**: Intelligent diagnostic for Claude Pro 149€ product  
**Goal**: Generate personalized, game-changing configuration by understanding client work style, pain points, strengths  
**Duration**: 10-20 minute conversation → strategic synthesis  
**Delivery**: 3-section output (Understanding, Transformation, Config Preview)

---

## Core Architectural Decisions

### 1. 9 Implicit Blocks (Not Linear Questionnaire)

**Decision**: Internal checklist, not user-visible order

```
Blocks (for reference):
1. Identity (who are you, role, context)
2. Offering (what you deliver to market)
3. Daily (how you spend your day)
4. Challenges (blocages you face)
5. Constraints (budget, team size, tech limits)
6. Security (sensitive data, compliance)
7. Work Style (pragmatic, structured, by-feeling, etc.)
8. Voice (how you communicate with clients/team)
9. Proposals (what you give clients)
```

**Why**: Rigid questionnaires (Q1, Q2, Q3...) feel robotic. Natural conversation explores these themes organically.

**Implementation**: System prompt guides coverage checking internally ("Am I at ~40% coverage? 70%?"). No visible "Now let's talk about block 5".

---

### 2. 4 Adaptive Question Strategies

**Decision**: Don't ask pre-written questions. Generate context-aware questions.

```
Strategies:
1. Follow-up Deepening: "I hear you export to 40 countries. What's your biggest challenge with that?"
2. Pattern Validation: If pattern detected (e.g., "works by feeling"), ask "How do you typically make important decisions?"
3. Block Coverage Check: If block "Security" not yet covered, ask naturally when context is right
4. Opportunity Linking: If pain_point("documentation") + pattern("works by feeling"), ask "Would you like decisions better documented?"
```

**Why**: Conversational + targeted, not generic.

---

### 3. Real-Time Metadata Enrichment (EPIC-2, EPIC-3, EPIC-4)

**Decision**: After each Claude response, detect patterns, opportunities, update metadata

```
Pipeline:
User message → Claude diagnostic response → [Collect full response]
  ↓
Pattern Detection (EPIC-2): 4 types
  - Recurring Blocages (keywords repeated across turns)
  - Work Style Traits (pragmatic, structured, etc.)
  - Strengths (what they excel at)
  - Risk Indicators (what they forget/struggle with)
  ↓
Opportunity Identification (EPIC-3): Linked to pain points + patterns
  - 10 predefined opportunities
  - Mapped to 6 mandatory + 2 contextual agents
  - Priority calculation (1-5 based on severity + impact)
  ↓
Synthesis Readiness Check (EPIC-5): Should synthesis be generated?
  - 8+ turns
  - 70%+ block coverage
  - 2+ pain points
  - 3+ opportunities
  - 0.6+ clarity score
  ↓
Save to Supabase (< 2KB constraint)
```

**Why**: Real-time detection = early insights, data available immediately, not collected at end.

---

### 4. Message Compression Strategy

**Decision**: Keep last 5 full, compress older in 10-message blocks

```
Example:
Full:     [msg 25, msg 26, msg 27, msg 28, msg 29]
Summary:  [msg 1-10 summary block] [msg 11-20 summary block] [msg 21-24 summary block]
```

**Token impact**: Instead of ~3,000 tokens for 30 messages, compress to ~400 tokens for summaries + last 5 full (~1,200 tokens total).

**Why**: Keeps conversations flowing long without timeout. Diagnostic can run 30-50 turns if needed.

---

### 5. Synthesis Readiness Criteria

**Decision**: Generate synthesis only when ALL conditions met

```
Trigger:
- turns_count >= 8
- coverage_percentage >= 70%
- pain_points.length >= 2
- claude_opportunities.length >= 3
- clarity_score >= 0.6
```

**Clarity Score Formula**:
- +0.20 if avg user response > 150 chars
- +0.15 if avg user response > 250 chars
- +0.15 if pain_points >= 2
- +0.10 if pain_points >= 3
- +0.15 if patterns >= 2
- +0.10 if patterns >= 3
- +0.10 if opportunities >= 3
- +0.10 if opportunities >= 5
- Max: 1.0

**Why**: Prevents premature synthesis (not enough data) and synthesis generation (insufficient confidence).

---

### 6. Synthesis Structure (3 Sections)

**Section 1: "Ce que j'ai compris de vous" (Understanding)**
- Identity (role, context, scope)
- Main blocages (2-3 pain points)
- Strengths
- Work style

**Section 2: "Où Claude devient vraiment game-changer pour vous" (Transformation)**
- 3-4 top opportunities
- Specific to THEIR context (not generic)
- Why Claude transforms (not just "Claude can help")
- Which agent handles each

**Section 3: "Votre config sera centrée sur" (Config Preview)**
- 6 mandatory agents (Miroir, Garde-Fou, Admin, Stratégie, Planif, Amélioration Continue)
- "Ma Mémoire" project
- Custom Instructions (2000+ chars)
- Key routines (Daily, Weekly, Monthly)

**Why**: 3 sections = complete handoff to config generation. Strategic (not summary). Justifies 149€.

---

### 7. Database Design: RLS + Metadata JSONB

**Decision**: Supabase with Row Level Security + JSONB metadata

```
Table: diagnostics
- session_id (UUID, PK)
- client_id (UUID, FK → auth.users, for RLS)
- metadata (JSONB, <2KB)
  └─ pain_points[]
  └─ patterns_detected[]
  └─ claude_opportunities[]
  └─ work_style_traits[]
  └─ coverage_tracking
  └─ conversation_quality_metrics
  └─ synthesis (3-section output)
- conversation_history (JSONB, last 100 messages)
- diagnostic_status (enum: in_progress, synthesis_generated, completed)
- created_at, updated_at, ended_at

RLS Policies:
- Users can only read/write their own diagnostics (auth.uid() = client_id)
```

**Why**: 
- RLS = security by design (no one can read another user's data)
- JSONB = flexible schema (no migrations for new metadata fields)
- < 2KB = density enforced (forces removal of redundant data)

---

### 8. Model Selection: Sonnet 4.6

**Decision**: Claude Sonnet 4.6 for diagnostic + synthesis

**Why Sonnet (not Opus, not Haiku)**:
- Haiku: Too fast/superficial for nuanced diagnostic
- Opus: Overkill cost for this use case
- Sonnet: Perfect balance (good quality, reasonable cost, fast enough)

**Temperature**: 0.7 (creative but coherent, not random)

---

### 9. Security: Secure-by-Design Framework

**Applied Framework**: Michael Ramarivelo's Secure-by-Design

**Key Controls**:
- ✅ RLS enabled on all tables
- ✅ API keys via environment variables (Deno.env.get)
- ✅ Server-side validation for all inputs
- ✅ No client-side trust assumptions
- ✅ No hardcoded secrets
- ✅ Message compression = no accidental API key leakage
- ✅ Metadata isolation per user (RLS)

**Audit**: Passed 100% on OWASP Top 10

---

### 10. Deployment: Supabase Edge Functions

**Decision**: Deno Edge Function on Supabase (not Lambda, not Node.js server)

**Why**:
- Cold start < 1s (important for UX)
- No server to manage
- Native Supabase integration (can call RLS-protected tables)
- Streaming support (SSE for real-time response)
- Environment secrets managed by Supabase

---

## Integration Flow

```
Client → POST /functions/v1/chat
         ↓
[Validate session_id, message]
         ↓
[Fetch metadata from Supabase (or create)]
         ↓
[Call Claude with system prompt v21 + current metadata + conversation history]
         ↓
[Collect full response + stream to client via SSE]
         ↓
[ASYNC: Pattern Detection]
         ↓
[ASYNC: Opportunity Identification]
         ↓
[ASYNC: Synthesis Readiness Check → Generate if ready]
         ↓
[Update metadata in Supabase]
         ↓
Response complete
```

**Async pipeline ensures** client doesn't wait for synthesis generation. Response streams immediately.

---

## EPIC Dependencies

| EPIC | Purpose | Dependencies |
|------|---------|--------------|
| 1 | Chat Edge Function | None |
| 2 | Pattern Detection | EPIC-1 |
| 3 | Opportunities | EPIC-1, EPIC-2 |
| 4 | Metadata Persistence | EPIC-1, EPIC-2, EPIC-3 |
| 5 | Synthesis Generation | EPIC-1, EPIC-2, EPIC-3, EPIC-4 |
| 6 | Agent Config Gen | EPIC-1-5 (after deployment validation) |
| 7 | Generate-Config Integration | EPIC-6 |
| 8 | E2E Testing | All EPICs |

---

## Performance Targets

- **Diagnostic latency**: < 90 seconds (15-20 turns)
- **Config generation latency**: < 60 seconds
- **Synthesis generation latency**: 3-5 seconds (Claude API call)
- **Message compression**: Keeps total turn tokens < 2,000

---

## Scalability Considerations

**Current**: Single Supabase instance (free tier OK for testing, pro tier for production)

**Future**:
- Monitor token usage across diagnostics
- Cache common opportunities (rarely change)
- Archive old conversation history (keep last 100 messages only)
- Consider OpenAI API caching for synthesis prompts (if needed)

---

## Trade-offs Made

| Trade-off | Chose | Over | Why |
|-----------|-------|------|-----|
| 9 blocks | Implicit checklist | Rigid questionnaire | Natural conversation |
| Compression | Keep-5 strategy | Keep-all (timeout) | Token efficiency |
| Metadata | < 2KB | Unlimited | Force density, prevent bloat |
| Model | Sonnet 4.6 | Opus 4.7 | Cost vs quality sweet spot |
| Database | JSONB | Normalized tables | Schema flexibility |
| Deployment | Supabase Edge | AWS Lambda | Cold start + integration |

---

## Future Extensions (EPIC-6+)

1. **Agent & Routine Config** (EPIC-6): Generate prompts for 6 agents from metadata
2. **Generate-Config Integration** (EPIC-7): Feed synthesis to v18-19, output custom config
3. **E2E Testing** (EPIC-8): Full flow validation
4. **Feedback Loop**: User satisfaction → improve synthesis quality
5. **Multi-language Support**: Extend system prompt to other languages
6. **Advanced Analytics**: Track which opportunities convert to config selection

---

**Last Updated**: 2026-04-27  
**Status**: ✅ All EPICs 1-5 implemented per these decisions
