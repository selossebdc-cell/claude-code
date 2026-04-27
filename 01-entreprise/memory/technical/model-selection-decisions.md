---
name: Claude Configurator — Model Selection Decisions
description: Diagnostic uses Sonnet 4.6 (not Opus) for cost/quality balance. Generate-config uses chunked generation + streaming.
type: project
updated: 2026-04-26
---

## Decision: Diagnostic Model = Sonnet 4.6
**Rejected**: Opus 4.7 (coût ~2-3x plus élevé)
**Selected**: Sonnet 4.6 (compromis qualité/coût, meilleure analyse qu'ancienne Sonnet 4-5)

### Justification
- Sonnet 4.6 = assez intelligent pour pattern detection + synthesis stratégique
- Coût modéré permet 149€ pricing avec marge acceptable
- Sufficient pour adapter questions en fonction des réponses
- Better quality than legacy Sonnet ensures diagnostic depth

### Why
Catherine voulait intelligence réelle mais aussi viabilité économique du produit. Sonnet 4.6 offre le balance point.

## Decision: Generate-Config = Chunked Generation + Streaming
- **Architecture**: 9 CONFIG_SECTIONS indépendantes, timeout 25s par section
- **Fallback**: Vide ou default si section timeout (pas de crash global)
- **Frontend**: ReadableStream + SSE pour affichage temps-réel (✓ custom_instructions, ✓ security_shield...)
- **Message Compression**: Keep last 5 messages full, summarize older messages en blocs 10-message

### Why
Monolithic generation (v16 avec max_tokens=8000) créait des timeouts 60+ secondes et des crashs. Chunked = plus robuste pour long diagnostics (2.5h sessions).

## Implementation Status
✅ v18-19: Message compression + fallback implemented
✅ Frontend: Streaming + progress display active
🟡 Diagnostic refactor: En cours (Factory MODEL phase)

## How to apply
- Diagnostic queries: always use Sonnet 4.6 (or newer Sonnet if available)
- Config generation: keep chunked architecture (don't revert to monolithic)
- Long conversations: ensure compression is active in generate-config
