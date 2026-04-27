# US-003: pg_cron Automated Cleanup Job

**EPIC**: EPIC-1 (Database Schema & Security)  
**User Story**: As an infrastructure engineer, I need automated cleanup so that old diagnostic data is deleted after 30 days.

---

## Acceptance Criteria

- [ ] pg_cron extension enabled in Supabase project
- [ ] Cron job created: `DELETE FROM diagnostics WHERE paid_at < NOW() - interval '30 days'`
- [ ] Job scheduled to run daily at 2 AM UTC
- [ ] Job runs only once per day (no duplicate executions)
- [ ] Only `diagnostics` rows deleted; `auth.users` preserved (allows re-purchase)
- [ ] Test inserts 30+ day old row, verifies deleted within 24 hours

## Definition of Done

1. pg_cron extension verified as enabled
2. Cron job scheduled successfully
3. Job ID returned and logged
4. Test data with old `paid_at` inserted
5. Wait ≤24h and verify row deleted
6. Verify auth.users row for that user still exists

## Technical Details

**Enable pg_cron**:
```sql
CREATE EXTENSION IF NOT EXISTS pg_cron;
```

**Create Cron Job**:
```sql
SELECT cron.schedule(
  'delete-expired-diagnostics',
  '0 2 * * *',  -- Daily at 2 AM UTC
  'DELETE FROM diagnostics WHERE paid_at < NOW() - interval ''30 days'''
);
```

**Verify Job**:
```sql
SELECT * FROM cron.job WHERE jobname = 'delete-expired-diagnostics';
```

**Test Scenario**:
1. Insert row: `INSERT INTO diagnostics (stripe_session_id, client_id, paid_at) VALUES ('test-old', user_uuid, NOW() - interval '31 days')`
2. Wait for cron job to run (or manually trigger for testing)
3. Verify row deleted: `SELECT COUNT(*) FROM diagnostics WHERE stripe_session_id = 'test-old'` → should return 0
4. Verify user still exists: `SELECT id FROM auth.users WHERE id = user_uuid` → should return user UUID

## Dependencies

Requires US-001 (diagnostics table exists).

## Related Specs

- Scope: **Section 4** (pg_cron Job, Q-008)
- Brief: **Objective 3** (Data retention: 30 days for diagnostics, forever for auth.users)
