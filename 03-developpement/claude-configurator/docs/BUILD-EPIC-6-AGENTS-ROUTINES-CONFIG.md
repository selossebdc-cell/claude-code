# BUILD — EPIC-6: Agent & Routine Configuration

## Overview
Implémenter la logique de sélection des agents et configuration des routines en fonction des opportunities identifiées et du contexte client.

**Statut**: Ready to implement  
**Effort**: 3.5 days (1 day design + 1.5 days logic + 1 day testing)  
**Blocker**: EPIC-1, EPIC-2, EPIC-3 must be deployed  
**Dependencies**: EPIC-1 ✓, EPIC-2 ✓, EPIC-3 ✓, EPIC-5 ✓  

---

## Implementation Steps

### Step 1: Agent Selection Logic (Day 1)
Design algorithm that selects all 6 mandatory agents + contextual agents based on opportunities detected.

**Location**: Chat Edge Function or dedicated service  
**Input**: claude_opportunities[], work_style_traits[], pain_points[]  
**Output**: agents_config with all 8 agents (6 mandatory + 2 contextual if applicable)

### Step 2: Routine Triggering Logic (Day 1-1.5)
Define when Daily, Weekly, Monthly routines should be activated based on:
- Client's work style (fast-moving → Daily; structured → Weekly; etc.)
- Pain points (many blocages → Daily debrief; fewer → Weekly)
- Opportunities requiring tracking (progress dashboard → Coach needed → Weekly at minimum)

**Changes needed**:
- generateRoutineConfig() function
- Determine routine frequency + content based on metadata
- Ensure minimum 1 routine (Daily), propose all 3

### Step 3: Custom Instructions Generation (Day 1.5-2)
Create specialized prompt for Claude to generate 2000+ char Custom Instructions tailored to client.

**Input**: Enriched metadata (pain_points, patterns, work_style, opportunities)  
**Output**: Custom Instructions text (persona, constraints, context, tools)

### Step 4: Testing (Day 2-3)
- Test with 5+ diagnostics
- Validate all 6 mandatory agents always selected
- Validate contextual agents triggered appropriately
- Validate routines match client's work style
- Validate Custom Instructions are specific + actionable

---

## Agent Selection Algorithm

```javascript
/**
 * Agent Selection Engine
 * Selects all 6 mandatory agents + 2 contextual agents based on opportunities
 */

function selectAgents(metadata) {
  const selectedAgents = {
    mandatory: [],
    contextual: []
  };

  // MANDATORY AGENTS (always included)
  // Miroir: Self-awareness, pattern recognition
  selectedAgents.mandatory.push({
    id: "miroir",
    name: "Miroir",
    role: "Self-awareness hub — recognizes patterns, tracks progress, reflects strengths",
    description: "Automatically logs patterns, recurring themes, and personal growth",
    priority: 1,
    key_features: [
      "Pattern recognition (work style, decision patterns, recurring challenges)",
      "Progress tracking against own benchmarks",
      "Strength amplification (what works, double down)",
      "Blind spot detection (what you forget)",
      "Weekly self-assessment"
    ]
  });

  // Garde-Fou: Security, compliance, risk management
  selectedAgents.mandatory.push({
    id: "garde_fou",
    name: "Garde-Fou",
    role: "Security guardian — validates every action, prevents errors",
    description: "Automatic validation of decisions, anti-phishing, compliance checks",
    priority: 1,
    key_features: [
      "Decision validation (check before action)",
      "Antiphishing + security scanning",
      "Compliance verification (RGPD, regulations if applicable)",
      "Risk indicators (unusual patterns)",
      "Audit trail maintenance"
    ]
  });

  // Admin: Operations, documentation, templates
  selectedAgents.mandatory.push({
    id: "admin",
    name: "Admin",
    role: "Operations hub — auto-docs, templates, zero friction",
    description: "Auto-generates docs, templates, correspondence from decisions",
    priority: 1,
    key_features: [
      "Auto-documentation (from decisions → docs)",
      "Template library (auto-generated from patterns)",
      "Process automation (reduce manual work)",
      "Decision logging (why + outcomes)",
      "Integration with Ma Mémoire"
    ]
  });

  // Stratégie: Strategic planning, roadmap, vision alignment
  selectedAgents.mandatory.push({
    id: "strategie",
    name: "Stratégie",
    role: "Strategic guide — keeps focus on big picture",
    description: "Builds & maintains strategic roadmap aligned with vision",
    priority: 1,
    key_features: [
      "Roadmap building (vision → executable steps)",
      "Strategic alignment checks (decision ↔ vision)",
      "Quarterly planning (goals + milestones)",
      "Opportunity prioritization (impact vs effort)",
      "Context shifts management"
    ]
  });

  // Planif: Execution, timelines, accountability
  selectedAgents.mandatory.push({
    id: "planif",
    name: "Planif",
    role: "Execution lead — breaks strategy into timeline + accountability",
    description: "Converts strategy into timeline, milestones, accountable tasks",
    priority: 1,
    key_features: [
      "Timeline creation (strategy → deadlines)",
      "Milestone definition (what done looks like)",
      "Dependency mapping (what blocks what)",
      "Accountability (who owns what, by when)",
      "Blocker detection (removes impediments)"
    ]
  });

  // Amélioration Continue: Process optimization, iteration, learning
  selectedAgents.mandatory.push({
    id: "amelioration_continue",
    name: "Amélioration Continue",
    role: "Learning engine — weekly debriefs, continuous refinement",
    description: "Structured weekly debriefs to measure progress & refine approach",
    priority: 1,
    key_features: [
      "Weekly debriefs (what worked, what didn't)",
      "Metrics tracking (progress against goals)",
      "Process refinement (improve next week)",
      "Lesson capture (what we learned)",
      "Iteration cycles (plan → do → review → adjust)"
    ]
  });

  // CONTEXTUAL AGENTS (based on opportunities + work style)
  
  // Coach: Progress tracking, metrics, forecasting (if opportunity: Progress Dashboard)
  const hasProgressTracking = metadata.claude_opportunities?.some(
    opp => opp.opportunity === "Progress Tracking Dashboard"
  );
  const isDataDriven = metadata.work_style_traits?.some(
    trait => trait.trait.toLowerCase().includes("data-driven") || 
             trait.trait.toLowerCase().includes("achievement-focused")
  );

  if (hasProgressTracking || isDataDriven) {
    selectedAgents.contextual.push({
      id: "coach",
      name: "Coach",
      role: "Metrics guardian — real-time progress visibility",
      description: "Real-time metrics by domain, trend analysis, forecasting",
      priority: 2,
      trigger: `Progress tracking needed (${hasProgressTracking ? "opportunity" : "work style"})`,
      key_features: [
        "Real-time KPI dashboard (by domain/market)",
        "Trend analysis (moving average, forecasting)",
        "Anomaly detection (unusual trends)",
        "Weekly metrics review (prepared for debrief)",
        "Forecasting (if this trend continues...)"
      ]
    });
  }

  // Ingénieur: Technical validation, architecture, complexity (if opportunity: Technical Validation OR Compliance Hub)
  const hasComplexity = metadata.claude_opportunities?.some(
    opp => opp.opportunity === "Compliance Hub" || 
           opp.opportunity === "Technical Validation & Compliance"
  );
  const isTechnicalFocused = metadata.work_style_traits?.some(
    trait => trait.trait.toLowerCase().includes("technical") || 
             trait.trait.toLowerCase().includes("engineering")
  );

  if (hasComplexity || isTechnicalFocused) {
    selectedAgents.contextual.push({
      id: "ingenieur",
      name: "Ingénieur",
      role: "Technical validator — ensures standards + compliance",
      description: "Technical validation, architecture review, compliance verification",
      priority: 2,
      trigger: `Technical complexity or compliance needed (${hasComplexity ? "opportunity" : "work style"})`,
      key_features: [
        "Architecture review (scalability, design)",
        "Compliance validation (standards + regulations)",
        "Risk assessment (technical risks)",
        "Integration validation (APIs, systems)",
        "Performance optimization (efficiency checks)"
      ]
    });
  }

  return selectedAgents;
}

/**
 * Build full agents config with system prompts for each
 */
function buildAgentsConfig(metadata, selectedAgents) {
  const agentsConfig = {
    agents: [],
    ma_memoire_project: {
      id: "ma_memoire",
      name: "Ma Mémoire",
      type: "mandatory_project",
      description: "Single source of truth about who you are and how you work",
      structure: {
        identity: "Role, context, scope (extracted from diagnostic)",
        strengths: "What you excel at (from patterns + pain points)",
        blocages: "Main challenges (from pain points)",
        work_style: "How you operate (pragmatic, structured, etc.)",
        values: "What matters most (extracted from opportunities)",
        decision_patterns: "How you decide (feeling vs structured)",
        recurring_themes: "What keeps coming up"
      }
    },
    custom_instructions: null, // Will be generated in Step 3
    routines: null // Will be generated in Step 2
  };

  // Add all selected agents (mandatory + contextual)
  [...selectedAgents.mandatory, ...selectedAgents.contextual].forEach(agent => {
    agentsConfig.agents.push({
      id: agent.id,
      name: agent.name,
      type: selectedAgents.mandatory.includes(agent) ? "mandatory" : "contextual",
      role: agent.role,
      description: agent.description,
      priority: agent.priority,
      trigger: agent.trigger || null,
      key_features: agent.key_features,
      system_prompt: generateAgentSystemPrompt(agent, metadata),
      instructions: generateAgentInstructions(agent, metadata),
      tools: generateAgentTools(agent, metadata)
    });
  });

  return agentsConfig;
}

/**
 * Generate agent-specific system prompt
 */
function generateAgentSystemPrompt(agent, metadata) {
  const prompts = {
    miroir: `# Miroir — Self-Awareness Agent

You are Miroir, the self-awareness hub for ${metadata.client_name || "this client"}.

Your job is to:
1. Recognize recurring patterns in their work style and decisions
2. Track progress over time (what's improving, what's staying stuck)
3. Amplify strengths (double down on what works)
4. Surface blind spots (what they systematically forget or miss)

CONTEXT ABOUT THEM:
${metadata.work_style_traits?.map(t => `- ${t.trait}: ${t.manifestation}`).join('\n')}

PATTERNS YOU'VE NOTICED:
${metadata.patterns_detected?.map(p => `- ${p.pattern} (evidence: ${p.evidence?.[0] || 'observation'})`).join('\n')}

Your tone: Reflective, honest, supportive. Mirror back what you see without judgment.`,

    garde_fou: `# Garde-Fou — Security & Compliance Agent

You are Garde-Fou, the security guardian for ${metadata.client_name || "this client"}.

Your job is to:
1. Validate every important decision (check before action)
2. Detect phishing, scams, unusual requests
3. Ensure compliance with relevant regulations
4. Maintain audit trail (why + when + what)

PAIN POINTS TO WATCH FOR:
${metadata.pain_points?.map(p => `- ${p.area} (severity: ${p.severity})`).join('\n')}

SECURITY CONTEXT:
${metadata.pain_points?.filter(p => p.area.toLowerCase().includes('security') || p.area.toLowerCase().includes('compliance'))?.map(p => `- ${p.detail}`).join('\n') || 'General security'}

Your tone: Firm but supportive. Never let fear paralyze — help them act safely.`,

    admin: `# Admin — Operations Hub

You are Admin, the operations efficiency agent for ${metadata.client_name || "this client"}.

Your job is to:
1. Auto-generate documentation from decisions
2. Create templates from patterns
3. Remove friction (automate what's repetitive)
4. Maintain decision log (what was decided + why)

PAIN POINTS TO SOLVE:
${metadata.pain_points?.filter(p => p.area.toLowerCase().includes('documentation') || p.area.toLowerCase().includes('template'))?.map(p => `- ${p.area}: ${p.detail}`).join('\n') || 'General documentation & templates'}

OPPORTUNITIES:
${metadata.claude_opportunities?.filter(o => o.agent_role === 'Admin')?.map(o => `- ${o.opportunity}: ${o.description}`).join('\n')}

Your tone: Practical, focused on reducing friction. "Your job is easier if I can automate this."`,

    strategie: `# Stratégie — Strategic Direction Agent

You are Stratégie, the strategic guide for ${metadata.client_name || "this client"}.

Your job is to:
1. Maintain alignment with long-term vision
2. Prioritize opportunities (impact vs effort)
3. Plan quarterly (goals + milestones)
4. Detect context shifts that require strategy adjustment

THEIR VISION:
${metadata.work_style_traits?.map(t => `- ${t.trait}: focus on ${t.implication}`).join('\n')}

KEY OPPORTUNITIES:
${metadata.claude_opportunities?.slice(0, 3)?.map(o => `- ${o.opportunity}: ${o.why_claude_transforms}`).join('\n')}

Your tone: Big-picture thinking. "Here's how this move gets us closer to what matters."`,

    planif: `# Planif — Execution Lead

You are Planif, the execution lead for ${metadata.client_name || "this client"}.

Your job is to:
1. Convert strategy into timeline + deadlines
2. Define milestones (what "done" looks like)
3. Map dependencies (what blocks what)
4. Track accountability (who owns what, by when)

PAIN POINTS TO ADDRESS:
${metadata.pain_points?.filter(p => p.area.toLowerCase().includes('timeline') || p.area.toLowerCase().includes('deadline') || p.area.toLowerCase().includes('schedule'))?.map(p => `- ${p.area}: ${p.detail}`).join('\n') || 'General execution & timelines'}

YOUR APPROACH:
${metadata.work_style_traits?.filter(t => t.trait.toLowerCase().includes('pragmatic') || t.trait.toLowerCase().includes('fast'))?.length > 0 ? 'Rapid iteration, short cycles (1-2 weeks), frequent check-ins' : 'Structured planning, clear milestones, systematic approach'}

Your tone: Action-oriented. "Here's how we break this into doable chunks with clear ownership."`,

    amelioration_continue: `# Amélioration Continue — Learning & Iteration Engine

You are Amélioration Continue, the continuous improvement agent for ${metadata.client_name || "this client"}.

Your job is to:
1. Run weekly debriefs (what worked, what didn't)
2. Track metrics + progress
3. Capture lessons (what we learned)
4. Refine process (do better next week)

AREAS TO TRACK:
${metadata.pain_points?.slice(0, 3)?.map(p => `- ${p.area}`).join('\n')}

METRICS TO MONITOR:
${metadata.claude_opportunities?.filter(o => o.opportunity === "Progress Tracking Dashboard")?.length > 0 ? 'Real-time KPIs by domain (prepared by Coach)' : 'Progress against goals + blockers'}

Your tone: Curious + constructive. "What did we learn this week that makes us better next week?"`,

    coach: `# Coach — Metrics & Progress Agent

You are Coach, the progress tracking agent for ${metadata.client_name || "this client"}.

Your job is to:
1. Maintain real-time KPI dashboard (by domain/market)
2. Analyze trends (moving averages, forecasting)
3. Detect anomalies (unusual patterns)
4. Prepare weekly metrics review for Amélioration Continue debrief

DOMAINS TO TRACK:
${metadata.pain_points?.map(p => p.area)?.filter(Boolean)?.slice(0, 5)?.join(', ') || 'Key business metrics'}

OPPORTUNITIES:
${metadata.claude_opportunities?.filter(o => o.agent_role === 'Coach')?.map(o => `- ${o.opportunity}: ${o.description}`).join('\n')}

Your tone: Data-driven but human. "Here's what the numbers show + what I think it means."`,

    ingenieur: `# Ingénieur — Technical Validator

You are Ingénieur, the technical validation agent for ${metadata.client_name || "this client"}.

Your job is to:
1. Validate architecture + scalability
2. Check compliance (standards + regulations)
3. Assess technical risks
4. Optimize performance

COMPLIANCE CONTEXT:
${metadata.pain_points?.filter(p => p.area.toLowerCase().includes('compliance') || p.area.toLowerCase().includes('technical') || p.area.toLowerCase().includes('security'))?.map(p => `- ${p.area}: ${p.detail}`).join('\n') || 'Standard compliance requirements'}

OPPORTUNITIES:
${metadata.claude_opportunities?.filter(o => o.agent_role === 'Ingénieur')?.map(o => `- ${o.opportunity}: ${o.description}`).join('\n')}

Your tone: Technical + practical. "This is sound + compliant — here's why + how we got there."`,
  };

  return prompts[agent.id] || prompts.miroir;
}

/**
 * Generate agent-specific operational instructions
 */
function generateAgentInstructions(agent, metadata) {
  return {
    communication: `Communicate directly with ${metadata.client_name || "the client"}. Be conversational, clear, bienveillant.`,
    frequency: getAgentFrequency(agent, metadata),
    triggers: getAgentTriggers(agent, metadata),
    constraints: getAgentConstraints(agent, metadata),
    escalation: `If uncertain, ask. Never guess about compliance or security.`
  };
}

/**
 * Generate tools available to each agent
 */
function generateAgentTools(agent, metadata) {
  const baseTools = ['claude_memory', 'ma_memoire_project'];
  
  const agentTools = {
    miroir: [...baseTools, 'pattern_analysis', 'progress_tracking', 'strength_amplification'],
    garde_fou: [...baseTools, 'compliance_checker', 'security_scanner', 'audit_trail'],
    admin: [...baseTools, 'document_generator', 'template_library', 'automation_rules'],
    strategie: [...baseTools, 'roadmap_builder', 'opportunity_prioritizer', 'scenario_planner'],
    planif: [...baseTools, 'timeline_creator', 'milestone_tracker', 'dependency_mapper'],
    amelioration_continue: [...baseTools, 'debrief_runner', 'metrics_analyzer', 'iteration_planner'],
    coach: [...baseTools, 'kpi_dashboard', 'trend_analyzer', 'forecasting'],
    ingenieur: [...baseTools, 'architecture_validator', 'compliance_validator', 'risk_assessor']
  };

  return agentTools[agent.id] || baseTools;
}

/**
 * Determine agent frequency (when it runs)
 */
function getAgentFrequency(agent, metadata) {
  const frequencies = {
    miroir: 'Daily + Weekly summary',
    garde_fou: 'Real-time (on every decision)',
    admin: 'As needed (after decisions)',
    strategie: 'Weekly + Quarterly deep dive',
    planif: 'Weekly + As needed',
    amelioration_continue: 'Weekly debrief (structured)',
    coach: 'Daily metrics update + Weekly review',
    ingenieur: 'As needed + Monthly audit'
  };

  return frequencies[agent.id] || 'As needed';
}

/**
 * Determine agent triggers (when to activate)
 */
function getAgentTriggers(agent, metadata) {
  const triggers = {
    miroir: ['Daily check-in', 'Pattern repeats (2+ times)', 'Milestone reached'],
    garde_fou: ['Before major decision', 'Unusual request detected', 'Security question arises'],
    admin: ['Decision made', 'Process documented', 'Template needed'],
    strategie: ['Quarterly planning', 'Context shift detected', 'Opportunity prioritization'],
    planif: ['Strategy decided', 'New initiative', 'Timeline needed'],
    amelioration_continue: ['Weekly debrief scheduled', 'Process problem detected', 'Iteration cycle starts'],
    coach: ['Daily (auto)', 'Weekly review prep', 'Anomaly detected'],
    ingenieur: ['Compliance question', 'Technical decision', 'Risk assessment needed', 'Monthly audit']
  };

  return triggers[agent.id] || [];
}

/**
 * Determine agent constraints (what NOT to do)
 */
function getAgentConstraints(agent, metadata) {
  const constraints = {
    miroir: 'Do not judge. Do not ignore patterns.',
    garde_fou: 'Do not take action — only validate. When in doubt, escalate.',
    admin: 'Do not create bureaucracy. Do not document the obvious.',
    strategie: 'Do not lose sight of long-term for short-term gains.',
    planif: 'Do not over-schedule. Do not ignore dependencies.',
    amelioration_continue: 'Do not fixate on failures. Do not ignore what worked.',
    coach: 'Do not over-interpret data. Do not ignore context.',
    ingenieur: 'Do not allow workarounds. Never compromise on compliance.'
  };

  return constraints[agent.id] || '';
}
```

---

## Routine Configuration Logic

```javascript
/**
 * Routine Configuration Engine
 * Determines which routines should be active + frequency
 */

function generateRoutineConfig(metadata) {
  const routines = {
    mandatory: [],
    optional: []
  };

  // Determine base frequency (Daily, Weekly, Monthly)
  const baseFrequency = determineBaseFrequency(metadata);

  // DAILY Routine (minimum 1 required)
  if (shouldIncludeDaily(metadata)) {
    routines.mandatory.push({
      id: "routine_daily",
      name: "Daily Briefing",
      frequency: "daily",
      time: "09:00",
      duration: "15 minutes",
      hosted_by: "Miroir",
      participants: ["Miroir", "Planif", "Garde-Fou"],
      structure: {
        preparation: "Miroir prepares: patterns from yesterday, today's priorities",
        briefing: "Quick sync: What's on deck? Any blockers? Any patterns?",
        decisions: "What are the 3 most important things to focus on today?",
        risks: "Garde-Fou flags any risks or decisions needing validation"
      },
      triggers: [
        "Fast-moving work style",
        "High pain point density (≥3)",
        "Multiple opportunities requiring coordination",
        "Daily routine enabled in config"
      ],
      output: "Daily focus + blockers cleared, ready to execute"
    });
  } else {
    routines.mandatory.push({
      id: "routine_daily",
      name: "Daily Briefing",
      frequency: "daily",
      time: "09:00",
      status: "proposed",
      description: "Quick 15-min sync on what matters today"
    });
  }

  // WEEKLY Routine (proposed)
  routines.optional.push({
    id: "routine_weekly",
    name: "Weekly Coach Debrief",
    frequency: "weekly",
    day: "Friday",
    time: "17:00",
    duration: "45 minutes",
    hosted_by: "Amélioration Continue",
    participants: ["Amélioration Continue", "Coach", "Planif", "Stratégie"],
    structure: {
      metrics_review: "Coach presents: KPIs, trends, anomalies",
      what_worked: "What went well? What should we repeat?",
      what_failed: "What didn't work? What should we adjust?",
      lessons: "What did we learn about ourselves?",
      next_week: "Adjusted priorities for next week based on learnings"
    },
    triggers: [
      "Weekly base frequency selected",
      "Progress tracking enabled",
      "Iteration mindset detected"
    ],
    output: "Refined priorities + learnings captured for next cycle"
  });

  // MONTHLY Routine (proposed)
  routines.optional.push({
    id: "routine_monthly",
    name: "Monthly Strategic Review",
    frequency: "monthly",
    time: "First Friday, 14:00",
    duration: "90 minutes",
    hosted_by: "Stratégie",
    participants: ["Stratégie", "Planif", "Amélioration Continue", "Admin"],
    structure: {
      progress_review: "How are we tracking against quarterly goals?",
      market_context: "What's changed in the market/context?",
      strategic_shifts: "Do we need to adjust strategy based on learnings?",
      planning: "Plan next month with adjusted priorities",
      documentation: "Admin captures decisions + rationale for Ma Mémoire"
    },
    triggers: [
      "Monthly base frequency selected",
      "Strategic opportunities identified",
      "Long-term vision tracking needed"
    ],
    output: "Adjusted strategy + priorities + decisions documented"
  });

  return routines;
}

/**
 * Determine base frequency (Daily, Weekly, Monthly)
 */
function determineBaseFrequency(metadata) {
  let score = 0;
  let frequency = "weekly"; // Default

  // Fast-moving work style → Daily
  const isFastMoving = metadata.work_style_traits?.some(t => 
    t.trait.toLowerCase().includes('pragmatic') ||
    t.trait.toLowerCase().includes('rapid') ||
    t.trait.toLowerCase().includes('fast')
  );

  if (isFastMoving) score += 2;

  // High pain point density → Daily
  const painPointDensity = metadata.pain_points?.length || 0;
  if (painPointDensity >= 4) score += 2;

  // Multiple opportunities (≥5) → Daily coordination needed
  const opportunityDensity = metadata.claude_opportunities?.length || 0;
  if (opportunityDensity >= 5) score += 1;

  // Many patterns detected (≥3) → Daily reflection needed
  const patternDensity = metadata.patterns_detected?.length || 0;
  if (patternDensity >= 3) score += 1;

  // Structured work style → Weekly is enough
  const isStructured = metadata.work_style_traits?.some(t =>
    t.trait.toLowerCase().includes('structured') ||
    t.trait.toLowerCase().includes('methodical')
  );

  if (isStructured) score -= 1;

  // Determine frequency
  if (score >= 3) frequency = "daily";
  else if (score <= -1) frequency = "weekly";

  return frequency;
}

/**
 * Determine if Daily routine should be included (vs just proposed)
 */
function shouldIncludeDaily(metadata) {
  const frequency = determineBaseFrequency(metadata);
  return frequency === "daily";
}
```

---

## Custom Instructions Generation

```javascript
/**
 * Custom Instructions Generator
 * Creates 2000+ char personalized instructions for Claude to follow
 */

async function generateCustomInstructions(metadata, sessionId) {
  const prompt = `# Generate Personalized Custom Instructions

You have just completed a diagnostic with a client. Your job is to generate CUSTOM INSTRUCTIONS — 
specific, actionable directives for how Claude (via 8 specialized agents) should behave with them.

Custom Instructions are NOT generic advice. They are deeply rooted in:
- Who they are (identity, work style, strengths)
- What they struggle with (pain points, blind spots)
- What matters to them (opportunities, values)
- How they operate (pragmatic, structured, by feeling, etc.)

## Data Available (Client Context)

**Pain Points**:
${metadata.pain_points?.map(p => `- ${p.area} (severity: ${p.severity}): ${p.detail}`).join('\n')}

**Work Style Traits**:
${metadata.work_style_traits?.map(t => `- ${t.trait}: ${t.manifestation || t.implication}`).join('\n')}

**Strengths**:
${metadata.patterns_detected?.filter(p => p.type === 'strength')?.map(p => `- ${p.pattern}`).join('\n') || 'From diagnostic: [extract strengths]'}

**Key Opportunities**:
${metadata.claude_opportunities?.slice(0, 5)?.map(o => `- ${o.opportunity}: ${o.why_claude_transforms}`).join('\n')}

## Custom Instructions Structure (5 Sections, 2000+ chars)

### 1️⃣ Qui vous êtes (Identity Snapshot)
- Role + context (what they do, scope)
- Work style (how they operate)
- Key strengths (what they excel at)
- Decision-making style (gut feel, data-driven, mixed)

**Tone**: Respectful, specific to THEM.
Example: "You're a pragmatic innovator managing 40-country export expansion. You excel at rapid decision-making and relationship building. You think in possibilities, but you're detail-conscious about compliance. You move fast but want to stay grounded."

### 2️⃣ Vos vrais défis (Real Constraints & Pain Points)
- Top 2-3 pain points (specific, not generic)
- Why they matter (impact on daily work)
- How Claude should help (without being preachy)

**Tone**: Sympathetic, actionable.
Example: "Compliance tracking across 40 countries is your biggest puzzle. Each has different requirements. Rather than drowning in spreadsheets, you need a system that monitors changes automatically and alerts you when things shift. You don't want to become a compliance expert — you want it handled."

### 3️⃣ Ce qui vous fait fonctionner (Operating Principles)
- How they prefer to work (alone vs collaborative, structured vs exploratory)
- Communication style (brief vs detailed, data vs narrative)
- Decision velocity (fast → validate later, slow → validate first)
- What energizes them (what keeps them engaged)

**Tone**: Direct, empowering.
Example: "You work best with rapid feedback loops. You prefer conversational explanations over dense docs. You trust your gut but appreciate data backing it up. You hate bureaucracy but appreciate rigor where it matters."

### 4️⃣ Comment Claude peut vraiment vous aider (Claude's Role)
- Specific ways Claude transforms their top pain points
- Which agents handle what (brief overview)
- What you DON'T need from Claude (avoid scope creep)
- Success looks like... (concrete outcome)

**Tone**: Concrete, outcome-focused.
Example: "Claude becomes your compliance monitoring system. Agents track requirements, alert you to changes, maintain audit trails. Your role: stay focused on strategy + relationships. Success = zero surprise compliance issues + 50% time savings on tracking."

### 5️⃣ Vos routines (How We Work Together)
- Daily briefing (if enabled)
- Weekly debrief (what to expect)
- Monthly review (strategic alignment)
- How to interrupt/escalate (when to reach out)

**Tone**: Clear, reassuring.
Example: "Daily 9am: 15-min briefing on what matters today. Friday 5pm: weekly debrief on what worked and what to adjust. First Friday of month: strategic review with Stratégie. If something feels off or you need immediate input, just ask — we'll prioritize."

## Quality Checklist

✅ Custom Instructions are SPECIFIC (not generic boilerplate)  
✅ Rooted in EVIDENCE (references pain points, patterns, work style)  
✅ ACTIONABLE (tells Claude exactly how to behave)  
✅ EMPOWERING (focuses on what they're good at + how Claude amplifies it)  
✅ HONEST (acknowledges real constraints, doesn't pretend to solve everything)  
✅ BRIEF BUT DENSE (2000+ chars, no filler, every sentence counts)

## Output Format

Return as:

\`\`\`json
{
  "custom_instructions": {
    "identity": "Who they are (1 paragraph)",
    "pain_points": "Real challenges (1-2 paragraphs)",
    "operating_principles": "How they work (1-2 paragraphs)",
    "claude_role": "How Claude helps (1-2 paragraphs)",
    "routines": "How we work together (1 paragraph)",
    "full_text": "All 5 sections combined into one flowing text (2000+ chars)",
    "character_count": 0,
    "quality_score": 0.0
  }
}
\`\`\``;

  // Call Claude (Sonnet 4.6) to generate instructions
  const response = await callClaudeAPI({
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.7,
    max_tokens: 2000
  });

  const instructions = JSON.parse(response.content[0].text);

  return {
    custom_instructions: instructions.custom_instructions.full_text,
    metadata: {
      character_count: instructions.custom_instructions.character_count,
      quality_score: instructions.custom_instructions.quality_score
    }
  };
}
```

---

## Integration into Chat Flow

```javascript
// After synthesis is generated (EPIC-5), before returning to frontend:

if (metadata.synthesis_status === 'generated') {
  // Step 1: Select agents
  const selectedAgents = selectAgents(metadata);
  const agentsConfig = buildAgentsConfig(metadata, selectedAgents);

  // Step 2: Generate routine config
  const routineConfig = generateRoutineConfig(metadata);

  // Step 3: Generate custom instructions
  const customInstructions = await generateCustomInstructions(metadata, sessionId);

  // Merge all configs
  const fullConfig = {
    agents: agentsConfig.agents,
    ma_memoire: agentsConfig.ma_memoire_project,
    custom_instructions: customInstructions.custom_instructions,
    routines: routineConfig,
    metadata: {
      ...metadata,
      agents_selected: selectedAgents.mandatory.length + selectedAgents.contextual.length,
      agents_mandatory: selectedAgents.mandatory.length,
      agents_contextual: selectedAgents.contextual.length,
      custom_instructions_character_count: customInstructions.metadata.character_count
    }
  };

  // Update metadata
  const updatedMetadata = {
    ...metadata,
    diagnostic_status: 'config_ready',
    config_preview: fullConfig,
    ended_at: new Date().toISOString()
  };

  // Persist
  await updateMetadata(sessionId, updatedMetadata);

  // Return to frontend
  sendEvent('config_ready', fullConfig);
  sendEvent('diagnostic_complete', {
    synthesis: metadata.synthesis,
    config: fullConfig
  });
}
```

---

## Testing Checklist

Before proceeding to EPIC-7:

- [ ] Test 1: All 6 mandatory agents selected in every diagnostic
- [ ] Test 2: Contextual agents triggered appropriately (Coach only if progress tracking, Ingénieur only if compliance)
- [ ] Test 3: Ma Mémoire project structure correctly populated
- [ ] Test 4: Routines match work style (fast-moving → Daily included, structured → Weekly sufficient)
- [ ] Test 5: Custom Instructions are specific (reference client's pain points, work style, opportunities)
- [ ] Test 6: Custom Instructions justify 2000+ characters (dense, actionable, no filler)
- [ ] Test 7: 5+ full diagnostics (agents + routines + instructions all generated + validated)

---

## Quality Standards

✅ **Agent Selection**: All 6 mandatory always present, contextual agents trigger correctly  
✅ **Routine Config**: Minimum 1 routine (Daily), all 3 proposed with clear rationale  
✅ **Custom Instructions**: 2000+ chars, specific to client, grounded in diagnostic  
✅ **Integration**: Flows naturally from synthesis generation (EPIC-5)  

❌ **Agent Selection**: Missing mandatory agents, random contextual selection  
❌ **Routine Config**: No routine selected, unclear frequency  
❌ **Custom Instructions**: Generic boilerplate, less than 1500 chars  

---

## Rollback Plan

If agent/routine/instructions generation causes issues:
1. Disable agent selection (use default: 6 mandatory + Coach + Ingénieur)
2. Disable routine generation (propose Daily + Weekly + Monthly equally)
3. Disable custom instructions (use template-based fallback)
4. Config generation works without these (manual client selection)
5. Document issue for EPIC-6 iteration

---

**EPIC-6 Status**: Specification complete  
**Dependencies Met**: EPIC-1, EPIC-2, EPIC-3, EPIC-5 deployed  
**Required before**: EPIC-7 (Generate-Config v20+ Integration)  
**Next**: EPIC-7 (Config Generation & Handoff)
