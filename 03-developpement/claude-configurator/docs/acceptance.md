# Acceptance Criteria — Claude Configurator v2: Diagnostic Intelligent

## End-to-End Success Criteria

### AC-001: Diagnostic Completes Without Crash (1-1.5h)
**Criterion**: A 1.5-hour client diagnostic session completes end-to-end with no timeouts, API errors, or frontend hangs.

**Validation**:
- [ ] Run E2E test: 10+ message exchanges, then config generation
- [ ] No timeout in chat Edge Function
- [ ] No "Network error" in frontend
- [ ] Config generates completely (all 9 sections)
- [ ] Benchmark: diagnostic + config gen < 90s total

**Reference**: Fred's 2.5h session must run without crash

---

### AC-002: Adaptive Questions Demonstrated
**Criterion**: Diagnostic questions visibly adapt based on earlier responses. Not a rigid questionnaire.

**Validation**:
- [ ] Test case: Client mentions "export to 40 countries" → follow-up asks about compliance challenges (not generic)
- [ ] Test case: Client says "I work by feeling" → assistant asks about decision-making triggers
- [ ] Questions re-order themselves (blocs implicites)
- [ ] At least 3 examples in test transcript showing adaptation

**Reference**: Compare with v1 (linear) transcript

---

### AC-003: Metadata Enriched & Extractible
**Criterion**: Enriched metadata (pain_points, patterns_detected, claude_opportunities) is captured in real-time and available for config generation.

**Validation**:
- [ ] Metadata JSON valid (schema matches F-004)
- [ ] Pain points ≥ 3 per diagnostic (specific, not generic)
- [ ] Patterns detected ≥ 2 per diagnostic (linked to pain points)
- [ ] Opportunities identified ≥ 3 per diagnostic (actionable)
- [ ] Metadata passed to generate-config (check console logs)
- [ ] Config generation uses metadata (directives visible in output)

**Example validation**:
```json
{
  "pain_points": [
    {"area": "compliance", "detail": "40 countries", "severity": "high"}
  ],
  "patterns_detected": [
    {"pattern": "works by feeling", "consequence": "risk of oversights"}
  ],
  "claude_opportunities": [
    {"opportunity": "Compliance hub (agent Ingénieur)", "linked_to": "pain_points[0]"}
  ]
}
```

---

### AC-004: Strategic Synthesis Generated
**Criterion**: Diagnostic output includes a strategic synthesis (not a summary) explaining where Claude becomes game-changing.

**Validation**:
- [ ] Synthesis titled "Où Claude devient vraiment game-changer pour vous"
- [ ] Includes 3 sections minimum:
  - [ ] "Ce que j'ai compris de vous" (blocages + forces)
  - [ ] "Où Claude transforme" (3+ opportunities with why)
  - [ ] "Votre config sera centrée sur" (preview of delivered config)
- [ ] Read by human (CEO/consultant): "Does this justify 149€?"
- [ ] Must reference Fred's config as analogy (not just generic)

**Tone check**: NOT "Vous avez dit X, Y, et Z. Conclusion: A, B, C."  
✅ YES "Vous êtes ingénieur innovant avec défi conformité 40-pays. Claude transforme cela via agent Ingénieur spécialisé. Voici comment."

---

### AC-005: Config Generated = Fred Standard
**Criterion**: Generated config for test client approaches quality/density of Fred's reference config.

**Validation**:
- [ ] Config includes Custom Instructions (>2000 chars, specific)
- [ ] Config includes 5 agents (Ingénieur, Admin, Miroir, Coach, Garde-Fou or equivalent roles)
- [ ] Config includes "Ma Mémoire" project (personalized, not boilerplate)
- [ ] Config includes 3+ scheduled tasks (specific times/purposes)
- [ ] Config shows high density (multiple layers, not surface-level suggestions)
- [ ] Comparison checklist: vs Fred's, what's missing? (identify gaps for next iteration)

**Validation method**: Read both configs side-by-side. Fred's should not look significantly richer.

---

### AC-006: Metadata Does Not Bloat Message Context
**Criterion**: Enriched metadata doesn't exceed 2KB and doesn't cause generate-config to timeout due to context explosion.

**Validation**:
- [ ] Metadata JSON size < 2KB (check in browser console)
- [ ] Message compression still active (last 5 full + summarize older)
- [ ] Generate-config timeout per section < 30s
- [ ] Full config generation < 90s

**Reference**: v18-19 compression strategy must remain functional

---

### AC-007: Diagnostic Improves Client Self-Understanding
**Criterion**: Client exits diagnostic with clearer understanding of their own blocages, strengths, and needs.

**Validation**:
- [ ] Test with human client: "Do you feel understood?" (qualitative)
- [ ] Transcript shows assistant paraphrasing back (not just listening)
- [ ] Follow-up questions are clarifying, not just information-gathering
- [ ] Client expresses "Oh, I hadn't thought of it that way" moments (evidence of insight)

**Measurement**: Post-diagnostic survey (1-2 questions, optional)

---

## Quality Gates

| Gate | Criterion | Validator | Decision |
|------|-----------|-----------|----------|
| G-001 | Diagnostic completes without crash (E2E test) | Dev + QA | PASS/FAIL |
| G-002 | Metadata extracted & schema valid | Dev (automated check) | PASS/FAIL |
| G-003 | Strategic synthesis quality reviewed | Catherine (CEO) | PASS/REMEDIATE |
| G-004 | Config vs Fred standard comparison | Catherine (consultant) | PASS/ITERATE |
| G-005 | Message context size within budget | Dev (automated check) | PASS/FAIL |
| G-006 | Adaptive question quality (3+ examples) | Code review | PASS/REMEDIATE |

---

## Deployment Readiness

**Pre-Deployment Checklist**:
- [ ] All ACs above: PASS
- [ ] Code reviewed (Factory ACT phase)
- [ ] Edge Function tested in staging
- [ ] Database migration tested (if schema changed)
- [ ] Customer comms ready ("v2 now live, expect smarter diagnostics")
- [ ] Rollback plan documented (revert to v17 if critical issue)

**Deployment Strategy**:
- Blue-green: v17 running, v2 starts in parallel, switch traffic gradually
- Monitoring: alert on timeouts, API errors, config generation failures
- Rollback trigger: >5% failure rate in first 24h

---

## Success Definition (Business)
✅ Claude Configurator v2 is **successful** when:
1. Diagnostic crash rate drops to ~0% (was endemic in v1)
2. Generated configs are consistently "transformative" (validated by Catherine vs Fred standard)
3. Customer retention improves (less churn due to generic configs)
4. 149€ price feels justified (customer feedback)

---

**Created**: 2026-04-27 (MODEL phase)  
**Last Reviewed**: 2026-04-27  
**Status**: Ready for PLAN phase
