# BUILD — EPIC-4: Metadata Enrichment System

## Overview
Implémenter le système complet de métadonnées enrichies: schéma JSON, persistence Supabase, real-time updates, passing downstream.

**Statut**: Ready to implement  
**Effort**: 3 days (0.5 day design + 1 day database + 1.5 days integration)  
**Blocker**: None (can run parallel with EPIC-1)  
**Dependencies**: EPIC-1, EPIC-2, EPIC-3 (populate metadata)

---

## Implementation Steps

### Step 1: Define JSON Schema (Day 0.5)
Formalize the metadata JSON structure (complete definition below).

**Location**: Documentation + Chat Edge Function type definitions  
**Action**: Create TypeScript interfaces for metadata objects  

### Step 2: Database Setup (Day 1)
Create Supabase table for storing diagnostic metadata.

**Action**:
- Run SQL migration: create `diagnostics` table
- Add `metadata` column (JSONB type for query efficiency)
- Create indexes for session_id, client_id
- Set up retention policy (auto-delete after 90 days)

### Step 3: Integration into Chat Function (Day 1-1.5)
- Initialize metadata on diagnostic start
- Update metadata after each response
- Persist to Supabase after each turn
- Return metadata in SSE stream

**Changes needed**:
- Load metadata from Supabase on diagnostic start
- Update after pattern detection (EPIC-2)
- Update after opportunity identification (EPIC-3)
- Persist after each response
- Include in response stream

### Step 4: Testing (Day 1.5-2)
- Test persistence (metadata saved correctly)
- Test retrieval (metadata loaded in new session)
- Test size < 2KB constraint
- Test real-time updates
- Test downstream passing to generate-config

---

## JSON Metadata Schema (Complete Definition)

```json
{
  "session_id": "uuid - unique diagnostic session identifier",
  "started_at": "ISO 8601 timestamp when diagnostic began",
  "client_name": "string (optional) - client's name if provided",
  "turns_count": "number - how many Q&A exchanges so far",
  
  "pain_points": [
    {
      "id": "pp_NNN - unique identifier",
      "area": "string - category (compliance, documentation, timeline, etc.)",
      "detail": "string - specific situation described by client",
      "severity": "high | medium | low",
      "context": "string - where mentioned (Turn N: ...)",
      "linked_opportunities": ["oc_001", "oc_002"],
      "resolved": false
    }
  ],
  
  "patterns_detected": [
    {
      "id": "pd_NNN - unique identifier",
      "type": "recurring_blocage | work_style | strength | risk_indicator",
      "pattern": "string - human-readable pattern description",
      "evidence": ["quote 1", "quote 2"],
      "confidence": 0.85,
      "consequence": "string - what this means for client",
      "implication_for_claude": "string - how Claude helps"
    }
  ],
  
  "work_style_traits": [
    {
      "id": "ws_NNN",
      "trait": "string (pragmatic, structured, feeling-based, innovative, etc.)",
      "manifestation": "string - how it shows up in their work",
      "implication": "string - what this means for config",
      "strength": true | false
    }
  ],
  
  "claude_opportunities": [
    {
      "id": "oc_NNN - unique identifier",
      "opportunity": "string - opportunity name (Compliance Hub, etc.)",
      "description": "string - what it does",
      "linked_pain_point": "pp_NNN | null",
      "linked_pattern": "pd_NNN | null",
      "why_claude_transforms": "string - why Claude changes the game",
      "agent_role": "string - which agent implements it",
      "agent_type": "mandatory | contextual",
      "priority": 1-5,
      "impact_estimate": "high | medium | low",
      "effort_estimate": "high | medium | low",
      "confidence": 0.0-1.0,
      "implemented": false
    }
  ],
  
  "assumptions_validated": [
    {
      "id": "av_NNN",
      "assumption": "string - what we thought about client",
      "validation_status": "confirmed | disproven | pending",
      "confidence": 0.0-1.0,
      "evidence": "string - proof or reason"
    }
  ],
  
  "coverage_tracking": {
    "blocs_covered": ["Identity", "Offering", "Challenges"],
    "blocs_pending": ["Security", "Voice", "Proposals"],
    "coverage_percentage": 55,
    "last_updated": "ISO 8601 timestamp"
  },
  
  "conversation_quality_metrics": {
    "turns_count": 8,
    "avg_response_length": 180,
    "client_engagement_level": "high | medium | low",
    "clarity_score": 0.87,
    "questions_asked": 5,
    "blockers_identified": 3
  },
  
  "metadata_version": "1.0",
  "last_updated": "ISO 8601 timestamp"
}
```

---

## Database Setup (SQL)

```sql
-- Create diagnostics table
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

-- Set retention policy (auto-delete after 90 days if not needed)
-- Note: Adjust based on your data retention policy
CREATE OR REPLACE FUNCTION delete_old_diagnostics()
RETURNS void AS $$
BEGIN
  DELETE FROM diagnostics
  WHERE diagnostic_status = 'completed'
    AND ended_at < NOW() - INTERVAL '90 days';
END;
$$ LANGUAGE plpgsql;

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
```

---

## Chat Edge Function Integration

```javascript
// Initialize metadata on diagnostic start
async function initializeDiagnostic(sessionId, clientName = null) {
  const initialMetadata = {
    session_id: sessionId,
    started_at: new Date().toISOString(),
    client_name: clientName,
    turns_count: 0,
    pain_points: [],
    patterns_detected: [],
    work_style_traits: [],
    claude_opportunities: [],
    assumptions_validated: [],
    coverage_tracking: {
      blocs_covered: [],
      blocs_pending: ["Identity", "Offering", "Daily", "Challenges", "Constraints", "Security", "Work Style", "Voice", "Proposals"],
      coverage_percentage: 0,
      last_updated: new Date().toISOString()
    },
    conversation_quality_metrics: {
      turns_count: 0,
      avg_response_length: 0,
      client_engagement_level: "medium",
      clarity_score: 0,
      questions_asked: 0,
      blockers_identified: 0
    },
    metadata_version: "1.0",
    last_updated: new Date().toISOString()
  };
  
  // Save to Supabase
  const { data, error } = await supabase
    .from('diagnostics')
    .insert({
      session_id: sessionId,
      client_name: clientName,
      metadata: initialMetadata,
      conversation_history: [],
      diagnostic_status: 'in_progress'
    })
    .select();
  
  if (error) {
    console.error('Failed to initialize diagnostic:', error);
    throw error;
  }
  
  return initialMetadata;
}

// Update metadata after each response
async function updateMetadata(sessionId, updates) {
  const { data, error: fetchError } = await supabase
    .from('diagnostics')
    .select('metadata, conversation_history')
    .eq('session_id', sessionId)
    .single();
  
  if (fetchError) throw fetchError;
  
  const currentMetadata = data.metadata || {};
  
  // Merge updates (from EPIC-1, EPIC-2, EPIC-3)
  const updatedMetadata = {
    ...currentMetadata,
    ...updates,
    turns_count: (currentMetadata.turns_count || 0) + 1,
    last_updated: new Date().toISOString(),
    coverage_tracking: {
      ...currentMetadata.coverage_tracking,
      coverage_percentage: calculateCoverage(currentMetadata),
      last_updated: new Date().toISOString()
    }
  };
  
  // Validate size constraint
  const metadataSize = JSON.stringify(updatedMetadata).length;
  if (metadataSize > 2048) {
    console.warn(`Metadata size ${metadataSize} exceeds 2KB limit — trimming`);
    // Keep only top 5 opportunities, top 3 patterns
    updatedMetadata.claude_opportunities = updatedMetadata.claude_opportunities.slice(0, 5);
    updatedMetadata.patterns_detected = updatedMetadata.patterns_detected.slice(0, 3);
  }
  
  // Persist to Supabase
  const { error: updateError } = await supabase
    .from('diagnostics')
    .update({
      metadata: updatedMetadata,
      updated_at: new Date().toISOString()
    })
    .eq('session_id', sessionId);
  
  if (updateError) {
    console.error('Failed to update metadata:', updateError);
    throw updateError;
  }
  
  return updatedMetadata;
}

// Retrieve metadata for new session or continuation
async function getOrCreateMetadata(sessionId, clientName = null) {
  const { data, error } = await supabase
    .from('diagnostics')
    .select('metadata')
    .eq('session_id', sessionId)
    .single();
  
  if (error && error.code === 'PGRST116') {
    // Not found — initialize new
    return await initializeDiagnostic(sessionId, clientName);
  } else if (error) {
    throw error;
  }
  
  return data.metadata;
}

// Calculate bloc coverage percentage
function calculateCoverage(metadata) {
  const mentionedBlocs = new Set();
  
  // Add blocs mentioned in pain points
  metadata.pain_points?.forEach(pp => {
    if (pp.area.includes('challenge')) mentionedBlocs.add('Challenges');
    if (pp.area.includes('constraint')) mentionedBlocs.add('Constraints');
    if (pp.area.includes('security')) mentionedBlocs.add('Security');
  });
  
  // Add blocs from patterns
  metadata.patterns_detected?.forEach(pd => {
    if (pd.type === 'work_style') mentionedBlocs.add('Work Style');
  });
  
  // Add blocs from opportunities
  metadata.claude_opportunities?.forEach(oc => {
    if (oc.agent_role === 'Stratégie') mentionedBlocs.add('Offering');
    if (oc.agent_role === 'Planif') mentionedBlocs.add('Daily');
  });
  
  const totalBlocs = 9;
  const coveredBlocs = mentionedBlocs.size;
  
  return Math.round((coveredBlocs / totalBlocs) * 100);
}

// In POST /chat handler, after generating response:
const userMessage = req.body.message;
const sessionId = req.body.session_id;

// Get current metadata
let metadata = await getOrCreateMetadata(sessionId, req.body.client_name);

// [EPIC-2] Detect patterns
const { newPatterns, updatedMetadata: metadataAfterPatterns } = detectPatterns(
  userMessage,
  conversationHistory,
  metadata
);

// [EPIC-3] Identify opportunities
const opportunities = identifyOpportunities(
  metadataAfterPatterns,
  workContext
);

// Merge all updates
const finalMetadata = {
  ...metadataAfterPatterns,
  claude_opportunities: [
    ...(metadataAfterPatterns.claude_opportunities || []),
    ...opportunities
  ],
  conversation_quality_metrics: {
    ...metadataAfterPatterns.conversation_quality_metrics,
    turns_count: (metadataAfterPatterns.turns_count || 0) + 1,
    avg_response_length: Math.round(assistantMessage.length)
  }
};

// Persist metadata
await updateMetadata(sessionId, finalMetadata);

// Return to frontend (SSE)
sendEvent('metadata_updated', finalMetadata);
sendEvent('message', {
  role: 'assistant',
  content: assistantMessage
});
```

---

## Metadata Size Optimization

Keep metadata under 2KB with these strategies:

```javascript
function compressMetadata(metadata) {
  // Keep only recent patterns (last 5)
  if (metadata.patterns_detected?.length > 5) {
    metadata.patterns_detected = metadata.patterns_detected.slice(-5);
  }
  
  // Keep only active opportunities (top 5 by priority)
  if (metadata.claude_opportunities?.length > 5) {
    metadata.claude_opportunities = metadata.claude_opportunities
      .sort((a, b) => a.priority - b.priority)
      .slice(0, 5);
  }
  
  // Remove evidence arrays (keep only summary)
  metadata.patterns_detected?.forEach(p => {
    if (p.evidence?.length > 2) {
      p.evidence = p.evidence.slice(0, 2);
    }
  });
  
  // Keep only highest-severity pain points
  if (metadata.pain_points?.length > 8) {
    const severityScore = { high: 3, medium: 2, low: 1 };
    metadata.pain_points = metadata.pain_points
      .sort((a, b) => severityScore[b.severity] - severityScore[a.severity])
      .slice(0, 8);
  }
  
  return metadata;
}
```

---

## Testing Checklist

Before proceeding to EPIC-5:

- [ ] Test 1: Metadata persists (save → retrieve → matches)
- [ ] Test 2: Metadata updates in real-time (each response updates)
- [ ] Test 3: Size constraint (metadata always < 2KB)
- [ ] Test 4: Compression works (when exceeding, top items preserved)
- [ ] Test 5: Retrieval on continuation (session continues, metadata loads)
- [ ] Test 6: Downstream passing (metadata received by generate-config)
- [ ] Test 7: 5+ full diagnostics (end-to-end, validate all metadata components)

---

## Monitoring & Maintenance

```javascript
// Monitor metadata size over time
async function monitorMetadataSize() {
  const { data } = await supabase
    .from('diagnostics')
    .select('session_id, metadata')
    .order('turns_count', { ascending: false })
    .limit(100);
  
  data?.forEach(diag => {
    const size = JSON.stringify(diag.metadata).length;
    if (size > 1800) {
      console.warn(`Session ${diag.session_id} metadata near limit: ${size} bytes`);
    }
  });
}

// Run daily to monitor
setInterval(monitorMetadataSize, 24 * 60 * 60 * 1000);
```

---

## Rollback Plan

If metadata system causes issues:
1. Disable metadata persistence (comment out `updateMetadata()`)
2. Chat Edge Function continues to work (metadata just in memory)
3. No metadata passed to generate-config (config generation works without it)
4. Metadata lost after session ends (acceptable for rollback)
5. Document issue for EPIC-4 iteration

---

## Integration with Downstream Systems

Metadata is consumed by:
1. **EPIC-5** (Strategic Synthesis) — uses all metadata to generate synthesis
2. **EPIC-7** (Generate-Config v20+) — uses opportunities + metadata to inform agent config

Format for downstream:
```json
{
  "diagnostic_metadata": {
    "pain_points": [...],
    "patterns_detected": [...],
    "claude_opportunities": [...],
    "work_style_traits": [...]
  },
  "conversation_metadata": {
    "turns_count": 12,
    "engagement_level": "high",
    "clarity_score": 0.85
  }
}
```

---

**EPIC-4 Status**: Specification complete  
**Can run parallel**: EPIC-1  
**Required before**: EPIC-5, EPIC-7  
**Next**: EPIC-5 (Strategic Synthesis Generator)
