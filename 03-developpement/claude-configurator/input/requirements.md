# Requirements — Diagnostic Assistant Intelligence Refactor

## Overview

Refactoriser le diagnostic assistant de CS Digital Setup pour passer d'une approche linéaire (9 blocs fixes) à une exploration conversationnelle vraiment intelligente. L'assistant doit analyser chaque réponse du client, détecter les patterns et pain points en temps réel, poser des questions adaptatives contextuelles, et générer une synthèse stratégique qui identifie où Claude devient vraiment game-changer pour le client. Objectif: justifier le prix 149€ par une config hyper-pertinente et transformatrice, pas générique.

## Scope & Objectives

- **OBJ-001**: Transformer le diagnostic de "questionnaire linéaire" à "exploration intelligente et adaptative"
- **OBJ-002**: Détecter automatiquement pain points, patterns, forces, et opportunités Claude spécifiques
- **OBJ-003**: Enrichir les métadonnées avec insights (pain_points, patterns_detected, claude_opportunities)
- **OBJ-004**: Créer une synthèse stratégique (pas une liste) qui guide vraiment la génération de config
- **OBJ-005**: Assurer que la config générée est hyper-spécifique et clairement transformatrice pour le client

## Requirements

### Functional Requirements

- **REQ-001**: Assistant analyze chaque réponse du client pour détecter patterns, pain points, blocages
- **REQ-002**: Questions adaptatives: chaque question dépend de ce qui a émergé précédemment (pas d'ordre linéaire)
- **REQ-003**: Détection active: identifier automatiquement les opportunities où Claude peut vraiment transformer le quotidien
- **REQ-004**: Métadonnées enrichies: tracker pain_points, patterns_detected, work_style_traits, claude_opportunities, assumptions_validated
- **REQ-005**: Synthèse stratégique: au lieu de "résumé de ce qui a été dit", une analyse "voici ce que j'ai compris de vous, voici où Claude devient vraiment game-changer"
- **REQ-006**: Guide intelligente du client vers la clarification (aider le client à se comprendre lui-même)

### Non-Functional Requirements

- **NFR-001**: Performance: diagnostic complet en 1-1.5h max (optimisé pour pas de questions inutiles)
- **NFR-002**: Intelligence: utiliser Opus 4.7 pour analyser et adapter (pas Sonnet)
- **NFR-003**: Conversationnel: pas robotique, naturel et bienveillant
- **NFR-004**: Extractive: métadonnées complètes et structurées pour la génération

## Data Types

### Inputs
- Client responses: réponses conversationnelles libres (pas de formulaire rigide)
- Session history: historique des messages précédents
- Current metadata: extracted data, pain_points, patterns détectés jusqu'à présent

### Outputs
- Enriched metadata: `{ extracted: {...}, pain_points: [...], patterns_detected: [...], claude_opportunities: [...] }`
- Strategic summary: synthèse qui dit "voici où vous bloquez, voici vos forces, voici où Claude change vraiment la donne"
- Config-ready insights: insights transformés en directives pour generate-config

## Constraints

- **Timeline**: Refonte majeure du prompt diagnostic + test E2E → 2-3 sessions (si factory bien appliquée)
- **Resources**: Opus 4.7 API (coût légèrement plus élevé que Sonnet, mais justifié par qualité)
- **Technical**: 
  - Chat Edge Function v20+ doit rester compatible
  - Métadonnées doivent rester sérialisables en JSON
  - Stream SSE doit continuer de fonctionner
  - Compression de contexte doit rester intacte (v18-19 generate-config)

## Success Criteria

- [ ] Diagnostic pose des questions adaptatives (démontrées dans exemples, pas linéaires)
- [ ] Métadonnées enrichies avec insights détectés en temps réel
- [ ] Synthèse stratégique générée (démontrée dans example output)
- [ ] Config générée hyper-spécifique (comparée à config "générique" pour le même métier)
- [ ] E2E test: diagnostic 1.5h + génération sans crash ni timeout
- [ ] Qualité validée vs référence Fred (config transformatrice, pas juste "correct")

## Questions & Assumptions

- **ASS-001**: Opus 4.7 justifié pour diagnostic (meilleure analyse, adaptation, synthèse)
- **ASS-002**: Métadonnées enrichies ne vont pas créer un blob trop gros pour generate-config
- **Q-001**: Faut-il garder les 9 blocs comme "thèmes d'exploration" ou les supprimer complètement? (Proposé: les utiliser en arrière-plan pour s'assurer qu'on explore tout, mais pas explicitement)
- **Q-002**: Comment valider que les insights détectés sont pertinents et non hallucinations?

---
**Created**: 2026-04-26  
**Last Updated**: 2026-04-26
**Phase**: BREAK phase intake initiated with specifications completed
