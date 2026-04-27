# Brief — Claude Configurator v2: Diagnostic Intelligent

## Vision
Transformer Claude Configurator d'un questionnaire linéaire en **exploration conversationnelle intelligente** qui détecte patterns, pain points, et opportunités Claude spécifiques en temps réel. Générer des configurations hyper-pertinentes et transformatrices, justifiant le tarif de 149€.

## Problème
La v1 approchait le diagnostic via 9 blocs fixes linéaires (Identity → Offering → Daily → Challenges → Constraints → Security → Work Style → Voice → Proposals). Résultats:
- Configs génériques, pas vraiment transformatrices
- Pas d'adaptation en fonction des réponses
- Pas de détection de patterns émergents
- Fred's diagnostic (2.5h) a crashé sur timeouts message
- Clients ne voyaient pas la value du 149€

## Objectifs
1. **Exploration intelligente** : Questions adaptatives posées en fonction de ce qui émerge (pas d'ordre pré-défini)
2. **Détection active** : Identifier automatiquement pain_points, patterns_detected, claude_opportunities au fur et à mesure
3. **Métadonnées enrichies** : Tracker insights en temps réel pour config generation downstream
4. **Synthèse stratégique** : Générer "où Claude devient vraiment game-changer pour vous" (pas juste résumé)
5. **Robustesse** : Diagnostic 1-1.5h max sans crash (message compression + chunked generation)
6. **Clarté client** : Aider le client à se comprendre lui-même via questions intelligentes

## Périmètre (Inclus)
- Refactor du prompt diagnostic (Sonnet 4.6)
- 9 blocs comme "mental model implicite" (l'assistant vérifie internement "tous les thèmes couverts?")
- Pattern detection logic (blocages récurrents, forces, work style traits)
- Metadata schema enrichie (pain_points[], patterns_detected[], claude_opportunities[])
- Strategic synthesis generator (transforme insights en "où Claude change la donne")
- Message compression fallback (keep last 5 + summarize older)
- Chat Edge Function v20+ compatibility

## Périmètre (Exclus)
- Modification du modèle Claude API
- Changement du pricing (reste 149€)
- Refactor de la config generation engine (v18-19 reste intacte)
- Nouvelle architecture de stockage

## Baseline de Qualité
**Fred's Config** (fournie par client, approuvée comme référence)
- 4400+ caractères Custom Instructions
- 5 agents spécialisés (Ingénieur, Admin, Miroir, Coach, Garde-Fou)
- "Ma Mémoire" project (système centralisé)
- 3 tâches programmées (daily, weekly, monthly)
- Hyper-spécifique à contexte réel (export multi-pays, conformité, innovation)

Critère de succès: Config générée pour nouveaux clients approche la densité + pertinence de Fred's config.

## Timeline
- BREAK phase ✅ (intake + questions.md complété)
- **MODEL phase** (current) → brief.md, scope.md, acceptance.md, DIAGNOSTIC-SPEC.md
- PLAN phase → epics, user stories, tasks
- ACT phase → implementation
- DEBRIEF phase → QA, validation vs Fred standard

---
**Created**: 2026-04-26 (BREAK phase)  
**Updated**: 2026-04-27 (MODEL phase)  
**Status**: MODEL phase in progress
