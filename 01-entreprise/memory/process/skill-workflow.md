---
name: SKILL Workflow — Build & Refactor Process
description: How we build, test, deploy, and maintain SKILLs — includes Notion→GDrive migration checklist
type: process
last_update: 2026-04-23
---

# SKILL Workflow — Build & Refactor Process

## Overview

A SKILL is a repeatable Claude workflow (usually template-based prompt + reference docs) that automates or semi-automates a business process. Each SKILL has:
- A `SKILL.md` file (prompt template + instructions)
- Reference docs (`/references/` folder)
- Test cases and success criteria
- Integration points with other systems

---

## Phase 1: Discovery & Design (Async, 1-2 days)

**Goal**: Define what problem the SKILL solves and what it needs.

### Steps
1. **Problem statement**
   - What's currently manual or broken?
   - Who does it? How often? How long?
   - What would success look like?

2. **Input requirements**
   - What data must the SKILL read? (files, APIs, forms)
   - Where does it live? (Google Drive, databases, web forms)
   - Who provides it?

3. **Output requirements**
   - What should the SKILL produce? (file, email, entry, code)
   - Where should it go? (Google Drive path, API endpoint, email)
   - What format? (markdown, HTML, JSON, plain text)

4. **Dependencies**
   - Does this SKILL depend on others? (e.g., proposal-generator → client-onboarding)
   - Are there blockers? (e.g., waiting on Brevo API access)
   - Timeline: can this ship independent of other work?

**Output**: 1-page design doc (problem + inputs/outputs/deps)

---

## Phase 2: Reference Docs & Prompts (Async, 2-3 days)

**Goal**: Create everything the SKILL needs to work correctly.

### Steps
1. **Create reference templates**
   - Example inputs (3-5 real examples)
   - Expected outputs (before/after samples)
   - Edge cases (what should fail gracefully?)
   - Success criteria (how do we know it worked?)

   Location: `/01-entreprise/skills/[skill-name]/references/`

2. **Write SKILL.md prompt**
   - Role definition (who is the AI in this workflow?)
   - Context (what's the business goal?)
   - Instructions (step-by-step)
   - Input format (what data structure?)
   - Output format (what should be produced?)
   - Examples (2-3 real test cases)

   Location: `/01-entreprise/skills/[skill-name]/SKILL.md`

3. **Integration checklist**
   - Where does input come from?
   - Where does output go?
   - Who needs to do what manually before/after?
   - Are there approval steps?

**Output**: SKILL.md + 2-3 reference docs + integration diagram

---

## Phase 3: Test & Validate (Catherine, 1 session)

**Goal**: Verify the SKILL works on real data before deploying.

### Steps
1. **Manual test run**
   - Use real client data (not examples)
   - Run through SKILL.md prompt manually (simulate)
   - Check: inputs parse correctly?
   - Check: outputs go to right place?
   - Check: formatting is correct?

2. **Edge case testing**
   - What if input is incomplete?
   - What if there are special characters?
   - What if output exceeds size limits?

3. **Integration test**
   - Does the next SKILL in chain work?
   - Does it read from where we're writing?
   - Are there permission issues?

4. **Feedback & fix**
   - Document what didn't work
   - Update SKILL.md, reference docs, templates

**Output**: Test report + SKILL.md ready for production

---

## Phase 4: Deployment (Catherine, <1 hour)

**Goal**: Make the SKILL live and documented.

### Steps
1. **Version the SKILL**
   - Commit SKILL.md + references to GitHub
   - Tag as `skill-[name]-v1.0`
   - Update MEMORY.md → `/process/skill-workflow.md`

2. **Document in MEMORY**
   - Add to process/skill-workflow.md: what this SKILL does, inputs/outputs
   - Update `/MEMORY.md` index if new SKILL

3. **Set up monitoring**
   - Who owns running this SKILL? (Catherine, team member, automated?)
   - How often? (daily, per client, on-demand)
   - Who gets alerts if it fails?

**Output**: SKILL live, documented, monitored

---

## Phase 5: Maintenance & Refactor (Ongoing)

**Goal**: Keep SKILLs accurate as business changes.

### When to refactor
- Reference data moves (e.g., Notion → Google Drive) = full refactor
- Business process changes (e.g., new approval step) = prompt update
- New edge cases discovered = add handling
- Integration point changes (e.g., new API) = test + update

### Refactor checklist
- [ ] Update SKILL.md instructions if process changed
- [ ] Update reference docs if data sources changed
- [ ] Re-test with real data
- [ ] Update integration points
- [ ] Commit with message: `refactor(skill-[name]): [what changed]`
- [ ] Update MEMORY.md → process/skill-workflow.md with change notes

---

## Current SKILLs (as of 2026-04-23)

| SKILL | Status | Owner | Last Updated | Notes |
|-------|--------|-------|--------------|-------|
| proposal-generator | ✅ Live | Catherine | 2026-04-23 | Creates HTML propositions for prospects |
| client-onboarding | 🟡 Needs refactor | Catherine | 2026-04-15 | Still creates Notion dashboards (should be GDrive folders) |
| session-report | 🟡 Needs refactor | Catherine | 2026-04-15 | Still writes to Notion (should be SESSIONS.md) |
| linkedin-content | ✅ Live | Catherine | 2026-04-23 | Processes events → inbox LinkedIn |
| brand-identity | ✅ Live | Catherine | 2026-04-23 | Visual identity reference (no Notion) |
| weekly-planner | ✅ Live | Catherine | 2026-04-23 | Aggregates GDrive sources |
| agenda-writer | ✅ Live | Catherine | 2026-04-23 | Writes calendar events from GDrive |
| invoice-generator | ✅ Live | Catherine | 2026-04-23 | Creates invoices via Shine + Stripe |
| admin-billing | ✅ Live | Catherine | 2026-04-23 | Post-signature billing automation |

---

## Known Refactors In Progress

### session-report → SESSIONS.md
- **Why**: Notion deprecation, consolidate to GDrive
- **Timeline**: Week of 2026-04-28
- **Change**: Write CRs to `/02-clients/[client]/SESSIONS.md` instead of Notion dashboards
- **Impact**: SESSIONS.md becomes source of truth for session history

### client-onboarding → GDrive folders
- **Why**: Notion deprecation, build folder structure instead of dashboard
- **Timeline**: Week of 2026-04-28
- **Change**: Create `/02-clients/[prospect]/` folder structure (NOTES.md, STATUS.md, etc.) instead of Notion page
- **Impact**: New clients onboarded to GDrive from day 1 (no Notion)

---

## Integration Map

```
proposal-generator
  └─→ outputs HTML to `/02-clients/prospects/[name]/proposition-[date].html`
  └─→ feeds context to client-onboarding

client-onboarding  
  └─→ creates `/02-clients/[client]/` folder structure (NOTES.md, SESSIONS.md, etc.)
  └─→ triggers roadmap-generator

roadmap-generator
  └─→ reads NOTES.md, SESSIONS.md, SUIVI.md
  └─→ outputs `/02-clients/[client]/feuille-de-route.md`

session-report
  └─→ reads feuille-de-route.md, prior CRs
  └─→ writes to `/02-clients/[client]/SESSIONS.md`
  └─→ updates NOTES.md with patterns

weekly-planner
  └─→ reads all `/02-clients/[client]/SUIVI.md` files
  └─→ reads `/01-entreprise/inbox/`
  └─→ generates weekly planning view

invoice-generator
  └─→ reads `/02-clients/[client]/STATUS.md` for contract info
  └─→ creates invoice via Shine
  └─→ generates Stripe payment link
  └─→ updates STATUS.md with invoice ID
```

---

## Standards

### SKILL.md Structure (required)
Every SKILL.md must have:
- **Role** section (who is the AI?)
- **Context** section (business goal)
- **Inputs** section (data required, format, location)
- **Process** section (step-by-step instructions)
- **Output** section (what gets produced, where it goes)
- **Examples** section (2-3 real test cases)
- **Error handling** section (what if X goes wrong?)

### Reference Docs (required)
Every SKILL needs at least:
- `template-[input-format].md` or `.html` (example input)
- `template-[output-format].md` or `.html` (example output)
- `success-criteria.md` (how to verify it worked)

### Testing (required before deployment)
- [ ] Manual test with real data (not examples)
- [ ] Edge cases tested (incomplete data, special chars)
- [ ] Integration test (works with upstream/downstream SKILLs)
- [ ] Documented: what worked, what didn't

---

**Last reviewed**: 2026-04-23  
**Next review**: After session-report and client-onboarding refactors (target: 2026-04-30)
