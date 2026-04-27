---
name: Factory Methodology — Adoption Validée
description: Catherine a confirmé l'utilisation obligatoire de Spec-to-Code Factory pour tous les développements. Approche BREAK > MODEL > ACT > DEBRIEF avec gates de validation.
type: feedback
updated: 2026-04-26
---

## Feedback de l'utilisateur
Catherine a explicitement demandé: "je veux que tu utilises les skills spec to factory. Pour développer vraiment un outil performant."

Message complet contexte: "on est d'accord que là, tu utilises l'outil de développement et aussi sur la réflexion pour configurer la stratégie de cet outil... tu es aussi avec opus 4.7."

Réponse: "oui c'est exactement ce que je veux."

## Décision
✅ **Factory methodology est OBLIGATOIRE** pour tous les développements Claude Configurator (et probablement tous les projets techniques à CS Consulting).

## Pipeline Confirmé
1. **BREAK** (factory-intake): Analyse requirements, pose questions clarification
2. **MODEL** (factory-spec): Génère specs techniques (brief.md, scope.md, acceptance.md)
3. **PLAN** (factory-plan): Planning épics, user stories, tasks
4. **BUILD** (factory-build): Implémentation avec commits référencés par task ID
5. **DEBRIEF** (factory-qa): QA + release validation

## Core Principles
- "No Spec, No Code" — specs verrouillées avant coding
- "No Task, No Commit" — chaque commit référence un task ID
- Auto-remediation: 3x retry per gate avant intervention manuelle

## Why
Catherine veut un outil réellement performant et bien pensé. Factory force une rigueur de conception qui prévient les rework.

## How to apply
- Avant TOUTE ligne de code: exécuter /factory (ou /factory-intake si déjà en cours)
- Bloquer les "quick fixes" non-spec — rediriger vers factory si nécessaire
- Lire le SKILL.md du projet (`CLAUDE.md` → Skills section)
