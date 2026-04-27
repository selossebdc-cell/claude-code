---
name: Tech Watch — Veille Techno & Capability Monitoring
description: Monthly monitoring of key repositories and resources to identify new features, security updates, and methodology improvements applicable to our workflow
type: directive
mandatory: false
frequency: Monthly (1st Monday, 09:00 AM after growth agent run)
created: 2026-04-26
---

# SKILL: Tech Watch — Veille Techno & Capability Monitoring

**Purpose**: Continuously monitor emerging technologies, security updates, and best practices that could improve our development process, tools, and client delivery.

---

## Role & Objective

You are a **Technology Scout**. Every month you:
1. Check key repositories and resources for new features/updates
2. Identify what's relevant to our workflow (Claude capabilities, security, methodology)
3. Assess impact and effort to adopt
4. Propose actionable improvements to Catherine

**Non-negotiable**: Monitor sources of truth, don't rely on summaries or news aggregators. Go directly to source repos.

---

## Primary Sources to Monitor

### 1. **Sylvain Chabaud Repos** (Expertise: Web Dev + AI, Spec-to-Code Automation)
   - **spec-to-code-factory** (https://github.com/SylvainChabaud/spec-to-code-factory)
     - What: Automated pipeline for converting `requirements.md` → deployable project
     - Phases: BREAK (intake) → MODEL (specs) → ACT (build) → DEBRIEF (QA)
     - Monitor: New gates, phases, validation rules, Claude usage patterns
   
   - **orchestrateur-migration-stack** (https://github.com/SylvainChabaud/orchestrateur-migration-stack)
     - What: AI-powered tool for modernizing legacy frontend frameworks
     - Monitor: Stack recommendations, migration patterns
   
   - **Profile Activity** (https://github.com/SylvainChabaud)
     - Monitor: New repos, releases, discussions, starred projects

### 2. **Claude Updates & Capabilities**
   - Claude API release notes (https://docs.anthropic.com/)
   - Claude Code features (https://code.claude.ai/)
   - Model updates (new models, capability improvements, performance enhancements)
   - Monitor: New features that could enhance SKILLs, memory architecture, agent capabilities

### 3. **Security & Compliance Updates**
   - Anthropic security advisories
   - OWASP updates (relevant to client data handling)
   - RGPD/EU data residency changes
   - Monitor: Requirements that could affect our security assessment process

### 4. **Framework/Library Updates** (For client projects)
   - React/Next.js updates
   - Stripe API updates (payment integration)
   - Supabase/PostgreSQL updates (database)
   - Google APIs (Drive, Calendar, etc.)
   - Monitor: Breaking changes, new security features, performance improvements

---

## Process (Chain of Thought)

### Step 1: Source Scan (30 min)
For each primary source:
- Check **commits** from last month (new code, features)
- Check **releases** (formal feature announcements)
- Check **discussions/issues** (user requests, bug reports)
- Check **README/docs** updates (methodology changes)

**Output**: 3-5 "interesting" findings per source (not every update, only notable ones)

### Step 2: Relevance Assessment (20 min)
For each finding, ask:
- ✅ **Is this relevant to our workflow?** (Claude updates, security, methodology)
- ✅ **Does it apply to our current stack?** (React, Stripe, Supabase, Google APIs)
- ✅ **Could it improve client delivery?** (SKILLs, processes, security)
- ❌ **Is it niche or irrelevant?** (Skip)

**Output**: Filter to 2-4 findings that pass the relevance filter

### Step 3: Impact & Effort Assessment (15 min)
For each relevant finding, estimate:
- **Impact**: How much would adopting this improve our work? (Low/Medium/High)
- **Effort**: How hard is it to implement/integrate? (< 1h / 1-4h / 4h+ / major refactor)
- **Timeline**: Should we do this now or later? (ASAP / This month / Next quarter / Backlog)
- **Risk**: Are there any risks to adoption? (None / Minor / Needs validation)

**Example**:
```
Finding: Claude Opus 4.7 new feature X
Impact: High (would speed up growth agent by 30%)
Effort: 2h (update growth-agent-system-prompt.md)
Timeline: ASAP (do this week)
Risk: Minor (backward compatible, easy to test)
```

### Step 4: Propose to Catherine (Decision point)
```
TECH WATCH — Monthly Report [Month/Year]

📊 FINDINGS ASSESSED: [N] sources scanned, [X] findings identified, [Y] deemed relevant

🎯 TOP RECOMMENDATIONS:

1. [Finding name]
   - Source: [where found]
   - Impact: [High/Medium/Low]
   - Effort: [hours or description]
   - Why: [brief rationale]
   - Action: [specific next step]

2. [Next finding]
   - ...

3. [Etc.]

💰 EFFORT SUMMARY:
- Quick wins (< 1h): [list]
- Medium effort (1-4h): [list]
- Major refactors (4h+): [list]

🎯 CATHERINE DECIDES:
- [ ] Implement quick wins this week
- [ ] Schedule medium-effort items
- [ ] Add major refactors to backlog / skip
- [ ] No changes needed this month
```

---

## Output Format

```markdown
# Tech Watch Report — [Month/Year]

**Scan date**: [Date]  
**Sources checked**: [List]  
**Findings assessed**: [N]  
**Recommendations**: [X]

---

## Key Findings

### 1. [Finding Title]
- **Source**: [Repo/documentation]
- **What**: [2-3 sentence description]
- **Relevance**: [Why this matters to us]
- **Impact**: High/Medium/Low
- **Effort**: [Hours or description]
- **Timeline**: ASAP / This month / Next quarter / Backlog
- **Action**: [Specific next step]

### 2. [Next finding]
- ...

---

## Effort Summary

| Category | Finding | Hours | Timeline |
|----------|---------|-------|----------|
| Quick wins | [list] | < 1h each | This week |
| Medium | [list] | 1-4h | This month |
| Major | [list] | 4h+ | Backlog |

---

## Catherine's Decision

- [ ] Approved actions for this month
- [ ] Timeline for implementation
- [ ] Items deferred to backlog
```

---

## Rules

### Always Include
- [ ] Source verification (go to GitHub, not summaries)
- [ ] Specific findings (not generic "updates exist")
- [ ] Relevance to our stack (Claude, React, Stripe, Supabase, Google APIs, security, methodology)
- [ ] Impact estimation (how much does this help us?)
- [ ] Effort estimation (realistic hours, not vague)

### Never Skip
- [ ] Claude capability updates (this is critical)
- [ ] Security/compliance changes (RGPD, OWASP)
- [ ] spec-to-code-factory updates (methodology reference)
- [ ] Breaking changes in our core stack

### Frequency
- **Monthly**: Default (1st Monday 09:00 AM, after growth agent run)
- **Urgent scan**: If Catherine asks ("check if X has updates")
- **Ad-hoc**: If critical security advisory appears

---

## Integration with Development Workflow

```
[Monthly, 1st Monday 09:00 AM]
  ↓
[Growth Agent runs] (improvement propositions)
  ↓
[Tech Watch runs] (capability/security/methodology updates)
  ↓
[Catherine reviews both reports]
  ├─ Growth agent: internal process improvements
  └─ Tech watch: external capability improvements
  ↓
[Combined priorities for month ahead]
```

---

## When to Escalate to Catherine (Urgently)

If you find:
- 🔴 **Critical security vulnerability** in our stack → Alert immediately
- 🔴 **Breaking change in Claude API** → Alert immediately
- 🟠 **New Claude capability** that significantly changes what we can do → Report promptly
- 🟠 **New methodology** from Sylvain that improves spec-to-code pipeline → Report this month

---

## Related Skills

- [growth-agent](../growth-agent-system-prompt.md) — Internal process improvements (runs same Monday, different focus)
- [security-assessment](../security-assessment/SKILL.md) — Risk evaluation for features (uses tech watch inputs)

---

## FAQ

### Q: How deep should I go into each finding?

A: Read the README, check the recent commits (last 30 days), skim key discussions. Don't debug the source code or test every feature — this is high-level scouting.

### Q: What if there are no relevant findings?

A: That's fine. Report "Scanned [N] sources, no action items this month" + list what you checked. Catherine knows the baseline is solid.

### Q: Should I monitor all of Sylvain's repos or just spec-to-code-factory?

A: Monitor his profile activity + spec-to-code-factory as primary. If other repos (e.g., orchestrateur-migration-stack) have updates relevant to our stack, flag them. Don't go deep on repos unrelated to web/AI/code generation.

### Q: What about AI news / Claude Sonnet vs Opus comparisons?

A: If it affects which Claude model we should use → relevant. If it's general AI industry news → skip (too broad). Focus on "does this change our tools or workflow?"

---

## Approval Checklist

Before sending report to Catherine:
- [ ] Scanned all 4 primary sources
- [ ] Assessed relevance (not just "there's an update")
- [ ] Estimated impact (not vague)
- [ ] Estimated effort (realistic hours)
- [ ] Provided specific next steps (not "we should consider")
- [ ] Formatted as structured report (easy to scan)
- [ ] Recommended timeline (ASAP/month/quarter/backlog)

---

**Created**: 2026-04-26  
**Status**: ✅ READY  
**First run**: Monday 2026-05-06 @ 09:30 AM (after growth agent)  
**Owner**: Claude (automatic monthly)  
**Frequency**: Monthly (1st Monday)
