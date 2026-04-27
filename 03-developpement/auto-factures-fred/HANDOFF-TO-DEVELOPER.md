# Handoff to Developer — BUILD Phase

**From**: Factory Build Skill (Orchestrator)  
**To**: Development Team  
**Date**: 2026-04-27  
**Status**: Ready for Implementation ✓  

---

## Quick Start: You Have 2 Days of Work

You are receiving a completely specified project. Your job is to implement 2 tasks that form the foundation.

**Timeline**:
- **TASK-0001** (2 days): Project setup
- **TASK-0002** (1-2 days): Database setup
- **Done by**: 2026-05-01

---

## What You're Building

**Auto-Factures Fred** — A Node.js invoice generation system with:

- REST API (Express 4.21.2)
- PostgreSQL database (6 tables)
- PDF generation (Puppeteer)
- Email delivery (Nodemailer)
- Authentication (JWT)
- Async job processing (Bull queue)
- Complete test coverage (Jest)

**V1 Release Target**: 2026-06-30

---

## Your Assignment: TASK-0001 + TASK-0002

### TASK-0001: Project Configuration & Setup (2 days)

**File**: docs/planning/v1/tasks/TASK-0001-project-config.md

**What to do**:
1. Open the file above (480 lines of specification)
2. Follow the 11 implementation steps **in exact order**
3. After each step, verify it works
4. Check off the Definition of Done checklist
5. Run the verification commands
6. Commit with message: `TASK-0001: Initialize project structure and dependencies`

**Expected deliverables**:
- Project structure (src/, tests/, db/ directories)
- package.json with exact versions
- Configuration files (ESLint, Prettier, Jest, .env.example)
- First passing test (health check endpoint)
- Pre-commit hooks (block .env commits)

**How to know you're done**:
```bash
pnpm test    # ✓ All tests pass
pnpm lint    # ✓ Zero errors
pnpm build   # ✓ Succeeds
pnpm dev     # ✓ Server starts on port 3000
curl http://localhost:3000/health  # ✓ {"status":"ok"}
```

---

### TASK-0002: Database Configuration & Migrations (1-2 days)

**File**: docs/planning/v1/tasks/TASK-0002-database-config.md

**Prerequisites**:
- TASK-0001 must be 100% complete
- PostgreSQL 14+ installed on your machine
- DATABASE_URL environment variable set

**What to do**:
1. Open the file above (490 lines of specification)
2. Follow the 12 implementation steps **in exact order**
3. Create the migration files exactly as specified
4. Run migrations and verify with psql
5. Check off the Definition of Done checklist
6. Run the verification commands
7. Commit with message: `TASK-0002: Configure database and create migrations`

**Expected deliverables**:
- PostgreSQL database (auto_factures_fred)
- 6 tables: customers, products, templates, transactions, invoices, audit_logs
- Migration framework (db/migrate.js)
- Seed data (1 template, 1 customer, 3 products)
- Updated health check (shows database status)

**How to know you're done**:
```bash
pnpm db:migrate      # ✓ All migrations run
psql auto_factures_fred -c "\dt"  # ✓ Shows 6 tables
pnpm db:reset        # ✓ Works without errors
curl http://localhost:3000/health  # ✓ Shows "database":"connected"
```

---

## Key Reference Documents

**READ THESE FIRST** (before coding):

1. **docs/specs/stack-reference.md** (70 lines)
   - Exact package versions you must use
   - Configuration code examples
   - This is the SOURCE OF TRUTH for versions

2. **.claude/rules/architecture.md** (250 lines)
   - Coding standards (error handling, logging, validation)
   - Database rules (queries, constraints)
   - API design rules

3. **.claude/rules/testing.md** (400 lines)
   - Test structure (unit, integration, E2E)
   - Mock strategies
   - Coverage requirements (>75%)

---

## Success Checklist

### Before Starting

- [ ] Node.js 20.x LTS installed (`node --version`)
- [ ] pnpm installed globally (`pnpm --version`)
- [ ] PostgreSQL 14+ installed (`psql --version`)
- [ ] Read TASK-0001 file completely
- [ ] Read TASK-0002 file completely
- [ ] Read architecture.md and testing.md
- [ ] Read stack-reference.md

### After TASK-0001

- [ ] `pnpm test` passes
- [ ] `pnpm lint` passes with zero errors
- [ ] `pnpm build` succeeds
- [ ] `pnpm dev` starts server (port 3000)
- [ ] `curl http://localhost:3000/health` returns `{"status":"ok"}`
- [ ] All Definition of Done criteria checked
- [ ] Git commit made with message `TASK-0001: ...`

### After TASK-0002

- [ ] `pnpm db:migrate` runs successfully
- [ ] `psql auto_factures_fred -c "\dt"` shows 6 tables
- [ ] `pnpm db:reset` completes without errors
- [ ] `curl http://localhost:3000/health` shows `"database":"connected"`
- [ ] `pnpm test` still passes
- [ ] All Definition of Done criteria checked
- [ ] Git commit made with message `TASK-0002: ...`

---

## Important Rules

### Rule 1: Use EXACT Versions

**DO NOT use latest versions.** Use EXACT versions from docs/specs/stack-reference.md:

```json
{
  "express": "4.21.2",     ✓ Exactly this version
  "pg": "8.12.0",          ✓ Exactly this version
  "jest": "29.7.0",        ✓ Exactly this version
  ... (all others)
}
```

If versions differ from stack-reference.md, STOP and escalate.

### Rule 2: Follow Steps In Order

Each task has numbered steps. Follow them in order (1, 2, 3...). Don't skip steps or reorder them.

Why? Each step builds on the previous one. Skipping can cause failures later.

### Rule 3: Don't Invent Code

Use the code examples provided in the task files. If you need to customize:
1. Follow the pattern shown
2. Respect the architecture rules (.claude/rules/architecture.md)
3. Test your changes

### Rule 4: Use Parameterized Queries

**DO NOT** concatenate SQL strings:
```javascript
// ❌ WRONG
const sql = `SELECT * FROM users WHERE id = '${id}'`;

// ✓ RIGHT
const sql = 'SELECT * FROM users WHERE id = $1';
db.query(sql, [id]);
```

### Rule 5: Always Test

After each step, run the tests:
```bash
pnpm test          # All tests
pnpm test:unit     # Unit tests only
pnpm lint          # Linting
```

Don't move to the next step until tests pass.

---

## Troubleshooting

### "pnpm install fails"

Check 1: Are versions EXACT from stack-reference.md?
```bash
pnpm list | grep express  # Should be 4.21.2
```

Check 2: Is Node.js 20.x?
```bash
node --version  # Should be v20.x.x
```

Check 3: Delete lock file and retry
```bash
rm pnpm-lock.yaml
pnpm install
```

### "PostgreSQL not found"

Check 1: Is PostgreSQL installed?
```bash
psql --version  # Should show version
```

Check 2: Is PostgreSQL service running?
```bash
# macOS
brew services list | grep postgres

# Ubuntu/Debian
sudo systemctl status postgresql

# Windows
Services.msc → PostgreSQL
```

Check 3: Can you connect?
```bash
psql -U postgres -c "SELECT 1"  # Should return 1
```

### "Database connection error"

Check 1: Does database exist?
```bash
createdb auto_factures_fred
```

Check 2: Is DATABASE_URL correct?
```bash
# In .env, should be:
DATABASE_URL=postgresql://localhost/auto_factures_fred
```

Check 3: Can you connect?
```bash
psql auto_factures_fred -c "SELECT NOW()"
```

### "Port 3000 already in use"

Use different port:
```bash
PORT=3001 pnpm dev
# Then test: curl http://localhost:3001/health
```

---

## Daily Standup Questions

**Every morning, ask yourself**:

1. What task am I on? (TASK-0001 or TASK-0002)
2. Which step? (Step 1, 2, 3... of 11 or 12)
3. Do I have the reference files open?
4. Have I run tests since my last change?
5. Do I understand why this step matters?

---

## When You're Stuck

**Step 1**: Read the task file again. The step you're on explains what to do.

**Step 2**: Check the reference files:
- For version issues → stack-reference.md
- For code patterns → .claude/rules/architecture.md
- For test patterns → .claude/rules/testing.md

**Step 3**: Look at the code examples in the task file. Copy-paste ready code is provided.

**Step 4**: If still stuck, run the verification commands. They tell you what's wrong.

**Step 5**: Check the troubleshooting section above.

**Step 6**: If still blocked, escalate with:
- What step you're on
- What error message you're seeing
- What you already tried

---

## File Locations You'll Need

### Task Specifications
```
docs/planning/v1/tasks/TASK-0001-project-config.md
docs/planning/v1/tasks/TASK-0002-database-config.md
```

### Reference Specifications
```
docs/specs/stack-reference.md          (← MOST IMPORTANT)
docs/specs/system.md                   (architecture overview)
docs/specs/domain.md                   (database schema)
docs/specs/api.md                      (REST endpoints)
```

### Architecture & Testing Rules
```
.claude/rules/architecture.md
.claude/rules/testing.md
```

### Architecture Decision Records
```
docs/adr/ADR-0001-stack-selection.md
docs/adr/ADR-0002-async-batch-processing.md
docs/adr/ADR-0003-authentication-strategy.md
```

---

## What Success Looks Like

After TASK-0001:
```
✓ Project structure created
✓ Dependencies installed (exact versions)
✓ Tests passing (pnpm test)
✓ Linting passing (pnpm lint)
✓ Server starts (pnpm dev)
✓ Health check working (curl http://localhost:3000/health)
✓ Pre-commit hooks installed
✓ Git commit made
```

After TASK-0002:
```
✓ All of above, PLUS:
✓ Database created
✓ 6 tables with correct schemas
✓ Migrations working (pnpm db:migrate)
✓ Seed data inserted
✓ Health check shows database connected
✓ Reset command works (pnpm db:reset)
✓ All tests still passing
✓ Git commit made
```

---

## Next After These 2 Tasks

Once TASK-0001 and TASK-0002 are complete:

1. **QA Verification** (1 day)
   - Someone reviews your code
   - Tests all verification checklist items
   - Checks Definition of Done

2. **Epic 2 Planning** (in parallel)
   - Product Manager approves Sprint 1 plan
   - Next tasks generated for domain entities

3. **Sprint 1 Continues** (starting 2026-05-02)
   - More developers assigned to Epic 2 tasks
   - You may continue with Epic 2 or other areas

---

## Timeline

| Date | Milestone | You |
|------|-----------|-----|
| 2026-04-27 | TASK-0001 assigned | Start |
| 2026-04-29 | TASK-0001 due | Complete + verify |
| 2026-04-29 | TASK-0002 assigned | Start |
| 2026-05-01 | TASK-0002 due | Complete + verify |
| 2026-05-02 | QA review | Wait |
| 2026-05-02 | Sprint 1 starts | Next assignment |

---

## Contact & Support

**For questions about**:
- What to code → Read the TASK file (it's 100% complete)
- How to code → Read .claude/rules/architecture.md
- What versions to use → Read docs/specs/stack-reference.md
- How to test → Read .claude/rules/testing.md

**For blockers**:
1. Check the Troubleshooting section above
2. Review the relevant TASK file
3. Check the reference documents
4. Escalate if still blocked

---

## Final Checklist Before You Start

- [ ] I have read TASK-0001 completely
- [ ] I have read TASK-0002 completely
- [ ] I have read docs/specs/stack-reference.md
- [ ] I have read .claude/rules/architecture.md
- [ ] I have read .claude/rules/testing.md
- [ ] I understand I must use EXACT versions
- [ ] I understand I must follow steps in order
- [ ] I have Node.js 20.x installed
- [ ] I have pnpm installed
- [ ] I have PostgreSQL 14+ installed
- [ ] I'm ready to start TASK-0001 today

---

## Your Success Metrics

**TASK-0001 Success**:
- [ ] `pnpm test` passes
- [ ] `pnpm lint` passes
- [ ] `pnpm build` succeeds
- [ ] Project structure matches spec
- [ ] All Definition of Done criteria met

**TASK-0002 Success**:
- [ ] `pnpm db:migrate` succeeds
- [ ] All 6 tables created
- [ ] Seed data inserted
- [ ] `pnpm db:reset` works
- [ ] All Definition of Done criteria met

**Both Tasks Success**:
- [ ] Code follows architecture rules
- [ ] Tests pass with >75% coverage
- [ ] Database constraints enforced
- [ ] No hardcoded secrets
- [ ] Git commits with TASK IDs

---

## Ready?

You have everything you need. Let's build Auto-Factures Fred V1.

1. Open docs/planning/v1/tasks/TASK-0001-project-config.md
2. Read it completely
3. Start Step 1
4. Follow steps 1-11 in order
5. Check off Definition of Done
6. Commit your work
7. Do the same for TASK-0002

**Estimated time**: 3-4 days (TASK-0001: 2 days, TASK-0002: 1-2 days)

**Target completion**: 2026-05-01

**Good luck!**

---

**Date Prepared**: 2026-04-27  
**Status**: Ready for Developer Assignment ✓  
**Next Step**: Assign to developer + monitor progress  

---

*This handoff document completes the BUILD phase orchestration. All specifications, guidance, and reference materials are in place. The developer is ready to implement.*
