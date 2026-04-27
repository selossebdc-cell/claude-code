# Scope — Claude Configurator v2: Diagnostic Intelligent

## Features à Implémenter

### F-001: Adaptive Question Generation
**Description**: Au lieu d'une séquence pré-définie, générer les questions suivantes en fonction de ce qui a émergé dans les réponses précédentes.

**Acceptance Criteria**:
- [ ] Assistant pose questions pertinentes à contexte (pas robotique)
- [ ] Questions adaptent leur formulation selon réponses précédentes
- [ ] Pas d'ordre linéaire fixe (les 9 blocs ne sont pas visibles dans l'ordre)
- [ ] Diagnostic progresse naturellement (conversation)

**Dependencies**: F-004 (metadata enrichment pour contextualiser)

---

### F-002: Pattern Detection in Real-Time
**Description**: Analyser chaque réponse pour identifier patterns, blocages récurrents, forces évidentes, work style traits caractéristiques.

**Acceptance Criteria**:
- [ ] Identifier au moins 2-3 patterns par diagnostic (pas vides)
- [ ] Patterns sont spécifiques au client (pas génériques)
- [ ] Detection happen in-session (metadata updated après chaque réponse)
- [ ] Patterns inform subsequent questions (loop fermée)

**Patterns à détecter**:
- Blocages récurrents (ex: "toujours face au même problème")
- Forces évidents (ex: "très bon à X")
- Work style traits (ex: "fonctionne mieux le matin", "au feeling vs structuré")
- Risk patterns (ex: "pas assez de documentation", "oubli de tâches")

**Dependencies**: Chat Edge Function upgrade (metadata tracking)

---

### F-003: Claude Opportunities Identification
**Description**: Détecter automatiquement où Claude peut vraiment transformer le quotidien du client (pas où "Claude peut aider un peu").

**Acceptance Criteria**:
- [ ] Identifier 3+ opportunities par diagnostic (minimum)
- [ ] Chaque opportunity a une justification (pourquoi Claude change la donne ici)
- [ ] Opportunities sont liées à pain points détectés
- [ ] Opportunities information la config generation (directives explicites)

**Exemples d'opportunities**:
- Client dit "je gère 40 pays différents" → Claude peut centraliser conformité multi-région
- Client dit "j'ai trop de docs à maintenir" → Claude peut documenter automatiquement
- Client dit "je travaille au feeling" → Claude peut structurer le feeling via Custom Instructions

**Dependencies**: F-002 (Pattern Detection)

---

### F-004: Enriched Metadata Schema
**Description**: Tracker les insights au fur et à mesure dans une structure JSON réutilisable par la config generation.

**Acceptance Criteria**:
- [ ] Schema inclut: pain_points[], patterns_detected[], work_style_traits[], claude_opportunities[]
- [ ] Chaque insight a un contexte (pourquoi je pense ça)
- [ ] Metadata reste < 2KB (pas de bloat)
- [ ] JSON sérialisable directement pour generate-config

**Structure**:
```json
{
  "pain_points": [
    {"area": "conformité", "detail": "40 pays différents", "severity": "high"},
    {"area": "documentation", "detail": "trop de doc à maintenir", "severity": "medium"}
  ],
  "patterns_detected": [
    {"pattern": "travaille au feeling", "consequence": "risque oublis", "opportunity": "structure via instructions"}
  ],
  "work_style_traits": [
    {"trait": "pragmatique", "implication": "veut résultats fast"},
    {"trait": "innovant", "implication": "open to new approaches"}
  ],
  "claude_opportunities": [
    {"opportunity": "Multi-region compliance hub", "linked_to": "pain_points[0]", "effort": "medium", "impact": "high"}
  ]
}
```

**Dependencies**: Chat Edge Function v20+ (JSON metadata field)

---

### F-005: Strategic Synthesis Generator
**Description**: Au lieu de juste "résumer ce qui a été dit", générer une analyse "voici ce que j'ai compris de vous, voici où Claude devient vraiment game-changer".

**Acceptance Criteria**:
- [ ] Synthèse n'est pas un résumé (structure différente)
- [ ] Inclut: "Vos blocages", "Vos forces", "Où Claude transforme"
- [ ] Synthèse a une narrativeLogique (pas liste)
- [ ] Justifie le 149€ (montre la densité de la config future)

**Structure attendue**:
```
## Ce que j'ai compris de vous
- Ingénieur inventeur en expansion (40 pays)
- Défi principal: conformité multi-régionale + innovation rapide
- Force: pragmatisme + feeling informé
- Constraint: pas de temps pour docs lourdes

## Où Claude devient vraiment game-changer
1. Conformité centraliseée (agent Ingénieur monitors tous les pays)
2. Documentation auto-générée (agent Admin)
3. Decision-making accelerée (agent Coach debriefs hebdo)

## Votre config sera centrée sur:
- Agents spécialisés (vs single general purpose)
- "Ma Mémoire" comme hub centralisé
- Automation scheduled (daily/weekly/monthly)
```

**Dependencies**: F-001, F-002, F-003, F-004

---

### F-006: Guide Client vers Clarification
**Description**: Aider le client à se comprendre lui-même via questions bienveillantes et précises. Pas d'interrogatoire mais du coaching.

**Acceptance Criteria**:
- [ ] Questions posées avec empathie (pas "vous aviez dit X pourquoi?")
- [ ] Client sent qu'on l'écoute (paraphrasing de ses points)
- [ ] Questions creusent (follow-ups pertinents)
- [ ] Client sort du diagnostic avec meilleure compréhension de lui-même

**Tone attendu**:
- Conversationnel, bienveillant
- Curiosité visible ("dites m'en plus sur...")
- Pas robotique, pas condescendant

**Dependencies**: Chat Edge Function conversation quality

---

## Non-Features (Exclus)
- ❌ Changement du modèle Claude API (reste Sonnet 4.6)
- ❌ Refactor de generate-config v18-19 (compression/chunking restent)
- ❌ Nouvelle interface client (chat reste HTML/JS actuel)
- ❌ Multi-language (français only pour MVP)

---

## Technical Boundaries

### In-Scope Technically
- Chat Edge Function (diagnostic logic)
- Metadata persistence (Supabase diagnostics table)
- SSE streaming (progress display)
- Message compression (fallback in generate-config)

### Out-of-Scope Technically
- Frontend redesign (chat.js unchanged)
- API restructuring (POST /chat remains)
- Auth system change
- Database schema major changes (only adding columns)

---

## Integration Points
1. **Chat Edge Function** ← Core diagnostic logic lives here
2. **Generate-Config** ← Consumes enriched metadata to improve config
3. **Supabase** ← Stores diagnostic session + metadata
4. **Frontend** ← Displays conversation + progress

---

**Created**: 2026-04-27 (MODEL phase)  
**Status**: Scope defined, ready for acceptance criteria review
