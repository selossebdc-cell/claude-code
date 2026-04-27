---
name: Claude Configurator v2 — Config as Living Proposal (Not Static)
description: Product requirement: Generated config must be a customizable proposal, updatable by client based on needs and Claude feature evolution
type: product
---

## Requirement: Config Generation as "Living Proposal"

**Status**: CRITICAL for EPIC-6 (Agent & Routine Configuration)  
**Discovered**: 2026-04-27 (during Phase MODEL auth/stripe)  
**Impact**: Affects config-display.js, EPIC-6 architecture, EPIC-7 integration

---

## The Issue

Generated configs cannot be static YAML/JSON that the client views read-only. This becomes obsolete when:
- Client needs change (their work style, blocages evolve)
- Claude releases new features (new agents, new capabilities)
- Client learns better how to use Claude (refines their approach)

## The Solution

Config must be presented as a **living proposal**:

```
Diagnostic → Synthesis → Config PROPOSAL 
                         ↓
                    Client sees proposal
                         ↓
                    Client can customize:
                    - Select/deselect agents
                    - Adjust routines (daily/weekly/monthly)
                    - Edit Custom Instructions
                    - Add/remove "Ma Mémoire" sections
                         ↓
                    Client saves to Claude
                         ↓
                    Client can UPDATE anytime:
                    - New Claude features (new agents)
                    - Work style changes
                    - Market shifts
```

## Technical Implications

### EPIC-6 (Agent & Routine Configuration)
- Don't generate static config
- Generate config TEMPLATE with:
  - All 6 mandatory agents (but selectable)
  - Routines as templates (not hardcoded)
  - Custom Instructions as draft (editable)
  - "Ma Mémoire" sections as checkboxes (pick what's relevant)

### Frontend (config-display.js)
- Show proposal with edit controls (not read-only)
- "Save to Claude" button (not auto-apply)
- "Update" button for future refinements
- Show which Claude features are available

### EPIC-7 (Generate-Config Integration)
- Feed synthesis to generator
- Output customizable proposal (not final config)
- Include version/date so client can track updates

## Design: Why This Matters

**149€ justification**: Not just "here's your config", but "here's a starting point you'll refine over time as you learn Claude better"

**Client experience**: Feels like a partner (not a robot), acknowledges their expertise, invites collaboration

**Product evolution**: When Claude adds new agents/features, client can easily adopt them without re-running diagnostic

---

## Scope Clarification

**Product is Claude-ONLY** (not multi-AI support for ChatGPT/Gemini/etc)
- Generate configs ONLY for Claude
- All agents, routines, instructions are Claude-native
- No "choose your AI" flow

---

## When to Implement

- **EPIC-6**: Design config generator to output proposal (not static)
- **EPIC-7**: Ensure generate-config integrates with proposal flow
- **Post-EPIC-7**: UX refinements (edit controls, versioning)

---

**Created**: 2026-04-27  
**Priority**: HIGH (affects architecture of EPIC-6/7)  
**Owner**: Catherine (product definition)
