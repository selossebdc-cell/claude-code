# Claude Code Configuration — CS Consulting Strategique

This document describes the architecture, automation, and best practices for this repository.

## 📁 Architecture Overview

### Single Source of Truth
- **Memory**: `~/.claude/memory` → symlink to `01-entreprise/memory/` (GitHub-versioned)
- **Skills**: `01-entreprise/skills/` (+ local commands in `.claude/commands/`)
- **Git**: Local (Google Drive, "Disponible hors connexion" mode) + GitHub backup

### Data Organization
```
01-entreprise/    # Shared, versioned, committed to GitHub
  - memory/       # Persistent learnings (symlinked to ~/.claude/memory)
  - skills/       # Reusable Claude Code skills
  - agents/       # Python automation agents

02-clients/       # Client data (versioned, public-safe)

03-developpement/ # Technical specs & code (versioned)

04-perso/         # ⚠️ NEVER committed (blocked by .gitignore + pre-commit hook)
```

## 🔒 Security & Protection

### File Protection
- **04-perso/** : Blocked by `.gitignore` and `pre-commit` hook
- **.env\*** : Blocked by `pre-commit` hook
- Both protections prevent accidental commit of sensitive data

### Git History
- Cleaned of any prior 04-perso/ data (see Phase 4 history)
- Force-pushed to GitHub to ensure clean remote

## 🚀 Automation

### Daily Routine (19:00)
```bash
cs-daily-push.sh  # Auto-commit + push any changes
Scheduled via: crontab (0 19 * * *)
```

### Weekly Audit
```bash
/repo-health      # Comprehensive security & sync audit
Run manually with: claude /repo-health
```

### Session Memory Capture
```
SessionEnd Hook → /memory-saver skill (in ~/.claude/settings.json)
Runs automatically when session ends
Captures learnings + detects stale memories (>6 months)
```

## 🛠️ Manual Commands

### Health Check (anytime)
```bash
cs-check          # Zsh alias for ~/bin/sync-check.sh
# Verifies: git sync, sensitive file protection, working directory cleanliness
```

### View Logs
```bash
tail -f ~/.logs/cs-daily-push.log
```

## 📝 Memory Management

- Auto-captured at session end via `/memory-saver`
- Location: `01-entreprise/memory/` (symlinked to `~/.claude/memory`)
- Types: user, feedback, project, reference
- Staleness: Detected if >6 months old

## ✅ Checklist Before Major Work

**Before ANY development or code review:**
- [ ] `claude /secure-by-design` — Mandatory security audit (Mickaël's framework)
- [ ] `cs-check` — Verify sync status
- [ ] `claude /repo-health` — Full system audit
- [ ] Verify Google Drive folder is in "Disponible hors connexion" mode
- [ ] Check MEMORY.md has recent updates

**Security-first**: Always ask "Could an attacker bypass this by modifying an HTTP request?" before writing any code.

## 🔄 Git Workflow

1. Work locally (all files on disk, not streamed from Drive)
2. Commit changes: `git commit -m "..."`
   - Pre-commit hook validates file paths
   - Won't allow 04-perso/ or .env* commits
3. Push to origin: `git push origin main`
4. Changes auto-sync to Google Drive
5. Daily 19:00: Cron pushes any uncommitted changes

## 📞 Troubleshooting

**"cs-check says git is out of sync"**
→ Run `git push origin main`

**"Pre-commit hook blocked my commit"**
→ Check which file triggered it (hook shows error)
→ Move file to 04-perso/ or .gitignore it

**"Memory not accessible via ~/.claude/memory"**
→ Check symlink: `ls -la ~/.claude/memory`
→ Should point to absolute path of 01-entreprise/memory/

**"Cron job not running"**
→ Check: `crontab -l | grep cs-daily-push`
→ Check logs: `tail ~/.logs/cs-daily-push.log`

---

**Last Updated**: 2026-04-26 (Phase 5 Automation)
