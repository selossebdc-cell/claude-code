---
name: Client Onboarding — Sales to Delivery
description: Full journey from prospect to active client, including memory creation, folder structure, first session prep
type: process
last_update: 2026-04-23
---

# Client Onboarding — Sales to Delivery Pipeline

## Overview

Client onboarding is the journey from prospect meeting → signed contract → first delivery. It creates all persistent client infrastructure (folders, memory files, documents) and preps for initial diagnostic session.

---

## Stage 1: Prospect Discovery (Async, 1-2 weeks)

**Goal**: Qualify the prospect and schedule an initial audit meeting.

### Steps
1. **Initial contact**
   - Prospect reaches out via LinkedIn, email, referral, or Airtable intake form
   - Log in Airtable: `Prospects` table with contact info + source

2. **Qualification call** (30 min async or sync)
   - Goal: Understand their business, challenge, timeline, budget
   - Questions:
     - What's your role and company? (industry, size)
     - What's the main challenge or goal?
     - What's your timeline? (when do you need this?)
     - What's your budget range? (rough estimate OK)
     - Who else needs to be involved?
   - Outcome: Qualified (yes/no) + proposal type (Accompagnement, Data/KPI, Cloud Team)

3. **Create prospect folder** (if qualified)
   - Location: `/02-clients/prospects/[prenom-nom]/`
   - Create: `[prenom-nom].md` (prospect memory file using template-prospect.md)
   - Fields: contact info, company, challenge, timeline, budget, proposal type, next step
   - Update Airtable: mark as "Qualified" + folder path

4. **Schedule audit meeting**
   - Offer 3 time slots
   - Confirm in calendar + send prep email
   - Attachment: "Audit Meeting Prep" (what we'll cover)

**Output**: Prospect folder + memory file + scheduled audit meeting

---

## Stage 2: Initial Audit (1 session, 2-3 hours)

**Goal**: Deep dive into current state, identify 3 main problems, scope 6-month engagement.

### Session structure
1. **Context setup** (15 min)
   - Review their business model
   - Understand current process
   - Clarify: what does success look like?

2. **Interviews** (90 min)
   - "Raconte-moi une semaine type" (walk through their week)
   - Time allocation: what % operational vs strategic vs management?
   - Key challenges: what's costing them most (time, money, stress)?
   - Existing tools & processes: what works, what doesn't?
   - Team capacity: can they dedicate time to this?

3. **Synthesis & next steps** (15 min)
   - Summarize 3 main problems
   - Propose engagement type (Accompagnement 18 sessions, Data/KPI module, etc.)
   - Next: we'll send you a proposal + roadmap

### After audit
- **Create session CR**: File in `/02-clients/prospects/[prenom-nom]/CR-[date].md`
- **Update prospect memory**: Audit findings, problems, initial assessment
- **Move forward if qualified**: proceed to Stage 3

**Output**: Audit CR + updated prospect memory + roadmap draft

---

## Stage 3: Proposal & Contract (Async, 3-5 days)

**Goal**: Send written proposal + feuille de route, get signature + payment.

### Steps
1. **Generate proposal**
   - Use `proposal-generator` SKILL
   - Inputs: prospect memory + audit findings
   - Output: `/02-clients/prospects/[prenom-nom]/proposition-[date].html`
   - Format: HTML (company branding, styled table of contents)
   - Contents:
     - Executive summary (problem + solution in 1 page)
     - 3 problems → 3-phase solution mapping
     - Timeline (6 months, phased delivery)
     - Cost & payment terms
     - Success criteria (KPIs at end of 6 months)

2. **Generate roadmap**
   - Use `roadmap-generator` SKILL  
   - Inputs: audit findings, proposal scope
   - Output: `/02-clients/prospects/[prenom-nom]/feuille-de-route-[date].md`
   - Contents: diagnostic, 3 phases, SOPs to create, timeline, risks, hypotheses

3. **Send proposal + roadmap**
   - Email: prospect + any stakeholders who need sign-off
   - Tone: excited but realistic (no overcommitments)
   - Include: "Next steps: sign contract + 50% advance, then we schedule kickoff"

4. **Negotiate & sign**
   - Answer questions
   - Adjust timeline if needed (but protect core scope)
   - Get signature (electronic or PDF)
   - Collect 50% advance payment (via Stripe or bank transfer)

5. **Admin setup**
   - Invoice client: use `invoice-generator` SKILL
   - Create Portail Client login (temp or full access?)
   - Log in Airtable: move from "Prospects" to "Clients" table
   - Update prospect memory: add contract date, end date, sessions planned

**Output**: Signed contract + paid advance + active client folder

---

## Stage 4: Client Activation (1 day, before first session)

**Goal**: Create all client infrastructure and prep for Session 1.

### Steps
1. **Create client folder structure**
   - Main location: `/02-clients/[prenom-nom]/`
   - Create files (copy templates):
     - `NOTES.md` (client memory: identity, patterns, motivators)
     - `SESSIONS.md` (session history + decisions)
     - `SUIVI.md` (current status: % complete, actions, blockers)
     - `STATUS.md` (health: KPIs, budget, risks, timeline)
     - `feuille-de-route.md` (6-month plan from proposal)

2. **Populate initial data**
   - NOTES.md: client name, company, dirigeant, email, tel, objectives
   - SESSIONS.md: header only (sessions will be added after RDV 1)
   - SUIVI.md: Phase 1 checklist (interviews, process mapping, etc.)
   - STATUS.md: contract dates, contract value, sessions planned (18 for Accompagnement), KPI targets
   - feuille-de-route.md: copy from proposal version

3. **Create Portail Client access** (if applicable)
   - Generate temp login: `[prenom-nom]@portail.csbusiness.fr` + temp password
   - Email client: "Here's your Portail Client access for session materials"
   - Set permissions: read-only for now (full access after Session 2?)

4. **Prep Session 1**
   - Create calendar event: `/02-clients/[prenom-nom]/SESSION-1-[date].md` (session prep notes)
   - Content: audit review, session objectives, pre-work requests
   - Send client: pre-session email with prep (what to bring, think about, etc.)

5. **Update MEMORY**
   - Create/update `/01-entreprise/memory/client/[prenom-nom].md`
   - Contents: contract value, sessions planned, current progress, blockers, patterns, KPIs
   - This file is read by growth agent every Monday

**Output**: Client folder fully structured + Portail access + Session 1 prep done

---

## Stage 5: First Session & Beyond

**Goal**: Execute first diagnostic session, establish rhythm.

### Session 1: Deep Diagnostic
- Location: `/02-clients/[prenom-nom]/SESSIONS.md` entry 1
- Duration: 2-3 hours
- Deliverable: CR (session notes + decisions) + updated feuille-de-route validation
- After: Update SUIVI.md with new actions, update STATUS.md with risk assessment

### Session 2: Roadmap Validation
- Validate feuille-de-route with client
- Approve 3 phases + timeline
- Confirm KPIs and success criteria
- Start Phase 1 process mapping

### Ongoing
- Every session: CR → SESSIONS.md entry
- Every 2 sessions: NOTES.md update (patterns, motivators, communication style)
- Every 4 sessions: SUIVI.md + STATUS.md update (progress, KPI trend)
- Weekly: growth agent reads memory, generates improvement suggestions

---

## Checklists

### Pre-Audit Checklist
- [ ] Prospect qualified (meets basic criteria)
- [ ] Audit time scheduled (3 options offered, 1 confirmed)
- [ ] Calendar invite sent + prep email
- [ ] Team member assigned (Catherine or delegate?)
- [ ] Audit prep done (understand their industry, any prior research?)

### Post-Audit Checklist
- [ ] Audit CR written and filed
- [ ] 3 main problems identified
- [ ] Proposal scope defined (which modules? how many sessions?)
- [ ] Roadmap drafted
- [ ] Prospect memory updated

### Pre-Signature Checklist
- [ ] Proposal sent + reviewed by prospect
- [ ] Roadmap sent + reviewed
- [ ] Contract template filled with dates + cost
- [ ] Questions answered
- [ ] Ready for sign-off

### Pre-Session-1 Checklist
- [ ] Contract signed + 50% paid
- [ ] Client folder created (`/02-clients/[prenom-nom]/` with all files)
- [ ] Memory file created (`/01-entreprise/memory/client/[prenom-nom].md`)
- [ ] Portail Client access provided (if applicable)
- [ ] Session 1 prep document ready
- [ ] Growth agent will read client memory by next Monday

---

## Troubleshooting

**Prospect not responding to proposal**
- Wait 3 days, send reminder email
- If still no response after 1 week: mark as "paused" in Airtable + update prospect memory with "status: paused"

**Prospect wants to change scope mid-proposal**
- Document the change request
- Reassess: does it still fit 6-month window? What shifts?
- Update proposal + roadmap + timeline
- Re-send for signature

**Prospect wants to start before paying advance**
- Policy: 50% advance required before Session 1
- Offer: we can do Session 1 prep (folder creation, roadmap review) while waiting for payment
- But: don't schedule Session 1 until paid

**Client wants to pause after Session X**
- Pause option: keep folder + memory, mark as "paused" in client memory
- Document reason + intended resume date
- Update STATUS.md: end_date moved to [new date]
- Keep SESSIONS.md as-is (history preserved)

---

## Metrics (tracked in growth agent)

- **Time from audit → signature**: target < 2 weeks (flag if > 3 weeks)
- **Time from signature → Session 1**: target < 1 week
- **Proposal acceptance rate**: % of proposals that convert to contracts (target > 70%)
- **Client folder creation time**: < 2 hours (after signature)

---

**Last reviewed**: 2026-04-23  
**Next review**: After first new client through full pipeline (target: 2026-05-15)  
**Known gap**: Refactor client-onboarding SKILL to create GDrive folders (currently still using Notion) — target: 2026-04-28
