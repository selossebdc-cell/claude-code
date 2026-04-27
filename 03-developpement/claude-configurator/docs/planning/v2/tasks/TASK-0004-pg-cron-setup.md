# TASK-0004: Setup pg_cron Cleanup Job

**Epic**: EPIC-1 (Database Schema & Security)  
**User Story**: US-003 (pg_cron Automated Cleanup Job)  
**Priority**: HIGH  
**Effort**: 1 hour

---

## Overview

Enable pg_cron extension and schedule daily cleanup job to delete diagnostics >30 days old.

---

## Acceptance Criteria

- [ ] pg_cron extension enabled in Supabase project
- [ ] Cron job scheduled: delete diagnostics where `paid_at < NOW() - '30 days'`
- [ ] Job runs daily at 2 AM UTC
- [ ] Test inserts old row, verifies deleted within 24 hours
- [ ] auth.users rows NOT deleted (preservation for re-purchase)

---

## Definition of Done

- [ ] Cron job created and job ID logged
- [ ] Test confirms cleanup works
- [ ] auth.users rows preserved after cleanup

---

## Implementation

### Step 1: Enable pg_cron Extension

Connect to Supabase and execute:

```sql
CREATE EXTENSION IF NOT EXISTS pg_cron;
```

Verify:
```sql
SELECT * FROM pg_extension WHERE extname = 'pg_cron';
```

### Step 2: Schedule Cleanup Job

```sql
SELECT cron.schedule(
  'delete-expired-diagnostics',
  '0 2 * * *',  -- Daily at 2 AM UTC
  'DELETE FROM diagnostics WHERE paid_at < NOW() - interval ''30 days'''
);
```

This returns a job ID (e.g., `1`). Note it for verification.

### Step 3: Verify Job Scheduled

```sql
-- List all cron jobs
SELECT jobid, jobname, schedule, command FROM cron.job;

-- Should show:
-- jobid | jobname                      | schedule    | command
-- ------|-------------------------------|-------------|---
--  1    | delete-expired-diagnostics   | 0 2 * * *   | DELETE FROM diagnostics WHERE ...
```

### Step 4: Verify Job Execution

```sql
-- Check job history (after 1st execution)
SELECT jobid, database, username, command, status, return_message, exec_time
FROM cron.job_run_details
WHERE jobid = 1
ORDER BY start_time DESC
LIMIT 5;
```

Expected: `status = 'succeeded'` and `return_message` shows number of rows deleted.

---

## Testing

### Test: Verify Cleanup Deletes Old Data

```bash
# 1. Insert test row with old paid_at (31 days ago)
psql -U postgres -d your_db -c "INSERT INTO diagnostics (stripe_session_id, client_id, paid_at) VALUES ('test-old', '00000000-0000-0000-0000-000000000001', NOW() - interval '31 days');"

# 2. Wait for cron job to run (2 AM UTC next day), or manually trigger
psql -U postgres -d your_db -c "SELECT cron.force_run('delete-expired-diagnostics');"

# 3. Verify row deleted
psql -U postgres -d your_db -c "SELECT COUNT(*) FROM diagnostics WHERE stripe_session_id = 'test-old';"
# Expected: 0

# 4. Verify auth.users row still exists (if tied to a user)
psql -U postgres -d your_db -c "SELECT id FROM auth.users WHERE id = '00000000-0000-0000-0000-000000000001';"
# Expected: User UUID returned (row preserved)
```

### Test Scenario (Full):

```typescript
// 1. Create test user
const testUser = await supabase.auth.admin.createUser({ email: 'old@test.com' });

// 2. Insert diagnostics row with old paid_at (31 days ago)
const oldPaidAt = new Date();
oldPaidAt.setDate(oldPaidAt.getDate() - 31);
await supabaseAdmin
  .from('diagnostics')
  .insert({
    stripe_session_id: 'cs_old_test',
    client_id: testUser.id,
    paid_at: oldPaidAt.toISOString()
  });

// 3. Verify row exists
let rows = await supabaseAdmin
  .from('diagnostics')
  .select('*')
  .eq('stripe_session_id', 'cs_old_test');
assert(rows.length === 1, 'Old row inserted');

// 4. Trigger cron job
await supabaseAdmin.rpc('cron.force_run', { job_id: 1 });
// Or wait for 2 AM UTC

// 5. Verify row deleted
rows = await supabaseAdmin
  .from('diagnostics')
  .select('*')
  .eq('stripe_session_id', 'cs_old_test');
assert(rows.length === 0, 'Old row deleted by cron');

// 6. Verify user preserved
const user = await supabaseAdmin.auth.admin.getUserById(testUser.id);
assert(user, 'auth.users row preserved');
```

---

## Monitoring

Add monitoring to track cleanup job:

```sql
-- Monitor job success rate
SELECT 
  DATE(start_time) as run_date,
  COUNT(*) as total_runs,
  COUNT(CASE WHEN status = 'succeeded' THEN 1 END) as succeeded,
  COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed
FROM cron.job_run_details
WHERE jobid = 1
GROUP BY DATE(start_time)
ORDER BY run_date DESC
LIMIT 30;
```

---

## Troubleshooting

**Job not running?**

1. Check extension enabled: `SELECT * FROM pg_extension WHERE extname = 'pg_cron';`
2. Check cron.job table: `SELECT * FROM cron.job WHERE jobname = 'delete-expired-diagnostics';`
3. Check job history for errors: `SELECT * FROM cron.job_run_details WHERE jobid = 1 ORDER BY start_time DESC;`
4. Verify time zone: Supabase uses UTC by default. Ensure `'0 2 * * *'` is 2 AM UTC (your intended time).

**Timezone Adjustments**:
- Current schedule: `'0 2 * * *'` = 2 AM UTC
- Change to `'0 14 * * *'` for 2 PM UTC
- Change to `'0 8 * * *'` for 8 AM UTC

---

## Deployment Sequence

1. Enable pg_cron extension
2. Create cron job
3. Verify scheduled (check cron.job table)
4. Run test to confirm cleanup works
5. Monitor for 1 week to ensure reliability

---

## Related Specs

- Scope: **Section 4** (pg_cron Job, Q-008)
- Brief: **Objective 3** (Data retention: 30 days for diagnostics, forever for auth.users)
