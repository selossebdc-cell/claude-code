# BUILD — EPIC-2: Pattern Detection Engine

## Overview
Implémenter la logique de détection de patterns en temps réel dans le diagnostic intelligent.

**Statut**: Ready to implement  
**Effort**: 3 days (1 day design + 1 day integration + 1 day testing)  
**Blocker**: EPIC-1 (Diagnostic Prompt) must be deployed first  
**Dependency**: EPIC-1 ✓  

---

## Implementation Steps

### Step 1: Pattern Detection Logic (Day 1)
Design the pattern detection algorithm that runs after each client response.

**Location**: Chat Edge Function v21 (post-response analysis)  
**Input**: Current client response + conversation history + current metadata  
**Output**: Updated metadata with new patterns detected

### Step 2: Integration into Chat Function (Day 1-2)
- Hook pattern detection after Claude generates response
- Update metadata object with detected patterns
- Include patterns in response stream to frontend
- Persist metadata to Supabase diagnostics table

**Changes needed**:
- Add `detectPatterns()` function in chat Edge Function
- Call it after each diagnostic response
- Merge results into metadata JSON
- Return updated metadata in SSE stream

### Step 3: Frontend Display (Day 2)
- Update chat.js to display detected patterns (optional debug view)
- Show pattern confidence/evidence
- Real-time metadata tracking visible to user

### Step 4: Testing (Day 2-3)
- Test with 5+ diverse diagnostics
- Validate ≥2 patterns detected per diagnostic
- Validate patterns are specific (not generic)
- Validate patterns are evidence-based (have quotes)
- Validate patterns inform subsequent questions

---

## Pattern Detection Logic (Code Specification)

```javascript
/**
 * Pattern Detection Engine
 * Analyzes client responses to detect recurring themes, work styles, strengths, risks
 */

function detectPatterns(currentResponse, conversationHistory, currentMetadata) {
  const detectedPatterns = [];
  
  // PATTERN 1: Recurring Blocages
  // Detect if same keyword/concept appears multiple times across conversation
  const recurringBlockages = detectRecurringKeywords(
    conversationHistory,
    ['compliance', 'documentation', 'workflow', 'deadlines', 'communication', 'process'],
    minOccurrences = 2
  );
  
  recurringBlockages.forEach(({ keyword, occurrences, contexts }) => {
    detectedPatterns.push({
      type: "recurring_blocage",
      pattern: `Recurring challenge: "${keyword}"`,
      evidence: contexts.slice(0, 2), // First 2 mentions
      severity: occurrences >= 3 ? "high" : "medium",
      consequence: `This appears frequently — it's a real pain point`,
      implication_for_claude: `Claude can help systematize or automate this`
    });
  });
  
  // PATTERN 2: Work Style Traits
  // Detect how client operates (pragmatic, structured, by feeling, etc.)
  const workStyleTraits = detectWorkStyle(conversationHistory);
  
  workStyleTraits.forEach(({ trait, evidence, implication }) => {
    detectedPatterns.push({
      type: "work_style",
      pattern: trait,
      evidence: [evidence],
      implication_for_claude: implication
    });
  });
  
  // PATTERN 3: Strength Signals
  // Detect what client excels at (confidence, passion, success stories)
  const strengths = detectStrengths(conversationHistory);
  
  strengths.forEach(({ strength, evidence }) => {
    detectedPatterns.push({
      type: "strength",
      pattern: `Strong at: ${strength}`,
      evidence: [evidence],
      strength_potential: `This is a core competency to leverage`,
      implication_for_claude: `Claude can amplify this strength`
    });
  });
  
  // PATTERN 4: Risk Indicators
  // Detect where client forgets or struggles (blind spots)
  const risks = detectRiskIndicators(conversationHistory);
  
  risks.forEach(({ risk, indicator_phrase }) => {
    detectedPatterns.push({
      type: "risk_indicator",
      pattern: `Risk: ${risk}`,
      evidence: [indicator_phrase],
      consequence: `Potential gap or oversight`,
      implication_for_claude: `Claude can systematize this area`
    });
  });
  
  return {
    newPatterns: detectedPatterns,
    updatedMetadata: mergePatterns(currentMetadata, detectedPatterns)
  };
}

/**
 * Detect Recurring Keywords
 * Scan conversation for repeated concepts
 */
function detectRecurringKeywords(history, keywords, minOccurrences = 2) {
  const occurrenceMap = {};
  const contexts = {};
  
  history.forEach((message, idx) => {
    if (message.role !== "user") return; // Only user responses
    const text = message.content.toLowerCase();
    
    keywords.forEach(keyword => {
      if (text.includes(keyword)) {
        occurrenceMap[keyword] = (occurrenceMap[keyword] || 0) + 1;
        if (!contexts[keyword]) contexts[keyword] = [];
        contexts[keyword].push({
          turn: idx,
          snippet: text.substring(0, 150) // First 150 chars
        });
      }
    });
  });
  
  return Object.entries(occurrenceMap)
    .filter(([_, count]) => count >= minOccurrences)
    .map(([keyword, count]) => ({
      keyword,
      occurrences: count,
      contexts: contexts[keyword].map(c => c.snippet)
    }));
}

/**
 * Detect Work Style
 * Identify operating patterns: pragmatic, structured, by feeling, rapid, methodical, etc.
 */
function detectWorkStyle(history) {
  const styleIndicators = {
    pragmatic: ['fast', 'quick', 'practical', 'results', 'reality', 'no-nonsense'],
    structured: ['process', 'system', 'step-by-step', 'organized', 'plan', 'schedule'],
    feeling_based: ['gut', 'feeling', 'sense', 'intuition', 'vibe', 'instinct'],
    innovative: ['try', 'experiment', 'new', 'different', 'test', 'explore'],
    risk_aware: ['careful', 'check', 'verify', 'compliance', 'rule', 'regulation']
  };
  
  const detected = [];
  const userResponses = history.filter(m => m.role === "user").map(m => m.content.toLowerCase());
  const combinedText = userResponses.join(" ");
  
  Object.entries(styleIndicators).forEach(([style, indicators]) => {
    const matchCount = indicators.filter(ind => combinedText.includes(ind)).length;
    
    if (matchCount >= 2) { // Threshold: at least 2 indicators
      detected.push({
        trait: style.charAt(0).toUpperCase() + style.slice(1),
        evidence: `Shows ${matchCount} indicators of "${style}" approach`,
        implication: `Claude setup should support ${style} work style`
      });
    }
  });
  
  return detected;
}

/**
 * Detect Strengths
 * Find what client is proud of or good at
 */
function detectStrengths(history) {
  const strengthPhrases = [
    /I(?:'m|\ am)\ (?:really\ )?good\ at\ (.+?)([.,!?]|$)/i,
    /I\ (?:love|enjoy|like)\ (.+?)([.,!?]|$)/i,
    /I'm\ (?:passionate|enthusiastic)\ about\ (.+?)([.,!?]|$)/i,
    /success.*?in\ (.+?)([.,!?]|$)/i
  ];
  
  const strengths = [];
  const userResponses = history.filter(m => m.role === "user").map(m => m.content);
  
  userResponses.forEach(response => {
    strengthPhrases.forEach(regex => {
      const match = response.match(regex);
      if (match && match[1]) {
        strengths.push({
          strength: match[1].trim(),
          evidence: match[0].trim()
        });
      }
    });
  });
  
  return [...new Set(strengths.map(s => s.strength))].map(strength => ({
    strength,
    evidence: `Client expressed competence/passion in: ${strength}`
  }));
}

/**
 * Detect Risk Indicators
 * Find blind spots or areas client forgets
 */
function detectRiskIndicators(history) {
  const riskPhrases = [
    /I (?:forget|forget\ to|often\ forget|always\ forget)\ (.+?)([.,!?]|$)/i,
    /I (?:struggle|have\ trouble)\ (?:with\ )?(.+?)([.,!?]|$)/i,
    /nobody\ (?:tracks|manages|checks)\ (.+?)([.,!?]|$)/i,
    /I\ don't\ (?:have|keep)\ (.+?)([.,!?]|$)/i
  ];
  
  const risks = [];
  const userResponses = history.filter(m => m.role === "user").map(m => m.content);
  
  userResponses.forEach(response => {
    riskPhrases.forEach(regex => {
      const match = response.match(regex);
      if (match && match[1]) {
        risks.push({
          risk: match[1].trim(),
          indicator_phrase: match[0].trim()
        });
      }
    });
  });
  
  return [...new Set(risks.map(r => r.risk))].slice(0, 3); // Top 3
}

/**
 * Merge newly detected patterns with existing metadata
 */
function mergePatterns(currentMetadata, newPatterns) {
  const updated = { ...currentMetadata };
  
  newPatterns.forEach(pattern => {
    if (pattern.type === "recurring_blocage") {
      // Add to pain_points if not already there
      if (!updated.pain_points) updated.pain_points = [];
      if (!updated.pain_points.some(p => p.area === pattern.pattern)) {
        updated.pain_points.push({
          area: pattern.pattern,
          severity: pattern.severity,
          context: pattern.evidence[0],
          opportunity_candidate: null
        });
      }
    } else if (pattern.type === "work_style") {
      if (!updated.work_style_traits) updated.work_style_traits = [];
      updated.work_style_traits.push({
        trait: pattern.pattern,
        implication: pattern.implication_for_claude
      });
    } else if (pattern.type === "strength") {
      if (!updated.work_style_traits) updated.work_style_traits = [];
      updated.work_style_traits.push({
        trait: `Strength: ${pattern.pattern}`,
        implication: pattern.implication_for_claude
      });
    } else if (pattern.type === "risk_indicator") {
      if (!updated.pain_points) updated.pain_points = [];
      updated.pain_points.push({
        area: pattern.pattern,
        severity: "medium",
        context: pattern.consequence,
        opportunity_candidate: null
      });
    }
  });
  
  return updated;
}
```

---

## Integration Steps (Edge Function v21+)

In the Chat Edge Function, after Claude generates a diagnostic response:

```javascript
// After Claude API call returns response
const assistantMessage = response.content[0].text;

// NEW: Detect patterns
const { newPatterns, updatedMetadata } = detectPatterns(
  userMessage,
  conversationHistory,
  currentMetadata
);

// NEW: Merge metadata
const finalMetadata = {
  ...updatedMetadata,
  coverage_tracking: {
    ...updatedMetadata.coverage_tracking,
    updated_at: new Date().toISOString()
  }
};

// Save to Supabase
await supabase
  .from('diagnostics')
  .update({ metadata: finalMetadata })
  .eq('session_id', sessionId);

// Return to frontend (SSE)
sendEvent('metadata_updated', finalMetadata);
sendEvent('message', assistantMessage);
```

---

## Metadata Output Example

After Turn 3 (compliance mentioned), metadata should include:

```json
{
  "pain_points": [
    {
      "area": "compliance",
      "detail": "40 countries, each with different certifications",
      "severity": "high",
      "context": "Turn 3: 'Each country has different certifications'",
      "opportunity_candidate": null
    }
  ],
  "patterns_detected": [
    {
      "pattern": "Recurring challenge: compliance",
      "evidence": ["Turn 2: '...different regs'", "Turn 3: '...different certifications'"],
      "consequence": "This is a systemic blocker",
      "implication_for_claude": "Agent Ingénieur can centralize multi-country compliance"
    },
    {
      "pattern": "Work style: pragmatic + fast-moving",
      "evidence": "Shows 3 indicators of pragmatic approach",
      "implication_for_claude": "Config should prioritize action > documentation"
    }
  ],
  "work_style_traits": [
    {
      "trait": "Pragmatic",
      "implication": "Prefers practical results over theory"
    },
    {
      "trait": "Risk-aware",
      "implication": "Careful about compliance and regulations"
    }
  ]
}
```

---

## Testing Checklist

Before proceeding to EPIC-3:

- [ ] Test 1: Pattern detection active (≥1 pattern detected per response)
- [ ] Test 2: Recurring keywords (same keyword mentioned 2x → marked as pattern)
- [ ] Test 3: Work style detection (pragmatic/structured/feeling-based traits identified)
- [ ] Test 4: Strength signals (client mentions "I'm good at X" → captured)
- [ ] Test 5: Risk indicators (client says "I forget Y" → marked as pain point)
- [ ] Test 6: Metadata consistency (patterns build on previous turns, not duplicated)
- [ ] Test 7: 5+ full diagnostics (run end-to-end, validate pattern quality)

---

## Quality Standards for Detected Patterns

✅ **Specific**: "Compliance across 40 countries" (not "has challenges")  
✅ **Grounded**: Includes evidence (quote from response, turn number)  
✅ **Actionable**: Informs subsequent questions or opportunities  
✅ **Lightweight**: Total metadata < 2KB even with 10+ patterns

❌ **Generic**: "Client seems busy"  
❌ **Ungrounded**: No evidence, no quotes  
❌ **Vague**: "Person-related issues"  

---

## Performance Considerations

- Pattern detection should run in < 500ms
- Metadata object should stay < 2KB (even with 15+ turns)
- No regex DoS vulnerabilities (limit regex complexity)
- Cache conversation history locally (don't re-fetch from DB each turn)

---

## Rollback Plan

If pattern detection causes issues:
1. Disable pattern detection function (comment out `detectPatterns()` call)
2. Revert to EPIC-1 system prompt (still works without pattern detection)
3. Metadata will be empty for patterns, but diagnostic continues
4. Document issue for EPIC-2 iteration

---

**EPIC-2 Status**: Specification complete  
**Dependencies Met**: EPIC-1 deployed  
**Next**: EPIC-3 (Claude Opportunities Identification)
