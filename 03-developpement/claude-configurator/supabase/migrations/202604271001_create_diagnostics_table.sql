-- Create diagnostics table for metadata persistence
CREATE TABLE IF NOT EXISTS diagnostics (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID NOT NULL UNIQUE,
  client_name TEXT,
  started_at TIMESTAMP DEFAULT NOW(),
  ended_at TIMESTAMP,
  metadata JSONB NOT NULL DEFAULT '{}',
  conversation_history JSONB NOT NULL DEFAULT '[]',
  diagnostic_status VARCHAR(50) DEFAULT 'in_progress',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_diagnostics_session_id ON diagnostics(session_id);
CREATE INDEX IF NOT EXISTS idx_diagnostics_started_at ON diagnostics(started_at);
CREATE INDEX IF NOT EXISTS idx_diagnostics_status ON diagnostics(diagnostic_status);

-- Create index on JSONB metadata for efficient queries
CREATE INDEX IF NOT EXISTS idx_diagnostics_metadata_pain_points
  ON diagnostics USING GIN ((metadata -> 'pain_points'));
CREATE INDEX IF NOT EXISTS idx_diagnostics_metadata_opportunities
  ON diagnostics USING GIN ((metadata -> 'claude_opportunities'));

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_diagnostics_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS diagnostics_updated_at_trigger ON diagnostics;
CREATE TRIGGER diagnostics_updated_at_trigger
BEFORE UPDATE ON diagnostics
FOR EACH ROW
EXECUTE FUNCTION update_diagnostics_updated_at();
