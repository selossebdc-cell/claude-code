// Opportunity Identification Engine for Diagnostic Intelligence
// Links pain_points + patterns to specific Claude opportunities and agents

import {
  ClaudeOpportunity,
  PainPoint,
  Pattern,
  WorkStyleTrait,
  DiagnosticMetadata,
} from "./metadata-manager.ts";

interface OpportunityDefinition {
  name: string;
  agentRole: string;
  agentType: "mandatory" | "contextual";
  triggers: {
    painPoints: string[];
    patterns: string[];
  };
  description: string;
  impact: "high" | "medium" | "low";
  effort: "high" | "medium" | "low";
  confidence: number;
  whyTransforms: (source: string) => string;
}

const OPPORTUNITY_MAP: OpportunityDefinition[] = [
  // SECURITY & COMPLIANCE
  {
    name: "Compliance Hub",
    agentRole: "Ingénieur",
    agentType: "contextual",
    triggers: {
      painPoints: ["compliance", "certifications", "regulations", "multi-country"],
      patterns: ["risk-aware", "risk_indicator"],
    },
    description:
      "Centralized compliance tracking across all regions and domains",
    impact: "high",
    effort: "medium",
    confidence: 0.95,
    whyTransforms: (source) =>
      `Agent Ingénieur monitors all ${source} requirements simultaneously, alerts on changes, maintains audit trail — no manual tracking`,
  },

  {
    name: "Security & Risk Shield",
    agentRole: "Garde-Fou",
    agentType: "mandatory",
    triggers: {
      painPoints: ["security", "data", "fraud", "phishing", "risk"],
      patterns: ["risk_indicator", "risk-aware"],
    },
    description: "Automated security monitoring, validation, transaction checks",
    impact: "high",
    effort: "low",
    confidence: 0.95,
    whyTransforms: (source) =>
      `Garde-Fou acts as your 24/7 security guard — every decision validated, every action checked. Zero human oversight needed`,
  },

  // DOCUMENTATION & ADMINISTRATION
  {
    name: "Auto-Documentation Hub",
    agentRole: "Admin",
    agentType: "mandatory",
    triggers: {
      painPoints: ["documentation", "templates", "processes", "workflow"],
      patterns: ["pragmatic", "work_style"],
    },
    description: "Auto-generate docs, templates, correspondence from decisions",
    impact: "high",
    effort: "medium",
    confidence: 0.9,
    whyTransforms: (source) =>
      `Admin auto-generates ${source} from your decisions — no manual writing, stays current automatically`,
  },

  {
    name: "Decision Logging & Memory",
    agentRole: "Miroir",
    agentType: "mandatory",
    triggers: {
      painPoints: ["decision", "tracking", "memory", "documentation"],
      patterns: ["work_style", "feeling_based"],
    },
    description:
      "Automatically logs decisions, rationale, and outcomes for future reference",
    impact: "medium",
    effort: "low",
    confidence: 0.85,
    whyTransforms: (source) =>
      `Miroir logs every ${source} with reasoning — you operate by instinct but every choice is documented for consistency`,
  },

  // STRATEGY & PLANNING
  {
    name: "Strategic Roadmap Engine",
    agentRole: "Stratégie",
    agentType: "mandatory",
    triggers: {
      painPoints: ["strategy", "vision", "planning", "growth", "scaling"],
      patterns: ["strength", "innovative"],
    },
    description: "Builds and maintains strategic roadmap aligned with your vision",
    impact: "high",
    effort: "medium",
    confidence: 0.85,
    whyTransforms: (source) =>
      `Stratégie translates your ${source} into executable steps — maintains alignment as context changes`,
  },

  {
    name: "Execution Planning",
    agentRole: "Planif",
    agentType: "mandatory",
    triggers: {
      painPoints: [
        "timeline",
        "deadlines",
        "milestones",
        "schedule",
        "execution",
      ],
      patterns: ["pragmatic", "work_style"],
    },
    description:
      "Breaks strategy into timeline, milestones, and accountable tasks",
    impact: "high",
    effort: "medium",
    confidence: 0.9,
    whyTransforms: (source) =>
      `Planif converts strategy into concrete ${source} with dependencies & accountability — no more vague plans`,
  },

  // CONTINUOUS IMPROVEMENT
  {
    name: "Weekly Debrief & Iteration",
    agentRole: "Amélioration Continue",
    agentType: "mandatory",
    triggers: {
      painPoints: ["progress", "iteration", "learning", "improvement"],
      patterns: ["work_style", "strength"],
    },
    description:
      "Structured weekly debriefs to measure progress and refine approach",
    impact: "medium",
    effort: "low",
    confidence: 0.9,
    whyTransforms: (source) =>
      `Amélioration Continue systematizes ${source} — every week, measure what worked, adjust next week`,
  },

  // CONTEXTUAL: PROGRESS TRACKING
  {
    name: "Progress Tracking Dashboard",
    agentRole: "Coach",
    agentType: "contextual",
    triggers: {
      painPoints: ["measurement", "progress", "metrics", "tracking"],
      patterns: ["strength", "pragmatic"],
    },
    description:
      "Real-time metrics by domain/market, trend analysis, and forecasting",
    impact: "medium",
    effort: "medium",
    confidence: 0.8,
    whyTransforms: (source) =>
      `Coach gives you ${source} by domain in real-time — no spreadsheet maintenance, automatic aggregation`,
  },

  // CONTEXTUAL: TECHNICAL VALIDATION
  {
    name: "Technical Validation & Compliance",
    agentRole: "Ingénieur",
    agentType: "contextual",
    triggers: {
      painPoints: [
        "technical",
        "validation",
        "architecture",
        "scalability",
        "compliance",
      ],
      patterns: ["pragmatic", "risk_indicator"],
    },
    description:
      "Technical validation, architecture review, and compliance verification",
    impact: "high",
    effort: "high",
    confidence: 0.85,
    whyTransforms: (source) =>
      `Ingénieur ensures ${source} against regulations/standards — automatic validation, zero manual checks`,
  },
];

export function identifyOpportunities(
  metadata: DiagnosticMetadata
): ClaudeOpportunity[] {
  const opportunities: ClaudeOpportunity[] = [];
  const addedNames = new Set<string>();

  // ANALYSIS 1: Pain Points → Opportunities
  (metadata.pain_points || []).forEach((painPoint) => {
    const matchedOpportunities = filterOpportunitiesByPainPoint(painPoint.area);

    matchedOpportunities.forEach((opp) => {
      if (!addedNames.has(opp.name)) {
        opportunities.push({
          opportunity: opp.name,
          description: opp.description,
          linked_pain_point: painPoint.area,
          why_claude_transforms: opp.whyTransforms(painPoint.area),
          agent_role: opp.agentRole,
          agent_type: opp.agentType,
          priority: calculatePriority(painPoint.severity || "medium", opp.impact),
          impact_estimate: opp.impact,
          effort_estimate: opp.effort,
          confidence: opp.confidence,
        });
        addedNames.add(opp.name);
      }
    });
  });

  // ANALYSIS 2: Patterns → Opportunities
  (metadata.patterns_detected || []).forEach((pattern) => {
    const matchedOpportunities = filterOpportunitiesByPattern(pattern.pattern);

    matchedOpportunities.forEach((opp) => {
      if (!addedNames.has(opp.name)) {
        opportunities.push({
          opportunity: opp.name,
          description: opp.description,
          linked_pattern: pattern.pattern,
          why_claude_transforms: opp.whyTransforms(pattern.pattern),
          agent_role: opp.agentRole,
          agent_type: opp.agentType,
          priority: calculatePriority("medium", opp.impact),
          impact_estimate: opp.impact,
          effort_estimate: opp.effort,
          confidence: opp.confidence,
        });
        addedNames.add(opp.name);
      }
    });
  });

  // ANALYSIS 3: Work Style Traits → Opportunities
  (metadata.work_style_traits || []).forEach((trait) => {
    const matchedOpportunities = filterOpportunitiesByWorkStyle(trait.trait);

    matchedOpportunities.forEach((opp) => {
      if (!addedNames.has(opp.name)) {
        opportunities.push({
          opportunity: opp.name,
          description: opp.description,
          why_claude_transforms: opp.whyTransforms(trait.trait),
          agent_role: opp.agentRole,
          agent_type: opp.agentType,
          priority: calculatePriority("low", opp.impact),
          impact_estimate: opp.impact,
          effort_estimate: opp.effort,
          confidence: Math.max(0, opp.confidence - 0.15), // Slightly lower for work style
        });
        addedNames.add(opp.name);
      }
    });
  });

  // Ensure mandatory agents are always included
  const mandatoryAgents = [
    "Admin",
    "Miroir",
    "Stratégie",
    "Planif",
    "Amélioration Continue",
    "Garde-Fou",
  ];

  mandatoryAgents.forEach((agentRole) => {
    const mandatoryOpp = OPPORTUNITY_MAP.find(
      (o) => o.agentRole === agentRole && o.agentType === "mandatory"
    );

    if (
      mandatoryOpp &&
      !opportunities.some((o) => o.opportunity === mandatoryOpp.name)
    ) {
      // Add generic version if no specific trigger matched
      opportunities.push({
        opportunity: mandatoryOpp.name,
        description: mandatoryOpp.description,
        why_claude_transforms: mandatoryOpp.whyTransforms("your workflow"),
        agent_role: mandatoryOpp.agentRole,
        agent_type: "mandatory",
        priority: 3,
        impact_estimate: mandatoryOpp.impact,
        effort_estimate: mandatoryOpp.effort,
        confidence: 0.75, // Lower confidence for generic fallback
      });
    }
  });

  // Sort by priority
  return opportunities.sort((a, b) => a.priority - b.priority);
}

function filterOpportunitiesByPainPoint(painPointArea: string): OpportunityDefinition[] {
  const normalizedArea = painPointArea.toLowerCase();

  return OPPORTUNITY_MAP.filter((opp) =>
    opp.triggers.painPoints.some(
      (p) =>
        normalizedArea.includes(p) ||
        p.includes(normalizedArea.substring(0, 10))
    )
  );
}

function filterOpportunitiesByPattern(pattern: string): OpportunityDefinition[] {
  const normalizedPattern = pattern.toLowerCase();

  return OPPORTUNITY_MAP.filter((opp) =>
    opp.triggers.patterns.some((p) =>
      normalizedPattern.includes(p) || p.includes(normalizedPattern.substring(0, 10))
    )
  );
}

function filterOpportunitiesByWorkStyle(workStyle: string): OpportunityDefinition[] {
  const normalizedStyle = workStyle.toLowerCase();

  return OPPORTUNITY_MAP.filter((opp) =>
    opp.triggers.patterns.some(
      (p) =>
        normalizedStyle.includes(p) || p.includes(normalizedStyle.substring(0, 8))
    )
  );
}

function calculatePriority(
  severity: "high" | "medium" | "low",
  impact: "high" | "medium" | "low"
): number {
  const severityScore: Record<string, number> = {
    high: 3,
    medium: 2,
    low: 1,
  };

  const impactScore: Record<string, number> = {
    high: 2,
    medium: 1,
    low: 0,
  };

  const score = (severityScore[severity] || 1) + (impactScore[impact] || 0);
  return Math.max(1, Math.min(5, score)); // Clamp to 1-5
}
