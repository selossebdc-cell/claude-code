---
name: Portail Client V2 — Template Isolation Bug (Resolved)
description: Fixed critical RLS isolation bug where Taïna (Guadeloupe Explor) saw Face Soul Yoga templates due to appState.currentClientId containing user ID instead of client_id
type: project
---

## Problem Identified (2026-04-27)

**Issue**: Taïna (Guadeloupe Explor user) could see Face Soul Yoga's 13 templates in the playbook process creation dropdown.

**Expected Behavior**: 
- Taïna should see 0 templates (Guadeloupe Explor has no templates)
- Aurélia should see 13 templates (Face Soul Yoga's templates)

**Root Cause**: Admin client selector function `initAdminClientSelector()` in playbook.html was:
1. Loading profiles from database but NOT selecting `client_id` column
2. Assigning `c.id` (user ID) instead of `c.client_id` to dropdown option values
3. Result: `appState.currentClientId` contained user ID (33790783-cb19-4693-9a22-d071afbcba42) instead of client ID (9940623d-3c30-47ea-b113-069327010288)

## Solution Implemented (2026-04-27)

**File**: `03-developpement/portail-client-v2/playbook.html`

**Changes**:
- Line 1337: Added `client_id` to SELECT query
  ```javascript
  // Before: .select('id, full_name, company, role')
  // After:  .select('id, full_name, company, role, client_id')
  ```

- Line 1343: Fixed dropdown value assignment
  ```javascript
  // Before: opt.value = c.id;  // ← User ID
  // After:  opt.value = c.client_id;  // ← Client ID
  ```

**Commits**:
- ae800bc: Code fix in playbook.html
- ae9157d: Documentation in MIGRATIONS-LOG.md

## Verification (2026-04-27)

✅ **Testing Results**:
- Taïna login: `appState.currentClientId` = 9940623d-3c30-47ea-b113-069327010288 (correct)
- Taïna playbook: Template dropdown = EMPTY (0 templates)
- Aurélia login: `appState.currentClientId` = 8ccc177f-b7d2-4b5e-ac70-a10a042e7b99 (correct)
- Aurélia playbook: Template dropdown = 13 templates (correct)

## Architecture Notes

**RLS Layer**: PostgreSQL RLS policies enforce client_id filtering at database layer
- Policy: `client_id = (SELECT client_id FROM profiles WHERE id = auth.uid())`
- RLS blocks queries that violate client isolation

**Frontend Layer**: JavaScript code now respects RLS by filtering with correct client_id
- `loadTemplates()` uses `appState.currentClientId` in `.eq('client_id', ...)`
- Defense-in-depth: Frontend filtering + RLS enforcement

**Multi-Tenant Model**:
```
playbook_clients (4 clients: Client A, Guadeloupe Explor, Face Soul Yoga, Taïna)
  ↓ FK chain
profiles.client_id (6 users assigned to clients)
  ↓ used by
appState.currentClientId (set during login and admin switching)
  ↓ passed to
loadTemplates() and other queries
  ↓ enforced by
RLS policies + application filters
```

## Key Insight

**Why:** Admin client selector was pulling user data (profiles) when it should have been using client data (playbook_clients). The mismatch caused user IDs to be treated as client IDs.

**Resolution**: Select `client_id` alongside user profile data, then use the correct field in dropdown values.

## Related Tasks

- TASK-0006: Frontend RLS Refactoring (extends this pattern to all playbook tables)
- TASK-0007: Frontend RLS on other tables (actions, contracts, sessions, etc.)
- Epic 4: Complete frontend RLS alignment with database policies
