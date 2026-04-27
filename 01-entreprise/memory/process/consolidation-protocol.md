---
name: Cloud Consolidation Protocol
description: Decision rules for handling file conflicts between Google Drive (source) and OneDrive (archive). Prevents future divergence.
type: process
created: 2026-04-26
source_of_truth: Google Drive
---

# Cloud Consolidation Protocol

**Status**: ✅ ACTIVE (Post-audit protocol, effective 2026-04-26)

This document establishes **decision rules** for handling scenarios where Google Drive and OneDrive contain different versions of the same file. Prevents recurring "which version is current?" confusion.

---

## Architecture Decision (Reference)

- **Source of Truth**: Google Drive (`/Drive partagés/CS - Consulting Stragégique/`)
- **Archive**: OneDrive (`/Claude Code/`) — contains backups, kept for reference only
- **Backup**: GitHub — unidirectional backup from GDrive (production → backup)
- **Flow**: Work in GDrive → Changes sync to GitHub monthly → OneDrive kept as historical archive

---

## File Conflict Scenarios & Decision Rules

### Scenario A: Same File Exists in Both Clouds — Different Content

**Situation**: File at `/GDrive/01-entreprise/[file.md`] differs from `/OneDrive/01-entreprise/[file.md`]

**Decision Rule** (in order of priority):

1. **If modification dates differ by > 1 day**: Use the NEWER version (within 1 day could be sync lag)
   - Reason: Assuming more recent = more up-to-date
   - Exception: If the older file contains critical edits (security fix, blocker resolution) missing in newer version, merge manually

2. **If modification dates are within 1 hour of each other**: File sync is in progress, wait 5 minutes and re-check
   - Reason: Real-time sync lag (OneDrive refresh delay)
   - Action: Don't edit during this window

3. **If modification dates are identical**: Content divergence (actual conflict, not just lag)
   - Check GDrive version first (source of truth)
   - If GDrive version is newer structurally (added sections, decisions, memory entries), use GDrive
   - If OneDrive version has edits missing in GDrive, merge the additions into GDrive version
   - Document the merge in `/memory/versioning/2026-04.md` with timestamp + what was merged

4. **If no modification date is available** (rare): Default to GDrive (source of truth always wins)

### Scenario B: File Exists Only in OneDrive

**Situation**: File at `/OneDrive/01-entreprise/[file.md`] but NOT in `/GDrive/01-entreprise/`

**Decision Rule**:

1. Check if file is **system-critical** (memory files, process docs, client data):
   - YES → Copy to GDrive immediately (it's valuable history or current decision)
   - NO → Archive in OneDrive (historical artifact, not needed going forward)

2. If copying to GDrive, preserve as-is + add metadata footer:
   ```markdown
   ---
   recovered_from: OneDrive archive 2026-04-26
   migrated_to_grive: [timestamp]
   ---
   ```

3. Update MEMORY.md to reflect new file location

### Scenario C: File Exists Only in Google Drive

**Situation**: File at `/GDrive/01-entreprise/[file.md`] but NOT in `/OneDrive/`

**Decision Rule**: No action needed. Google Drive is source of truth.
- If file was recently created (< 1 week) in GDrive: Normal workflow, no backport to OneDrive
- If file is critical and GDrive is only copy: Verify GitHub backup exists

### Scenario D: File Deleted from One Cloud, Exists in Other

**Situation**: File was at `/OneDrive/01-entreprise/[file.md`], now deleted, but exists in `/GDrive/`

**Decision Rule**:

1. If deleted from OneDrive (likely intentional archive): No action. OneDrive is archive only.

2. If deleted from GDrive but exists in OneDrive: **ALERT — Unintended deletion**
   - Restore from OneDrive copy to GDrive immediately
   - Check git history: why was it deleted?
   - Update MEMORY.md versioning changelog with recovery note

3. If deleted from both (intentional deprecation): Confirm in DECISIONS.md why (e.g., "Sunset Notion references, old file archived 2026-04-26")

### Scenario E: File Structure Differs (Same Content, Different Paths)

**Situation**: Same content exists at different paths (e.g., `/GDrive/memory/technical/blockers.md` vs `/OneDrive/01-entreprise/memory/blockers.md`)

**Decision Rule**:

1. Keep only GDrive version at canonical path
2. If OneDrive version has different frontmatter or additions, extract and merge into GDrive version
3. Delete redundant OneDrive copy (it's now in archive, safe)
4. Update MEMORY.md index to point only to GDrive canonical location

---

## Content Merge Rules

When merging files from OneDrive into GDrive version:

### For Memory Files (MEMORY.md, client/*, technical/*, process/*, versioning/*)

**Priority Order** (highest to lowest):
1. GDrive version is authoritative (it's the working copy)
2. Merge new entries from OneDrive IF they're not already in GDrive
3. For decision records (DECISIONS.md, 2026-04.md): merge if decision date is newer or missing in GDrive
4. For client files: merge recent notes/status updates from OneDrive if GDrive version is older

**Merge Process**:
- Open both files side-by-side
- Copy over new sections/entries from OneDrive that don't exist in GDrive
- Update timestamps to reflect when merge occurred
- Document merge in versioning changelog: "[filename] merged from OneDrive backup, [N] entries added"

### For Client/Skills Files (02-clients/*, 03-developpement/*)

**Priority Order** (highest to lowest):
1. **Modification date** is primary signal (newer = more likely to be current)
2. If GDrive is older but has more content: Manual review needed (ask Catherine)
3. If both are current but differ (divergent edits): Don't auto-merge, report to Catherine with both versions highlighted
4. For CRs (session reports): Always take most recent (usually GDrive)

**Why manual review for client files**: Client data is revenue-critical. Auto-merge could lose important context.

---

## Prevention Strategy (Future-Proofing)

### To Prevent Future Divergence:

1. **Single Editing Location**: Always edit in Google Drive (never edit OneDrive copies)
   - OneDrive is archive only (read-only reference, not editing destination)
   - If you accidentally edit OneDrive: manually sync changes back to GDrive

2. **Sync Monitoring** (Monthly audit):
   - First Monday of each month: Claude does quick audit
   - Check 3 files at random: verify GDrive version is most recent
   - If divergence detected: run full merge process (document why it happened)

3. **Archival Discipline**:
   - Archive OneDrive folder timestamps clearly: `/archive_claude-code_[YYYY-MM-DD_HHMMSS]/`
   - When archiving, add metadata file: `_ARCHIVED_[date]_source_files_migrated_to_google_drive.txt`
   - This prevents "which archive is current?" confusion later

4. **GitHub as Backup Verification**:
   - Monthly: Spot-check that critical GDrive files are backed up to GitHub
   - If GitHub is missing recent changes: trigger manual backup

5. **Documentation in Changelog**:
   - Every merge/consolidation action recorded in `versioning/2026-04.md` (or current month)
   - Format: `[2026-04-26 14:30] Merged [filename] from OneDrive, [N] entries added. Reason: [security assessment decisions]`

---

## Decision Matrix: "Which File Wins?"

| Scenario | GDrive Newer? | OneDrive Newer? | Decision | Action |
|----------|---------------|-----------------|----------|--------|
| Both exist, dates differ > 1 day | YES | NO | Use GDrive | Done |
| Both exist, dates differ > 1 day | NO | YES | Use OneDrive content, save to GDrive | Copy + verify |
| Both exist, dates within 1 hour | N/A | N/A | Sync in progress | Wait + re-check |
| Both exist, dates identical | N/A | N/A | Conflict exists | Manual merge |
| Only OneDrive | System file? | YES | Copy to GDrive | Copy + timestamp |
| Only OneDrive | System file? | NO | Archive only | Keep OneDrive copy |
| Only GDrive | N/A | N/A | Normal | Use GDrive |
| Deleted from GDrive, in OneDrive | N/A | N/A | Unintended | Restore from OneDrive |
| Different paths, same content | N/A | N/A | Consolidate paths | Keep GDrive path, delete OneDrive |

---

## Checklist: After Resolving a Conflict

- [ ] Verify the winning file is in Google Drive
- [ ] If merged: Confirm all important content from both versions is in GDrive version
- [ ] Update MEMORY.md if structure changed
- [ ] Update versioning changelog with timestamp + what was merged
- [ ] Verify GitHub backup has the latest version
- [ ] Close OneDrive copy (don't edit it anymore; it's archive)
- [ ] If multiple files had same conflict: Document pattern (helps future prevention)

---

## FAQ

### Q: What if I'm in a session and need a file but Google Drive is slow?

A: Use OneDrive as a **read-only reference** only. Don't edit it. If changes are needed, make them in GDrive (even if slower) to maintain single source of truth.

### Q: If OneDrive version is newer but less complete, which do I use?

A: Use GDrive (source of truth). OneDrive being newer could mean a file was reverted by accident. Check git history to verify.

### Q: How often should I audit for divergence?

A: **Monthly** (first Monday). Spot-check 3-5 files. If no divergence found 3 months in a row, can reduce to quarterly.

### Q: What if GitHub backup is missing something?

A: This shouldn't happen if GDrive → GitHub sync is working. If it does: manually push missing file to GitHub + document why in changelog.

### Q: Can I edit files in both clouds?

A: **NO**. Edit only in Google Drive. OneDrive is archive (read-only reference). This prevents the original problem.

---

## Related Files

- [MEMORY.md](../MEMORY.md) — Rules for when to update memory files
- [DECISIONS.md](../versioning/DECISIONS.md) — Decision 1 (Google Drive = source of truth)
- [2026-04.md](../versioning/2026-04.md) — Changelog (record every consolidation action)

---

**Created**: 2026-04-26  
**Status**: ✅ ACTIVE  
**Last reviewed**: 2026-04-26  
**Next monthly audit**: 2026-05-05 (first Monday of May)
