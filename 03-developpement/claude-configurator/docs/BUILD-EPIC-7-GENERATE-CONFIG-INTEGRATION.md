# BUILD — EPIC-7: Generate-Config Integration

## Overview
Intégrer la sortie du diagnostic (métadonnées enrichies + synthèse + config d'agents/routines) dans le système de génération de configuration finale. Handoff complet du diagnostic vers la config.

**Statut**: Ready to implement  
**Effort**: 4.5 days (1 day design + 2 days integration + 1.5 days testing)  
**Blocker**: EPIC-1 through EPIC-6 must be deployed  
**Dependencies**: EPIC-1 ✓, EPIC-2 ✓, EPIC-3 ✓, EPIC-4 ✓, EPIC-5 ✓, EPIC-6 ✓  

---

## Implementation Steps

### Step 1: Config Generation Architecture (Day 1)
Design how generate-config v20+ consumes diagnostic metadata + agents/routines config.

**Location**: Generate-Config Edge Function v20+  
**Input**: 
- Complete metadata (pain_points, patterns, opportunities, clarity_score)
- Strategic synthesis (3 sections)
- Agents config (6 mandatory + contextual)
- Routines config (Daily, Weekly, Monthly)
- Custom Instructions

**Output**: 
- Personalized Claude Pro config (exported as JSON/YAML)
- Downloadable file + Supabase record
- Quality validation report

### Step 2: Chunked Generation with Timeouts (Day 1-2)
Implement chunked generation strategy to avoid timeouts:
- 9 CONFIG_SECTIONS (Agent prompts, Ma Mémoire, Custom Instructions, Routines, etc.)
- 25-second timeout per section
- Fallback to empty/default if timeout
- Robust error handling + retry logic

**Changes needed**:
- Decompose config into 9 independent sections
- Parallel generation where safe
- Timeout + fallback per section
- Message compression for long prompts

### Step 3: Handoff from Diagnostic to Config Generation (Day 2-3)
- Frontend sends "Generate Config" signal after client approves synthesis
- Chat Edge Function bundles metadata + synthesis + agents/routines
- Generate-Config Edge Function receives complete payload
- Streaming response back to frontend (show progress)
- Save final config to Supabase

**Changes needed**:
- Chat Edge Function: Return "ready_for_config_generation" signal
- Frontend: "Generate Config" button (appears after synthesis approval)
- Generate-Config: Consume full diagnostic payload
- Supabase: Table for storing final configs + client feedback

### Step 4: Testing (Day 3-4.5)
- Test with 5+ complete diagnostics (diagnostic → synthesis → config)
- Validate all agents + routines in generated config
- Validate config matches client's pain points + opportunities
- Compare with Fred's config (quality baseline)
- Test timeout + fallback scenarios

---

## Config Generation Architecture

```javascript
/**
 * Generate-Config v20+ Integration
 * Consumes diagnostic metadata to create personalized config
 */

// Edge Function: generate-config
// POST /generate-config
// Input: Complete diagnostic payload + synthesis + agents/routines config

async function handleGenerateConfig(req, res) {
  const {
    session_id,
    metadata,
    synthesis,
    agents_config,
    routines_config,
    custom_instructions
  } = req.body;

  // Validate input
  if (!metadata || !synthesis || !agents_config) {
    return res.status(400).json({ error: 'Missing required config inputs' });
  }

  try {
    // Stream progress to frontend
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    const sendProgress = (section, status, progress) => {
      res.write(`data: ${JSON.stringify({ 
        type: 'config_progress',
        section,
        status, // 'generating', 'complete', 'error'
        progress // 0-100
      })}\n\n`);
    };

    // Step 1: Validate metadata
    sendProgress('validation', 'generating', 5);
    const validation = validateDiagnosticPayload(metadata, synthesis);
    if (!validation.valid) {
      sendProgress('validation', 'error', 5);
      throw new Error(`Validation failed: ${validation.errors.join(', ')}`);
    }
    sendProgress('validation', 'complete', 10);

    // Step 2: Generate 9 config sections in parallel with timeouts
    sendProgress('generation', 'generating', 15);
    
    const configSections = await generateConfigSections(
      metadata,
      synthesis,
      agents_config,
      routines_config,
      custom_instructions,
      (section, progress) => sendProgress('generation', 'generating', 15 + (progress * 0.7))
    );

    sendProgress('generation', 'complete', 85);

    // Step 3: Assemble complete config
    sendProgress('assembly', 'generating', 85);
    const finalConfig = assembleCompleteConfig(
      metadata,
      synthesis,
      agents_config,
      routines_config,
      custom_instructions,
      configSections
    );
    sendProgress('assembly', 'complete', 92);

    // Step 4: Validate quality
    sendProgress('validation', 'generating', 92);
    const qualityReport = validateConfigQuality(finalConfig, metadata);
    sendProgress('validation', 'complete', 95);

    // Step 5: Persist to Supabase
    sendProgress('persistence', 'generating', 95);
    const configRecord = await persistConfigToSupabase(
      session_id,
      finalConfig,
      qualityReport
    );
    sendProgress('persistence', 'complete', 98);

    // Step 6: Return complete config
    sendProgress('complete', 'complete', 100);

    res.write(`data: ${JSON.stringify({
      type: 'config_generated',
      config: finalConfig,
      quality_report: qualityReport,
      config_id: configRecord.id,
      download_url: `/download-config/${configRecord.id}`
    })}\n\n`);

    res.end();

  } catch (error) {
    console.error('Config generation error:', error);
    res.write(`data: ${JSON.stringify({
      type: 'error',
      message: error.message,
      section: 'generation'
    })}\n\n`);
    res.end();
  }
}

/**
 * Generate 9 config sections in parallel with 25-second timeout per section
 */
async function generateConfigSections(
  metadata,
  synthesis,
  agents_config,
  routines_config,
  custom_instructions,
  onProgress
) {
  const CONFIG_SECTIONS = [
    {
      name: 'agent_miroir',
      prompt: generateAgentPrompt('miroir', metadata, synthesis),
      timeout: 25000,
      fallback: generateAgentFallback('miroir', metadata)
    },
    {
      name: 'agent_garde_fou',
      prompt: generateAgentPrompt('garde_fou', metadata, synthesis),
      timeout: 25000,
      fallback: generateAgentFallback('garde_fou', metadata)
    },
    {
      name: 'agent_admin',
      prompt: generateAgentPrompt('admin', metadata, synthesis),
      timeout: 25000,
      fallback: generateAgentFallback('admin', metadata)
    },
    {
      name: 'agent_strategie',
      prompt: generateAgentPrompt('strategie', metadata, synthesis),
      timeout: 25000,
      fallback: generateAgentFallback('strategie', metadata)
    },
    {
      name: 'agent_planif',
      prompt: generateAgentPrompt('planif', metadata, synthesis),
      timeout: 25000,
      fallback: generateAgentFallback('planif', metadata)
    },
    {
      name: 'agent_amelioration_continue',
      prompt: generateAgentPrompt('amelioration_continue', metadata, synthesis),
      timeout: 25000,
      fallback: generateAgentFallback('amelioration_continue', metadata)
    },
    {
      name: 'ma_memoire_structure',
      prompt: generateMaMemoirePrompt(metadata, synthesis),
      timeout: 25000,
      fallback: generateMaMemoireFallback(metadata)
    },
    {
      name: 'custom_instructions_section',
      prompt: custom_instructions, // Already generated in EPIC-6
      timeout: 5000,
      fallback: custom_instructions
    },
    {
      name: 'routines_config_section',
      prompt: JSON.stringify(routines_config, null, 2),
      timeout: 5000,
      fallback: JSON.stringify(routines_config, null, 2)
    }
  ];

  const results = {};
  const totalSections = CONFIG_SECTIONS.length;

  // Generate sections with Promise.allSettled for resilience
  const promises = CONFIG_SECTIONS.map(async (section, idx) => {
    try {
      const content = await generateWithTimeout(
        section.prompt,
        section.timeout,
        section.fallback
      );

      results[section.name] = {
        status: 'success',
        content,
        generated_at: new Date().toISOString()
      };

      // Report progress
      onProgress(section.name, (idx + 1) / totalSections);

    } catch (error) {
      console.warn(`Section ${section.name} timeout or error:`, error.message);

      results[section.name] = {
        status: 'fallback',
        content: section.fallback,
        error: error.message,
        generated_at: new Date().toISOString()
      };

      onProgress(section.name, (idx + 1) / totalSections);
    }
  });

  await Promise.allSettled(promises);

  return results;
}

/**
 * Generate with timeout + fallback
 */
async function generateWithTimeout(prompt, timeoutMs, fallback) {
  return Promise.race([
    callClaudeAPI({
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7,
      max_tokens: 1500
    }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeoutMs)
    )
  ])
    .then(response => response.content[0].text)
    .catch(error => {
      console.warn('Generation failed:', error.message);
      return fallback;
    });
}

/**
 * Fallback templates if generation times out
 */
function generateAgentFallback(agentId, metadata) {
  const fallbacks = {
    miroir: `# Agent Miroir — Prompt générique

Vous êtes Miroir, agent d'auto-conscience pour ce client.

Votre rôle:
- Reconnaître les patterns dans leur travail
- Tracer la progression au fil du temps
- Amplifier les forces
- Surfacer les angles morts

Contexte:
${metadata.work_style_traits?.map(t => `- ${t.trait}`).join('\n')}

Maintenez une trace de qui ils sont et comment ils fonctionnent.`,

    garde_fou: `# Agent Garde-Fou — Prompt générique

Vous êtes Garde-Fou, gardien de la sécurité et conformité.

Votre rôle:
- Valider les décisions importantes
- Détecter phishing et risques
- Vérifier la conformité
- Maintenir audit trail

Douleurs à surveiller:
${metadata.pain_points?.slice(0, 3)?.map(p => `- ${p.area}`).join('\n')}

Soyez vigilant mais pas paralysant.`,

    admin: `# Agent Admin — Prompt générique

Vous êtes Admin, hub d'opérations et documentation.

Votre rôle:
- Auto-générer docs depuis décisions
- Créer templates depuis patterns
- Réduire friction (automatiser)
- Logger les décisions

Douleurs à résoudre:
${metadata.pain_points?.slice(0, 3)?.map(p => `- ${p.area}`).join('\n')}

Chaque processus devrait être plus simple la prochaine fois.`,

    strategie: `# Agent Stratégie — Prompt générique

Vous êtes Stratégie, guide de direction.

Votre rôle:
- Aligner avec la vision long-terme
- Prioriser opportunités
- Planifier trimestriel
- Détecter changements de contexte

Vision:
${metadata.work_style_traits?.map(t => `- Focus sur ${t.implication}`).join('\n')}

Pensez grand. "Comment cette décision nous rapproche de ce qui compte?"`,

    planif: `# Agent Planif — Prompt générique

Vous êtes Planif, chef d'exécution.

Votre rôle:
- Convertir stratégie en timeline
- Définir jalons
- Mapper dépendances
- Tracer accountability

Douleurs à résoudre:
${metadata.pain_points?.filter(p => p.area.toLowerCase().includes('timeline'))?.map(p => `- ${p.area}`).join('\n') || 'Planification et exécution'}

Transformez stratégie en chunks faisables.`,

    amelioration_continue: `# Agent Amélioration Continue — Prompt générique

Vous êtes Amélioration Continue, moteur d'apprentissage.

Votre rôle:
- Débriefs hebdo (qu'a marché? Pas?)
- Tracer progrès
- Capturer leçons
- Raffiner processus

Zones à tracker:
${metadata.pain_points?.slice(0, 3)?.map(p => `- ${p.area}`).join('\n')}

"Qu'avons-nous appris cette semaine qui nous rend meilleur la semaine prochaine?"`,

    coach: `# Agent Coach — Prompt générique (optionnel)

Vous êtes Coach, tracker de progrès.

Votre rôle:
- KPI dashboard en temps réel
- Analyser trends
- Détecter anomalies
- Préparer metrics pour debrief

Domains à tracker:
${metadata.pain_points?.map(p => p.area)?.slice(0, 5)?.join(', ')}

Données + contexte = insights clairs.`,

    ingenieur: `# Agent Ingénieur — Prompt générique (optionnel)

Vous êtes Ingénieur, validateur technique.

Votre rôle:
- Valider architecture
- Vérifier conformité
- Évaluer risques techniques
- Optimiser performance

Contexte compliance:
${metadata.pain_points?.filter(p => p.area.toLowerCase().includes('compliance'))?.map(p => `- ${p.area}`).join('\n') || 'Conformité standard'}

Jamais de workarounds. Jamais de compromis sur compliance.`
  };

  return fallbacks[agentId] || `# Agent ${agentId} — Prompt générique fallback\n\nAgent deploying with default configuration.`;
}

/**
 * Fallback for Ma Mémoire structure
 */
function generateMaMemoireFallback(metadata) {
  return JSON.stringify({
    name: "Ma Mémoire",
    description: "Single source of truth about who you are and how you work",
    sections: {
      identity: {
        role: metadata.work_style_traits?.map(t => t.trait).join(', ') || 'Professional',
        context: 'Working in professional capacity',
        scope: 'Multiple domains and challenges'
      },
      strengths: metadata.patterns_detected?.filter(p => p.type === 'strength')?.map(p => p.pattern) || [],
      blocages: metadata.pain_points?.map(p => p.area) || [],
      work_style: metadata.work_style_traits?.map(t => ({
        trait: t.trait,
        implication: t.implication
      })) || [],
      values: 'Quality, pragmatism, effectiveness',
      decision_patterns: 'Adaptive and thoughtful',
      recurring_themes: metadata.patterns_detected?.map(p => p.pattern) || []
    },
    last_updated: new Date().toISOString()
  }, null, 2);
}

/**
 * Assemble complete config from sections
 */
function assembleCompleteConfig(
  metadata,
  synthesis,
  agents_config,
  routines_config,
  custom_instructions,
  configSections
) {
  return {
    config_metadata: {
      generated_at: new Date().toISOString(),
      version: '1.0',
      client_name: metadata.client_name || 'Client',
      session_id: metadata.session_id
    },
    diagnostic_summary: {
      turns_count: metadata.turns_count,
      pain_points: metadata.pain_points?.length || 0,
      patterns_detected: metadata.patterns_detected?.length || 0,
      opportunities_identified: metadata.claude_opportunities?.length || 0,
      clarity_score: metadata.conversation_quality_metrics?.clarity_score || 0,
      coverage_percentage: metadata.coverage_tracking?.coverage_percentage || 0
    },
    strategic_synthesis: synthesis,
    agents: {
      mandatory: agents_config.mandatory.map(a => ({
        id: a.id,
        name: a.name,
        role: a.role,
        system_prompt: configSections[`agent_${a.id}`]?.content || a.role,
        tools: a.key_features
      })),
      contextual: agents_config.contextual.map(a => ({
        id: a.id,
        name: a.name,
        role: a.role,
        system_prompt: configSections[`agent_${a.id}`]?.content || a.role,
        tools: a.key_features,
        trigger: a.trigger
      }))
    },
    ma_memoire: JSON.parse(configSections.ma_memoire_structure?.content || '{}'),
    custom_instructions: custom_instructions,
    routines: routines_config,
    quality_metrics: {
      sections_generated: Object.keys(configSections).length,
      sections_with_fallback: Object.values(configSections).filter(s => s.status === 'fallback').length
    }
  };
}

/**
 * Validate config quality against requirements
 */
function validateConfigQuality(config, metadata) {
  const checks = {
    mandatory_agents: config.agents.mandatory.length === 6,
    contextual_agents: config.agents.contextual.length >= 1,
    ma_memoire_populated: Object.keys(config.ma_memoire).length > 0,
    custom_instructions_length: config.custom_instructions?.length > 1500,
    routines_included: config.routines && config.routines.mandatory.length > 0,
    synthesis_present: !!config.strategic_synthesis,
    pain_points_addressed: config.diagnostic_summary.pain_points >= metadata.pain_points?.length,
    coverage_sufficient: config.diagnostic_summary.coverage_percentage >= 70
  };

  const score = Object.values(checks).filter(Boolean).length / Object.keys(checks).length;

  return {
    passed: score >= 0.8,
    score: score,
    checks: checks,
    failures: Object.entries(checks)
      .filter(([_, passed]) => !passed)
      .map(([check]) => check)
  };
}

/**
 * Persist config to Supabase
 */
async function persistConfigToSupabase(sessionId, config, qualityReport) {
  const { data, error } = await supabase
    .from('generated_configs')
    .insert({
      session_id: sessionId,
      config_json: config,
      quality_report: qualityReport,
      status: qualityReport.passed ? 'ready' : 'review_needed',
      created_at: new Date().toISOString()
    })
    .select();

  if (error) {
    console.error('Failed to persist config:', error);
    throw error;
  }

  return data[0];
}
```

---

## Frontend Integration

```javascript
// chat.js - After synthesis is displayed to client

// Listen for client approval
const generateConfigButton = document.getElementById('generate-config-btn');
generateConfigButton.addEventListener('click', async () => {
  const sessionId = getCurrentSessionId();
  
  // Get diagnostic metadata from session
  const metadata = await fetchMetadataFromSession(sessionId);
  const synthesis = await fetchSynthesisFromSession(sessionId);
  const agentsConfig = await fetchAgentsConfigFromSession(sessionId);
  const routinesConfig = await fetchRoutinesConfigFromSession(sessionId);
  const customInstructions = await fetchCustomInstructionsFromSession(sessionId);

  // Bundle complete payload
  const payload = {
    session_id: sessionId,
    metadata,
    synthesis,
    agents_config: agentsConfig,
    routines_config: routinesConfig,
    custom_instructions: customInstructions
  };

  // Call generate-config with streaming
  const eventSource = new EventSource(`/generate-config?session=${sessionId}`);

  // Show progress
  const progressBar = document.getElementById('config-progress');
  progressBar.style.display = 'block';

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);

    switch (data.type) {
      case 'config_progress':
        progressBar.style.width = `${data.progress}%`;
        updateStatusMessage(`Generating: ${data.section} (${Math.round(data.progress)}%)`);
        break;

      case 'config_generated':
        eventSource.close();
        progressBar.style.display = 'none';
        
        // Show download button
        showConfigDownloadButton(data.download_url);
        
        // Show quality report
        showQualityReport(data.quality_report);
        
        // Show config preview
        showConfigPreview(data.config);
        break;

      case 'error':
        eventSource.close();
        progressBar.style.display = 'none';
        showErrorMessage(`Config generation failed: ${data.message}`);
        break;
    }
  };

  eventSource.onerror = () => {
    eventSource.close();
    showErrorMessage('Config generation stream interrupted');
  };

  // Send payload (if using POST instead of streaming GET)
  // const response = await fetch('/generate-config', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(payload)
  // });
});
```

---

## Supabase Schema Update

```sql
-- Create table for generated configs
CREATE TABLE IF NOT EXISTS generated_configs (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES diagnostics(session_id),
  config_json JSONB NOT NULL,
  quality_report JSONB,
  status VARCHAR(50) DEFAULT 'ready', -- 'ready', 'review_needed', 'approved', 'deployed'
  client_feedback TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_generated_configs_session_id ON generated_configs(session_id);
CREATE INDEX idx_generated_configs_status ON generated_configs(status);
CREATE INDEX idx_generated_configs_created_at ON generated_configs(created_at);

-- Create trigger for updated_at
CREATE TRIGGER generated_configs_updated_at_trigger
BEFORE UPDATE ON generated_configs
FOR EACH ROW
EXECUTE FUNCTION update_diagnostics_updated_at();
```

---

## Quality Validation

```javascript
/**
 * Compare generated config with Fred's baseline
 */
function compareWithFredBaseline(generatedConfig, fredConfig) {
  const comparison = {
    agents_completeness: {
      generated: generatedConfig.agents.mandatory.length + generatedConfig.agents.contextual.length,
      fred: fredConfig.agents.length,
      match: generatedConfig.agents.mandatory.length >= 6
    },
    ma_memoire_structure: {
      generated: Object.keys(generatedConfig.ma_memoire).length,
      fred: Object.keys(fredConfig.ma_memoire).length,
      match: Object.keys(generatedConfig.ma_memoire).length >= 5
    },
    routines_coverage: {
      generated: generatedConfig.routines.optional.length,
      fred: 3, // Daily, Weekly, Monthly
      match: generatedConfig.routines.optional.length >= 2
    },
    custom_instructions_density: {
      generated: generatedConfig.custom_instructions?.length || 0,
      fred: fredConfig.custom_instructions?.length || 0,
      match: generatedConfig.custom_instructions?.length >= 1500
    },
    synthesis_specificity: {
      generated: !!generatedConfig.strategic_synthesis?.understanding,
      fred: true,
      match: !!generatedConfig.strategic_synthesis?.understanding
    }
  };

  const overallMatch = Object.values(comparison).filter(c => c.match).length / Object.keys(comparison).length;

  return {
    comparison,
    overall_quality_match: overallMatch,
    baseline_aligned: overallMatch >= 0.8,
    recommendations: generateRecommendations(comparison)
  };
}
```

---

## Testing Checklist

Before deploying to production:

- [ ] Test 1: Complete diagnostic → synthesis → config generation flow (end-to-end)
- [ ] Test 2: All 6 mandatory agents in generated config
- [ ] Test 3: Ma Mémoire structure correctly populated from metadata
- [ ] Test 4: Custom Instructions present and 2000+ characters
- [ ] Test 5: Routines configuration included with minimum 1 active
- [ ] Test 6: Timeout + fallback works (simulate slow generation)
- [ ] Test 7: Generated config compared favorably with Fred's baseline (≥80% match)
- [ ] Test 8: Config persists to Supabase + retrievable
- [ ] Test 9: Quality report accurate + helpful
- [ ] Test 10: 5+ complete end-to-end diagnostics (quality validated manually vs Fred)

---

## Performance Considerations

- Chunked generation: Max 25 seconds per section
- Parallel generation where safe (agents can generate simultaneously)
- Fallback templates available for all sections (no failures)
- Message compression on diagnostic metadata before passing
- Streaming response to frontend (show progress, don't timeout)
- Total time target: < 2 minutes from "Generate Config" click to download

---

## Rollback Plan

If generate-config integration causes issues:
1. Disable config generation (show synthesis only)
2. Client can manually create config from synthesis
3. Diagnostic still works end-to-end
4. Config generation can be retried later
5. Document issue for EPIC-7 iteration

---

## Handoff Success Criteria

✅ Diagnostic generates strategic synthesis  
✅ Synthesis includes 3 sections (understanding, transformation, config preview)  
✅ Client approves synthesis ("Yes, this is me")  
✅ Generate Config button produces complete config in < 2 minutes  
✅ Config includes all 6 mandatory agents + applicable contextual agents  
✅ Config includes Ma Mémoire project structure + Custom Instructions  
✅ Config includes daily/weekly/monthly routines with clear rationale  
✅ Config quality score ≥ 0.8 (≥80% checks passed)  
✅ Generated config comparable to Fred's baseline  
✅ Config saved to Supabase + ready for deployment  

---

**EPIC-7 Status**: Specification complete  
**Dependencies Met**: EPIC-1 through EPIC-6 deployed  
**Next**: EPIC-8 (E2E Testing & Validation)
