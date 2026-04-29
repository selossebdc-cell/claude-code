/**
 * EPIC-7 — Assemble exportable Claude configuration from diagnostic outputs.
 * Deterministic bundle (no extra LLM call) for reliability and predictable deploy size.
 */

export interface SynthesisSections {
  understanding: string;
  transformation: string;
  config_preview: string;
}

export interface AssemblyAgent {
  role: string;
  trigger: string;
  prompt: string;
  why_for_you: string;
  expected_outcome: string;
}

export interface AssemblyRoutine {
  cadence: string;
  title: string;
  trigger_timing: string;
  prompt: string;
  expected_output: string;
  linked_agents: string[];
}

export interface AssemblyMemorySection {
  title: string;
  description: string;
  recommended: boolean;
}

export interface LivingProposalLike {
  proposal_version?: string;
  generated_at?: string;
  agents?: AssemblyAgent[];
  routines?: AssemblyRoutine[];
  memory_sections?: AssemblyMemorySection[];
  custom_instructions_draft?: string;
  expected_impacts?: Array<{
    area: string;
    metric: string;
    timeframe: string;
    expected_change: string;
    rationale: string;
  }>;
  benchmark_signals?: {
    social_proof_placeholders?: string[];
    founder_authority_block?: string;
    cta_strategy_slots?: string[];
  };
}

export interface DiagnosticLike {
  session_id?: string;
  client_name?: string;
  synthesis?: SynthesisSections;
  living_proposal?: LivingProposalLike;
}

export interface GeneratedConfigPackage {
  format_version: "2026.04.epic7";
  generated_at: string;
  session_id: string;
  sources: {
    has_synthesis: boolean;
    has_living_proposal: boolean;
  };
  markdown_bundle: string;
  structured: {
    synthesis?: SynthesisSections;
    living_proposal?: LivingProposalLike;
    custom_instructions: string;
  };
  validation: {
    ready: boolean;
    warnings: string[];
  };
}

function truncate(s: string, max: number): string {
  if (!s || s.length <= max) return s;
  return `${s.slice(0, max - 10)}\n…(truncated)`;
}

function buildMarkdown(pkg: GeneratedConfigPackage): string {
  const lp = pkg.structured.living_proposal;
  const syn = pkg.structured.synthesis;
  const lines: string[] = [];

  lines.push("# Claude Configurator — Pack de configuration personnalisé");
  lines.push("");
  lines.push(`Session: ${pkg.session_id}`);
  lines.push(`Généré: ${pkg.generated_at}`);
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## Synthèse stratégique");
  lines.push("");
  if (syn) {
    lines.push("### Ce que nous avons compris");
    lines.push(syn.understanding || "(non disponible)");
    lines.push("");
    lines.push("### Où Claude devient game-changer");
    lines.push(syn.transformation || "(non disponible)");
    lines.push("");
    lines.push("### Aperçu de votre config");
    lines.push(syn.config_preview || "(non disponible)");
    lines.push("");
  } else {
    lines.push("_Synthèse non encore disponible — régénérez après diagnostic complet._");
    lines.push("");
  }

  lines.push("---");
  lines.push("");
  lines.push("## Custom Instructions (proposition)");
  lines.push("");
  lines.push(pkg.structured.custom_instructions || "(non défini)");
  lines.push("");

  if (lp?.agents?.length) {
    lines.push("---");
    lines.push("");
    lines.push("## Agents (6 noyaux)");
    lines.push("");
    for (const a of lp.agents) {
      lines.push(`### ${a.role}`);
      lines.push(`- **Déclencheur**: ${a.trigger}`);
      lines.push(`- **Pourquoi vous**: ${a.why_for_you}`);
      lines.push(`- **Résultat attendu**: ${a.expected_outcome}`);
      lines.push("");
      lines.push("```text");
      lines.push(a.prompt || "");
      lines.push("```");
      lines.push("");
    }
  }

  if (lp?.routines?.length) {
    lines.push("---");
    lines.push("");
    lines.push("## Routines recommandées");
    lines.push("");
    for (const r of lp.routines) {
      lines.push(`### ${r.title} (${r.cadence})`);
      lines.push(`- **Quand**: ${r.trigger_timing}`);
      lines.push(`- **Agents**: ${(r.linked_agents || []).join(", ")}`);
      lines.push("");
      lines.push(`**Prompt**: ${r.prompt}`);
      lines.push("");
      lines.push(`**Sortie attendue**: ${r.expected_output}`);
      lines.push("");
    }
  }

  if (lp?.memory_sections?.length) {
    lines.push("---");
    lines.push("");
    lines.push('## Structure « Ma Mémoire » (sections à activer)');
    lines.push("");
    for (const m of lp.memory_sections) {
      lines.push(`- **${m.title}** ${m.recommended ? "(recommandé)" : ""}: ${m.description}`);
    }
    lines.push("");
  }

  if (lp?.expected_impacts?.length) {
    lines.push("---");
    lines.push("");
    lines.push("## Impacts attendus (benchmark)");
    lines.push("");
    for (const i of lp.expected_impacts) {
      lines.push(
        `- **${i.area}** — ${i.metric}: ${i.expected_change} (${i.timeframe}). _${i.rationale}_`
      );
    }
    lines.push("");
  }

  if (lp?.benchmark_signals) {
    lines.push("---");
    lines.push("");
    lines.push("## Signaux marketing / landing (à compléter)");
    lines.push("");
    if (lp.benchmark_signals.social_proof_placeholders?.length) {
      lines.push("### Social proof");
      for (const s of lp.benchmark_signals.social_proof_placeholders) {
        lines.push(`- ${s}`);
      }
      lines.push("");
    }
    if (lp.benchmark_signals.founder_authority_block) {
      lines.push("### Crédibilité fondatrice");
      lines.push(lp.benchmark_signals.founder_authority_block);
      lines.push("");
    }
    if (lp.benchmark_signals.cta_strategy_slots?.length) {
      lines.push("### Emplacements CTA");
      for (const c of lp.benchmark_signals.cta_strategy_slots) {
        lines.push(`- ${c}`);
      }
    }
  }

  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push(
    "_Ce document est une proposition vivante : ajustez les prompts et routines avant de les figer dans Claude._"
  );

  return lines.join("\n");
}

export function assembleConfigPackage(
  sessionId: string,
  metadata: DiagnosticLike
): GeneratedConfigPackage {
  const warnings: string[] = [];
  const hasSynth = Boolean(
    metadata.synthesis?.understanding ||
      metadata.synthesis?.transformation ||
      metadata.synthesis?.config_preview
  );
  const hasLp = Boolean(
    metadata.living_proposal?.agents && metadata.living_proposal.agents.length > 0
  );

  if (!hasSynth) warnings.push("Strategic synthesis missing — run diagnostic until synthesis is generated.");
  if (!hasLp) warnings.push("Living proposal missing — complete at least one chat turn after EPIC-6 deploy.");

  const customInstructions =
    metadata.living_proposal?.custom_instructions_draft ||
    "Fill custom instructions after reviewing the diagnostic synthesis.";

  const pkg: GeneratedConfigPackage = {
    format_version: "2026.04.epic7",
    generated_at: new Date().toISOString(),
    session_id: sessionId,
    sources: {
      has_synthesis: hasSynth,
      has_living_proposal: hasLp,
    },
    markdown_bundle: "",
    structured: {
      synthesis: metadata.synthesis,
      living_proposal: metadata.living_proposal,
      custom_instructions: customInstructions,
    },
    validation: {
      ready: hasSynth && hasLp,
      warnings,
    },
  };

  let md = buildMarkdown(pkg);
  md = truncate(md, 48000);
  pkg.markdown_bundle = md;

  return pkg;
}
