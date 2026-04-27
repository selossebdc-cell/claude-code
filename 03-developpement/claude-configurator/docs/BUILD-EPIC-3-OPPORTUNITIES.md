# BUILD — EPIC-3: Claude Opportunities Identification

## Overview
Implémenter la détection automatique des opportunités où Claude devient vraiment game-changer pour le client.

**Statut**: Ready to implement  
**Effort**: 3.5 days (1 day design + 1 day integration + 1.5 days testing)  
**Blocker**: EPIC-2 (Pattern Detection) must be deployed first  
**Dependency**: EPIC-2 ✓  

---

## Implementation Steps

### Step 1: Opportunity Detection Logic (Day 1)
Design algorithm that links pain_points + patterns to specific Claude opportunities.

**Location**: Chat Edge Function v21+ (opportunity analyzer)  
**Input**: Detected pain_points + patterns + work_style_traits  
**Output**: claude_opportunities[] with priority, agent role, justification

### Step 2: Agent Role Assignment (Day 1)
Map each opportunity to appropriate agent:
- **Miroir**: Self-understanding, pattern recognition
- **Garde-Fou**: Security, compliance, risk management
- **Admin**: Document management, automation, templates
- **Stratégie**: Strategic planning, roadmap, long-term vision
- **Planif**: Task management, timelines, execution
- **Amélioration Continue**: Process optimization, iteration cycles
- **Coach** (contextual): Progress tracking, metrics
- **Ingénieur** (contextual): Technical validation, complexity

### Step 3: Opportunity-Metadata Linking (Day 2)
- Link each opportunity to its source pain_point
- Include why Claude transforms (vs manual approach)
- Track opportunity priority (1-5, where 1 is critical)
- Calculate impact + effort estimates

### Step 4: Testing (Day 2-3)
- Test with 5+ diverse diagnostics
- Validate ≥3 opportunities detected per diagnostic
- Validate opportunities are specific (not generic)
- Validate linked to pain_points correctly
- Validate agent role assignments make sense

---

## Opportunity Detection Logic (Code Specification)

```javascript
/**
 * Opportunity Identification Engine
 * Links pain_points + patterns to specific Claude opportunities
 * Maps to mandatory/contextual agents
 */

function identifyOpportunities(metadata, workContext) {
  const opportunities = [];
  const opportunityMap = buildOpportunityMap();
  
  // ANALYSIS 1: Direct Pain Point → Opportunity Mapping
  metadata.pain_points?.forEach((painPoint, idx) => {
    const matchedOpportunities = opportunityMap.filterByPainPoint(painPoint.area);
    
    matchedOpportunities.forEach(opp => {
      opportunities.push({
        id: `oc_${opportunities.length + 1}`,
        opportunity: opp.name,
        description: opp.description,
        linked_pain_point: painPoint.area,
        why_claude_transforms: opp.whyTransforms(painPoint),
        agent_role: opp.agentRole,
        agent_type: opp.agentType, // "mandatory" or "contextual"
        priority: calculatePriority(painPoint.severity, opp.impact),
        impact_estimate: opp.impact,
        effort_estimate: opp.effort,
        confidence: opp.confidence
      });
    });
  });
  
  // ANALYSIS 2: Pattern → Opportunity Linking
  metadata.patterns_detected?.forEach(pattern => {
    const matchedOpportunities = opportunityMap.filterByPattern(pattern.pattern);
    
    matchedOpportunities.forEach(opp => {
      // Avoid duplicates
      if (!opportunities.some(o => o.opportunity === opp.name)) {
        opportunities.push({
          id: `oc_${opportunities.length + 1}`,
          opportunity: opp.name,
          description: opp.description,
          linked_pattern: pattern.pattern,
          why_claude_transforms: opp.whyTransformsByPattern(pattern),
          agent_role: opp.agentRole,
          agent_type: opp.agentType,
          priority: calculatePriority("medium", opp.impact),
          impact_estimate: opp.impact,
          effort_estimate: opp.effort,
          confidence: opp.confidence
        });
      }
    });
  });
  
  // ANALYSIS 3: Work Style → Optimization Opportunities
  metadata.work_style_traits?.forEach(trait => {
    const optimizations = opportunityMap.filterByWorkStyle(trait.trait);
    
    optimizations.forEach(opt => {
      if (!opportunities.some(o => o.opportunity === opt.name)) {
        opportunities.push({
          id: `oc_${opportunities.length + 1}`,
          opportunity: opt.name,
          description: opt.description,
          linked_work_style: trait.trait,
          why_claude_transforms: opt.whyTransformsWorkStyle(trait),
          agent_role: opt.agentRole,
          agent_type: opt.agentType,
          priority: calculatePriority("low", opt.impact),
          impact_estimate: opt.impact,
          effort_estimate: opt.effort,
          confidence: 0.7 // Lower confidence for optimizations
        });
      }
    });
  });
  
  // Sort by priority
  return opportunities.sort((a, b) => a.priority - b.priority);
}

/**
 * Build Opportunity Map
 * Defines all possible opportunities and their triggers
 */
function buildOpportunityMap() {
  const opportunities = [
    // COMPLIANCE & SECURITY Opportunities
    {
      name: "Compliance Hub",
      agentRole: "Ingénieur",
      agentType: "contextual",
      triggers: {
        painPoints: ["compliance", "regulations", "certifications", "multi-country"],
        patterns: ["risk-aware"]
      },
      description: "Centralized compliance tracking across all regions/domains",
      whyTransforms: (painPoint) => 
        `Agent Ingénieur monitors all ${painPoint.area} requirements simultaneously, 
         alerts on changes, maintains audit trail — no manual tracking`,
      impact: "high",
      effort: "medium",
      confidence: 0.95
    },
    
    {
      name: "Security & Risk Shield",
      agentRole: "Garde-Fou",
      agentType: "mandatory",
      triggers: {
        painPoints: ["security", "data", "fraud", "phishing"],
        patterns: ["risk-aware"]
      },
      description: "Automated security monitoring, antiphishing, transaction validation",
      whyTransforms: (painPoint) =>
        `Garde-Fou acts as your 24/7 security guard — every action validated, 
         every decision checked. Zero human oversight needed`,
      impact: "high",
      effort: "low",
      confidence: 0.95
    },
    
    // DOCUMENTATION & ADMIN Opportunities
    {
      name: "Auto-Documentation Hub",
      agentRole: "Admin",
      agentType: "mandatory",
      triggers: {
        painPoints: ["documentation", "templates", "processes"],
        patterns: ["pragmatic", "fast-moving"]
      },
      description: "Auto-generate docs, templates, correspondence from decisions",
      whyTransforms: (painPoint) =>
        `Admin auto-generates ${painPoint.area} from your decisions — no manual writing, 
         stays current automatically`,
      impact: "high",
      effort: "medium",
      confidence: 0.9
    },
    
    {
      name: "Decision Logging & Memory",
      agentRole: "Miroir",
      agentType: "mandatory",
      triggers: {
        painPoints: ["decisions", "tracking", "memory"],
        patterns: ["feeling-based", "fast-moving"]
      },
      description: "Automatically logs decisions, rationale, outcomes for future reference",
      whyTransforms: (painPoint) =>
        `Miroir logs every ${painPoint.area} with reasoning — you operate by instinct 
         but every choice is documented for consistency`,
      impact: "medium",
      effort: "low",
      confidence: 0.85
    },
    
    // STRATEGY & PLANNING Opportunities
    {
      name: "Strategic Roadmap Engine",
      agentRole: "Stratégie",
      agentType: "mandatory",
      triggers: {
        painPoints: ["strategy", "vision", "planning", "growth"],
        patterns: ["innovative", "growth-focused"]
      },
      description: "Builds & maintains strategic roadmap aligned with your vision",
      whyTransforms: (painPoint) =>
        `Stratégie translates your ${painPoint.area} into executable steps — 
         maintains alignment as context changes`,
      impact: "high",
      effort: "medium",
      confidence: 0.85
    },
    
    {
      name: "Execution Planning",
      agentRole: "Planif",
      agentType: "mandatory",
      triggers: {
        painPoints: ["timeline", "deadlines", "milestones", "schedule"],
        patterns: ["pragmatic"]
      },
      description: "Breaks strategy into timeline, milestones, accountable tasks",
      whyTransforms: (painPoint) =>
        `Planif converts strategy into concrete ${painPoint.area}} with dependencies 
         & accountability — no more vague plans`,
      impact: "high",
      effort: "medium",
      confidence: 0.9
    },
    
    // CONTINUOUS IMPROVEMENT Opportunities
    {
      name: "Weekly Debrief & Iteration",
      agentRole: "Amélioration Continue",
      agentType: "mandatory",
      triggers: {
        painPoints: ["progress", "iteration", "learning"],
        patterns: ["all"]
      },
      description: "Structured weekly debriefs to measure progress & refine approach",
      whyTransforms: (painPoint) =>
        `Amélioration Continue systematizes ${painPoint.area}} — every week, 
         measure what worked, adjust next week`,
      impact: "medium",
      effort: "low",
      confidence: 0.9
    },
    
    // CONTEXTUAL Opportunities
    {
      name: "Progress Tracking Dashboard",
      agentRole: "Coach",
      agentType: "contextual",
      triggers: {
        painPoints: ["measurement", "progress", "metrics"],
        patterns: ["achievement-focused", "data-driven"]
      },
      description: "Real-time metrics by domain/market, trend analysis, forecasting",
      whyTransforms: (painPoint) =>
        `Coach gives you ${painPoint.area}} by domain in real-time — 
         no spreadsheet maintenance, automatic aggregation`,
      impact: "medium",
      effort: "medium",
      confidence: 0.8
    },
    
    {
      name: "Technical Validation & Compliance",
      agentRole: "Ingénieur",
      agentType: "contextual",
      triggers: {
        painPoints: ["technical", "validation", "architecture", "scalability"],
        patterns: ["technical-focused"]
      },
      description: "Technical validation, architecture review, compliance verification",
      whyTransforms: (painPoint) =>
        `Ingénieur ensures ${painPoint.area}} against regulations/standards — 
         automatic validation, zero manual checks`,
      impact: "high",
      effort: "high",
      confidence: 0.85
    }
  ];
  
  return {
    filterByPainPoint: (painPointArea) => 
      opportunities.filter(o => 
        o.triggers.painPoints.some(p => painPointArea.toLowerCase().includes(p) || p.includes(painPointArea))
      ),
    filterByPattern: (pattern) =>
      opportunities.filter(o =>
        o.triggers.patterns.includes("all") || 
        o.triggers.patterns.some(p => pattern.toLowerCase().includes(p))
      ),
    filterByWorkStyle: (workStyle) =>
      opportunities.filter(o =>
        o.triggers.patterns.some(p => p.toLowerCase().includes(workStyle.toLowerCase()))
      )
  };
}

/**
 * Calculate Opportunity Priority
 * High-severity pain_points → high priority
 * High-impact opportunities → higher priority
 */
function calculatePriority(severity, impact) {
  const severityScore = {
    "high": 3,
    "medium": 2,
    "low": 1
  }[severity] || 1;
  
  const impactScore = {
    "high": 2,
    "medium": 1,
    "low": 0
  }[impact] || 0;
  
  return Math.max(1, severityScore + impactScore); // 1-5 scale
}
```

---

## Opportunity Mapping Matrix

```
Pain Point → Opportunity → Agent Role → Priority
──────────────────────────────────────────────────
Compliance (high) → Compliance Hub → Ingénieur (contextual) → P1
Documentation (high) → Auto-Documentation → Admin (mandatory) → P1
Timeline/Deadlines → Execution Planning → Planif (mandatory) → P2
Growth/Strategy → Strategic Roadmap → Stratégie (mandatory) → P2
Measurement/Progress → Progress Dashboard → Coach (contextual) → P3
Security/Risk → Security Shield → Garde-Fou (mandatory) → P1
Decisions (feeling-based) → Decision Logging → Miroir (mandatory) → P2
Iteration/Learning → Weekly Debrief → Amélioration Continue (mandatory) → P2
Technical Validation → Tech Validation → Ingénieur (contextual) → P2
```

---

## Metadata Integration (EPIC-3 Output)

After opportunity identification, metadata should include:

```json
{
  "claude_opportunities": [
    {
      "id": "oc_001",
      "opportunity": "Compliance Hub",
      "description": "Centralized monitoring across 40 countries",
      "linked_pain_point": "compliance",
      "why_claude_transforms": "Agent monitors all requirements simultaneously, alerts on changes",
      "agent_role": "Ingénieur",
      "agent_type": "contextual",
      "priority": 1,
      "impact_estimate": "high",
      "effort_estimate": "medium",
      "confidence": 0.95
    },
    {
      "id": "oc_002",
      "opportunity": "Auto-Documentation Hub",
      "description": "Auto-generate docs from decisions",
      "linked_pain_point": "documentation",
      "why_claude_transforms": "Admin auto-generates from your decisions, stays current",
      "agent_role": "Admin",
      "agent_type": "mandatory",
      "priority": 1,
      "impact_estimate": "high",
      "effort_estimate": "medium",
      "confidence": 0.9
    },
    {
      "id": "oc_003",
      "opportunity": "Strategic Roadmap Engine",
      "description": "Builds roadmap aligned with vision",
      "linked_pain_point": "strategy",
      "why_claude_transforms": "Translates vision into executable steps, maintains alignment",
      "agent_role": "Stratégie",
      "agent_type": "mandatory",
      "priority": 2,
      "impact_estimate": "high",
      "effort_estimate": "medium",
      "confidence": 0.85
    }
  ]
}
```

---

## Testing Checklist

Before proceeding to EPIC-4:

- [ ] Test 1: Opportunities detected (≥3 per diagnostic)
- [ ] Test 2: Linked to pain_points (each opp has source)
- [ ] Test 3: Agent roles assigned correctly (mandatory agents always included)
- [ ] Test 4: Contextual agents triggered appropriately (Coach for progress pain points, Ingénieur for technical)
- [ ] Test 5: Priority calculation (high-severity pain_points → high priority opps)
- [ ] Test 6: Why-transforms justification (specific to client, not generic)
- [ ] Test 7: 5+ full diagnostics (end-to-end, validate opportunity quality + diversity)

---

## Quality Standards for Opportunities

✅ **Specific**: "Compliance monitoring across 40 countries" (not "help with compliance")  
✅ **Linked**: Shows which pain_point or pattern it addresses  
✅ **Justified**: Explains why Claude transforms (vs manual approach)  
✅ **Actionable**: Maps to specific agent that will implement it  
✅ **Confident**: Confidence score reflects certainty

❌ **Generic**: "Claude can help with your workflow"  
❌ **Unlinked**: No reference to pain_points  
❌ **Vague**: "Process optimization" with no specifics  
❌ **Impossible**: Promises things Claude can't deliver  

---

## Impact vs Effort Grid

```
Impact: How much does this opportunity improve client's daily life?
- High: Transforms a major pain point or blocker
- Medium: Reduces friction, improves efficiency
- Low: Nice-to-have, optimizations

Effort: How much work to implement in config?
- Low: Simple agent prompt + routine
- Medium: Requires agent + multiple routines + custom instructions
- High: Requires multiple agents + complex integration + "Ma Mémoire" setup
```

---

## Rollback Plan

If opportunity identification causes issues:
1. Disable opportunity identification (comment out `identifyOpportunities()`)
2. Use patterns + pain_points directly (EPIC-2 continues working)
3. Metadata will be empty for opportunities, but diagnostic continues
4. Document issue for EPIC-3 iteration

---

**EPIC-3 Status**: Specification complete  
**Dependencies Met**: EPIC-2 deployed  
**Next**: EPIC-4 (Metadata Enrichment System)
