---
name: Session Reporting — CRs & Memory Enrichment
description: Process for writing session reports (CRs), archiving in SESSIONS.md, and enriching client memory with patterns
type: process
last_update: 2026-04-23
---

# Session Reporting — CRs & Memory Enrichment

## Overview

After each client session, we:
1. Write a detailed CR (session report)
2. Archive it in `/02-clients/[client]/SESSIONS.md`
3. Extract patterns + insights → update `/02-clients/[client]/NOTES.md`
4. Track decisions & blockers → update `/02-clients/[client]/SUIVI.md`
5. Update KPIs & risks → `/02-clients/[client]/STATUS.md`

This turns individual sessions into institutional memory.

---

## Phase 1: Immediate Post-Session (same day, <1 hour)

**Goal**: Capture raw session data while it's fresh.

### Steps
1. **Write raw CR notes**
   - Location: Create temp file `/02-clients/[client]/CR-DRAFT-[date].md`
   - Structure:
     ```
     # Session [N] — [Date]
     
     **Duration**: [start time - end time]  
     **Participants**: [names]
     
     ## Topics Covered
     - [Topic 1]: [what we discussed]
     - [Topic 2]: [what we discussed]
     
     ## Key Decisions Made
     - [Decision 1]: [what was agreed]
     - [Decision 2]: [what was agreed]
     
     ## Actions — Client
     - [ ] [Action 1]: [by date]
     - [ ] [Action 2]: [by date]
     
     ## Actions — Us
     - [ ] [Action 1]: [by date]
     - [ ] [Action 2]: [by date]
     
     ## Blockers / Risks / Vigilances
     - [Blocker 1]: [what's stuck]
     - [Risk 1]: [what could go wrong]
     - [Vigilance 1]: [what to watch]
     
     ## Raw Observations
     [Free-form notes on client mood, reactions, surprises, patterns seen]
     ```

2. **Attach supporting materials**
   - Photos, screenshots, documents from session? File in session folder
   - Client deliverables? Store in appropriate subfolder

3. **Review + refine**
   - Re-read raw notes
   - Fix typos, add clarity
   - Reorganize into structured sections if needed

**Output**: CR-DRAFT-[date].md (ready for archival)

---

## Phase 2: Archive to SESSIONS.md (same day or next morning, <30 min)

**Goal**: Move CR into permanent client history with consistent structure.

### Steps
1. **Open `/02-clients/[client]/SESSIONS.md`**
   - This is the session history database
   - Each session is one entry
   - Newest at top (reverse chronological)

2. **Add new session entry**
   - Format:
     ```
     ## Session [N] — [Date] ([Time duration])
     
     **Participants**: [names]  
     **Status**: ✅ Completed (or 🔴 Blocked, 🟡 Partial)
     
     ### Topics & Decisions
     - [Topic 1]: [outcome/decision]
     - [Topic 2]: [outcome/decision]
     
     ### Client Actions
     - [ ] [Action 1] — due [date]
     - [ ] [Action 2] — due [date]
     
     ### Our Actions
     - [ ] [Action 1] — due [date]
     - [ ] [Action 2] — due [date]
     
     ### Blockers & Risks
     - [Blocker 1]: [description] → escalating to [owner]
     - [Risk 1]: [description] → mitigation [plan]
     
     ### Key Insights
     [Patterns, quotes, observations that inform future sessions]
     ```

3. **Reference CR-DRAFT**
   - Link to original: `[Full CR →](CR-DRAFT-[date].md)`
   - This preserves raw notes for reference if needed

4. **Clean up draft**
   - Delete CR-DRAFT-[date].md (we have the canonical version in SESSIONS.md now)
   - Or move to `/[client]/archive/CR-[date].md` if you want to preserve raw versions

**Output**: New entry in SESSIONS.md + raw CR archived/deleted

---

## Phase 3: Memory Enrichment (next 2 business days, <1 hour)

**Goal**: Extract patterns from session and update client memory files.

### Step 1: Update NOTES.md (Client Memory)
- Location: `/02-clients/[client]/NOTES.md`
- Look for patterns in this session vs prior sessions:
  - **Communication style**: How did they respond? Decisive? Cautious? Perfectionist?
  - **Motivators**: What animated the conversation? Where did energy come from?
  - **Blockers**: What's stopping them? Perfectionism? Procrastination? Delegation struggle?
  - **Communication preference**: Tutoiement/vouvoiement? Meetings vs async? Frequency of contact?
- Update sections:
  - Patterns Observés → Communication (add new observations)
  - Patterns Observés → Moteurs (update: ce qui l'anime, ce qui la bloque)
  - Any new quotes or "pépites" (content angles)?
- Link to session: Add note: "Updated after Session [N] — [date]"

### Step 2: Update SUIVI.md (Current Status)
- Location: `/02-clients/[client]/SUIVI.md`
- Update progress:
  - Phase 1 (Cartographie): [now X%] (was Y%)
  - Phase 2 (Optimisation): [now X%]
  - Phase 3 (Déploiement): [now X%]
- Update action lists:
  - Move completed actions to ✅
  - Add new actions from session
  - Update blockers list
  - Next session date: [date]

### Step 3: Update STATUS.md (Project Health)
- Location: `/02-clients/[client]/STATUS.md`
- Update KPIs:
  - Baseline → Current (what changed since last session?)
  - Risk: any new risks from session? (update risk table)
  - Timeline: are we on track? (any date shifts?)
- Timeline note: "On track" or "At risk" based on session progress

**Output**: NOTES.md, SUIVI.md, STATUS.md all updated with session insights

---

## Phase 4: Growth Agent Input (weekly, automated)

**Goal**: Client memory feeds growth agent for continuous improvement.

### What growth agent reads
- **SESSIONS.md**: Session history + decisions + blockers
- **NOTES.md**: Patterns, communication style, motivators, risks
- **SUIVI.md**: Progress % by phase, current actions, blockers
- **STATUS.md**: KPI trends, timeline risk, team health

### What agent looks for
- Is this client progressing on-track? (% movement session-to-session)
- Are blockers recurring? (appears in 3+ sessions = systemic issue)
- Are KPIs trending toward goals? (or stalling?)
- Communication friction? (showing up in patterns?)
- Automation opportunities? (can we free up client time?)

### Agent output
- Propositions like: "Fred's Phase 1 stuck 2 weeks; blockers repeating (process doc + tool choice). Suggest: [specific action]"
- Or: "Taïna's KPI trending wrong; risk: [mitigation suggested]"
- Or: "Pattern: perfectionism paralyzing decisions; suggest: [session reframe]"

---

## Standards

### Session CR Structure (required)
Every session CR must include:
- Session #, date, duration, participants
- 3-5 topics covered (not just bullet points — what was the outcome?)
- 2-5 decisions made (explicit agreements)
- 3-10 client actions (with due dates)
- 2-5 our actions (with due dates)
- 1-3 blockers/risks (with escalation or mitigation plan)
- Raw observations (what surprised you? What patterns did you see?)

### NOTES.md Update (every 2-3 sessions)
- Communication style: specific examples (e.g., "prefers async updates, not surprise calls")
- Motivators: "Driven by: [what energizes them]"
- Blockers: "Struggles with: [specific friction]"
- Any new quotes or "pépites"

### SUIVI.md Update (after every session)
- Phase progress: update % completed
- Action list: move completed items, add new items
- Blockers: any new blockers or resolved ones?
- Next session: scheduled date + prep work if any

### STATUS.md Update (every 4 sessions or monthly)
- KPI: record current values, compare to target
- Timeline: "On track" or "At risk" — explain why
- Team capacity: has team member availability changed?

---

## Automation Opportunities

Currently session reporting is **manual** (Catherine writes CR). Options for future:

1. **Audio recording → CR draft**
   - Record session → transcribe → summarize key points
   - Would save ~30 min on CR writing
   - Caveat: would still need structure + link to actions

2. **Template-driven CR**
   - Use form/checklist instead of free-form
   - Forces structured capture (topics, decisions, actions)
   - Faster to fill, easier to parse for patterns

3. **Automated memory enrichment**
   - SESSIONS.md entry → extract actions/blockers
   - Auto-update SUIVI.md action lists
   - Flag patterns (same blocker 3x = alert)
   - Would save ~15 min on enrichment

**Note**: Growth agent could flag automation opportunities: "3 sessions written, clear pattern in CR structure — ready for template automation"

---

## Troubleshooting

**Session ran over, CR very long**
- Still capture it all in SESSIONS.md (don't abbreviate content)
- But: summarize for growth agent (agent reads long CRs, but we summarize key points in SUIVI update)

**Session didn't happen / rescheduled**
- Create entry anyway: "## Session [N] — [original date] — RESCHEDULED to [new date]"
- Document reason (client issue, your issue, force majeure?)
- Don't lose the session slot in history

**Blocker from session is blocking other clients**
- Add to `/technical/blockers.md` immediately (don't wait for growth agent)
- Link the blocker: "Affecting clients: Fred, Taïna"
- This alerts Catherine + growth agent to priority

**Client action not done by due date**
- In next session CR: note "Fred's action [X] — originally due [date], now due [new date]"
- In SUIVI.md: move action to "Delayed — due [new date]"
- In next growth agent report: flag if pattern (repeatedly delayed = timeline risk)

---

## Metrics (tracked in growth agent)

- **Time from session → CR archived**: target < 1 day (flag if > 2 days)
- **Time from CR → NOTES.md enriched**: target < 2 business days
- **Session attendance rate**: % of scheduled sessions completed (target > 95%)
- **Action completion rate**: % of client actions done on-time (target > 80%)
- **Blocker resolution time**: avg days from blocker creation → resolved (watch for > 14 days)

---

**Last reviewed**: 2026-04-23  
**Next review**: After session-report SKILL refactor (target: 2026-04-30)  
**Known gap**: session-report SKILL still writes to Notion instead of SESSIONS.md — refactor in progress
