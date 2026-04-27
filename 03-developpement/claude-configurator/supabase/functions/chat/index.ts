import Anthropic from "https://esm.sh/@anthropic-ai/sdk@0.24.3";
import {
  getOrCreateMetadata,
  updateMetadata,
  saveConversationMessage,
  DiagnosticMetadata,
} from "./metadata-manager.ts";
import { detectPatterns } from "./pattern-detector.ts";
import { identifyOpportunities } from "./opportunity-detector.ts";
import {
  shouldGenerateSynthesis,
  generateSynthesis,
  validateSynthesisQuality,
} from "./synthesis-generator.ts";

// Initialize Anthropic client
const anthropic = new Anthropic({
  apiKey: Deno.env.get("ANTHROPIC_API_KEY"),
});

// SYSTEM PROMPT v21 — Diagnostic Agent Intelligent
const DIAGNOSTIC_SYSTEM_PROMPT_V21 = `# Claude Configurator — Diagnostic Agent Intelligent v21

## Rôle & Contexte

You are an intelligent diagnostic agent for Claude Pro configurations (149€ product).
Your job is NOT to ask a questionnaire. Your job is to help clients understand themselves
better through conversational exploration, detect patterns and opportunities in real-time,
and generate a strategic synthesis that guides their personalized Claude configuration.

You will:
1. Analyze each response for patterns, pain points, blocages
2. Ask adaptive questions based on what emerges (NOT a rigid script)
3. Build enriched metadata in real-time (pain_points, patterns, opportunities)
4. Guide the client toward clarity
5. Generate a strategic synthesis (not just a summary)

Tone: Conversational, curious, bienveillant. No jargon. Direct. Pragmatic.
Length: Keep responses natural (~150-250 words typically)

---

## Mental Model: 9 Implicit Blocks

The 9 blocks (Identity, Offering, Daily, Challenges, Constraints, Security,
Work Style, Voice, Proposals) are your INTERNAL checklist. You ensure all themes
are covered, but NOT in a visible linear order.

After each response, ask yourself:
- What patterns am I noticing?
- What pain points are emerging?
- What opportunities could Claude unlock?
- Which block should I gently explore next?
- Am I at ~40% coverage? 70%? 100%?

---

## Pattern Detection (Real-Time)

Detect and track patterns as you go:

### Recurring Blocages
Scan for concepts/keywords repeated across responses.
Example: Client mentions "compliance" in turns 2, 5, 7 → high-severity pain_point

### Work Style Traits
How does this client operate? Pragmatic? Structured? By feeling? Fast? Slow?
Evidence: Look for verbs, adverbs, decision-making language.

### Strength Signals
What does client excel at? What energizes them?
Evidence: "I love...", "I'm good at...", success stories.

### Risk Indicators
Where does client forget or struggle?
Evidence: "I forget...", "I struggle with...", "nobody tracks..."

---

## Metadata Enrichment (JSON Schema)

Maintain this metadata object, updated after each response:

\`\`\`json
{
  "pain_points": [
    {
      "area": "string (e.g., 'compliance')",
      "detail": "client's specific situation",
      "severity": "high | medium | low",
      "context": "where this was mentioned",
      "opportunity_candidate": "which opportunity addresses this?"
    }
  ],
  "patterns_detected": [
    {
      "pattern": "string (e.g., 'works by feeling + rapid iteration')",
      "evidence": ["quote 1", "quote 2"],
      "consequence": "what this means for them",
      "strength_potential": "positive angle?",
      "implication_for_claude": "how Claude helps"
    }
  ],
  "work_style_traits": [
    {
      "trait": "string (e.g., 'pragmatic')",
      "manifestation": "how it shows up",
      "implication": "what this means for config"
    }
  ],
  "claude_opportunities": [
    {
      "opportunity": "string (e.g., 'Compliance Hub')",
      "description": "what it does",
      "linked_pain_point": "which pain_point does it solve?",
      "why_claude_transforms": "why Claude is special here",
      "priority": 1,
      "agent_role": "which agent?"
    }
  ],
  "coverage_tracking": {
    "blocs_covered": ["Identity", "Offering"],
    "blocs_pending": ["Daily", "Challenges"],
    "coverage_percentage": 25
  }
}
\`\`\`

---

## Adaptive Question Generation (Strategies)

Generate next question using these strategies (not a rigid list):

### Strategy 1: Follow-Up Deepening
If client says: "I export to 40 countries"
Natural follow-up: "What's your biggest challenge with that export?"
(vs generic: "Tell me about your constraints")

### Strategy 2: Pattern Validation
If pattern detected: "works by feeling"
Question: "How do you typically make important decisions?"
(To validate + deepen understanding)

### Strategy 3: Block Coverage Check
If block "Security" not yet covered and context is right:
Question: "Are there sensitive elements in your work?"
(vs rigid: "Let's talk about security")

### Strategy 4: Opportunity Linking
If pain_point("documentation") + pattern("works by feeling"):
Question: "Would you like your decisions to be better documented for your team?"
(Linking pain + opportunity)

---

## When to Generate Strategic Synthesis

Detect when diagnostic is complete (typically after 10-15 exchanges):
- Coverage ≥ 80% (most blocks touched)
- All 6 mandatory agent opportunities identified
- Client clarity seems high (they understand themselves better)
- Natural conclusion point (client seems satisfied)

Then generate synthesis structured as:

### Ce que j'ai compris de vous
- Your key identity (role, context)
- Your main blocages (pain points)
- Your strengths (what you excel at)
- Your work style

### Où Claude devient vraiment game-changer pour vous
For each opportunity (3-5):
- What it solves
- Why Claude transforms it (not just "Claude can help")
- Which agent handles it

### Votre config sera centrée sur
- 6 mandatory agents (Miroir, Garde-Fou, Admin, Stratégie, Planif, Amélioration Continue)
- "Ma Mémoire" project (personalized hub)
- Specific custom instructions (2000+ chars tailored)
- Recommended routines (Daily, Weekly, Monthly)

---

## Metadata Context Integration

CRITICAL: Before responding, check if metadata is provided in context:
- If metadata exists: review it (patterns, coverage, previous opportunities)
- Use it to inform your response (be consistent, build on previous insights)
- Update it in your response JSON
- If metadata is missing: start fresh (assume turn 1)

---

## Quality Standards

### Conversation Quality Checklist
- [ ] Questions feel conversational (not robotic)
- [ ] You paraphrase back (show understanding)
- [ ] Follow-ups are clarifying (not just info-gathering)
- [ ] Tone remains curious + bienveillant

### Metadata Quality Checklist
- [ ] Pain points are SPECIFIC (not "I have challenges")
- [ ] Patterns are GROUNDED (with evidence/quotes)
- [ ] Opportunities are ACTIONABLE (not vague)
- [ ] Metadata size < 2KB (no bloat)

### Synthesis Quality Checklist
- [ ] Not a summary (re-structures insights)
- [ ] Justifies 149€ price (shows density)
- [ ] Clear config direction (agent roles, projects, tasks)

---

## Handoff to Generate-Config

When synthesis is complete, ensure:
- Metadata JSON is complete + valid
- pain_points[], patterns[], opportunities[] are all populated
- coverage_tracking shows ≥80%
- Strategic synthesis is ready for generate-config to consume

Generate-Config will use this metadata to create hyper-specific agents, routines, and Custom Instructions.

---

## Non-Examples (What NOT to do)

❌ DON'T: Ask a questionnaire (Q1, Q2, Q3, Q4...)
✅ DO: Ask conversational follow-ups based on responses

❌ DON'T: Jump to next block abruptly ("OK, moving to Daily...")
✅ DO: Transition naturally based on what emerges

❌ DON'T: Generate generic advice ("You should...")
✅ DO: Ask clarifying questions that help client understand themselves

❌ DON'T: Ignore metadata from previous turns
✅ DO: Build on previous insights, show consistency
`;

// Type definitions
interface Message {
  role: "user" | "assistant" | "system";
  content: string;
}

interface ChatRequest {
  session_id: string;
  message: string;
  conversation_history?: Message[];
  metadata?: Record<string, unknown>;
  client_name?: string;
}

// Compress old messages in conversation history
function compressMessages(messages: Message[], keepLast = 5): Message[] {
  if (!messages || messages.length === 0) return [];
  if (messages.length <= keepLast + 10) return messages;

  const keepFull = messages.slice(-keepLast);
  const toCompress = messages.slice(0, messages.length - keepLast);
  const compressed: Message[] = [];

  // Summarize in blocks of 10
  for (let i = 0; i < toCompress.length; i += 10) {
    const chunk = toCompress.slice(i, Math.min(i + 10, toCompress.length));
    const keyPoints: string[] = [];

    for (const msg of chunk) {
      if (msg.role === "user") {
        const firstLine = msg.content.split("\n")[0].trim();
        if (firstLine.length > 0) {
          const truncated = firstLine.length > 60 ? firstLine.slice(0, 60) + "..." : firstLine;
          keyPoints.push(`Q: ${truncated}`);
        }
      }
    }

    if (keyPoints.length > 0) {
      compressed.push({
        role: "system",
        content: `[DIAGNOSTIC_HISTORY] Messages ${i + 1}-${Math.min(i + 10, toCompress.length)}: ${keyPoints.join(" | ")}`,
      });
    }
  }

  return [...compressed, ...keepFull];
}

// Main handler
async function handler(req: Request): Promise<Response> {
  // Handle CORS
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" },
    });
  }

  try {
    const body = (await req.json()) as ChatRequest;
    const { session_id, message, conversation_history = [], metadata: requestMetadata, client_name } = body;

    if (!session_id || !message) {
      return new Response(
        JSON.stringify({ error: "Missing session_id or message" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // Get or create metadata from Supabase
    let metadata: DiagnosticMetadata;
    try {
      metadata = await getOrCreateMetadata(session_id, client_name);
    } catch (error) {
      console.error("Error managing metadata:", error);
      // Fallback to request metadata if Supabase fails
      metadata = requestMetadata as DiagnosticMetadata || {
        session_id,
        client_name,
        started_at: new Date().toISOString(),
        turns_count: 0,
        pain_points: [],
        patterns_detected: [],
        work_style_traits: [],
        claude_opportunities: [],
        coverage_tracking: { blocs_covered: [], blocs_pending: [], coverage_percentage: 0 },
        conversation_quality_metrics: {
          turns_count: 0,
          avg_response_length: 0,
          client_engagement_level: "medium",
          clarity_score: 0,
        },
        metadata_version: "1.0",
        last_updated: new Date().toISOString(),
      };
    }

    // Prepare messages for Claude
    const messages: Message[] = [
      ...compressMessages(conversation_history),
      { role: "user", content: message },
    ];

    // Add metadata as context
    if (metadata && Object.keys(metadata).length > 0) {
      messages.unshift({
        role: "system",
        content: `[CURRENT_METADATA]\n${JSON.stringify(metadata, null, 2)}`,
      });
    }

    // Save user message to conversation history
    try {
      await saveConversationMessage(session_id, "user", message);
    } catch (error) {
      console.error("Error saving user message:", error);
      // Don't fail the entire request if saving fails
    }

    // Call Claude API with streaming
    const stream = anthropic.messages.stream({
      model: "claude-sonnet-4-20250514",
      max_tokens: 800,
      temperature: 0.7,
      system: DIAGNOSTIC_SYSTEM_PROMPT_V21,
      messages: messages,
    });

    // Collect the full response for saving
    let fullResponse = "";

    // Transform stream to SSE format and collect response
    const sseStream = stream.on("message", (event) => {
      if (event.type === "content_block_delta") {
        const delta = event.delta as { type: string; text?: string };
        if (delta.type === "text_delta" && delta.text) {
          fullResponse += delta.text;
        }
      }
    }).toReadableStream();

    // Save assistant response after streaming + detect patterns
    // Note: We'll do this in a separate async task to not block the response
    (async () => {
      try {
        await saveConversationMessage(session_id, "assistant", fullResponse);

        // EPIC-2: Detect patterns in real-time
        const { updatedMetadata: metadataWithPatterns } = detectPatterns(
          message, // current user message
          messages.filter((m) => m.role !== "system"), // conversation history without system prompts
          metadata
        );

        // EPIC-3: Identify opportunities based on patterns + pain points
        const opportunities = identifyOpportunities(metadataWithPatterns);
        const metadataWithOpportunities = {
          ...metadataWithPatterns,
          claude_opportunities: opportunities,
        };

        // EPIC-5: Check if synthesis should be generated
        let metadataWithSynthesis = metadataWithOpportunities;
        const conversationHistoryForSynthesis = messages.filter(
          (m) => m.role !== "system"
        );

        if (
          shouldGenerateSynthesis(
            metadataWithOpportunities,
            conversationHistoryForSynthesis
          )
        ) {
          try {
            const synthesisOutput = await generateSynthesis(
              metadataWithOpportunities,
              anthropic
            );

            if (
              synthesisOutput.synthesis_status === "generated" &&
              synthesisOutput.synthesis
            ) {
              // Validate synthesis quality
              const qualityCheck = validateSynthesisQuality(
                synthesisOutput.synthesis,
                metadataWithOpportunities
              );

              if (qualityCheck.passed) {
                metadataWithSynthesis = {
                  ...metadataWithOpportunities,
                  synthesis: synthesisOutput.synthesis,
                  diagnostic_status: "synthesis_generated",
                  ended_at: new Date().toISOString(),
                };

                console.log(
                  "Synthesis generated successfully",
                  qualityCheck.score
                );
              }
            }
          } catch (error) {
            console.error("Error generating synthesis:", error);
            // Continue without synthesis if generation fails
          }
        }

        // Update metadata with new turn + detected patterns + opportunities + synthesis
        await updateMetadata(session_id, {
          ...metadataWithSynthesis,
          turns_count: (metadata.turns_count || 0) + 1,
          conversation_quality_metrics: {
            ...metadata.conversation_quality_metrics,
            turns_count: (metadata.turns_count || 0) + 1,
            avg_response_length: fullResponse.length,
          },
        });
      } catch (error) {
        console.error("Error saving response and updating metadata:", error);
      }
    })();

    // Create response with streaming
    const response = new Response(sseStream, {
      status: 200,
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Access-Control-Allow-Origin": "*",
      },
    });

    return response;
  } catch (error) {
    console.error("Chat handler error:", error);

    return new Response(
      JSON.stringify({
        error: error instanceof Error ? error.message : "Unknown error",
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}

// Export handler
Deno.serve(handler);
