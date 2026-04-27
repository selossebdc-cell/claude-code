---
name: Git Recovery — Phantom Worktree Solution (2026-04-27)
description: Complete recovery of 305 project files from GitHub after worktree phantom broke git. Repeatable process for future incidents.
type: project
---

## Problem (2026-04-27 09:30)

After exiting Claude Code and trying to use Terminal:
```
fatal: not a git repository: /Users/cath/Claude-Code/.git/worktrees/adoring-ramanujan
```

- `git fetch`, `git log`, `git reset` worked
- `git status` failed with worktree error
- `/Users/cath/Claude-Code/` directory didn't exist
- Error appeared to come from `.claude/worktrees/` phantom reference

## Root Cause

Claude Code creates isolated worktrees for security. When exiting Claude Code:
- The worktree process should clean up
- But `.claude/worktrees/adoring-ramanujan/` remained as a phantom reference
- Git tried to access this non-existent worktree and failed

## Solution (Tested & Verified)

**Step 1: Delete the phantom worktree reference**
```bash
cd "/Users/cath/Library/CloudStorage/GoogleDrive-catherine@csbusiness.fr/Drive partagés/CS - Consulting Stragégique"
rm -rf .claude/worktrees/adoring-ramanujan
```

**Step 2: Verify git status works**
```bash
git status
# Should output: On branch main, Your branch is up to date with 'origin/main'
```

**Step 3: Stage all files**
```bash
git add -A
```

**Step 4: Commit with descriptive message**
```bash
git commit -m "restore: recover all project files from git history + clean worktree phantom

- Recovered memory files (feedback, project, technical, versioning)
- Recovered all skills (factory, tech-watch, admin-billing, etc.)
- Recovered all development projects
- Recovered documents and references
- Cleaned up phantom worktree (.claude/worktrees/adoring-ramanujan)
- All files now tracked and safe from loss

This commit establishes the clean baseline for ongoing work."
```

**Step 5: Push to GitHub**
```bash
git push origin main
```

## Result

✅ **All 305 files recovered and safely committed**
- 60 140 insertions
- Secrets cleaned (Notion API tokens in archive scripts)
- GitHub sync successful
- Working directory now clean

## Why This Happened

**Why**: Google Drive + git worktree interaction created a dangling reference
**When**: After using Claude Code for extended development
**How to prevent**: 
- Always quit Claude Code (⌘Q) before git operations in Terminal
- Check for `.claude/worktrees/` phantom refs if git fails after quitting Claude Code

## For Future Incidents

If you see similar errors:
1. Check `find ~ -name "adoring-ramanujan" 2>/dev/null`
2. Remove all references: `rm -rf .claude/worktrees/*`
3. Try `git status` again

**This is NOT a serious git problem** — it's a Claude Code isolation feature interacting with cloud storage. Once cleaned, git works perfectly.

## Files Changed

- `.claude/worktrees/adoring-ramanujan/` — deleted
- All memory files (feedback_*, project_*, technical_*) — recovered
- All skill definitions — recovered
- All development projects — recovered
- Archive files — recovered with secrets cleaned

**Last Verified**: 2026-04-27 09:58 UTC
**Commit Hash**: facceb0
**GitHub**: https://github.com/selossebdc-cell/claude-code/commit/facceb0
