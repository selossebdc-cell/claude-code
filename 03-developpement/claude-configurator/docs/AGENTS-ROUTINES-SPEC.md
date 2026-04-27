# Agents & Routines Specification

## Overview
Ce document définit lesquels des agents et routines sont **obligatoires** vs **contextuels** dans la config générée.

---

## Agents

### ✅ OBLIGATOIRES (Always Present)

| Agent | Rôle | Description |
|-------|------|-------------|
| **Miroir** | Self-awareness | Vos patterns, forces, blocages, rituels qui marchent. Vous aide à vous connaître. |
| **Garde-Fou** | Security/Compliance | Antiphishing absolue, RGPD stricte, responsabilité produit, transactions sécurisées. |
| **Admin** | Operations | Documents, correspondance, templates, automation, zéro rigidité. |
| **Stratégie** | Strategic Direction | Stratégie entreprise, roadmap, vision, orientation long-terme. |
| **Planif** | Planning & Timeline | Planning, timeline, jalons, étapes, structuration des projets. |
| **Amélioration Continue** | Continuous Improvement | Debriefs, retours d'expérience, optimisations, cycles d'amélioration. Vous aide à progresser systématiquement. |

**Implication**: Chaque config générée MUST inclure ces 6 agents, peu importe le contexte client.

---

### 🟡 CONTEXTUELS (Proposed if Context Matches)

| Agent | Trigger Condition | Description |
|-------|-------------------|-------------|
| **Coach** | IF client needs progress tracking OR weekly structure | Debriefs hebdos, mesure progrès par marché/domaine, défis pertinents. Proposer si pain_point = "pas de suivi". |
| **Ingénieur** | IF client has technical/compliance complexity | Conformité produit, validation multi-pays, cartographie réglementaire, architecture. Proposer si pain_point = "compliance" ou "technical validation". |
| **Autres** | Future | Réservé pour besoins spécifiques (ex: Agent Créatif, Agent Finance, etc.). À définir au cas par cas. |

**Logique**: Ces agents sont proposés SEULEMENT si patterns/pain_points détectés pendant diagnostic le justifient.

---

## Projects & Systems

### ✅ OBLIGATOIRE

| Project | Purpose |
|---------|---------|
| **"Ma Mémoire"** | Centralized hub that all agents consult. Contains: who you are, how you operate, what works, what blocks, security rules, weekly progress. Single source of truth. |

**Implication**: MUST be created in every config, populated with client-specific insights.

---

## Routines (Scheduled Tasks)

### ✅ OBLIGATOIRE (At Least One)
Every config MUST have at least 1 scheduled routine.

### 🟡 CONTEXT-DEPENDENT (Propose All Three)
Suggest Daily, Weekly, Monthly routines based on client's work style + pain points.

| Routine | Default Time | Trigger | Content |
|---------|--------------|---------|---------|
| **Daily** | 6:30am (or client's morning) | Every day | Briefing: priorities, alerts, focus for the day |
| **Weekly** | Thursday 5pm (or client's preference) | Every week | Debrief: progress, blockers, lessons, next week plan |
| **Monthly** | 1st of month @ 9am | Every month | Compliance alert, metrics review, strategic check-in |

**Proposal Logic**:
- If client works daily: suggest Daily routine
- If client mentioned weekly reviews: suggest Weekly routine
- If client has compliance obligations: suggest Monthly routine
- Default: suggest all three, let client opt-out

---

## Custom Instructions

### ✅ OBLIGATOIRE

**What is it**: A global configuration for Claude Pro (not an agent, not a project).  
Defined once, applies to ALL conversations with Claude.

**Content** (2000+ characters):
- Who you are (role, title, context)
- How you operate (style, preferences, decision-making)
- Your 3 main challenges
- Your non-negotiable rules
- Communication preferences (tables > text, pragmatic > theoretical)

**Example for Fred**:
```
Qui tu es:
- Ingénieur inventeur, export 40 pays
- Pragmatique & innovant

Comment tu fonctionnes:
- 6h-10h productifs, au feeling informé
- Deadlines = motivation
- Prefer pragmatic action over theory

Tes 3 défis:
1. Conformité multi-régionale
2. Innovation rapide sans doc lourde
3. Gestion commerciale export

Tes règles:
- Zéro bullshit
- Tables > text
- Chiffres > théories
- Brouillons relisibles
```

**Implication**: MUST be generated (never empty or generic). Highly specific to client's context.

---

## Summary Table

| Element | Status | Frequency | Notes |
|---------|--------|-----------|-------|
| Agent Miroir | ✅ Mandatory | Always | Core to self-awareness |
| Agent Garde-Fou | ✅ Mandatory | Always | Core to security |
| Agent Admin | ✅ Mandatory | Always | Core to operations |
| Agent Stratégie | ✅ Mandatory | Always | Core to direction |
| Agent Planif | ✅ Mandatory | Always | Core to execution |
| Agent Amélioration Continue | ✅ Mandatory | Always | Core to continuous progress |
| Agent Coach | 🟡 Contextual | If progress tracking needed | Triggered by patterns |
| Agent Ingénieur | 🟡 Contextual | If technical complexity | Triggered by pain_points |
| Ma Mémoire Project | ✅ Mandatory | Always | Single source of truth |
| Custom Instructions | ✅ Mandatory | Once (global) | Global configuration |
| Daily Routine | 🟡 Proposed | If client needs it | At least 1 routine required |
| Weekly Routine | 🟡 Proposed | If client needs it | Suggest all 3, client chooses |
| Monthly Routine | 🟡 Proposed | If client needs it | Suggest all 3, client chooses |

---

## Implementation Notes

### For Diagnostic Prompt
When generating config recommendation (strategic synthesis), ensure:
1. All 5 mandatory agents are listed + described
2. Contextual agents (Coach, Ingénieur) are proposed with reasoning
3. Ma Mémoire project is highlighted as hub
4. Custom Instructions section is drafted with client specifics
5. All 3 routines are proposed; indicate which is minimum required

### For Generate-Config v20+
When generating the actual config:
1. Mandatory agents: generate in full (system prompts, instructions)
2. Contextual agents: generate only if diagnostic recommends them
3. Ma Mémoire: always generate (populate with diagnostic metadata)
4. Custom Instructions: always generate (specific to client)
5. Routines: include at minimum 1 (suggest all 3 as options)

### For Acceptance Criteria
Validation checklist:
- [ ] 5 mandatory agents present in config
- [ ] Ma Mémoire project created & populated
- [ ] Custom Instructions drafted (2000+ chars, specific)
- [ ] At least 1 routine scheduled
- [ ] If Coach/Ingénieur proposed, reasoning documented
- [ ] Config density comparable to Fred's reference

---

**Created**: 2026-04-27  
**Status**: Part of MODEL phase specs  
**Next**: Update PLAN phase to reference this specification
