---
name: "Technical Blockers"
type: "technical"
last_update: "2026-04-24"
---

# 🔴 Blockers Actifs

Tous les blocages qui empêchent la progression. Chaque lundi, l'agent vérifie ceux qui sont résolus.

## 1. FSY Circle Migration — Brevo Sync

**Status**: 🔴 BLOCKED  
**Since**: 2026-04-15 (9 jours)  
**Owner**: Michael (integration dev)  
**Impact**: FSY cannot bill 78 clients until resolved (revenue risk)

### Problem
- Brevo API returns 401 (auth issue or key rotated)
- Contact list sync failing for 2500+ contacts
- Cannot send invoices via Circle automated workflow

### Root Cause
[TBD — awaiting Michael's investigation]

### Dependencies
- Michael's availability (partial, competing priorities)
- Brevo support response (slow)

### Solution in Progress
1. [ ] Verify Brevo API key in .env
2. [ ] Check Brevo contact sync logs
3. [ ] Test with fresh API token
4. [ ] If still fails: escalate to Brevo support

**Unblocks**: Portail V2 payment links, Circle billing automation

---

## 2. Portail V3 Design — Scope Creep

**Status**: 🟡 IN PROGRESS  
**Since**: 2026-03-01 (54 days — overdue)  
**Owner**: [Design person?]  
**Impact**: All new clients stuck on V2 (temporary workaround)

### Problem
- V3 scope keeps expanding (multi-tenant, advanced reporting, etc)
- Current design covers basic features only
- No timeline for completion

### Root Cause
- Unclear MVP requirements
- No dedicated designer (shared resource?)
- Perfectionism: aiming for "final product" not MVP

### Solution in Progress
1. [ ] Lock MVP scope (3 features only: sessions, documents, actions)
2. [ ] Define "V3 final" separately (v3.1, v3.2 roadmap)
3. [ ] Get design review by [date]
4. [ ] Start frontend dev by [date]

**Unblocks**: New client onboarding, portail.csbusiness.fr consolidation

---

## 3. Session-Report Skill — Notion References Still Active

**Status**: 🟡 DEGRADED  
**Since**: 2026-04-23 (1 day)  
**Owner**: Claude (refactoring)  
**Impact**: CRs still go to Notion, not Google Drive (inconsistent data)

### Problem
- session-report still writes CRs to Notion dashboards
- client-onboarding still creates Notion dashboards (not Google Drive folders)
- 2 skills out of 10 not refactored in Notion→GoogleDrive migration

### Root Cause
- These 2 skills were excluded from initial 8-skill refactor (out of scope)
- Higher complexity (Notion API calls required)

### Solution in Progress
1. [ ] Refactor session-report to write to SESSIONS.md instead of Notion
2. [ ] Refactor client-onboarding to create GDrive folder structure instead of Notion
3. [ ] Test with 1 client (Fred session next)

**Unblocks**: Complete Notion deprecation, memory consolidation

---

## Resolved (Archive)

*Resolved blockers moved to `/versioning/DECISIONS.md` after 7 days*

---

**Last reviewed**: 2026-04-24  
**Next review**: Monday 2026-04-28 (growth agent scan)
