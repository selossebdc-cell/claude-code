# BUILD — EPIC-8: E2E Testing & Validation

## Overview
Implémenter une stratégie complète de test end-to-end : diagnostic → synthèse → config, validation contre baseline Fred, tests de qualité, gestion des cas d'erreur.

**Statut**: Ready to implement  
**Effort**: 3.5 days (1 day test infrastructure + 1.5 days manual testing + 1 day validation)  
**Blocker**: All EPIC-1 through EPIC-7 must be deployed  
**Dependencies**: EPIC-1 ✓, EPIC-2 ✓, EPIC-3 ✓, EPIC-4 ✓, EPIC-5 ✓, EPIC-6 ✓, EPIC-7 ✓  

---

## Implementation Steps

### Step 1: Test Infrastructure Setup (Day 1)
Create testing framework with test data, validation utilities, reporting.

**Location**: tests/ directory in claude-configurator project  
**Includes**:
- Test data fixtures (5 diverse diagnostic scenarios)
- Validation helpers (checks for metadata, synthesis, config)
- Quality comparison utilities (against Fred's baseline)
- Test runner + reporting

### Step 2: Manual Testing (Day 1-2)
Run 5+ complete diagnostics end-to-end with diverse personas.

**Scenarios**:
1. **FastMoving (Engineer)**: Pragmatic, compliance-heavy, international scope
2. **StructuredLeader (Manager)**: Organized, process-focused, team management
3. **CreativeFreeSpirit (Consultant)**: Feeling-based, innovative, flexible
4. **RiskAware (Compliance Officer)**: Detail-focused, regulatory, verification
5. **GrowthFocused (Entrepreneur)**: Vision-driven, scaling, opportunity-seeking

**For each scenario**:
- Run complete diagnostic
- Generate synthesis
- Generate config
- Validate against quality criteria
- Compare with Fred's baseline
- Document any issues

### Step 3: Validation & Reporting (Day 2-3)
Validate results, compare with Fred, generate test report.

**Outputs**:
- Test execution log (diagnostic transcripts)
- Quality validation report (metrics, checklist results)
- Baseline comparison report (how close to Fred)
- Issues + blockers log (what needs fixing)
- Recommended improvements

---

## Test Data Fixtures

```javascript
/**
 * Test Fixtures
 * 5 diverse diagnostic scenarios for end-to-end testing
 */

const testScenarios = {
  // Scenario 1: Fast-moving engineer with compliance challenges
  fastMovingEngineer: {
    name: "Scenario 1: Fast-Moving Engineer",
    persona: "Electronics engineer, 40-country export, compliance-heavy",
    simulatedResponses: [
      {
        turn: 1,
        userMessage: "I'm an engineer managing export to 40 countries. Electronic products, so each market has different certifications and regs.",
        expectedPatterns: ["international scope", "compliance complexity"],
        expectedPainPoints: ["compliance", "regulation tracking"]
      },
      {
        turn: 2,
        userMessage: "Right now I track it with spreadsheets. Someone checks monthly, but it's ad-hoc. With growth, this is going to break.",
        expectedPatterns: ["manual process", "scaling risk"],
        expectedPainPoints: ["documentation", "compliance tracking"]
      },
      {
        turn: 3,
        userMessage: "I'm pretty pragmatic. Fast decisions, I trust my gut but I want data backing it. Team is small, maybe 5 people.",
        expectedPatterns: ["pragmatic decision-making", "feeling-based"],
        expectedPainPoints: ["team coordination"],
        expectedWorkStyle: ["pragmatic", "fast-moving", "gut-based"]
      },
      {
        turn: 4,
        userMessage: "Security is not my biggest worry right now. Compliance and getting right people are the real blockers.",
        expectedPainPoints: ["team hiring", "resource constraints"]
      },
      {
        turn: 5,
        userMessage: "I'd love to automate compliance tracking. Right now my time is split between compliance and strategic stuff, which I actually enjoy.",
        expectedOpportunities: ["Compliance Hub", "Compliance automation"],
        expectedStrengths: ["strategic thinking", "decision-making"]
      }
    ],
    expectedOutcome: {
      painPointCount: 4,
      patternCount: 3,
      opportunityCount: 4,
      synthesisSpecificity: "Should reference 40 countries, compliance, pragmatism"
    }
  },

  // Scenario 2: Structured manager with process focus
  structuredLeader: {
    name: "Scenario 2: Structured Manager",
    persona: "Department manager, process-focused, team leadership",
    simulatedResponses: [
      {
        turn: 1,
        userMessage: "I manage a team of 12. We run marketing and client success. Everything is very process-driven here.",
        expectedPatterns: ["structured approach", "process orientation"],
        expectedPainPoints: ["process documentation", "team coordination"]
      },
      {
        turn: 2,
        userMessage: "My biggest challenge is keeping everyone aligned. We have templates for everything, but communication gaps still happen.",
        expectedPainPoints: ["communication", "alignment"]
      },
      {
        turn: 3,
        userMessage: "I love planning. We do quarterly planning, weekly standups, everything scheduled. I'd say I'm detail-oriented.",
        expectedWorkStyle: ["structured", "process-focused", "detail-oriented"]
      },
      {
        turn: 4,
        userMessage: "One thing that's always a problem: decisions get made, but nobody remembers WHY 6 months later. We lose context.",
        expectedPainPoints: ["decision logging", "institutional memory"]
      },
      {
        turn: 5,
        userMessage: "I need better visibility into what the team is doing. Metrics, progress, blockers — all in one place.",
        expectedOpportunities: ["Progress Tracking", "Decision Logging", "Communication Hub"]
      }
    ],
    expectedOutcome: {
      painPointCount: 4,
      patternCount: 2,
      opportunityCount: 3,
      synthesisSpecificity: "Should reference team of 12, process-driven, alignment challenges"
    }
  },

  // Scenario 3: Creative freelancer with flexibility focus
  creativeFreespirit: {
    name: "Scenario 3: Creative Free Spirit",
    persona: "Independent consultant, creative work, flexible structure",
    simulatedResponses: [
      {
        turn: 1,
        userMessage: "I'm a freelance consultant. I work on diverse projects — sometimes strategy, sometimes operational. Very flexible.",
        expectedPatterns: ["flexible", "diverse", "creative"],
        expectedPainPoints: ["context switching", "project management"]
      },
      {
        turn: 2,
        userMessage: "I work mostly from my gut and intuition. I'm good at seeing patterns other people miss. But I'm terrible at admin.",
        expectedWorkStyle: ["feeling-based", "intuitive"],
        expectedStrengths: ["pattern recognition", "creative thinking"]
      },
      {
        turn: 3,
        userMessage: "My pain point? Documentation. I hate it. I have notebooks everywhere, voice memos, nothing centralized.",
        expectedPainPoints: ["documentation", "information management"]
      },
      {
        turn: 4,
        userMessage: "I get overwhelmed by too much structure. I like tools that adapt to how I work, not the other way around.",
        expectedPainPoints: ["rigid systems"]
      },
      {
        turn: 5,
        userMessage: "I'd kill for a system that remembers what I've learned from clients, without me having to organize it.",
        expectedOpportunities: ["Decision Logging", "Memory System", "Auto-Documentation"]
      }
    ],
    expectedOutcome: {
      painPointCount: 4,
      patternCount: 3,
      opportunityCount: 4,
      synthesisSpecificity: "Should reference freelance, flexibility, gut-based decisions"
    }
  },

  // Scenario 4: Risk-aware compliance officer
  riskAwareCompliance: {
    name: "Scenario 4: Risk-Aware Compliance Officer",
    persona: "Compliance professional, regulation-focused, detail-oriented",
    simulatedResponses: [
      {
        turn: 1,
        userMessage: "I work in compliance for a financial services firm. Everything is regulated, everything is audited.",
        expectedPatterns: ["risk-aware", "regulation-focused"],
        expectedPainPoints: ["compliance pressure", "audit requirements"]
      },
      {
        turn: 2,
        userMessage: "My biggest challenge is staying on top of changes. Regulations change monthly, I need to track and implement immediately.",
        expectedPainPoints: ["regulation tracking", "change management"]
      },
      {
        turn: 3,
        userMessage: "I'm very systematic. Everything documented, verified, signed off. I check and double-check.",
        expectedWorkStyle: ["systematic", "careful", "verification-focused"]
      },
      {
        turn: 4,
        userMessage: "The worst thing would be a missed requirement. I lose sleep over blind spots.",
        expectedPainPoints: ["risk management", "oversight"]
      },
      {
        turn: 5,
        userMessage: "I need a system that makes sure nothing falls through cracks. Checklists, alerts, audit trails.",
        expectedOpportunities: ["Security Shield", "Compliance Hub", "Risk Management"]
      }
    ],
    expectedOutcome: {
      painPointCount: 4,
      patternCount: 3,
      opportunityCount: 3,
      synthesisSpecificity: "Should reference financial services, regulation, risk-aversion"
    }
  },

  // Scenario 5: Growth-focused entrepreneur
  growthFocusedFounder: {
    name: "Scenario 5: Growth-Focused Founder",
    persona: "Startup founder, scaling rapidly, opportunity-driven",
    simulatedResponses: [
      {
        turn: 1,
        userMessage: "I'm a founder. We're scaling fast — growing headcount from 5 to 15 this year. Revenue tripled.",
        expectedPatterns: ["fast-growing", "opportunity-focused"],
        expectedPainPoints: ["scaling challenges", "team growth"]
      },
      {
        turn: 2,
        userMessage: "Everything is moving so fast, I can barely keep up. I'm involved in hiring, strategy, product, everything.",
        expectedPatterns: ["overwhelmed", "multitasking"],
        expectedPainPoints: ["context switching", "bottleneck"]
      },
      {
        turn: 3,
        userMessage: "I'm very vision-driven. I see the 5-year goal and work backwards. Sometimes I miss details that bite us later.",
        expectedWorkStyle: ["vision-driven", "big-picture"],
        expectedPainPoints: ["detail blind spots"]
      },
      {
        turn: 4,
        userMessage: "My team thinks I forget decisions. I'll decide something, then a month later I suggest something contradictory.",
        expectedPainPoints: ["decision consistency", "communication"]
      },
      {
        turn: 5,
        userMessage: "I need something that keeps me aligned with my vision while scaling. Strategic clarity + execution visibility.",
        expectedOpportunities: ["Strategic Roadmap", "Decision Logging", "Progress Tracking"]
      }
    ],
    expectedOutcome: {
      painPointCount: 5,
      patternCount: 3,
      opportunityCount: 4,
      synthesisSpecificity: "Should reference startup, rapid scaling, vision-driven approach"
    }
  }
};
```

---

## Test Validation Framework

```javascript
/**
 * Test Validation Helpers
 * Validate diagnostic output at each stage
 */

class DiagnosticValidator {
  /**
   * Validate metadata completeness after diagnostic
   */
  static validateMetadata(metadata, scenario) {
    const checks = {
      sessionId: !!metadata.session_id,
      turnsCount: metadata.turns_count >= scenario.expectedOutcome.painPointCount,
      painPointsDetected: metadata.pain_points?.length >= scenario.expectedOutcome.painPointCount,
      patternsDetected: metadata.patterns_detected?.length >= scenario.expectedOutcome.patternCount,
      opportunitiesIdentified: metadata.claude_opportunities?.length >= scenario.expectedOutcome.opportunityCount,
      workStyleTraitsDetected: metadata.work_style_traits?.length >= 1,
      clarityScoreComputed: metadata.conversation_quality_metrics?.clarity_score > 0.5,
      coverageComputed: metadata.coverage_tracking?.coverage_percentage >= 50
    };

    return {
      passed: Object.values(checks).every(v => v),
      score: Object.values(checks).filter(Boolean).length / Object.keys(checks).length,
      checks,
      failures: Object.entries(checks)
        .filter(([_, v]) => !v)
        .map(([check]) => check)
    };
  }

  /**
   * Validate synthesis quality
   */
  static validateSynthesis(synthesis, metadata, scenario) {
    const checks = {
      hasUnderstandingSection: synthesis?.understanding?.length > 100,
      hasTransformationSection: synthesis?.transformation?.length > 100,
      hasConfigPreviewSection: synthesis?.config_preview?.length > 100,
      specificity: this._checkSpecificity(synthesis, scenario),
      justifies149: (synthesis?.understanding?.length || 0) + 
                     (synthesis?.transformation?.length || 0) + 
                     (synthesis?.config_preview?.length || 0) > 2000,
      mentionsAllAgents: this._checksIfMentionsAgents(synthesis),
      mentionsOpportunities: (synthesis?.transformation?.match(/Claude/g) || []).length >= 3,
      citesMetadata: this._checksCitesMetadata(synthesis, metadata)
    };

    return {
      passed: Object.values(checks).every(v => v),
      score: Object.values(checks).filter(Boolean).length / Object.keys(checks).length,
      checks,
      failures: Object.entries(checks)
        .filter(([_, v]) => !v)
        .map(([check]) => check)
    };
  }

  /**
   * Validate generated config
   */
  static validateConfig(config, metadata, scenario) {
    const checks = {
      allMandatoryAgents: config.agents.mandatory.length === 6,
      contextualAgentsIncluded: config.agents.contextual.length >= 1,
      maMemoirePopulated: Object.keys(config.ma_memoire || {}).length >= 5,
      customInstructionsLength: (config.custom_instructions?.length || 0) >= 1500,
      routinesConfigured: config.routines?.mandatory?.length >= 1 && config.routines?.optional?.length >= 2,
      qualityScoreAdequate: config.quality_metrics?.quality_score >= 0.8,
      configMatchesMetadata: this._checkConfigMatchesMetadata(config, metadata)
    };

    return {
      passed: Object.values(checks).every(v => v),
      score: Object.values(checks).filter(Boolean).length / Object.keys(checks).length,
      checks,
      failures: Object.entries(checks)
        .filter(([_, v]) => !v)
        .map(([check]) => check)
    };
  }

  /**
   * Compare config with Fred's baseline
   */
  static compareWithFredBaseline(generatedConfig, fredConfig) {
    return {
      agentComparison: {
        generated: generatedConfig.agents.mandatory.length + generatedConfig.agents.contextual.length,
        fred: fredConfig.agents.length,
        match: generatedConfig.agents.mandatory.length >= 6
      },
      maMemoireComparison: {
        generated: Object.keys(generatedConfig.ma_memoire || {}).length,
        fred: Object.keys(fredConfig.ma_memoire || {}).length,
        match: Object.keys(generatedConfig.ma_memoire || {}).length >= Object.keys(fredConfig.ma_memoire || {}).length * 0.9
      },
      routinesComparison: {
        generated: generatedConfig.routines?.optional?.length || 0,
        fred: 3,
        match: (generatedConfig.routines?.optional?.length || 0) >= 2
      },
      customInstructionsComparison: {
        generated: (generatedConfig.custom_instructions?.length || 0),
        fred: (fredConfig.custom_instructions?.length || 0),
        match: (generatedConfig.custom_instructions?.length || 0) >= 1500
      },
      synthesisPresence: {
        generated: !!generatedConfig.strategic_synthesis,
        fred: true,
        match: !!generatedConfig.strategic_synthesis
      }
    };
  }

  // Helper methods
  static _checkSpecificity(synthesis, scenario) {
    const specificKeywords = scenario.expectedOutcome.synthesisSpecificity
      .split(',')
      .map(k => k.trim().toLowerCase());
    
    const synthesisText = `${synthesis?.understanding || ''} ${synthesis?.transformation || ''} ${synthesis?.config_preview || ''}`.toLowerCase();
    
    return specificKeywords.some(kw => synthesisText.includes(kw));
  }

  static _checksIfMentionsAgents(synthesis) {
    const agents = ['Miroir', 'Garde-Fou', 'Admin', 'Stratégie', 'Planif', 'Amélioration'];
    const synthesisText = `${synthesis?.understanding || ''} ${synthesis?.transformation || ''} ${synthesis?.config_preview || ''}`;
    
    return agents.filter(agent => synthesisText.includes(agent)).length >= 4;
  }

  static _checksCitesMetadata(synthesis, metadata) {
    const painPointAreas = metadata.pain_points?.map(p => p.area.toLowerCase()) || [];
    const synthesisText = `${synthesis?.understanding || ''} ${synthesis?.transformation || ''}`.toLowerCase();
    
    return painPointAreas.some(area => synthesisText.includes(area));
  }

  static _checkConfigMatchesMetadata(config, metadata) {
    // Check if config addresses top pain points
    const painPointCount = metadata.pain_points?.length || 0;
    const opportunityCount = config.agents.mandatory.length + config.agents.contextual.length;
    
    return opportunityCount >= Math.max(4, painPointCount - 1);
  }
}

/**
 * Test Runner
 */
async function runEndToEndTest(scenario) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`Running Test: ${scenario.name}`);
  console.log(`${'='.repeat(60)}\n`);

  const sessionId = generateSessionId();
  let metadata = {};
  let synthesis = {};
  let config = {};

  // Phase 1: Run diagnostic
  console.log('📋 Phase 1: Running Diagnostic...');
  try {
    for (const response of scenario.simulatedResponses) {
      const result = await runDiagnosticTurn(sessionId, response);
      metadata = result.metadata;
      console.log(`  ✓ Turn ${response.turn}`);
    }
    console.log('✓ Diagnostic Complete\n');
  } catch (error) {
    console.error('✗ Diagnostic failed:', error);
    return { passed: false, error: error.message };
  }

  // Phase 2: Validate metadata
  console.log('🔍 Phase 2: Validating Metadata...');
  const metadataValidation = DiagnosticValidator.validateMetadata(metadata, scenario);
  console.log(`  Score: ${(metadataValidation.score * 100).toFixed(0)}%`);
  if (!metadataValidation.passed) {
    console.log(`  Failures: ${metadataValidation.failures.join(', ')}`);
  }
  console.log();

  // Phase 3: Generate synthesis
  console.log('✨ Phase 3: Generating Synthesis...');
  try {
    synthesis = await generateSynthesis(sessionId, metadata);
    console.log('✓ Synthesis Generated\n');
  } catch (error) {
    console.error('✗ Synthesis generation failed:', error);
    return { passed: false, error: error.message };
  }

  // Phase 4: Validate synthesis
  console.log('🔍 Phase 4: Validating Synthesis...');
  const synthesisValidation = DiagnosticValidator.validateSynthesis(synthesis, metadata, scenario);
  console.log(`  Score: ${(synthesisValidation.score * 100).toFixed(0)}%`);
  if (!synthesisValidation.passed) {
    console.log(`  Failures: ${synthesisValidation.failures.join(', ')}`);
  }
  console.log();

  // Phase 5: Generate config
  console.log('⚙️  Phase 5: Generating Config...');
  try {
    config = await generateConfig(sessionId, metadata, synthesis);
    console.log('✓ Config Generated\n');
  } catch (error) {
    console.error('✗ Config generation failed:', error);
    return { passed: false, error: error.message };
  }

  // Phase 6: Validate config
  console.log('🔍 Phase 6: Validating Config...');
  const configValidation = DiagnosticValidator.validateConfig(config, metadata, scenario);
  console.log(`  Score: ${(configValidation.score * 100).toFixed(0)}%`);
  if (!configValidation.passed) {
    console.log(`  Failures: ${configValidation.failures.join(', ')}`);
  }
  console.log();

  // Phase 7: Compare with Fred's baseline
  console.log('📊 Phase 7: Comparing with Fred\'s Baseline...');
  const fredComparison = DiagnosticValidator.compareWithFredBaseline(config, FRED_CONFIG);
  console.log(`  Agents: Generated ${fredComparison.agentComparison.generated} vs Fred ${fredComparison.agentComparison.fred}`);
  console.log(`  Ma Mémoire: Generated ${fredComparison.maMemoireComparison.generated} vs Fred ${fredComparison.maMemoireComparison.fred}`);
  console.log(`  Routines: Generated ${fredComparison.routinesComparison.generated} vs Fred ${fredComparison.routinesComparison.fred}`);
  console.log();

  const overallPassed = 
    metadataValidation.passed && 
    synthesisValidation.passed && 
    configValidation.passed;

  return {
    passed: overallPassed,
    scenario: scenario.name,
    results: {
      metadata: metadataValidation,
      synthesis: synthesisValidation,
      config: configValidation,
      fredComparison
    },
    sessionId
  };
}

/**
 * Run all test scenarios
 */
async function runAllTests() {
  const results = [];
  let passCount = 0;
  let failCount = 0;

  for (const [key, scenario] of Object.entries(testScenarios)) {
    const result = await runEndToEndTest(scenario);
    results.push(result);
    
    if (result.passed) {
      passCount++;
    } else {
      failCount++;
    }
  }

  // Generate report
  generateTestReport(results, passCount, failCount);

  return {
    totalTests: results.length,
    passed: passCount,
    failed: failCount,
    results
  };
}

/**
 * Generate test report
 */
function generateTestReport(results, passCount, failCount) {
  const report = `
# E2E Test Report

**Date**: ${new Date().toISOString()}
**Total Tests**: ${results.length}
**Passed**: ${passCount} ✓
**Failed**: ${failCount} ✗
**Success Rate**: ${((passCount / results.length) * 100).toFixed(0)}%

## Test Results

${results.map(r => `
### ${r.scenario}
- **Passed**: ${r.passed ? '✓' : '✗'}
- Metadata Score: ${(r.results.metadata.score * 100).toFixed(0)}%
- Synthesis Score: ${(r.results.synthesis.score * 100).toFixed(0)}%
- Config Score: ${(r.results.config.score * 100).toFixed(0)}%
- Fred Baseline Match: Agents ${r.results.fredComparison.agentComparison.match ? '✓' : '✗'}

${r.results.metadata.failures.length > 0 ? `
**Metadata Issues**: ${r.results.metadata.failures.join(', ')}` : ''}

${r.results.synthesis.failures.length > 0 ? `
**Synthesis Issues**: ${r.results.synthesis.failures.join(', ')}` : ''}

${r.results.config.failures.length > 0 ? `
**Config Issues**: ${r.results.config.failures.join(', ')}` : ''}
`).join('\n')}

## Recommendations

${passCount === results.length ? '✓ All tests passed! Ready for production.' : `✗ ${failCount} test(s) failed. Review issues above.`}
`;

  return report;
}
```

---

## Testing Checklist (Complete)

**Diagnostic Stage**:
- [ ] Test 1: Pattern detection active (≥2 patterns per diagnostic)
- [ ] Test 2: Pain points identified (≥3 per diagnostic)
- [ ] Test 3: Opportunities detected (≥3 per diagnostic)
- [ ] Test 4: Metadata size < 2KB (even with 15+ turns)
- [ ] Test 5: Coverage tracking updates (turns → coverage grows)

**Synthesis Stage**:
- [ ] Test 6: Synthesis triggers at right time (≥70% coverage, ≥3 opportunities)
- [ ] Test 7: Synthesis is strategic (not a summary)
- [ ] Test 8: Synthesis specific to client (not generic)
- [ ] Test 9: All 3 sections present (understanding, transformation, config preview)
- [ ] Test 10: Synthesis justifies 149€ (shows density)

**Config Generation Stage**:
- [ ] Test 11: All 6 mandatory agents selected
- [ ] Test 12: Contextual agents triggered appropriately
- [ ] Test 13: Ma Mémoire structure populated correctly
- [ ] Test 14: Custom Instructions present + 2000+ chars
- [ ] Test 15: Routines configured (min 1 active)

**Quality & Baseline**:
- [ ] Test 16: Generated config ≥80% match with Fred's baseline
- [ ] Test 17: Config quality score ≥0.8
- [ ] Test 18: Quality report accurate + helpful

**End-to-End**:
- [ ] Test 19: 5 complete scenarios (diverse personas)
- [ ] Test 20: All scenarios pass end-to-end (diagnostic → synthesis → config)
- [ ] Test 21: Error handling works (timeout + fallback scenarios)

---

## Acceptance Criteria

✅ **All 5 Test Scenarios Pass**:
- FastMovingEngineer diagnostic → synthesis → config ✓
- StructuredLeader diagnostic → synthesis → config ✓
- CreativeFreespirit diagnostic → synthesis → config ✓
- RiskAwareCompliance diagnostic → synthesis → config ✓
- GrowthFocusedFounder diagnostic → synthesis → config ✓

✅ **Quality Metrics**:
- Metadata completeness ≥ 90%
- Synthesis quality ≥ 85%
- Config quality ≥ 80%
- Fred baseline alignment ≥ 80%

✅ **Error Handling**:
- Timeout fallback works (25-second timeout per section)
- No crashes on edge cases
- Error messages are helpful

✅ **Documentation**:
- Test report generated + reviewed
- Issues logged with reproducible steps
- Recommendations documented

---

## Known Issues & Mitigations

| Issue | Severity | Mitigation |
|-------|----------|-----------|
| Synthesis sometimes generic | Medium | Increase specificity prompt guidance |
| Config generation timeout on slow connections | Medium | Increase chunk size, implement caching |
| Fred baseline not perfectly aligned | Low | Adjust agent selection logic incrementally |
| Custom Instructions too short sometimes | Low | Add minimum length validation |

---

**EPIC-8 Status**: Specification complete  
**All EPIC Specifications**: Delivered (EPIC-1 through EPIC-8)  
**Sprint 2 Status**: Complete  
**Next Phase**: ACT (Implementation)
