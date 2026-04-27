-- MIGRATION: Add authentication & Stripe payment columns to diagnostics
-- Purpose: Enable Stripe payment tracking, user authentication, and webhook deduplication
-- Created: 2026-04-27

-- Step 1: Add columns to diagnostics table
-- stripe_session_id: Stripe checkout session ID (unique key for idempotence)
-- client_id: Foreign key to auth.users (for RLS isolation)
-- paid_at: Payment timestamp (for 30-day retention cleanup)

ALTER TABLE diagnostics
ADD COLUMN stripe_session_id VARCHAR UNIQUE NOT NULL DEFAULT gen_random_uuid()::text,
ADD COLUMN client_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
ADD COLUMN paid_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW();

-- Step 2: Create indexes for query performance
-- idx_diagnostics_client_id: Used in RLS policies (auth.uid() = client_id)
-- idx_diagnostics_paid_at: Used in pg_cron cleanup (WHERE paid_at < NOW() - interval '30 days')

CREATE INDEX idx_diagnostics_client_id ON diagnostics(client_id);
CREATE INDEX idx_diagnostics_paid_at ON diagnostics(paid_at);

-- Step 3: Create stripe_events table for webhook audit log & deduplication
-- Prevents processing same Stripe event twice (replay safety)
-- Tracks webhook status for troubleshooting

CREATE TABLE stripe_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stripe_event_id VARCHAR UNIQUE NOT NULL,
  event_type VARCHAR NOT NULL,
  event_data JSONB,
  processed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  response_code INT,
  error_message TEXT,
  client_email VARCHAR
);

CREATE INDEX idx_stripe_events_event_id ON stripe_events(stripe_event_id);
CREATE INDEX idx_stripe_events_processed_at ON stripe_events(processed_at);
