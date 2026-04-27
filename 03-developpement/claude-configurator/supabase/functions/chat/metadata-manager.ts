// Metadata Manager for Diagnostic System
// Handles initialization, updates, and retrieval of diagnostic metadata

import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";

// Initialize Supabase client
const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";

const supabase = createClient(supabaseUrl, supabaseServiceKey);

// Type definitions
export interface PainPoint {
  id?: string;
  area: string;
  detail?: string;
  severity: "high" | "medium" | "low";
  context?: string;
  linked_opportunities?: string[];
  resolved?: boolean;
}

export interface Pattern {
  id?: string;
  type: "recurring_blocage" | "work_style" | "strength" | "risk_indicator";
  pattern: string;
  evidence: string[];
  confidence?: number;
  consequence?: string;
  implication_for_claude?: string;
}

export interface WorkStyleTrait {
  id?: string;
  trait: string;
  manifestation?: string;
  implication?: string;
  strength?: boolean;
}

export interface ClaudeOpportunity {
  id?: string;
  opportunity: string;
  description: string;
  linked_pain_point?: string;
  linked_pattern?: string;
  why_claude_transforms?: string;
  agent_role?: string;
  agent_type?: "mandatory" | "contextual";
  priority?: number;
  impact_estimate?: "high" | "medium" | "low";
  effort_estimate?: "high" | "medium" | "low";
  confidence?: number;
  implemented?: boolean;
}

export interface DiagnosticMetadata {
  session_id: string;
  started_at: string;
  client_name?: string;
  turns_count: number;
  pain_points: PainPoint[];
  patterns_detected: Pattern[];
  work_style_traits: WorkStyleTrait[];
  claude_opportunities: ClaudeOpportunity[];
  assumptions_validated?: Array<{
    id?: string;
    assumption: string;
    validation_status: "confirmed" | "disproven" | "pending";
    confidence?: number;
    evidence?: string;
  }>;
  coverage_tracking: {
    blocs_covered: string[];
    blocs_pending: string[];
    coverage_percentage: number;
    last_updated?: string;
  };
  conversation_quality_metrics: {
    turns_count: number;
    avg_response_length: number;
    client_engagement_level: "high" | "medium" | "low";
    clarity_score: number;
    questions_asked?: number;
    blockers_identified?: number;
  };
  metadata_version: string;
  last_updated: string;
}

/**
 * Initialize metadata for a new diagnostic session
 */
export async function initializeDiagnostic(
  sessionId: string,
  clientName?: string
): Promise<DiagnosticMetadata> {
  const initialMetadata: DiagnosticMetadata = {
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
      blocs_pending: [
        "Identity",
        "Offering",
        "Daily",
        "Challenges",
        "Constraints",
        "Security",
        "Work Style",
        "Voice",
        "Proposals",
      ],
      coverage_percentage: 0,
      last_updated: new Date().toISOString(),
    },
    conversation_quality_metrics: {
      turns_count: 0,
      avg_response_length: 0,
      client_engagement_level: "medium",
      clarity_score: 0,
      questions_asked: 0,
      blockers_identified: 0,
    },
    metadata_version: "1.0",
    last_updated: new Date().toISOString(),
  };

  // Save to Supabase
  const { data, error } = await supabase
    .from("diagnostics")
    .insert({
      session_id: sessionId,
      client_name: clientName,
      metadata: initialMetadata,
      conversation_history: [],
      diagnostic_status: "in_progress",
    })
    .select();

  if (error) {
    console.error("Failed to initialize diagnostic:", error);
    throw error;
  }

  return initialMetadata;
}

/**
 * Get or create metadata for a session
 */
export async function getOrCreateMetadata(
  sessionId: string,
  clientName?: string
): Promise<DiagnosticMetadata> {
  const { data, error } = await supabase
    .from("diagnostics")
    .select("metadata")
    .eq("session_id", sessionId)
    .single();

  if (error && error.code === "PGRST116") {
    // Not found — initialize new
    return await initializeDiagnostic(sessionId, clientName);
  } else if (error) {
    console.error("Error retrieving metadata:", error);
    throw error;
  }

  return data?.metadata || {};
}

/**
 * Update metadata after each diagnostic turn
 */
export async function updateMetadata(
  sessionId: string,
  updates: Partial<DiagnosticMetadata>
): Promise<DiagnosticMetadata> {
  const { data, error: fetchError } = await supabase
    .from("diagnostics")
    .select("metadata, conversation_history")
    .eq("session_id", sessionId)
    .single();

  if (fetchError) {
    console.error("Error fetching current metadata:", fetchError);
    throw fetchError;
  }

  const currentMetadata = data?.metadata || {};

  // Merge updates
  const updatedMetadata: DiagnosticMetadata = {
    ...currentMetadata,
    ...updates,
    turns_count: (currentMetadata.turns_count || 0) + 1,
    last_updated: new Date().toISOString(),
    coverage_tracking: {
      ...(currentMetadata.coverage_tracking || {}),
      coverage_percentage: calculateCoverage(currentMetadata),
      last_updated: new Date().toISOString(),
    },
  };

  // Validate size constraint (< 2KB)
  const metadataSize = JSON.stringify(updatedMetadata).length;
  if (metadataSize > 2048) {
    console.warn(
      `Metadata size ${metadataSize} exceeds 2KB limit — compressing`
    );
    // Keep only top 5 opportunities, top 3 patterns
    updatedMetadata.claude_opportunities = (
      updatedMetadata.claude_opportunities || []
    ).slice(0, 5);
    updatedMetadata.patterns_detected = (
      updatedMetadata.patterns_detected || []
    ).slice(0, 3);
  }

  // Persist to Supabase
  const { error: updateError } = await supabase
    .from("diagnostics")
    .update({
      metadata: updatedMetadata,
      updated_at: new Date().toISOString(),
    })
    .eq("session_id", sessionId);

  if (updateError) {
    console.error("Failed to update metadata:", updateError);
    throw updateError;
  }

  return updatedMetadata;
}

/**
 * Save conversation message to history
 */
export async function saveConversationMessage(
  sessionId: string,
  role: "user" | "assistant",
  content: string
): Promise<void> {
  const { data, error: fetchError } = await supabase
    .from("diagnostics")
    .select("conversation_history")
    .eq("session_id", sessionId)
    .single();

  if (fetchError) {
    console.error("Error fetching conversation history:", fetchError);
    throw fetchError;
  }

  const conversationHistory = data?.conversation_history || [];
  conversationHistory.push({
    role,
    content,
    timestamp: new Date().toISOString(),
  });

  // Keep only last 100 messages to manage size
  const trimmedHistory =
    conversationHistory.length > 100
      ? conversationHistory.slice(-100)
      : conversationHistory;

  const { error: updateError } = await supabase
    .from("diagnostics")
    .update({
      conversation_history: trimmedHistory,
      updated_at: new Date().toISOString(),
    })
    .eq("session_id", sessionId);

  if (updateError) {
    console.error("Failed to save conversation message:", updateError);
    throw updateError;
  }
}

/**
 * Calculate diagnostic coverage percentage
 */
function calculateCoverage(metadata: Partial<DiagnosticMetadata>): number {
  const mentionedBlocs = new Set<string>();

  // Add blocs mentioned in pain points
  (metadata.pain_points || []).forEach((pp) => {
    if (pp.area.toLowerCase().includes("challenge"))
      mentionedBlocs.add("Challenges");
    if (pp.area.toLowerCase().includes("constraint"))
      mentionedBlocs.add("Constraints");
    if (pp.area.toLowerCase().includes("security"))
      mentionedBlocs.add("Security");
    if (pp.area.toLowerCase().includes("proposal"))
      mentionedBlocs.add("Proposals");
  });

  // Add blocs from patterns
  (metadata.patterns_detected || []).forEach((pd) => {
    if (pd.type === "work_style") mentionedBlocs.add("Work Style");
  });

  // Add blocs from opportunities
  (metadata.claude_opportunities || []).forEach((oc) => {
    if (oc.agent_role === "Stratégie") mentionedBlocs.add("Offering");
    if (oc.agent_role === "Planif") mentionedBlocs.add("Daily");
  });

  // Add identity from work style traits
  if ((metadata.work_style_traits || []).length > 0)
    mentionedBlocs.add("Identity");

  const totalBlocs = 9;
  const coveredBlocs = mentionedBlocs.size;

  return Math.round((coveredBlocs / totalBlocs) * 100);
}

/**
 * Mark diagnostic as complete
 */
export async function completeDiagnostic(
  sessionId: string,
  synthesis?: Record<string, unknown>
): Promise<void> {
  const { error } = await supabase
    .from("diagnostics")
    .update({
      diagnostic_status: "synthesis_generated",
      ended_at: new Date().toISOString(),
      metadata: supabase.rpc("jsonb_set", {
        target: { $1: "metadata" },
        key_path: ["synthesis"],
        new_value: synthesis,
      }),
      updated_at: new Date().toISOString(),
    })
    .eq("session_id", sessionId);

  if (error) {
    console.error("Failed to complete diagnostic:", error);
    throw error;
  }
}
