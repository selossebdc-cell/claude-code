---
name: Session Report Automation V2
description: Automated end-of-session CR generation with WhatsApp/Telegram validation and Portail V2 sync
type: project
---

# Session Report Automation V2 — Projet en cours

**Status**: Requirements gathering (2026-04-27)  
**Priority**: High (repetitive manual process, 3+ clients)  
**Timeline**: TBD (awaiting clarifications)

## Context & Problem

**Current state**: Manual CR generation after each client session
- Multiple input sources: Claude Plaud, Fireflies (client tool), Fathom, manual notes
- **No single tool standardized** — unpredictable which tool will be used
- Manual process: transcript → CR generation → Notion → actions → memory updates → portal sync

**Desired state**: Automated CR pipeline with human validation
- Catherine triggers: "CR session Fred + [transcript]"
- Claude generates complete CR + extracts actions + proposes LinkedIn insights
- Catherine validates via **WhatsApp Business or Telegram** (client preference TBD)
- Python agent publishes everything automatically

## Architecture Overview

### Input (Flexible)
- Any transcript format: Claude Plaud, Fireflies, Fathom, or plain text notes
- Catherine manually triggers (will remain manual — no single tool to auto-detect)

### Generation Pipeline
1. **Claude processes transcript** → generates CR in structured format
2. **Extract components**:
   - Full CR (Markdown + YAML frontmatter)
   - Client actions (prioritized by color: 🔴🟠🟡)
   - Catherine actions
   - LinkedIn nuggets (pour contenu futur)
   - Next session details

3. **Python agent formats proposal** for validation
4. **Send to Catherine** via WhatsApp/Telegram with interactive approval buttons

### Publication (Upon Approval)
- Create `/02-clients/[client]/sessions/cr-session[N]-[client].md`
- Update `/02-clients/[client]/SESSIONS.md` (add entry to index)
- Enrich `/02-clients/[client]/[client].md` (memory file):
  - Session counter (+1)
  - Session history table (date, theme, decisions, progress)
  - Patterns & observations
  - LinkedIn nuggets collected
- Update Portail V2:
  - Create actions for client (status: "À faire", assigned to client)
  - Create actions for Catherine (status: "À faire", assigned to Catherine)
  - Link CR in client dashboard
- Git commit + push automatically

## Key Data Structures

### CR Format (Markdown + YAML frontmatter)
```yaml
---
client: [NAME]
entreprise: [COMPANY]
session: [N]
date: YYYY-MM-DD
duree: Xh
theme: [TITLE]
lien_fathom: [URL]
prochaine_session: [DATE] [TIME]
---
```

### Client Folder Structure
```
02-clients/[client]/
├── [client].md          # Memory: identity, patterns, context
├── SESSIONS.md          # Index of all sessions
├── SUIVI.md            # Phase tracking (diagnostic → design → deploy)
├── STATUS.md           # Current status
├── NOTES.md            # Raw notes
└── sessions/
    ├── cr-session1-[client].md
    ├── cr-session2-[client].md
    └── cr-session3-[client].md
```

### Memory File (client.md)
Contains:
- Identity: entreprise, sector, program length, sessions used
- Profile: personality, communication style, tools, neuro-diversity notes
- Patterns observed: what works, blockers, recurring themes
- Key quotes & insights
- Outils actuels: every tool they use + config details
- LinkedIn nuggets: quotes/situations for future content

**Key field**: `Sessions: X / 18` (e.g., 10/18 = 10 used of 18 total)

## Open Questions (TBD)

### 1. Validation Channel
- [ ] WhatsApp Business? (need: business account URL + webhook)
- [ ] Telegram? (need: bot token + Catherine's chat ID)
- [ ] Who decides? **CATHERINE to confirm**

### 2. Portail V2 Integration
- [ ] Where is Portail V2? (Supabase? Other?)
- [ ] API endpoint for creating actions?
- [ ] How to link CR? (direct file URL in Google Drive? Share link?)
- [ ] Who decides structure? **CATHERINE to clarify**

### 3. LinkedIn Nuggets Storage
- [ ] Centralized doc for all nuggets across clients?
- [ ] Or per-client in memory file (client.md)?
- [ ] Who reviews & proposes posts? **CATHERINE to decide**

### 4. NOTION Legacy Code
- **CRITICAL**: Old `session-report/SKILL.md` still references Notion
- All Notion IDs in `fred.md` (Dashboard, Meeting Agendas, Objectifs & Actions) are now **OBSOLETE**
- Suggestion: Update SKILL.md to remove all Notion references before building agent

## Implementation Phases

### Phase 1: Foundation (Build Agent)
- [ ] Python agent skeleton (input → CR generation → output proposal)
- [ ] CR template + frontmatter generator
- [ ] Action extraction (client vs Catherine, priority colors)
- [ ] LinkedIn nugget extractor
- [ ] File system integration (write to client folder)

### Phase 2: Validation Channel (Integrate WhatsApp or Telegram)
- [ ] Setup webhook or bot
- [ ] Send proposal with approval buttons
- [ ] Handle Catherine's response (validate / modify / reject)
- [ ] Iterate on modifications if needed

### Phase 3: Publication Automation
- [ ] Git operations (create file, commit, push)
- [ ] Update SESSIONS.md
- [ ] Update memory file (client.md)
- [ ] Update Portail V2 (if API available)

### Phase 4: UX Polish
- [ ] Create CLI command `/session-report-auto` or similar
- [ ] Preview before publishing
- [ ] Rollback mechanism (undo last publish)

## Next Steps

1. **Catherine clarifies**:
   - WhatsApp Business or Telegram?
   - Portail V2 location + API?
   - LinkedIn nuggets centralized or per-client?

2. **Claude updates SKILL.md**:
   - Remove all Notion references
   - Repoint to Google Drive structure
   - Document new Python agent integration

3. **Build agent** (once approvals clear)

---

**Created**: 2026-04-27 (in-conversation discovery)  
**Last modified**: 2026-04-27  
**Owner**: Catherine  
**Status**: Awaiting clarifications before build
