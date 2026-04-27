# BUILD — EPIC-5: Strategic Synthesis Generator

## Overview
Implémenter la génération de synthèse stratégique (pas juste un résumé) qui justifie le 149€ et guide la config generation.

**Statut**: Ready to implement  
**Effort**: 3.5 days (1 day design + 1.5 days prompt engineering + 1 day testing)  
**Blocker**: EPIC-1, EPIC-2, EPIC-3 must be deployed  
**Dependencies**: EPIC-1 ✓, EPIC-2 ✓, EPIC-3 ✓  

---

## Implementation Steps

### Step 1: Synthesis Detection Logic (Day 1)
Design algorithm that detects when diagnostic is complete and ready for synthesis.

**Location**: Chat Edge Function v21+  
**Input**: Current metadata + conversation history  
**Output**: Signal to generate synthesis OR continue diagnostic

### Step 2: Synthesis Prompt Engineering (Day 1-1.5)
Create specialized prompt for Claude to generate strategic synthesis.

**Input**: Enriched metadata (pain_points, patterns, opportunities)  
**Output**: Strategic synthesis text (3 sections)

### Step 3: Synthesis Integration (Day 1.5-2)
- Hook synthesis generation into chat flow
- Trigger when diagnostic concludes
- Return synthesis in response stream
- Save synthesis to Supabase

### Step 4: Testing (Day 2-3)
- Test with 5+ diagnostics
- Validate synthesis quality (strategic vs summary)
- Validate synthesis justifies 149€
- Validate readability + professionalism
- Compare with Fred's config analogy

---

## Synthesis Detection Algorithm

```javascript
/**
 * Detect when diagnostic is ready for synthesis
 * Returns true when client has sufficient clarity and coverage
 */
function shouldGenerateSynthesis(metadata, conversationHistory) {
  // Criteria for synthesis readiness
  
  // 1. Minimum turns (at least 8-10 exchanges)
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
  
  // 5. Client clarity score (≥0.75)
  if ((metadata.conversation_quality_metrics?.clarity_score || 0) < 0.75) {
    return false;
  }
  
  // 6. Natural conclusion signal (client says "ok", "done", "that's it", etc.)
  const lastUserMessage = conversationHistory
    .filter(m => m.role === 'user')
    .pop()?.content || '';
  
  const conclusionSignals = ['i think that', 'that should', 'that covers', 'ok i think', 'i think we'];
  const hasSignal = conclusionSignals.some(signal => 
    lastUserMessage.toLowerCase().includes(signal)
  );
  
  // All criteria met
  return true; // All above checks passed
}

/**
 * Generate engagement + clarity metrics
 * For synthesis readiness assessment
 */
function calculateClarityMetrics(metadata, conversationHistory) {
  const userMessages = conversationHistory.filter(m => m.role === 'user');
  const avgResponseLength = userMessages.reduce((sum, m) => sum + m.content.length, 0) / userMessages.length;
  
  // Clarity indicators
  let clarityScore = 0;
  
  // Longer responses = more detail = higher clarity
  if (avgResponseLength > 150) clarityScore += 0.2;
  if (avgResponseLength > 250) clarityScore += 0.2;
  
  // Multiple pain points = better understanding
  if ((metadata.pain_points?.length || 0) >= 3) clarityScore += 0.2;
  
  // Patterns detected = clear picture of work style
  if ((metadata.patterns_detected?.length || 0) >= 2) clarityScore += 0.2;
  
  // Opportunities mapped = actionable insights
  if ((metadata.claude_opportunities?.length || 0) >= 5) clarityScore += 0.2;
  
  return Math.min(1.0, clarityScore);
}
```

---

## Strategic Synthesis Prompt

```
# Generate Strategic Synthesis for Claude Configurator

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
Example: "Vous êtes ingénieur innovant export 40 pays. Votre défi principal: 
conformité multi-régionale qui grandit avec votre export. Force: pragmatisme, 
décisions rapides. Vous opérez au feeling mais vous voulez garder la trace."

---

### 2️⃣ Où Claude devient vraiment game-changer pour vous (Transformation)

Start with: "Claude transforme vraiment votre quotidien via..."

For EACH top 3-4 opportunities:
- Name the opportunity (e.g., "Compliance Hub")
- What it does (1 sentence)
- Why Claude transforms it (not just "Claude can help", but WHY Claude is special)
- Which agent handles it (so they see the structure)

Tone: Concrete, specific to their context, show density.

Example for Fred:
"Agent Ingénieur crée un hub de conformité centralisé — chaque pays monitored, 
changes alerted, audit trail maintained. Plus besoin de spreadsheets manuels. 
Chaque pays a ses règles, tu les ignores pas, Claude les track."

---

### 3️⃣ Votre config sera centrée sur (Config Preview)

Start with: "Votre config sera architecturée autour de..."

Include:
- 6 mandatory agents (Miroir, Garde-Fou, Admin, Stratégie, Planif, Amélioration Continue)
  - Very briefly for each (1 line): what it does
- "Ma Mémoire" project (single source of truth for who you are)
- Custom Instructions (2000+ chars specific to them)
- Key routines (Daily, Weekly, Monthly)

Tone: Practical, shows comprehensive coverage.

Example:
"6 agents spécialisés travaillent pour vous:
- Miroir: vos patterns, forces, blocages
- Garde-Fou: sécurité absolue, antiphishing, RGPD
- Admin: auto-documentation, templates, zero friction
- Stratégie: roadmap alignée à votre vision
- Planif: timeline, jalons, accountability
- Amélioration Continue: debriefs hebdo, itération

'Ma Mémoire' project = votre hub centralisé (qui vous êtes, comment vous marchez).

Custom Instructions = 2000+ caractères spécifiques à votre pragmatisme + contexte export.

Routines: Daily briefing, Weekly coach debrief, Monthly compliance alert."

---

## Quality Checklist

✅ Synthesis is STRATEGIC (re-structures insights, not a summary)
✅ Specific to CLIENT (not generic boilerplate)
✅ Grounded in EVIDENCE (references pain points, patterns)
✅ Shows DENSITY (not surface-level suggestions)
✅ Justifies 149€ (shows comprehensive config)
✅ Readable (clear sections, good flow)
✅ References Fred's config (where applicable, as analogy)

---

## Output Format

Return synthesis as:
\`\`\`json
{
  "synthesis_status": "generated",
  "synthesis_text": "Full synthesis text (3 sections above)",
  "synthesis_sections": {
    "understanding": "Ce que j'ai compris...",
    "transformation": "Où Claude devient vraiment...",
    "config_preview": "Votre config sera..."
  },
  "metadata": {
    "clarity_score": 0.87,
    "coverage_percentage": 82,
    "pain_points_addressed": 4,
    "opportunities_identified": 5
  }
}
\`\`\`

---

## Non-Example (What NOT to do)

❌ "You mentioned X, Y, Z. Here are recommendations: A, B, C."
✅ "You're a pragmatic innovator scaling globally. Your blocage: compliance 
   tracking across 40 countries. Claude transforms this via Agent Ingénieur 
   who centrally monitors all regulations."

---

## Handoff to Config Generation

When synthesis is complete, ensure:
- Metadata is complete (pain_points, patterns, opportunities)
- Synthesis is saved to Supabase
- Synthesis is returned to frontend (displayed to client)
- Client confirms: "Yes, this is me"
- Ready for generate-config to consume metadata + synthesis
```

---

## Integration into Chat Flow

```javascript
// In Chat Edge Function, after diagnostic continues or concludes:

if (shouldGenerateSynthesis(metadata, conversationHistory)) {
  // Prepare synthesis prompt with metadata
  const synthesisPrompt = `
    ${STRATEGIC_SYNTHESIS_PROMPT}
    
    Pain Points: ${JSON.stringify(metadata.pain_points, null, 2)}
    Patterns: ${JSON.stringify(metadata.patterns_detected, null, 2)}
    Work Style: ${JSON.stringify(metadata.work_style_traits, null, 2)}
    Opportunities: ${JSON.stringify(metadata.claude_opportunities, null, 2)}
  `;
  
  // Call Claude (Sonnet 4.6) to generate synthesis
  const synthesisResponse = await callClaudeAPI({
    messages: [{ role: 'user', content: synthesisPrompt }],
    temperature: 0.7,
    max_tokens: 1500
  });
  
  const synthesis = synthesisResponse.content[0].text;
  
  // Parse synthesis
  const parsedSynthesis = parseSynthesisResponse(synthesis);
  
  // Update metadata
  const updatedMetadata = {
    ...metadata,
    synthesis: parsedSynthesis,
    diagnostic_status: 'synthesis_generated',
    ended_at: new Date().toISOString()
  };
  
  // Persist
  await updateMetadata(sessionId, updatedMetadata);
  
  // Return to frontend (SSE)
  sendEvent('synthesis_generated', {
    synthesis: parsedSynthesis,
    metadata: updatedMetadata
  });
  
  // Signal end of diagnostic (but allow client to say "continue" for more discussion)
  sendEvent('diagnostic_milestone', 'synthesis_complete');
}
```

---

## Synthesis Quality Validation

Before deploying, validate synthesis against Fred's config:

```javascript
function validateSynthesisQuality(synthesis, metadata) {
  const checks = {
    hasUnderstandingSection: synthesis.includes('Ce que j'),
    hasTransformationSection: synthesis.includes('Où Claude'),
    hasConfigPreview: synthesis.includes('config sera'),
    mentionsAtLeast3Agents: (synthesis.match(/Agent/g) || []).length >= 3,
    mentionsOpportunities: synthesis.includes('Claude transforme') || synthesis.includes('game-changer'),
    specificToPain: metadata.pain_points?.some(pp => synthesis.includes(pp.area)),
    referencesMetadata: synthesis.includes(metadata.work_style_traits?.[0]?.trait),
    justifies149: synthesis.length > 800, // Substantial content
  };
  
  const score = Object.values(checks).filter(Boolean).length / Object.keys(checks).length;
  
  return {
    passed: score >= 0.8,
    score: score,
    failures: Object.entries(checks)
      .filter(([_, passed]) => !passed)
      .map(([check]) => check)
  };
}
```

---

## Testing Checklist

Before proceeding to EPIC-6:

- [ ] Test 1: Synthesis triggers at right time (≥70% coverage, ≥3 opportunities)
- [ ] Test 2: Synthesis is strategic (not a summary)
- [ ] Test 3: Specific to client (references their context, not generic)
- [ ] Test 4: Justifies 149€ (shows density, comprehensive)
- [ ] Test 5: All 3 sections present (understanding, transformation, config preview)
- [ ] Test 6: References agents correctly (matches opportunities)
- [ ] Test 7: 5+ full diagnostics (synthesis quality reviewed, validated vs Fred)

---

## Rollback Plan

If synthesis generation causes issues:
1. Disable synthesis generation (comment out `shouldGenerateSynthesis()`)
2. Diagnostic continues as normal (just no synthesis at end)
3. No synthesis passed to generate-config (config generation works without it)
4. Client sees end-of-diagnostic but no summary
5. Document issue for EPIC-5 iteration

---

**EPIC-5 Status**: Specification complete  
**Dependencies Met**: EPIC-1, EPIC-2, EPIC-3 deployed  
**Required before**: EPIC-7 (Generate-Config integration)  
**Next**: EPIC-6 (Agent & Routine Configuration)
