---
name: Claude Code Worktree — Solution Pattern
description: How to resolve git operations when working in Claude Code. Worktree isolation blocks commits from within Claude Code. Solution: Exit Claude Code, use Terminal, commit succeeds.
type: feedback
---

## Problem Pattern

When working on code in Claude Code (the IDE), git operations fail with:
```
fatal: not a git repository: /Users/cath/Claude-Code/.git/worktrees/[name]
```

This happens even when:
- You're in the correct project directory (`cd /path/to/project`)
- The project has a valid `.git` folder
- You explicitly use `git -C` or `GIT_DIR` environment variables

**Why**: Claude Code creates an isolated worktree for each project (security feature). All git operations from within Claude Code route to this worktree, not the main repository.

---

## Solution (VERIFIED WORKING)

**Remove the worktree isolation:**
1. **Quit Claude Code completely** (⌘Q, not just close window)
2. **Open Terminal** (native macOS app)
3. **Navigate to project** (`cd /path/to/project`)
4. **Run git commands** (status, add, commit, push)
5. ✅ Works perfectly

**Why this works**: When Claude Code closes, it releases the worktree lock. Git can now access the main `.git` directory normally.

---

## When to Apply

**After implementation is complete and code is on disk:**
- ✅ Code is written and tested
- ✅ All files are created locally
- ✅ You're ready to commit to GitHub
- → Exit Claude Code → Use Terminal

**Not needed for**:
- Editing code (Claude Code is fine)
- Running tests (Claude Code is fine)
- Reading git log (if using a git GUI is available)

---

## How to Prevent Future Issues

**Best practice**:
1. **Work in Claude Code** until code is production-ready
2. **Create an HTML checklist** (like the one created for this project: `/tmp/git-commit-steps.html`)
3. **Use the checklist** to step through commit workflow in Terminal
4. **Verify** git push succeeds before reopening Claude Code

---

## Implementation for This Project

**HTML Guide Created**: `/tmp/git-commit-steps.html`
- 9 step-by-step instructions
- Copy-paste buttons for each git command
- Checkbox tracking (persisted in browser localStorage)
- Expected output for each step
- No secrets or hardcoded values

**Used for**: Committing EPIC-1 through EPIC-5 implementations

---

## Key Insight

Claude Code's worktree isolation is **a feature, not a bug**. It:
- Protects projects from accidental interference
- Allows multiple projects open simultaneously
- Isolates dependencies and configurations

**The solution isn't to disable it** — it's to recognize when to work around it. Git commits need a "clean" environment outside Claude Code.

---

## Future Automation Opportunity

Could create a `.claude/commands/commit-with-guide` command that:
1. Displays the HTML guide
2. Reminds user to quit Claude Code
3. Auto-opens Terminal
4. Pre-fills directory path
5. Waits for user to complete workflow

**But for now**: Manual workflow + HTML checklist = reliable + transparent
