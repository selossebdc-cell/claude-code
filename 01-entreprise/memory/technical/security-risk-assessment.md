---
name: Security Risk Assessment — Template & Examples
description: Examples of how to evaluate security risks for features, with effort estimates and decision outcomes
type: technical
last_update: 2026-04-26
---

# Security Risk Assessment — Template & Examples

Use this as reference when running the **security-assessment SKILL** before developing features.

---

## Template (Blank)

```markdown
# Security Assessment: [Feature Name]

## Context
- **Feature**: [Description]
- **Data types**: [What data is handled]
- **Users**: [Who has access]
- **Criticality**: [Internal / Client-facing / Public]

## ⚠️ Risks Identified

| Risk | Scenario | Probability | Impact | If Exploited |
|------|----------|-------------|--------|--------------|
| | | | | |

## ✅ Mitigations Proposed

| Risk | Mitigation | Effort | Criticality |
|------|-----------|--------|-------------|
| | | | |

## 💰 Effort Summary
- MUST DO mitigations: X hours
- SHOULD DO mitigations: Y hours
- NICE TO HAVE mitigations: Z hours
- **Total if all**: X+Y+Z hours

## 🎯 Catherine's Decision
- Effort level chosen: ___
- Risks accepted (if any): ___
- Approved on: [date]
```

---

## Example 1: Portail V2 — Add "Comments" Feature

### Context
- **Feature**: Clients can post comments on session documents
- **Data types**: Comments (user-generated text), author identity, timestamps
- **Users**: Client team members (registered users)
- **Criticality**: Client-facing (comments are part of deliverables)

### ⚠️ Risks Identified

| Risk | Scenario | Probability | Impact | If Exploited |
|------|----------|-------------|--------|--------------|
| **XSS (Cross-Site Scripting)** | Attacker posts `<script>alert('hacked')</script>` in comment → steals cookies of other users viewing that comment | Medium | High | Session hijack, account takeover, impersonation |
| **Auth bypass** | Attacker modifies HTTP request to edit/delete comments from OTHER clients (not their own) | Medium | High | Comment tampering, document integrity loss |
| **No audit trail** | Comments posted but no record of who posted when → can't investigate tampering later | Low | Medium | RGPD violation, no compliance audit trail |
| **DB injection** (unlikely but possible) | Comment with SQL-like syntax somehow bypasses sanitization → query executed | Low | CRITICAL | Full database compromise |

### ✅ Mitigations Proposed

| Risk | Mitigation | Effort | Criticality |
|------|-----------|--------|-------------|
| **XSS** | Sanitize all user inputs: use React's auto-escaping + sanitize HTML libs (DOMPurify) | 1h | MUST DO |
| **Auth bypass** | Add RLS policy: comments.user_id must match auth.uid() for UPDATE/DELETE | 1h | MUST DO |
| **Auth bypass** | Add server-side auth check in API route before returning comments from other clients | 1h | MUST DO |
| **No audit trail** | Add audit trigger to comments table (logs who posted what when) | 1.5h | SHOULD DO |
| **DB injection** | Use parameterized queries (Supabase/ORM handles this by default) | 0h | Already done |

### 💰 Effort Summary
- MUST DO mitigations: 3 hours
- SHOULD DO mitigations: 1.5 hours
- NICE TO HAVE mitigations: 0 hours
- **Total if all**: 4.5 hours

### 🎯 Catherine's Decision (Example)
- **Effort level chosen**: MUST DO + SHOULD DO (4.5h total)
- **Risks accepted**: None
- **Approved on**: 2026-04-26
- **Justification**: "Comments are part of client deliverables (high trust). XSS + auth bypass are deal-breakers. Audit trail is RGPD requirement. Worth the 4.5h investment."

**Status**: ✅ APPROVED → Proceed with 4.5h scope

---

## Example 2: Airtable Integration — Sync Prospect Data

### Context
- **Feature**: Automatic sync of prospect info from Airtable → Google Drive `/02-clients/prospects/[name]/`
- **Data types**: Name, company, email, phone, budget (PII + some sensitive business info)
- **Users**: Internal team only (not client-facing)
- **Criticality**: Internal tool (but contains prospect PII)

### ⚠️ Risks Identified

| Risk | Scenario | Probability | Impact | If Exploited |
|------|----------|-------------|--------|--------------|
| **API key leak** | Airtable API key hardcoded in script or logged in errors → attacker uses key to modify prospect data | Medium | High | Prospect data corrupted, false contact info sent |
| **No sync verification** | Script overwrites prospect data with stale Airtable data → newer notes from Claude lost | Medium | Medium | Data loss, overwrites manual updates |
| **No audit trail** | Sync happens silently, no log of "Airtable synced at X time, changed Y fields" → can't investigate issues | Low | Medium | Debugging difficulty, no compliance trail |
| **Unauthorized Airtable access** | Someone with Airtable URL but not authorized in GDrive could trigger sync | Low | Medium | Data exposure, unauthorized modifications |

### ✅ Mitigations Proposed

| Risk | Mitigation | Effort | Criticality |
|------|-----------|--------|-------------|
| **API key leak** | Store Airtable API key in `.env` (not code), use `process.env.AIRTABLE_KEY` | 30min | MUST DO |
| **API key leak** | Add error handler: if API error occurs, log "Airtable sync failed" (no key in logs) | 30min | MUST DO |
| **Sync verification** | Before overwriting, compare new data vs old → only update changed fields | 1.5h | SHOULD DO |
| **No audit trail** | Log sync events: "Synced prospect X at Y time, fields changed: [list]" | 1h | SHOULD DO |
| **Unauthorized access** | Require authentication check before sync starts (only internal auth can trigger) | 1h | SHOULD DO |

### 💰 Effort Summary
- MUST DO mitigations: 1 hour
- SHOULD DO mitigations: 3.5 hours
- NICE TO HAVE mitigations: 0 hours
- **Total if all**: 4.5 hours

### 🎯 Catherine's Decision (Example)
- **Effort level chosen**: MUST DO only (1h)
- **Risks accepted**:
  - "Sync verification" — can be done manually for now (only 1-2 syncs/week)
  - "Audit trail" — prospects are low-risk, can skip for MVP
  - "Unauthorized access" — script runs locally/manual trigger, low risk
- **Approved on**: 2026-04-26
- **Justification**: "This is internal + low-volume integration. API key protection is critical, rest can come later if needed."

**Status**: ✅ APPROVED → Proceed with 1h scope (MUST DO only)

---

## Example 3: Claude Setup App — No Risks Identified

### Context
- **Feature**: Generate Claude configuration based on user input (psychology axes, chat flow, pricing)
- **Data types**: User inputs (text fields), Claude API responses
- **Users**: Internal team only (Taina, etc.)
- **Criticality**: Internal helper app (no client data, no authentication, no persistence)

### ⚠️ Risks Identified

| Risk | Scenario | Probability | Impact | If Exploited |
|------|----------|-------------|--------|--------------|
| **None** | App is internal, stateless, no data storage, no API access → no attack surface | N/A | N/A | N/A |

### ✅ Mitigations Proposed
None needed.

### 💰 Effort Summary
- **Total**: 0 hours (no mitigations required)

### 🎯 Catherine's Decision
- **Risk level**: ✅ GREEN — No security concerns
- **Approval**: Proceed without mitigations
- **Approved on**: 2026-04-26

**Status**: ✅ APPROVED → Proceed immediately (0h security work)

---

## Decision Matrix

| Risk Level | Action | Effort Impact |
|-----------|--------|----------------|
| 🟢 **GREEN** (no risks) | Proceed immediately | +0h |
| 🟡 **YELLOW** (low/medium risks, low impact) | Include SHOULD DO mitigations | +1-3h |
| 🟠 **ORANGE** (medium risks, high impact) | Include MUST DO + SHOULD DO | +3-6h |
| 🔴 **RED** (critical risks) | Include ALL, consider redesign | +6h+ or redesign |

---

## Checklist Before Approving Any Assessment

- [ ] All data types identified (PII? Financial? Client secrets?)
- [ ] All user types identified (internal? clients? public?)
- [ ] Risks are **concrete scenarios** (not generic "could be hacked")
- [ ] Mitigations are **specific technical actions** (not "improve security")
- [ ] Effort estimates are **realistic hours** (30min, 1h, 2h, not "quick")
- [ ] Criticality labels are **clear** (MUST/SHOULD/NICE)
- [ ] Total effort is **understood by Catherine** before approval

---

**Last updated**: 2026-04-26  
**Next review**: When first feature security assessment is completed
