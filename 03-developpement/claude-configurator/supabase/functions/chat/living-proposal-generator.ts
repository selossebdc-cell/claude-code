import {
  ClaudeOpportunity,
  DiagnosticMetadata,
  LivingProposal,
  ConfiguredAgent,
  ConfiguredRoutine,
  MemorySection,
  ExpectedImpact,
} from "./metadata-manager.ts";

const MANDATORY_AGENT_ROLES = [
  "Miroir",
  "Garde-Fou",
  "Admin",
  "Stratégie",
  "Planif",
  "Amélioration Continue",
];

function pickOpportunityForAgent(
  opportunities: ClaudeOpportunity[],
  agentRole: string
): ClaudeOpportunity | undefined {
  return opportunities.find((o) => o.agent_role === agentRole);
}

function buildAgentPrompt(
  agentRole: string,
  metadata: DiagnosticMetadata,
  source?: ClaudeOpportunity
): string {
  const topPainPoints = (metadata.pain_points || [])
    .slice(0, 3)
    .map((p) => p.area)
    .join(", ");
  const workStyle = (metadata.work_style_traits || [])
    .slice(0, 3)
    .map((t) => t.trait)
    .join(", ");

  return [
    `You are the "${agentRole}" agent for this consulting leader.`,
    `Current key pain points: ${topPainPoints || "to be clarified with user context"}.`,
    `Observed work style traits: ${workStyle || "adaptive"}.
`,
    source?.why_claude_transforms
      ? `Priority context: ${source.why_claude_transforms}`
      : "Priority context: Focus on concrete operational leverage.",
    "Always return concise, actionable guidance with clear next steps and trade-offs.",
  ].join("\n");
}

function buildAgents(metadata: DiagnosticMetadata): ConfiguredAgent[] {
  const opportunities = metadata.claude_opportunities || [];

  return MANDATORY_AGENT_ROLES.map((role) => {
    const matched = pickOpportunityForAgent(opportunities, role);
    const id = role.toLowerCase().replace(/\s+/g, "-");
    const trigger =
      role === "Miroir"
        ? "Chaque matin"
        : role === "Amélioration Continue"
          ? "Chaque fin de semaine"
          : "A la demande + routine hebdomadaire";

    return {
      id: `agent-${id}`,
      role,
      mandatory: true,
      selected: true,
      recommended: true,
      editable: true,
      trigger,
      prompt: buildAgentPrompt(role, metadata, matched),
      why_for_you:
        matched?.description ||
        `Agent ${role} activé pour structurer une partie critique de ton activité.`,
      expected_outcome:
        matched?.opportunity
          ? `Résoudre ${matched.opportunity.toLowerCase()} de manière reproductible.`
          : `Améliorer la prise de décision et l'exécution sur le scope ${role}.`,
    };
  });
}

function buildRoutines(metadata: DiagnosticMetadata): ConfiguredRoutine[] {
  const hasSecurityNeed = (metadata.pain_points || []).some((p) =>
    p.area.toLowerCase().includes("risk")
      || p.area.toLowerCase().includes("security")
  );

  const routines: ConfiguredRoutine[] = [
    {
      id: "routine-daily-priorities",
      cadence: "daily",
      title: "Brief priorités du jour",
      trigger_timing: "Tous les matins (9h)",
      prompt: "Donne-moi mes 3 priorités stratégiques du jour et ce qui peut bloquer.",
      expected_output: "Top 3 priorités + 1 mitigation par risque",
      effort_estimate: "low",
      linked_agents: ["Miroir", "Planif"],
      recommended: true,
      editable: true,
    },
    {
      id: "routine-weekly-decision-audit",
      cadence: "weekly",
      title: "Audit décisions de la semaine",
      trigger_timing: hasSecurityNeed ? "Mercredi 12h + Vendredi 17h" : "Vendredi 17h",
      prompt: "Analyse mes décisions clés, signale les angles morts, propose 2 améliorations.",
      expected_output: "Score décision + risques + améliorations",
      effort_estimate: "medium",
      linked_agents: ["Garde-Fou", "Amélioration Continue"],
      recommended: true,
      editable: true,
    },
    {
      id: "routine-monthly-strategy-review",
      cadence: "monthly",
      title: "Revue stratégique mensuelle",
      trigger_timing: "1er lundi du mois",
      prompt: "Sommes-nous alignés avec les objectifs trimestriels? Que faut-il ajuster?",
      expected_output: "Ajustements stratégiques + priorités du mois",
      effort_estimate: "medium",
      linked_agents: ["Stratégie", "Admin"],
      recommended: true,
      editable: true,
    },
    {
      id: "routine-as-needed-big-projects",
      cadence: "as_needed",
      title: "Lancement projet complexe",
      trigger_timing: "A déclencher pour tout projet > 5 jours",
      prompt: "Découpe le projet en étapes, dépendances, risques, et plan d'exécution.",
      expected_output: "Plan exécutable avec jalons",
      effort_estimate: "low",
      linked_agents: ["Planif", "Admin"],
      recommended: true,
      editable: true,
    },
  ];

  return routines;
}

function buildMemorySections(metadata: DiagnosticMetadata): MemorySection[] {
  const hasDecisionPain = (metadata.pain_points || []).some((p) =>
    p.area.toLowerCase().includes("decision")
  );

  return [
    {
      id: "memory-identity",
      title: "Identity",
      description: "Rôle, vision, critères de décision, priorités.",
      recommended: true,
      editable: true,
    },
    {
      id: "memory-business-context",
      title: "Business Context",
      description: "Marché, offre, contraintes et objectifs de croissance.",
      recommended: true,
      editable: true,
    },
    {
      id: "memory-decision-log",
      title: "Decision Log",
      description: "Historique des décisions, rationale, résultats observés.",
      recommended: hasDecisionPain,
      editable: true,
    },
    {
      id: "memory-patterns",
      title: "Patterns",
      description: "Ce qui fonctionne, ce qui bloque, signaux faibles récurrents.",
      recommended: true,
      editable: true,
    },
    {
      id: "memory-weekly-learnings",
      title: "Weekly Learnings",
      description: "Leçons de la semaine et ajustements pour la suivante.",
      recommended: true,
      editable: true,
    },
  ];
}

function buildExpectedImpacts(metadata: DiagnosticMetadata): ExpectedImpact[] {
  const painPointCount = (metadata.pain_points || []).length;
  const opportunityCount = (metadata.claude_opportunities || []).length;

  return [
    {
      id: "impact-decision-speed",
      area: "Decision",
      metric: "Temps moyen de décision",
      timeframe: "30 jours",
      expected_change: "-30% a -50%",
      rationale: `Basé sur ${opportunityCount} opportunités identifiées et routines d'audit.`,
    },
    {
      id: "impact-operational-clarity",
      area: "Operations",
      metric: "Clarté des priorités hebdomadaires",
      timeframe: "2 semaines",
      expected_change: "+1 niveau (de flou à structuré)",
      rationale: "Brief quotidien + planification as-needed sur projets complexes.",
    },
    {
      id: "impact-admin-load",
      area: "Admin",
      metric: "Temps administratif hebdo",
      timeframe: "4 semaines",
      expected_change: "-5h à -10h/semaine",
      rationale: `Réduction des frictions autour de ${Math.max(1, painPointCount)} zones de blocage principales.`,
    },
  ];
}

function buildCustomInstructionsDraft(metadata: DiagnosticMetadata): string {
  const topTraits = (metadata.work_style_traits || [])
    .slice(0, 4)
    .map((t) => t.trait)
    .join(", ");
  const topPainPoints = (metadata.pain_points || [])
    .slice(0, 4)
    .map((p) => p.area)
    .join(", ");

  return [
    "You are supporting a business owner/consultant in France.",
    `Decision style observed: ${topTraits || "pragmatic and adaptive"}.`,
    `Main pain points to keep in view: ${topPainPoints || "prioritization and execution consistency"}.`,
    "Prefer concise, high-signal outputs: 3 options max + 1 recommendation.",
    "Always include trade-offs, risk flags, and the smallest executable next step.",
    "When uncertain, ask one clarifying question before proposing a full plan.",
  ].join("\n");
}

export function generateLivingProposal(
  metadata: DiagnosticMetadata
): LivingProposal {
  const now = new Date().toISOString();
  const agents = buildAgents(metadata);
  const routines = buildRoutines(metadata);
  const memorySections = buildMemorySections(metadata);
  const expectedImpacts = buildExpectedImpacts(metadata);

  return {
    proposal_version: "v1",
    generated_at: now,
    source_session_id: metadata.session_id,
    update_reason: "Initial EPIC-6 proposal generated from diagnostic metadata",
    agents,
    routines,
    memory_sections: memorySections,
    custom_instructions_draft: buildCustomInstructionsDraft(metadata),
    expected_impacts: expectedImpacts,
    benchmark_signals: {
      social_proof_placeholders: [
        "Ajouter 2 témoignages chiffrés (temps gagné, décisions accélérées)",
        "Ajouter 1 preuve sectorielle (consulting/PME)",
      ],
      founder_authority_block:
        "Inclure bloc crédibilité fondatrice: expérience terrain + transformations obtenues.",
      cta_strategy_slots: [
        "CTA Hero + garantie",
        "CTA après gap analysis",
        "CTA après pricing anchor",
        "CTA footer avec risk reversal",
      ],
    },
  };
}
