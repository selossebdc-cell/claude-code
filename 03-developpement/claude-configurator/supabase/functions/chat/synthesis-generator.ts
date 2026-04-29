// Strategic Synthesis Generator for Diagnostic Intelligence
// Generates transformative synthesis that justifies 149€ price point

import Anthropic from "https://esm.sh/@anthropic-ai/sdk@0.24.3";
import { DiagnosticMetadata } from "./metadata-manager.ts";

interface SynthesisResponse {
  understanding: string;
  transformation: string;
  config_preview: string;
}

const SYNTHESIS_PROMPT = `# Generate Strategic Synthesis for Claude Configurator

You have just completed an intelligent diagnostic with a client.
Your job now is to generate a STRATEGIC SYNTHESIS (not a summary) that:

1. Shows what you understood about them (identity, blocages, strengths, work style)
2. Identifies where Claude becomes truly game-changer (linked to opportunities)
3. Previews their personalized config direction
4. Justifies the 149€ price point

## Data Available (Client Context)

**Pain Points Identified**:
{{pain_points_summary}}

**Patterns Detected**:
{{patterns_summary}}

**Work Style**:
{{work_style_summary}}

**Claude Opportunities**:
{{opportunities_summary}}

## Synthesis Structure (3 Sections)

### 1️⃣ Ce que j'ai compris de vous (Understanding)

Start with: "Voici ce que j'ai compris..."

Include:
- Who they are (role, context, scope) — 1-2 sentences
- Their main blocages (top 2-3 pain points) — specific, not generic
- Their strengths (what they excel at) — grounded in conversation
- How they operate (work style traits) — pragmatic, feeling-based, etc.

Tone: Direct, respectful, specific to THEM (not generic).

---

### 2️⃣ Où Claude devient vraiment game-changer pour vous (Transformation)

Start with: "Claude transforme vraiment votre quotidien via..."

For EACH top 3-4 opportunities:
- Name the opportunity (e.g., "Compliance Hub")
- What it does (1 sentence)
- Why Claude transforms it (not just "Claude can help", but WHY Claude is special)
- Which agent handles it

Tone: Concrete, specific to their context, show density.

---

### 3️⃣ Votre config sera centrée sur (Config Preview)

Start with: "Votre config sera architecturée autour de..."

Include:
- 6 mandatory agents (Miroir, Garde-Fou, Admin, Stratégie, Planif, Amélioration Continue)
- "Ma Mémoire" project
- Custom Instructions (2000+ chars)
- Key routines (Daily, Weekly, Monthly)

Tone: Practical, shows comprehensive coverage.

---

## Quality Checklist

✅ Synthesis is STRATEGIC (re-structures insights, not a summary)
✅ Specific to CLIENT (not generic boilerplate)
✅ Grounded in EVIDENCE (references pain points, patterns)
✅ Shows DENSITY (not surface-level suggestions)
✅ Justifies 149€ (shows comprehensive config)
✅ Readable (clear sections, good flow)

Return synthesis as three clear sections separated by "---".
`;

export interface SynthesisOutput {
  synthesis_status: "generated" | "not_ready";
  synthesis?: SynthesisResponse;
  metadata?: {
    clarity_score: number;
    coverage_percentage: number;
    pain_points_addressed: number;
    opportunities_identified: number;
  };
}

export function shouldGenerateSynthesis(
  metadata: DiagnosticMetadata,
  conversationHistory: Array<{ role: string; content: string }>
): boolean {
  // 1. Minimum turns (at least 8 exchanges)
  if ((metadata.turns_count || 0) < 8) {
    return false;
  }

  // 2. Sufficient bloc coverage (≥70%)
  if ((metadata.coverage_tracking?.coverage_percentage || 0) < 70) {
    return false;
  }

  // 3. Minimum pain points identified (≥2)
  if ((metadata.pain_points?.length || 0) < 2) {
    return false;
  }

  // 4. Minimum opportunities identified (≥3)
  if ((metadata.claude_opportunities?.length || 0) < 3) {
    return false;
  }

  // 5. Client clarity score (≥0.6)
  const clarityScore = calculateClarityMetrics(metadata, conversationHistory);
  if (clarityScore < 0.6) {
    return false;
  }

  return true;
}

export function calculateClarityMetrics(
  metadata: DiagnosticMetadata,
  conversationHistory: Array<{ role: string; content: string }>
): number {
  const userMessages = conversationHistory.filter((m) => m.role === "user");
  if (userMessages.length === 0) return 0;

  const avgResponseLength =
    userMessages.reduce((sum, m) => sum + m.content.length, 0) /
    userMessages.length;

  let clarityScore = 0;

  // Longer responses = more detail = higher clarity
  if (avgResponseLength > 150) clarityScore += 0.2;
  if (avgResponseLength > 250) clarityScore += 0.15;

  // Multiple pain points = better understanding
  const painPointCount = metadata.pain_points?.length || 0;
  if (painPointCount >= 2) clarityScore += 0.15;
  if (painPointCount >= 3) clarityScore += 0.1;

  // Patterns detected = clear picture of work style
  const patternCount = metadata.patterns_detected?.length || 0;
  if (patternCount >= 2) clarityScore += 0.15;
  if (patternCount >= 3) clarityScore += 0.1;

  // Opportunities mapped = actionable insights
  const opportunityCount = metadata.claude_opportunities?.length || 0;
  if (opportunityCount >= 3) clarityScore += 0.1;
  if (opportunityCount >= 5) clarityScore += 0.1;

  return Math.min(1.0, clarityScore);
}

export async function generateSynthesis(
  metadata: DiagnosticMetadata,
  anthropic: typeof Anthropic.prototype
): Promise<SynthesisOutput> {
  try {
    // Prepare context summaries
    const painPointsSummary = (metadata.pain_points || [])
      .slice(0, 5)
      .map((pp) => `- ${pp.area}: ${pp.detail || pp.context}`)
      .join("\n");

    const patternsSummary = (metadata.patterns_detected || [])
      .slice(0, 5)
      .map((p) => `- ${p.pattern} (${p.type}): ${p.evidence?.[0] || ""}`)
      .join("\n");

    const workStyleSummary = (metadata.work_style_traits || [])
      .slice(0, 5)
      .map((w) => `- ${w.trait}: ${w.implication || ""}`)
      .join("\n");

    const opportunitiesSummary = (metadata.claude_opportunities || [])
      .slice(0, 5)
      .map((o) => `- ${o.opportunity} (${o.agent_role}): ${o.description}`)
      .join("\n");

    // Prepare synthesis prompt with client data
    const synthesisPrompt = SYNTHESIS_PROMPT.replace(
      "{{pain_points_summary}}",
      painPointsSummary || "(No pain points identified)"
    )
      .replace("{{patterns_summary}}", patternsSummary || "(No patterns detected)")
      .replace("{{work_style_summary}}", workStyleSummary || "(No work style traits)")
      .replace(
        "{{opportunities_summary}}",
        opportunitiesSummary || "(No opportunities identified)"
      );

    // Call Claude to generate synthesis
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 1500,
      temperature: 0.7,
      messages: [
        {
          role: "user",
          content: synthesisPrompt,
        },
      ],
    });

    const synthesisText =
      response.content[0].type === "text" ? response.content[0].text : "";

    // Parse synthesis into three sections
    const synthesis = parseSynthesisResponse(synthesisText);

    // Calculate metrics
    const clarityScore =
      metadata.conversation_quality_metrics?.clarity_score ?? 0;
    const coverage = metadata.coverage_tracking?.coverage_percentage || 0;
    const painPointCount = metadata.pain_points?.length || 0;
    const opportunityCount = metadata.claude_opportunities?.length || 0;

    return {
      synthesis_status: "generated",
      synthesis,
      metadata: {
        clarity_score: clarityScore,
        coverage_percentage: coverage,
        pain_points_addressed: painPointCount,
        opportunities_identified: opportunityCount,
      },
    };
  } catch (error) {
    console.error("Error generating synthesis:", error);
    return {
      synthesis_status: "not_ready",
    };
  }
}

function parseSynthesisResponse(text: string): SynthesisResponse {
  // Extract three sections from synthesis text
  const sections = text.split(/#{1,2}\s+.*?(?=#{1,2}\s+|$)/i);

  // Look for section markers
  const understandingMatch = text.match(
    /(?:Ce que j'ai compris|Understanding)[\s\S]*?(?=(?:Où Claude|Transformation|Votre config)|$)/i
  );
  const transformationMatch = text.match(
    /(?:Où Claude|Transformation)[\s\S]*?(?=(?:Votre config|Config Preview)|$)/i
  );
  const configMatch = text.match(
    /(?:Votre config|Config Preview)[\s\S]*?$/i
  );

  return {
    understanding: understandingMatch
      ? understandingMatch[0].trim()
      : sections[0]?.trim() || "",
    transformation: transformationMatch
      ? transformationMatch[0].trim()
      : sections[1]?.trim() || "",
    config_preview: configMatch ? configMatch[0].trim() : sections[2]?.trim() || "",
  };
}

export function validateSynthesisQuality(
  synthesis: SynthesisResponse,
  metadata: DiagnosticMetadata
): {
  passed: boolean;
  score: number;
  failures: string[];
} {
  const fullText = `${synthesis.understanding} ${synthesis.transformation} ${synthesis.config_preview}`;

  const checks = {
    hasUnderstandingSection: synthesis.understanding.length > 100,
    hasTransformationSection: synthesis.transformation.length > 100,
    hasConfigPreview: synthesis.config_preview.length > 100,
    mentionsAtLeast3Agents: (fullText.match(/Agent|Miroir|Garde-Fou|Admin|Stratégie|Planif|Amélioration/gi) || [])
      .length >= 3,
    mentionsOpportunities: fullText.toLowerCase().includes("claude transforme") ||
      fullText.toLowerCase().includes("game-changer"),
    specificToPain: metadata.pain_points?.length! > 0,
    referencesWork: metadata.work_style_traits?.length! > 0,
    justifies149: fullText.length > 800,
  };

  const score =
    Object.values(checks).filter(Boolean).length / Object.keys(checks).length;

  return {
    passed: score >= 0.8,
    score: score,
    failures: Object.entries(checks)
      .filter(([_, passed]) => !passed)
      .map(([check]) => check),
  };
}
