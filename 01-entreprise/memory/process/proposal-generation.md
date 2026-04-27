---
name: Proposal Generation — From Audit to Contract
description: End-to-end proposal workflow from Fillout audit form through HTML generation to signature
type: process
last_update: 2026-04-23
---

# Proposal Generation — From Audit to Contract

## Overview

Proposal generation turns audit findings into a polished, branded commercial document. We use:
1. **Fillout** — Client fills audit questionnaire (business model, challenges, timeline)
2. **Claude** — Proposal SKILL synthesizes audit + prospect memory → HTML
3. **HTML** — Styled, professional document sent for review + signature

---

## Phase 1: Audit Questionnaire (client, 15-30 min)

**Goal**: Capture prospect's situation, challenges, timeline, budget in structured format.

### Setup
- Create Fillout form: `Audit Initial` (reused for all prospects)
- Form fields:
  - **Company Info**: name, sector, # employees, website
  - **Contact**: first name, last name, role, email, phone
  - **Current Situation**: 
    - Time allocation (% operational vs strategic vs management)
    - Main tools used
    - Team capacity (# people helping, skills)
  - **3 Main Challenges**: (open-ended, prioritized)
  - **Goals for Next 6 Months**: (what's the vision?)
  - **Timeline**: (when do you need this ready?)
  - **Budget**: (rough range: <50k, 50-100k, 100-200k, >200k)
  - **Success Metrics**: (how will we know we succeeded?)

### Prospect workflow
1. Schedule audit meeting
2. Send Fillout link + deadline ("Please fill before our meeting")
3. Prospect completes form
4. We review form before session to prep

**Output**: Fillout form data → download as JSON or CSV

---

## Phase 2: Audit Session (Catherine, 2-3 hours)

**Goal**: Deep-dive into current state, validate questionnaire, identify 3 main problems.

### Before session
- Review prospect memory (if first contact)
- Review Fillout questionnaire
- Prep questions based on their answers
- Send prep email: "Here's what we'll cover..."

### During session
- Walk through business model (confirm questionnaire)
- Deep-dive on 3 challenges: root cause, impact, timeline
- Understand constraints (budget, team, timeline)
- Identify quick wins (things we could do first)
- Discuss engagement: 6 months? Multiple phases? Team training?

### After session
- Write audit CR (file in prospect memory)
- Extract: 3 main problems, proposed solution phases, timeline, estimated cost
- Next: Generate proposal

**Output**: Audit CR + synthesis (3 problems, 3 phases, cost estimate)

---

## Phase 3: Proposal Generation (Catherine, <1 hour with SKILL)

**Goal**: Turn audit + prospect memory into polished HTML proposal.

### Inputs to proposal-generator SKILL
- **Prospect memory** (from `/02-clients/prospects/[name]/[name].md`):
  - Company info, contact, challenge, initial assessment
- **Audit findings** (from CR):
  - 3 main problems + root causes
  - Proposed solution (3 phases)
  - Estimated timeline
  - Cost estimate
- **Engagement type**:
  - "Accompagnement" (18 sessions, 6 months)
  - "Data/KPI" (module-based)
  - "Cloud Team" (implementation support)

### SKILL process
The `proposal-generator` SKILL:
1. Reads prospect memory + audit CR
2. Structures proposal:
   - Executive summary (problem + solution, 1 page)
   - "Your 3 Challenges" section (maps each problem to a phase)
   - Timeline (6 months, week-by-week phased plan)
   - Investment (cost breakdown by phase)
   - Success criteria (KPIs at end of engagement)
   - Company logo + branding
3. Formats as HTML (styled, professional, print-ready)
4. Outputs to: `/02-clients/prospects/[name]/proposition-[date].html`

### Quality checks
- [ ] Company info correct (name, address, contact)
- [ ] Problems accurately summarized (matches audit)
- [ ] Solution logically flows (problem → phase → outcome)
- [ ] Timeline is realistic (18 sessions over 6 months = ~2/week)
- [ ] Cost is competitive (compare to market + our standard rates)
- [ ] HTML renders correctly (links, formatting, logo)
- [ ] No typos or inconsistencies

**Output**: Polished HTML proposal + saved to prospect folder

---

## Phase 4: Proposal Review & Refinement (async, 1-3 days)

**Goal**: Iterate on proposal based on feedback before sending to prospect.

### Internal review (Catherine alone)
- Read proposal as if you're the prospect
- Does it address their challenges clearly?
- Is the cost reasonable?
- Does timeline align with their stated needs?
- Tone: professional, confident, not overpromising?

### Revisions
If changes needed:
- Edit HTML directly (or re-run SKILL with adjusted inputs)
- Common adjustments:
  - Timeline (shift phases if client needs results faster)
  - Cost (adjust if initial estimate was off)
  - Scope (add/remove modules based on audit)
  - Tone (make more casual or formal based on client style)

### Final sign-off
- Get proposal to "ready to send" state
- Schedule: when to send to prospect?
  - Ideal: within 3 days of audit (momentum)
  - Latest: within 1 week (grows stale)

**Output**: Final proposal HTML ready for prospect

---

## Phase 5: Prospect Review & Negotiation (async, 3-5 days)

**Goal**: Prospect reviews, asks questions, we negotiate contract terms.

### Send proposal
- Email: prospect + anyone else who needs to approve (finance, partner, etc.)
- Message:
  ```
  Hi [Name],
  
  Following our audit on [date], I've prepared a proposal for your 6-month engagement.
  
  Key highlights:
  - 3 phases addressing your [challenge 1], [challenge 2], [challenge 3]
  - Timeline: [X] weeks to full implementation
  - Investment: [Y]€
  
  Attached: full proposal (HTML) + roadmap (PDF)
  
  Next steps:
  1. Review with your team (deadline: [date])
  2. Any questions? Let's do a quick call
  3. Once approved: we'll send contract for signature
  4. After signature + 50% deposit: we schedule your first session
  
  Looking forward to partnering!
  Catherine
  ```

### Prospect questions
- "Can we do [phase] faster?" → adjust timeline
- "Is [tool] included?" → clarify scope
- "What if [scenario]?" → address concerns
- "Can we negotiate price?" → be clear on margins, offer value-adds instead (extra sessions, training, etc.)

### Negotiation rules
- **Timeline**: flexible (can compress or extend, affects cost)
- **Cost**: small wiggle room (5-10% discount if paying upfront, or adding features for same price)
- **Scope**: don't reduce core 3 phases (but can shift phases or add modules)
- **Modules**: Data/KPI or Cloud Team can be added on (upsell if mentioned)

### Approval flow
- Prospect approves (email: "looks good, let's sign")
- Move to Stage 3: Contract + Payment (in client-onboarding process)

**Output**: Proposal approved by prospect + ready for contract

---

## Phase 6: Contract & Payment (integration with client-onboarding)

See: `/process/client-onboarding.md` → Stage 3: Proposal & Contract

---

## Proposal Standards

### Content Requirements
Every proposal must include:
- **Executive summary** (what we're solving, why it matters) — 1 page
- **Your challenges** (mapped to our 3 phases) — 2-3 pages
- **Our approach** (what we'll do in each phase) — 2-3 pages
- **Timeline** (week-by-week or month-by-month) — 1 page
- **Investment** (cost breakdown, payment terms) — 1 page
- **Success criteria** (KPIs you'll measure at end) — 1 page
- **Appendix** (FAQs, team bios, references if relevant) — optional

### Format Requirements
- **Format**: HTML (styled with company branding)
- **Styling**: Professional, clean, readable (not overly fancy)
- **Tone**: Confident but realistic (no overcommitments, no heroic language)
- **Length**: 8-12 pages total (no longer)
- **Deliverable**: Single HTML file (no external stylesheets/images if possible)

### Tone Guidelines
- **Use**: qualifiers like "typically", "usually", "often", "can expect"
- **Avoid**: absolute guarantees ("we will triple your revenue")
- **Avoid**: vacation/personal references (stay professional)
- **Avoid**: assuming delegation ("your team will implement")
- **Focus**: "we'll help you X" not "you'll automatically get X"

---

## Proposal-Generator SKILL

Location: `/01-entreprise/skills/proposal-generator/SKILL.md`

### Inputs
- Prospect name, company, contact email
- 3 main problems (from audit CR)
- Proposed solution (3 phases, timeline)
- Cost estimate (total + breakdown)
- Engagement type (Accompagnement, Data/KPI, Cloud Team)
- Company branding (logo URL, colors, fonts)

### Process
1. Validate inputs (all required fields present)
2. Structure proposal outline
3. Generate each section (executive summary, challenges, approach, timeline, investment, success criteria)
4. Apply branding (logo, colors, fonts)
5. Convert to HTML
6. Save to `/02-clients/prospects/[name]/proposition-[date].html`

### Output
- HTML file (self-contained, print-ready)
- Status: "ready for review" or "needs refinement"

---

## Metrics & KPIs (tracked by growth agent)

- **Proposal quality**: % of proposals sent that convert to contract (target > 70%)
- **Proposal turnaround**: days from audit → proposal sent (target < 3 days)
- **Revision cycle**: avg revisions before prospect approval (target < 1.5 revisions)
- **Price negotiation**: avg discount given (target < 5%)
- **Contract signature rate**: % of proposals that get signed contracts (target > 80%)

---

## Troubleshooting

**Prospect asks for "quick version" (1-page summary)**
- Deliver: 1-page executive summary + note: "Full proposal attached for reference"
- They often appreciate quick version for approvals, but still want full details

**Prospect wants to change engagement type mid-review**
- Allowed: "Accompagnement" ↔ "Data/KPI" (similar cost)
- Not allowed: "Full 6-month" → "Just 3 sessions" (changes entire structure)
- If they want partial: offer "you can start with Phase 1 only (3 months)" + option to add phases

**Prospect says "too expensive"**
- Don't immediately discount
- Ask: "What's your budget range?" → see if we can restructure
- Options: 
  - Pay in installments (doesn't reduce cost, spreads payment)
  - Start Phase 1 only, add phases later
  - Add modules (Data/KPI) for same price
  - Offer: "25% discount if you pay upfront" (improves cash flow for us)

**Prospect goes silent after proposal sent**
- Day 3: send gentle follow-up ("any questions?")
- Day 7: second follow-up ("ready to move forward?")
- Day 10: move to "paused" in Airtable + update prospect memory with status

---

**Last reviewed**: 2026-04-23  
**Next review**: After proposal-generator refactor or first new proposal generated (target: 2026-05-01)
