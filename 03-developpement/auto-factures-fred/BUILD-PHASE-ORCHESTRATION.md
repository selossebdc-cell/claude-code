# BUILD Phase Orchestration — Auto-Factures Fred

**Phase**: ACT (Build & Implementation)  
**Status**: STARTED  
**Date**: 2026-04-27  
**Orchestrator**: Factory Build Skill  

---

## Overview

The BUILD phase implements the project by executing tasks in batches, organized by architectural layer. For Auto-Factures Fred V1, only Epic 1 (Foundation) has tasks ready. This orchestration document guides the sequential implementation.

---

## Batch Structure

### Batch: SETUP (Foundation Layer)

**Type**: Sequential batch (tasks depend on each other)  
**Tasks**: 2 (TASK-0001, TASK-0002)  
**Duration**: 3-4 days  
**Status**: Ready to implement  

**Execution Order** (MANDATORY SEQUENTIAL):
1. TASK-0001: Project Configuration & Setup (2 days)
2. TASK-0002: Database Configuration & Migrations (1-2 days)

---

## TASK-0001: Project Configuration & Setup

**File**: docs/planning/v1/tasks/TASK-0001-project-config.md  
**Epic**: Epic 1 - Project Foundation & Infrastructure  
**User Story**: US-0001 - Project Initialization  
**Priority**: Critical (foundation task)  
**Effort**: 2 days  
**Dependencies**: None  

### Quick Start for TASK-0001

1. **Read the complete TASK-0001 file** (480 lines of detailed specs)
2. **Follow the 11 implementation steps** in exact order
3. **Verify each step** before moving to next
4. **Run the Definition of Done checklist** at the end
5. **Run the verification commands** to confirm everything works

### Key Deliverables (TASK-0001)

- Complete Node.js project structure
- package.json with exact versions from stack-reference.md
- Configuration files: database.js, app.js, index.js
- ESLint, Prettier, Jest configurations
- .env.example with all required variables
- First passing test (health check endpoint)
- Pre-commit hooks (block .env commits, block 04-perso/)
- Initial Git commit

### Success Criteria (TASK-0001)

- [ ] Git repository initialized
- [ ] Directory structure created
- [ ] Dependencies installed with exact versions
- [ ] Configuration files created
- [ ] Health check endpoint working
- [ ] First test passes (pnpm test)
- [ ] Linting passes (pnpm lint)
- [ ] Development server starts (pnpm dev)
- [ ] Pre-commit hooks installed
- [ ] Initial commit made

---

## TASK-0002: Database Configuration & Migrations

**File**: docs/planning/v1/tasks/TASK-0002-database-config.md  
**Epic**: Epic 1 - Project Foundation & Infrastructure  
**User Story**: US-0002 - Database Setup & Migrations  
**Priority**: Critical  
**Effort**: 1-2 days  
**Dependencies**: TASK-0001 (must be 100% complete first)  

### Quick Start for TASK-0002

1. **Read the complete TASK-0002 file** (490 lines of detailed specs)
2. **Prerequisites check**:
   - TASK-0001 completed
   - PostgreSQL 14+ installed
   - pnpm available
3. **Follow the 12 implementation steps** in exact order
4. **Run the verification commands** to confirm database works
5. **Run the Definition of Done checklist** at the end

### Key Deliverables (TASK-0002)

- PostgreSQL database created (auto_factures_fred)
- Connection pooling configured (min 5, max 20)
- All 6 tables created with schemas:
  - customers
  - products
  - invoice_templates
  - transactions
  - invoices
  - audit_logs
- Foreign key constraints enforced
- Enum types created (transaction_status, invoice_status)
- Database constraints enforced (email validation, amount checks, date rules)
- Performance indexes created
- Migration framework (db/migrate.js)
- Seed data inserted
- Health check updated to verify database connectivity
- npm scripts added (db:migrate, db:seed, db:reset)

### Success Criteria (TASK-0002)

- [ ] PostgreSQL database created
- [ ] Connection pooling configured
- [ ] All 6 tables created with correct schemas
- [ ] Foreign keys enforced
- [ ] Enum types created
- [ ] Constraints enforced
- [ ] Indexes created
- [ ] Migration framework functional
- [ ] Seed data inserted
- [ ] Health check includes database status
- [ ] Migrations are idempotent
- [ ] All tests pass
- [ ] Database reset works (pnpm db:reset)

---

## Implementation Workflow

### Phase 1: TASK-0001 (Today)

**Duration**: 2 days (can be compressed to 1 day with focus)

1. Clone or create local working directory
2. Follow TASK-0001 steps 1-11 in exact order
3. After each step, verify it works before moving to next
4. Run Definition of Done checklist
5. Run verification commands
6. Commit with message: `TASK-0001: Initialize project structure and dependencies`

**Expected state after TASK-0001**:
```
auto-factures-fred/
├── src/
│   ├── config/
│   │   └── database.js
│   ├── app.js
│   ├── index.js
│   └── ...
├── tests/
│   └── unit/
│       └── app.test.js
├── .husky/
│   └── pre-commit
├── package.json (with exact versions)
├── .env.example
├── .eslintrc.js
├── .prettierrc
├── jest.config.js
├── .gitignore
└── README.md
```

### Phase 2: TASK-0002 (After TASK-0001)

**Duration**: 1-2 days  
**Prerequisites**: TASK-0001 must be 100% complete

1. Prerequisites check:
   - PostgreSQL 14+ installed
   - DATABASE_URL environment variable set
2. Follow TASK-0002 steps 1-12 in exact order
3. Create migration files exactly as specified
4. Run migrations and verify with psql
5. Update health check endpoint
6. Run Definition of Done checklist
7. Run verification commands
8. Commit with message: `TASK-0002: Configure database and create migrations`

**Expected state after TASK-0002**:
```
auto-factures-fred/
├── db/
│   ├── migrations/
│   │   ├── 001-create-tables.sql
│   │   └── 002-seed-data.sql
│   └── migrate.js
├── src/
│   ├── config/
│   │   └── database.js (enhanced)
│   ├── app.js (updated with database health check)
│   └── ...
├── .env (with DATABASE_URL)
├── package.json (with db:migrate, db:seed, db:reset scripts)
└── ...
```

---

## Quality Standards

### Architecture Rules

All code must follow `.claude/rules/architecture.md`:
- Error handling: always use try-catch, log errors
- Async/await: never use floating promises
- Validation: validate input at route level
- Database: use parameterized queries
- Logging: use Pino structured logging
- Testing: >80% coverage for routes/services

### Testing Rules

All code must follow `.claude/rules/testing.md`:
- Unit tests: >60% of coverage
- Integration tests: >25% of coverage
- E2E tests: >15% of coverage
- Coverage threshold: >75% overall
- Test structure: describe/it with clear assertions
- Mock external dependencies

### Code Quality

- ESLint: zero warnings
- Prettier: consistent formatting
- TypeScript: (future) strict mode
- No hardcoded secrets (use .env)
- No console.log (use logger.info())
- Max file size: 150 lines for components
- Max function size: 30 lines

---

## Reference Documents

### Required Reading

Before starting each task:

1. **Task File** (MANDATORY):
   - TASK-0001: docs/planning/v1/tasks/TASK-0001-project-config.md
   - TASK-0002: docs/planning/v1/tasks/TASK-0002-database-config.md

2. **Specifications**:
   - Stack Reference: docs/specs/stack-reference.md
   - Domain Model: docs/specs/domain.md
   - System Architecture: docs/specs/system.md

3. **Architecture & Testing Rules**:
   - Architecture: .claude/rules/architecture.md
   - Testing: .claude/rules/testing.md

4. **Decision Records**:
   - ADR-0001: Stack Selection (docs/adr/ADR-0001-stack-selection.md)
   - ADR-0002: Async Batch Processing (docs/adr/ADR-0002-async-batch-processing.md)
   - ADR-0003: Authentication Strategy (docs/adr/ADR-0003-authentication-strategy.md)

### Optional Reading

- Planning Index: docs/planning/v1/INDEX.md
- Plan Phase Summary: PLAN-PHASE-SUMMARY.md
- User Stories: docs/planning/v1/us/US-0001-project-initialization.md, US-0002-database-setup.md

---

## Verification Checklist

### Before Starting TASK-0001

- [ ] Git repository initialized or cloned
- [ ] Node.js 20.x LTS installed
- [ ] pnpm installed globally
- [ ] Read TASK-0001 file completely
- [ ] Read stack-reference.md for exact versions
- [ ] Read architecture.md for coding standards
- [ ] Read testing.md for test requirements

### After Completing TASK-0001

- [ ] Run `pnpm test` — all tests pass
- [ ] Run `pnpm lint` — zero errors/warnings
- [ ] Run `pnpm build` — succeeds
- [ ] Run `pnpm dev` — server starts on port 3000
- [ ] Run `curl http://localhost:3000/health` — returns {"status":"ok"}
- [ ] Test pre-commit hook: `echo "test" > .env && git add .env && git commit -m "test"` — should FAIL
- [ ] Directory structure matches spec
- [ ] package.json has exact versions from stack-reference.md
- [ ] Git initial commit made

### After Completing TASK-0002

- [ ] PostgreSQL database created: `psql -l | grep auto_factures_fred`
- [ ] Run `pnpm db:migrate` — all migrations executed
- [ ] Run `psql auto_factures_fred -c "\dt"` — 6 tables exist
- [ ] Run `psql auto_factures_fred -c "SELECT COUNT(*) FROM customers;"` — returns 1
- [ ] Run `psql auto_factures_fred -c "SELECT COUNT(*) FROM products;"` — returns 3
- [ ] Run `pnpm dev` — server starts
- [ ] Run `curl http://localhost:3000/health` — returns database connected status
- [ ] Run `pnpm db:migrate` again — all migrations already executed (no errors)
- [ ] Run `pnpm db:reset` — completes without errors
- [ ] Run `pnpm test` — all tests pass (should be same as TASK-0001)

---

## Troubleshooting

### TASK-0001 Issues

**"pnpm install fails with version conflicts"**
→ Check that EXACT versions match stack-reference.md  
→ Delete pnpm-lock.yaml and try again  
→ Verify Node.js version: `node --version` (must be 20.x)

**"ESLint fails on import syntax"**
→ Check .eslintrc.js has `sourceType: 'module'`  
→ Files should use ES6 imports (`import X from 'Y'`)

**"Jest test fails"**
→ Check jest.config.js has `testEnvironment: 'node'`  
→ Verify test file imports match (use `.js` extension)

**"Pre-commit hook doesn't work"**
→ Run `npx husky install` to initialize hooks  
→ Check `.husky/pre-commit` is executable: `chmod +x .husky/pre-commit`

### TASK-0002 Issues

**"PostgreSQL database doesn't exist"**
→ Run `createdb auto_factures_fred`  
→ Or: `createdb -U postgres auto_factures_fred`  
→ Verify: `psql -l | grep auto_factures_fred`

**"DATABASE_URL connection error"**
→ Check .env has correct DATABASE_URL: `postgresql://localhost/auto_factures_fred`  
→ Verify PostgreSQL is running: `psql -l`
→ Test connection: `psql auto_factures_fred -c "SELECT NOW()"`

**"Migration fails with 'table already exists'"**
→ Database was already created in previous run  
→ Either drop and recreate: `dropdb auto_factures_fred && createdb auto_factures_fred`  
→ Or continue (migrations table should track already-executed ones)

**"Foreign key constraint error"**
→ Ensure migration steps are run in order (001, then 002)  
→ Check that enum types are created before tables using them  
→ Verify no manual edits to migration files

---

## Timeline

| Task | Duration | Start | End | Status |
|------|----------|-------|-----|--------|
| TASK-0001 | 2 days | 2026-04-27 | 2026-04-29 | Ready |
| TASK-0002 | 1-2 days | 2026-04-29 | 2026-05-01 | Blocked on TASK-0001 |
| **Batch SETUP Complete** | 3-4 days total | 2026-04-27 | 2026-05-01 | Pending |

---

## Success Criteria for Batch SETUP

When both TASK-0001 and TASK-0002 are complete:

- [x] Project structure initialized
- [x] Dependencies installed (exact versions)
- [x] Configuration files created
- [x] Database created and migrated
- [x] All tables with constraints
- [x] Seed data inserted
- [x] Health check endpoint working
- [x] Database connectivity verified
- [x] All tests passing (>75% coverage)
- [x] Linting passing
- [x] Pre-commit hooks working
- [x] Git commits made with TASK IDs

---

## Next Steps After Batch SETUP

Once TASK-0001 and TASK-0002 are complete:

1. **Review**: Check that all Definition of Done criteria are met
2. **QA**: Verify health checks work (app + database)
3. **Gates**: Run any available quality gates (future: factory-qa phase)
4. **Planning**: Generate TASK-0003+ for Epic 2 (domain entities)
5. **Timeline**: Target Sprint 1 completion by 2026-05-11

---

## Contact & Support

**For questions about**:
- Task specifications → Read the complete TASK-XXXX file
- Code standards → Review .claude/rules/architecture.md
- Stack versions → Reference docs/specs/stack-reference.md
- Database schema → See docs/specs/domain.md
- Architecture decisions → Check docs/adr/

**For blockers**:
1. Check the Troubleshooting section above
2. Review the relevant TASK file (detailed specs)
3. Reference the specification documents
4. Escalate if needed

---

**Prepared by**: Factory Build Skill  
**Phase**: ACT (Build)  
**Status**: Ready for Developer Assignment  
**Date**: 2026-04-27  

---

*This document orchestrates the implementation of Epic 1 (Foundation) for Auto-Factures Fred V1.*
