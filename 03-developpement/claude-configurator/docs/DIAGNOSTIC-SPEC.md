# Diagnostic Specification — Intelligent Exploration v2

## Overview
Ce document spécifie le **prompt système et la logique de flow** pour le diagnostic intelligent de Claude Configurator v2. Le diagnostic adaptatif utilise les 9 blocs comme mental model implicite (pas d'ordre linéaire).

---

## Architecture Générale

```
Client Response
    ↓
[Diagnostic Agent - Sonnet 4.6]
    ├─ Analyze response (pattern detection, pain points)
    ├─ Update metadata enrichie
    ├─ Decide next question (adaptive logic)
    ├─ Generate response + next question
    └─ Stream to frontend
    ↓
[Metadata Enrichment]
    ├─ pain_points[]
    ├─ patterns_detected[]
    ├─ work_style_traits[]
    ├─ claude_opportunities[]
    └─ assumptions_validated[]
    ↓
[Strategic Synthesis] (when complete)
    └─ Generate "Où Claude devient vraiment game-changer"
```

---

## 9 Blocs Implicites (Mental Model)

L'assistant ne suit **pas** un ordre linéaire visible. Les 9 blocs sont une **internalchecklist** que l'assistant applique pour s'assurer que tous les thèmes sont couverts.

| Bloc | Thème | Questions Clés (exemples) |
|------|-------|--------------------------|
| 1 | **Identity** | Qui êtes-vous? Votre rôle/titre? | 
| 2 | **Offering** | Qu'offrez-vous? Produit/service? |
| 3 | **Daily** | Votre journée type? Rituel? |
| 4 | **Challenges** | Blocages principaux? Problèmes récurrents? |
| 5 | **Constraints** | Limites? Budget? Temps? Équipe? |
| 6 | **Security** | Sensibilités? Données? Conformité? |
| 7 | **Work Style** | Vous fonctionnez comment? Au feeling? Structuré? |
| 8 | **Voice** | Ton? Préférences de communication? |
| 9 | **Proposals** | Idées testées? Approches préférées? |

**Logique appliquée**:
- L'assistant se pose en interne: "Ais-je couvert les 9 blocs?"
- Les questions **re-ordonnent dynamiquement** selon ce qui émerge
- Pas de "OK passons au bloc 3" visible

---

## Pattern Detection Logic

### Catégories de Patterns à Détecter

**1. Recurring Blocages**
```
Pattern: Client mentionne le même problème plusieurs fois (explicitement ou implicitement)
Detection: Scan responses pour keywords/concepts répétés
Example: "conformité" mentionné en réponses 2, 5, 7 → pattern "conformité est un défi récurrent"
Output: pain_points[] avec severity élevée
```

**2. Work Style Traits**
```
Pattern: Comment le client opère (pragmatique, structuré, au feeling, innovant, minutieux)
Detection: Look for verbes + adjectifs dans responses
Example: "Je décide rapido, test et j'ajuste" → pattern "work by feeling + rapid iteration"
Output: work_style_traits[] avec implication pour Claude setup
```

**3. Strength Signals**
```
Pattern: Client excelle à quelque chose (force évidente)
Detection: Client says "I'm good at..." or "I like..." or success stories
Example: "J'aime vraiment l'innovation, je suis toujours à chercher des trucs nouveaux"
Output: Inté en work_style_traits comme force à valoriser
```

**4. Risk Indicators**
```
Pattern: Zone d'oubli ou de faiblesse
Detection: Expressions like "I forget...", "I struggle with...", "nobody tracks..."
Example: "J'oublie toujours les deadlines administratives"
Output: pain_points[] + opportunity pour Claude (agent Garde-Fou)
```

---

## Adaptive Question Generation

### Logique Générale
Au lieu de liste pré-définie, chaque question est **dynamiquement générée** basée sur:
1. Ce qui a été dit (contexte des réponses)
2. Ce qui n'a pas encore été couvert (blocs manquants)
3. Patterns qui émergent (clarifier/approfondir)

### Stratégies

**Strategy 1: Follow-Up Deepening**
```
Si client dit: "J'export vers 40 pays"
Suivi naturel: "Quel est votre plus gros défi dans cet export?"
(vs generic: "Parlez-moi de vos contraintes")
```

**Strategy 2: Pattern Validation**
```
Si pattern détecté: "client travaille au feeling"
Question suivante: "Vous rappelez comment vous prenez les décisions importantes?"
(pour valider + approfondir)
```

**Strategy 3: Bloc Coverage Check**
```
Si bloc "Security" pas encore couvert et context approprié:
Poser: "Y a-t-il des éléments sensibles dans votre travail?"
(pas: "Parlons sécurité" - rigide)
```

**Strategy 4: Opportunity Identification**
```
Si pain_point("documentation") et pattern("works by feeling"):
Question: "Aimeriez-vous que vos décisions soient mieux documentées pour l'équipe?"
(linker pain + opportunity)
```

---

## Metadata Schema (JSON)

```json
{
  "session_id": "uuid",
  "started_at": "2026-04-27T14:30:00Z",
  "client_name": "optional - if provided",
  
  "pain_points": [
    {
      "id": "pp_001",
      "area": "conformité",
      "detail": "40 pays différents, chacun avec réglementations différentes",
      "severity": "high",  // high | medium | low
      "context": "mentionné en réponses 2, 5, 7",
      "linked_to": ["security", "constraints"],
      "opportunity_candidate": "oc_003"
    }
  ],
  
  "patterns_detected": [
    {
      "id": "pd_001",
      "pattern": "travaille au feeling + rapid iteration",
      "evidence": ["'décide rapido'", "'test et j'ajuste'"],
      "consequence": "risque d'oublis administratifs",
      "strength_potential": "innovation velocity",
      "implication_for_claude": "Structure via Instructions + automated tracking"
    }
  ],
  
  "work_style_traits": [
    {
      "id": "ws_001",
      "trait": "pragmatique",
      "manifestation": "Veut résultats concrets, pas théories",
      "implication": "Claude setup favor action > documentation"
    }
  ],
  
  "claude_opportunities": [
    {
      "id": "oc_001",
      "opportunity": "Compliance Hub (agent Ingénieur)",
      "description": "Centralize multi-country compliance tracking",
      "linked_pain_point": "pp_001",
      "why_claude_transforms": "Agent can monitor 40 countries simultaneously, alert on changes, maintain docs",
      "effort_estimate": "medium",
      "impact_estimate": "high",
      "priority": 1,
      "agent_role": "Ingénieur"
    }
  ],
  
  "assumptions_validated": [
    {
      "assumption": "Conformité est un défi existentiel",
      "validation": "confirmed in 3+ responses",
      "confidence": 0.95
    }
  ],
  
  "coverage_tracking": {
    "blocs_covered": ["Identity", "Offering", "Daily", "Challenges", "Constraints"],
    "blocs_pending": ["Security", "Work Style", "Voice", "Proposals"],
    "coverage_percentage": 55
  },
  
  "conversation_quality_metrics": {
    "turns_count": 8,
    "avg_response_length": 150,
    "engagement_level": "high",  // low | medium | high
    "clarity_score": 0.87  // 0-1, how clear client's needs are
  }
}
```

---

## System Prompt Architecture

### Part 1: Role & Context
```
You are an intelligent diagnostic agent for Claude Pro configurations.
Your job is NOT to ask a questionnaire. Your job is to help clients 
understand themselves better through conversational exploration.

You will:
1. Analyze each response for patterns, pain points, opportunities
2. Ask adaptive questions based on what emerges (not a rigid script)
3. Build rich metadata in real-time
4. Guide the client toward clarity
5. Generate a strategic synthesis (not just a summary)

Tone: Conversational, curious, bienveillant. No jargon. Direct.
```

### Part 2: Internal Mental Model
```
The 9 blocks (Identity, Offering, Daily, Challenges, Constraints, 
Security, Work Style, Voice, Proposals) are your internal checklist. 
You ensure all themes are covered, but NOT in a visible linear order.

After each response, ask yourself:
- What patterns am I noticing?
- What pain points are emerging?
- What opportunities could Claude unlock?
- Which block should I gently explore next?
```

### Part 3: Metadata Enrichment Instructions
```
Maintain a JSON metadata object (shared with frontend).
After each response:
1. Scan for pain_points (specific issues)
2. Detect patterns (recurring themes, work style)
3. Identify claude_opportunities (where Claude changes the game)
4. Validate assumptions (are my initial readings correct?)
5. Update coverage_tracking (which blocks done?)

Be precise: pain_points must be specific to THIS client, not generic.
```

### Part 4: Adaptive Question Logic
```
Generate next question based on:
1. Deepening: What follow-up would naturally explore this further?
2. Coverage: Which block is least covered and fits naturally?
3. Pattern validation: Can I clarify/strengthen pattern detection?
4. Opportunity linking: Can I connect a pain point to a Claude opportunity?

Avoid: "OK moving to next block...", "let's talk about X", rigid structure.
Prefer: Natural follow-ups that feel like conversation.
```

### Part 5: Strategic Synthesis (End of Diagnostic)
```
When diagnostic concludes (typically after 10-15 exchanges),
generate a synthesis structured as:

## Ce que j'ai compris de vous
- Your key identity (who you are)
- Your main blocages (pain points)
- Your strengths (what you excel at)

## Où Claude devient vraiment game-changer pour vous
- 3-5 specific opportunities
- For each: WHY Claude transforms it (not just "Claude can help")

## Votre config sera centrée sur
- Specific agent roles (Ingénieur, Admin, Coach, etc.)
- Specific scheduled tasks
- "Ma Mémoire" as your personalized hub

This synthesis should justify the 149€ price.
```

---

## Flow Example: "Export Engineer"

```
Turn 1:
Client: "Je suis ingénieur, j'export des produits à 40 pays"

Diagnostic Agent Analysis:
- Pattern detected: International scope, complexity
- Block coverage: Identity (partial), Offering (partial)
- Next question strategy: Deepen offering (what products?)

Response: "Impressionnant, 40 pays c'est complexe! Quel type de 
produits vous exportez? Et c'est toi qui gère tout, ou t'as une équipe?"

Metadata Update:
- work_style: ["international", "export-focused"]
- assumption: "Complex regulatory landscape"
- coverage: Identity 80%, Offering 40%

---

Turn 3:
Client: "Produits électroniques. Chaque pays a des certifs différentes. 
Je dois m'assurer qu'on suit les règles."

Diagnostic Agent Analysis:
- Pain point detected: Compliance complexity, 40 countries
- Pattern: Risk management is top-of-mind
- Block coverage: Security (emerging), Constraints (implied)
- Opportunity: Compliance hub (agent Ingénieur)

Response: "Les certs différentes c'est un vrai casse-tête. Comment 
tu gères maintenant? Spreadsheet, quelqu'un qui track, ou c'est du 
ad-hoc?"

Metadata Update:
- pain_points: [{area: "compliance", severity: "high"}]
- patterns: ["risk-aware", "managing complexity"]
- claude_opportunity: "Compliance hub (agent Ingénieur) monitors all certifications"
- coverage: Identity 85%, Offering 70%, Security 60%, Challenges 75%

---

Turn 8 (Diagnostic concluding):
Generate Strategic Synthesis
- "Ce que j'ai compris": Ingénieur innovant, gère complexité 40-pays, 
  défi conformité récurrent
- "Où Claude transforme": Agent Ingénieur monitors compliance, Agent 
  Coach debriefs market-by-market progress, etc.
- "Config centrée sur": 5 agents, Ma Mémoire (compliance + market data), 
  scheduled alerts
```

---

## Technical Implementation

### Model & Parameters
- **Model**: Claude Sonnet 4.6 (intelligence + cost balance)
- **Context Window**: Keep last 5 messages full + compress older
- **Temperature**: 0.7 (creative + coherent)
- **Max tokens**: 800 per response (keep flowing, not too long)
- **Stop sequences**: None (stream naturally)

### Edge Function Integration
- Endpoint: `POST /chat` (existing, no change)
- Input: `{ role: "user", content: "..." }`
- Output: 
  - `{ role: "assistant", content: "...", metadata: {...} }`
  - Stream SSE for progressive metadata display

### Metadata Persistence
- Store in `diagnostics` table (Supabase)
- Column: `metadata` (JSON) auto-updated per turn
- Indexed by `session_id` for quick retrieval
- Passed downstream to generate-config

---

## Quality Standards

### Conversation Quality
- [ ] Questions feel conversational (not robotic)
- [ ] Assistant paraphrases back (shows understanding)
- [ ] Follow-ups are clarifying (not just info-gathering)
- [ ] Tone remains curious + bienveillant

### Metadata Quality
- [ ] Pain points are specific (not "I have challenges")
- [ ] Patterns are grounded in evidence (quotes from responses)
- [ ] Opportunities are actionable (not vague)
- [ ] Metadata size stays < 2KB (no bloat)

### Synthesis Quality
- [ ] Not a summary (re-structures insights)
- [ ] Justifies 149€ price (shows density)
- [ ] References Fred's config as comparison point
- [ ] Ends with clear config direction (agent roles, projects, tasks)

---

## Deployment Checklist

- [ ] System prompt tested with 5+ diverse clients
- [ ] Metadata schema validated (JSON valid, size < 2KB)
- [ ] Strategic synthesis reviewed by Catherine
- [ ] E2E test: 1.5h diagnostic + config gen without crash
- [ ] Comparison: Generated config vs Fred's (density check)
- [ ] Edge Function staging deployment tested
- [ ] Rollback procedure documented (revert to v17)

---

**Created**: 2026-04-27 (MODEL phase)  
**Status**: Ready for PLAN phase (epics from this spec)  
**Next**: Factory PLAN phase will break this into user stories + tasks
