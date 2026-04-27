# US-001: Database Schema & Migrations

**EPIC**: EPIC-1 (Database Schema & Security)  
**User Story**: As an engineer, I need the database schema updated so that I can store payment and authentication data.

---

## Acceptance Criteria

- [ ] `diagnostics` table has `stripe_session_id` (VARCHAR, UNIQUE, NOT NULL)
- [ ] `diagnostics` table has `client_id` (UUID, FK to auth.users, NOT NULL)
- [ ] `diagnostics` table has `paid_at` (TIMESTAMP WITH TIME ZONE, NOT NULL)
- [ ] `diagnostics` table has `created_at` (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())
- [ ] Indexes created on `client_id` and `paid_at` for query performance
- [ ] Existing diagnostics data preserved during migration (backward compatible)

## Definition of Done

1. Migration files created in `supabase/migrations/`
2. All SQL syntax validated (no duplicate columns, valid types)
3. Indexes created for `client_id` and `paid_at`
4. Migration applied to development database successfully
5. FOREIGN KEY constraint enforces referential integrity
6. UNIQUE constraint on `stripe_session_id` prevents duplicates

## Technical Details

**Table Structure**:
```sql
ALTER TABLE diagnostics ADD COLUMN stripe_session_id VARCHAR UNIQUE NOT NULL;
ALTER TABLE diagnostics ADD COLUMN client_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE;
ALTER TABLE diagnostics ADD COLUMN paid_at TIMESTAMP WITH TIME ZONE NOT NULL;
CREATE INDEX idx_diagnostics_client_id ON diagnostics(client_id);
CREATE INDEX idx_diagnostics_paid_at ON diagnostics(paid_at);
```

**Rationale**:
- `stripe_session_id`: Unique identifier for idempotence (prevents duplicate users on webhook replay)
- `client_id`: Link to Supabase auth user (enables RLS and payment validation)
- `paid_at`: Timestamp for 30-day retention logic and payment status checks
- Indexes: Fast lookups for JWT validation (`client_id`) and cleanup job (`paid_at`)

## Dependencies

None (first US in EPIC-1).

## Related Specs

- Scope: **Section 4** (Database Migrations)
- Brief: **Objective 3** (Data retention & RLS)
