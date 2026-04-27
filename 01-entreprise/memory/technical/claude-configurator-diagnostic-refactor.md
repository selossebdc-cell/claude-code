---
name: Claude Configurator v2 — Diagnostic Intelligent
description: Refactor diagnostic from linear 9-block questionnaire to adaptive conversation. Detects patterns, pain points, opportunities. Metadata enrichment + strategic synthesis.
type: project
updated: 2026-04-26
---

## Contexte
Claude Configurator est un produit premium (149€) qui génère une config Claude personnalisée en fonction d'un diagnostic client. La v1 avait une approche linéaire (9 blocs fixes) et a crashé lors du diagnostic de Fred après 2.5h.

## Objectif Principal
Transformer le diagnostic en **exploration intelligente et adaptative** qui:
1. Analyse chaque réponse pour détecter patterns, pain points, blocages
2. Pose des questions adaptatives (pas d'ordre linéaire pré-défini)
3. Détecte automatiquement les opportunities où Claude change vraiment la donne
4. Génère une synthèse stratégique (pas juste un résumé) qui justifie le 149€

## Approche Technique
- **9 blocs en arrière-plan** : Identity, Offering, Daily, Challenges, Constraints, Security, Work Style, Voice, Proposals — utilisés comme "checklist implicite" (l'assistant se pose en interne "ai-je couvert tous les thèmes?") mais pas d'ordre linéaire visible
- **Métadonnées enrichies** : tracker pain_points, patterns_detected, work_style_traits, claude_opportunities, assumptions_validated en temps réel
- **Strategic synthesis** : Pas "résumé de ce qui a été dit" mais "voici ce que j'ai compris de vous, voici où Claude devient vraiment game-changer"
- **Model choice** : Sonnet 4.6 (balance qualité/coût, meilleure analyse que Sonnet 4-5)

## Résultats Attendus
- Diagnostic complet en 1-1.5h max
- Config hyper-spécifique (comparable à config Fred)
- Aucun crash (message compression + chunked generation)
- Metadata extractibles pour generate-config

## Why
Le diagnostic linéaire classique génère des configs génériques. Fred a validé une config vraiment transformatrice — c'est le standard de qualité attendu pour tous les clients.

## How to apply
Lors du prochain développement de features diagnostic:
- Toujours utiliser Factory methodology (BREAK > MODEL > ACT > DEBRIEF)
- Valider specs contre Fred standard avant implémentation
- Implémenter pattern detection + opportunity recognition comme core logic
