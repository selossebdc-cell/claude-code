---
name: Fred's Claude Implementation Guide
description: Concrete steps to deploy Fred's personalized config in Claude (replaces OpenAI Custom Instructions with Claude-native equivalents)
type: reference
updated: 2026-04-27
---

# Fred's Claude Implementation Guide

## ⚠️ CRITICAL: No "Instructions personnalisées" in Claude

**There is NO settings panel for "Custom Instructions" in Claude.**

Claude has **zero UI** for personalization. Everything is configured via **files**:
- `CLAUDE.md` (text file)
- `settings.json` (config file)
- `~/.claude/memory/client/fred.md` (markdown file)

That's it. No UI panels, no wizards, no settings menus. Just text files.

---

## Step 1: Create Your Project CLAUDE.md

**File**: `.claude/CLAUDE.md` in your project root

⚠️ **Claude has NO "Custom Instructions" settings panel** (that's OpenAI). You configure everything in code, not UI.

This CLAUDE.md is your personalized system configuration.

```markdown
# Fred's Claude Configuration

## Who You Are
- Ingénieur Inventeur, 40+ countries, pragmatic & innovative
- Best productivity: 6h-10h, "feeling informé", deadlines = motivation
- 3 priorities: export compliance, regulatory mapping, commercial

## How Claude Should Work With You
- Direct, pragmatic language (no bullshit)
- Prefer: tables > text, numbers > theory
- Drafts should be readable, not polished (iterate fast)
- Ask before: shipping to production, big decisions, security changes

## Non-Negotiable Rules
1. **Antiphishing**: Read-only on sensitive files (contracts, credentials, banking)
2. **RGPD Strict**: No R&D shared publicly, validate before any data movement
3. **Validation Required**: Before any transaction or production deployment
4. **Weekly Rhythm**: Thursday 17h debrief on market progress

## Your Working Patterns (That Work)
- Deadlines are real motivation (not "soon")
- Export compliance is blocking 40 countries
- Admin is 30% of your time — automate it with n8n
- Weekly rhythm: checkpoint → adjust → execute
```

---

## Step 2: Configure settings.json

**File**: `.claude/settings.json` in your project

```json
{
  "model": "claude-opus-4-7",
  "system_prompt": "You are working with Fred (Ingénieur Inventeur). Key: direct/pragmatic, tables>text, numbers>theory. Ask before: production ships, big decisions, security changes. Antiphishing: read-only on sensitive files.",
  
  "hooks": {
    "sessionStart": "Load Fred's current priorities from ~/.claude/memory/client/fred.md",
    "sessionEnd": "Auto-save session learnings to memory"
  },
  
  "permissions": {
    "bash": ["allowed"],
    "file_operations": {
      "sensitive_files": ["read-only"],
      "contracts": ["read-only"],
      "credentials": ["read-only"]
    }
  }
}
```

---

## Step 3: Set Up Memory (Ma Mémoire in Claude)

**Structure**:
```
~/.claude/memory/client/fred.md
  └─ Current priorities
  └─ Market progress tracking
  └─ Blockers & solutions
  └─ Operational guidelines
```

**Copy this to ~/.claude/memory/client/fred.md**:
```markdown
# Fred's Operational Memory

## 🎯 Current Priorities (This Week)
- [ ] Priority 1: [Your actual blocker]
- [ ] Priority 2: [Market you're focusing on]
- [ ] Priority 3: [Automation to build]

## 📊 Market Progress (Track Weekly)
| Market | Status | Blocker | ETA |
|--------|--------|---------|-----|
| France | Live | - | - |
| Germany | In Dev | Regulatory mapping | 2026-05-15 |
| Spain | Planned | Compliance audit | 2026-06-01 |

## 🚫 Known Blockers
- **Export Conformity**: Regulatory requirements for 40+ countries
- **Admin Time**: ~30% of week spent on manual docs → n8n opportunity
- **Session Coordination**: Weekly Thursday 17h = hard deadline

## ✅ Patterns That Work
- Deadlines motivate me (not "soon")
- Weekly checkpoint-adjust-execute rhythm
- Table format for decisions (not paragraphs)
```

---

## Step 4: Schedule Your Weekly/Daily Tasks

**Use Claude's `schedule` skill** to automate your 3 recurring tasks:

### Daily Briefing (6h30)
```bash
claude /schedule "daily 6h30"
Prompt: "Good morning Fred. What are today's top 3 priorities based on ~/claude/memory/client/fred.md? Show market status."
```

### Weekly Coach Debrief (Thursday 17h)
```bash
claude /schedule "weekly thursday 17h"
Prompt: "Fred, debrief time. (1) What moved this week? (2) What blocked? (3) What's your rhythm for next week? Update ~/claude/memory/client/fred.md with progress."
```

### Monthly Compliance Alert (1st of month)
```bash
claude /schedule "monthly 1st 09:00"
Prompt: "Fred, monthly compliance check. Scan your 40 markets for regulatory changes that impact your export roadmap. Flag any urgent changes."
```

---

## Step 5: Create Specialized Workflows (Replaces "Agents")

These are SKILLs you can invoke when needed. Create `.claude/skills/` directory:

### fred-engineer.md (Conformity & Multi-Country Validation)
```markdown
# Fred Engineer Workflow

Analyze for: compliance risk, regulatory gaps, country-specific blockers
```

### fred-admin.md (Docs, Templates, Automation)
```markdown
# Fred Admin Workflow

Build: document templates, n8n workflows, automation plans
```

### fred-coach.md (Reflection & Pattern Recognition)
```markdown
# Fred Coach Workflow

Debrief: What moved? What blocked? Patterns? Rhythm adjustments?
```

### fred-security.md (Antiphishing, RGPD, Transactions)
```markdown
# Fred Security Workflow

Validate: No credentials exposed, RGPD compliance, secure before shipping
```

---

## Step 6: Deploy (Simple Checklist)

- [ ] Create `.claude/CLAUDE.md` with your config
- [ ] Create `.claude/settings.json` with system_prompt + hooks
- [ ] Create `~/.claude/memory/client/fred.md` with your priorities
- [ ] Run `claude /schedule` for daily (6h30), weekly (Thu 17h), monthly (1st)
- [ ] Test one workflow (e.g., fred-engineer for a compliance check)
- [ ] Verify memory loads at session start

---

## What You Get

✅ **Personalized Claude** — Every session loads your priorities, blockers, patterns  
✅ **Weekly Rhythm** — Auto-briefings (daily), debrief (Thursday), compliance alerts (monthly)  
✅ **Specialized Workflows** — Engineer/Admin/Coach/Security workflows at your fingertips  
✅ **Security Locked** — Read-only on sensitive files, validated transactions  
✅ **Pragmatic Style** — Direct, tables, numbers, no BS  

---

## Troubleshooting

**"Memory not loading at session start"**
→ Check `~/.claude/memory/client/fred.md` exists and is readable

**"Scheduled tasks not running"**
→ Run `claude /schedule list` to see what's active

**"System prompt not being used"**
→ Verify `.claude/settings.json` is in your project root (not home dir)

**"Need to update priorities mid-week"**
→ Edit `~/.claude/memory/client/fred.md` directly — next session will load it

---

**Status**: Ready to deploy  
**Next Step**: Follow the 6-step checklist above  
**Questions**: Reference `/memory/reference/fred-config-standard.md` for the design rationale
