# TASK-0002: Create Database Migrations

**Epic**: EPIC-1 (Database Schema & Security)  
**User Story**: US-001 (Database Schema & Migrations)  
**Priority**: CRITICAL  
**Effort**: 2 hours

---

## Overview

Create and apply Supabase migrations to add columns, create indexes, and setup stripe_events table.

---

## Acceptance Criteria

- [ ] Migration files created in `supabase/migrations/`
- [ ] ALTER TABLE adds `stripe_session_id`, `client_id`, `paid_at` columns
- [ ] UNIQUE constraint on `stripe_session_id` prevents duplicates
- [ ] FOREIGN KEY on `client_id` references `auth.users(id)`
- [ ] Indexes created for `client_id` and `paid_at`
- [ ] stripe_events table created (audit log)
- [ ] Migration applies without errors
- [ ] Existing diagnostics data preserved (backward compatible)

---

## Definition of Done

- [ ] All SQL syntax validated
- [ ] Migration applied to development database
- [ ] FOREIGN KEY constraint enforces referential integrity
- [ ] Indexes created and functional
- [ ] Data integrity verified (no NULL values in NOT NULL columns)

---

## Implementation

### Step 1: Create Migration File

Supabase auto-generates migration timestamp. Create in `supabase/migrations/`:

Filename: `20260427000001_add_auth_stripe_columns.sql` (or similar)

```sql
-- Add columns to diagnostics table
ALTER TABLE diagnostics ADD COLUMN stripe_session_id VARCHAR UNIQUE NOT NULL;
ALTER TABLE diagnostics ADD COLUMN client_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE;
ALTER TABLE diagnostics ADD COLUMN paid_at TIMESTAMP WITH TIME ZONE NOT NULL;

-- Create indexes for query performance
CREATE INDEX idx_diagnostics_client_id ON diagnostics(client_id);
CREATE INDEX idx_diagnostics_paid_at ON diagnostics(paid_at);

-- Create stripe_events table for audit/deduplication
CREATE TABLE stripe_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stripe_event_id VARCHAR UNIQUE NOT NULL,
  event_type VARCHAR NOT NULL,
  processed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  response_code INT,
  error_message TEXT
);

CREATE INDEX idx_stripe_events_event_id ON stripe_events(stripe_event_id);
```

### Step 2: Validate Migration

```bash
# Check migration syntax (local Postgres)
psql -U postgres -d postgres -f supabase/migrations/20260427000001_add_auth_stripe_columns.sql
```

### Step 3: Apply Migration via Supabase CLI

```bash
# Push migration to development database
supabase db push

# Verify migration status
supabase migration list
```

### Step 4: Verify Schema Changes

Connect to Supabase and run:

```sql
-- Verify columns exist
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'diagnostics' 
ORDER BY ordinal_position;

-- Verify indexes
SELECT indexname FROM pg_indexes WHERE tablename = 'diagnostics';

-- Verify FOREIGN KEY
SELECT constraint_name, constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'diagnostics';
```

### Step 5: Verify stripe_events Table

```sql
-- Verify table created
SELECT * FROM information_schema.tables WHERE table_name = 'stripe_events';

-- Verify indexes
SELECT indexname FROM pg_indexes WHERE tablename = 'stripe_events';
```

---

## Deployment Sequence

1. Create migration file
2. Apply to local Supabase (via `supabase start`)
3. Test data insertion with new columns
4. Push to staging environment (if applicable)
5. Deploy to production

---

## Rollback Plan

If migration fails:

```bash
# List migrations
supabase migration list

# Revert last migration (development only)
supabase db reset

# Modify migration file and re-apply
```

---

## Technical Notes

**UNIQUE Constraint on stripe_session_id**:
- Prevents duplicate user creation if webhook replayed
- PostgreSQL enforces uniqueness at database level (not application)

**FOREIGN KEY with ON DELETE CASCADE**:
- If auth.users row deleted, diagnostics row automatically deleted
- Maintains referential integrity

**Indexes on client_id and paid_at**:
- `client_id`: Fast lookups during JWT validation (query: `SELECT paid_at WHERE client_id = ?`)
- `paid_at`: Fast queries for 30-day cleanup job (query: `DELETE WHERE paid_at < NOW() - '30 days'`)

---

## Related Specs

- Scope: **Section 4** (Database Migrations)
- Stack Reference: `/docs/specs/stack-reference.md` (Supabase version info)
