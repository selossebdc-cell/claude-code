-- MIGRATION: Setup pg_cron extension and schedule 30-day data retention cleanup
-- Purpose: Auto-delete diagnostics older than 30 days for GDPR compliance + data hygiene
-- Security: Preserves auth.users rows (allows re-purchase), only deletes diagnostics data

-- Step 1: Enable pg_cron extension
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Step 2: Schedule daily cleanup job at 2 AM UTC
-- Deletes diagnostics where paid_at < NOW() - 30 days
-- Preserves auth.users rows (for user to re-purchase if needed)
SELECT cron.schedule(
  'delete-expired-diagnostics',
  '0 2 * * *',  -- Daily at 2 AM UTC (cron format: minute hour day month weekday)
  'DELETE FROM diagnostics WHERE paid_at < NOW() - interval ''30 days'''
);

-- Step 3: Optional - Schedule monthly audit log cleanup (stripe_events)
-- Keep stripe_events for 90 days for debugging
SELECT cron.schedule(
  'delete-old-stripe-events',
  '0 3 1 * *',  -- Monthly on 1st day at 3 AM UTC
  'DELETE FROM stripe_events WHERE processed_at < NOW() - interval ''90 days'''
);

-- Comment: Job IDs are auto-generated. Run `SELECT * FROM cron.job;` to verify.
-- Expected output:
--   jobid | jobname                      | schedule    | command
--   ------|-------------------------------|-------------|---
--     1   | delete-expired-diagnostics   | 0 2 * * *   | DELETE FROM diagnostics WHERE ...
--     2   | delete-old-stripe-events     | 0 3 1 * *   | DELETE FROM stripe_events WHERE ...
