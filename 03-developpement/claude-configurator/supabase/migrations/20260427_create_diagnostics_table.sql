-- Create diagnostics table for metadata persistence
CREATE TABLE IF NOT EXISTS diagnostics (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID NOT NULL UNIQUE,
  client_id UUID REFERENCES auth.users(id),
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
CREATE INDEX idx_diagnostics_session_id ON diagnostics(session_id);
CREATE INDEX idx_diagnostics_client_id ON diagnostics(client_id);
CREATE INDEX idx_diagnostics_started_at ON diagnostics(started_at);
CREATE INDEX idx_diagnostics_status ON diagnostics(diagnostic_status);

-- Create index on JSONB metadata for efficient queries
CREATE INDEX idx_diagnostics_metadata_pain_points
  ON diagnostics USING GIN (metadata -> 'pain_points');
CREATE INDEX idx_diagnostics_metadata_opportunities
  ON diagnostics USING GIN (metadata -> 'claude_opportunities');

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_diagnostics_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER diagnostics_updated_at_trigger
BEFORE UPDATE ON diagnostics
FOR EACH ROW
EXECUTE FUNCTION update_diagnostics_updated_at();

-- Enable RLS for security
ALTER TABLE diagnostics ENABLE ROW LEVEL SECURITY;

-- Allow authenticated users to view/update their own diagnostics
CREATE POLICY "Users can view own diagnostics"
  ON diagnostics FOR SELECT
  USING (auth.uid() = client_id OR client_id IS NULL);

CREATE POLICY "Users can update own diagnostics"
  ON diagnostics FOR UPDATE
  USING (auth.uid() = client_id OR client_id IS NULL);

-- Allow service role (Edge Functions) full access
CREATE POLICY "Service role has full access"
  ON diagnostics FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');
