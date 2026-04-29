-- MIGRATION: Enable RLS and create access control policies
-- Purpose: Prevent cross-user data leakage, allow admin access
-- Security: Implements Secure-by-Design principle (auth.uid() = client_id OR admin)

-- Step 1: Enable Row Level Security on diagnostics table
ALTER TABLE diagnostics ENABLE ROW LEVEL SECURITY;

-- Step 2: CREATE SELECT policy
-- Users can see their own diagnostics
-- Admins can see all diagnostics (admin account verification required separately)
DROP POLICY IF EXISTS "Users see own diagnostics" ON diagnostics;
CREATE POLICY "Users see own diagnostics"
  ON diagnostics
  FOR SELECT
  USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );

-- Step 3: CREATE INSERT policy
-- Only authenticated users can insert (prevents anonymous writes)
-- client_id is set from auth.uid() during insert
DROP POLICY IF EXISTS "Users can create diagnostics" ON diagnostics;
CREATE POLICY "Users can create diagnostics"
  ON diagnostics
  FOR INSERT
  WITH CHECK (auth.uid()::uuid IS NOT NULL);

-- Step 4: CREATE UPDATE policy
-- Users can update their own rows
-- Admins can update any row
DROP POLICY IF EXISTS "Users update own diagnostics" ON diagnostics;
CREATE POLICY "Users update own diagnostics"
  ON diagnostics
  FOR UPDATE
  USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  )
  WITH CHECK (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );

-- Step 5: CREATE DELETE policy
-- Users can delete their own rows
-- Admins can delete any row
DROP POLICY IF EXISTS "Users delete own diagnostics" ON diagnostics;
CREATE POLICY "Users delete own diagnostics"
  ON diagnostics
  FOR DELETE
  USING (
    (auth.uid()::uuid = client_id)
    OR (auth.role() = 'admin')
  );

-- Step 6: RLS on stripe_events table (audit log, admin-only)
ALTER TABLE stripe_events ENABLE ROW LEVEL SECURITY;

-- Only admin can read stripe_events (for debugging webhooks)
DROP POLICY IF EXISTS "Admin only access to stripe_events" ON stripe_events;
CREATE POLICY "Admin only access to stripe_events"
  ON stripe_events
  FOR SELECT
  USING (auth.role() = 'admin');

-- Only admin can insert (via service_role during webhook processing)
DROP POLICY IF EXISTS "Admin only insert stripe_events" ON stripe_events;
CREATE POLICY "Admin only insert stripe_events"
  ON stripe_events
  FOR INSERT
  WITH CHECK (auth.role() = 'admin');
