---
name: Fred's Configuration — Quality Reference
description: Fred's personalized Claude Pro setup is the quality baseline for Claude Configurator. Defines what "transformative" means (not generic).
type: reference
updated: 2026-04-26
location: /Users/cath/Downloads/Votre\ configuration\ Claude\ Pro\ —\ Fred.rtfd/TXT.rtf
---

## Config Fred Overview
Fred: Ingénieur Inventeur — Export 40 pays — Pragmatique & Innovant

### Components de la Config Fred (Implémentation Claude-Native)

⚠️ **CRITICAL**: Claude has **NO "Custom Instructions" settings panel**. Everything is code-based in CLAUDE.md + settings.json. There's no UI for this.

1. **Project CLAUDE.md** (Code-based configuration, not UI)
   - Qui Fred est, comment il fonctionne vraiment
   - 6h-10h productifs, au feeling informé, deadlines = motivation
   - 3 défis prioritaires: export, conformité, commercial
   - Règles non-négociables
   - **Implémentation Claude**: CLAUDE.md fichier texte dans le projet (pas de panneau de paramètres)

2. **Project "Ma Mémoire"** ✅ Implémentable
   - Système centralisé consulté par tous les agents
   - Qui Fred est, comment il opère, ce qui marche, ce qui bloque
   - Règles de sécurité, progression hebdomadaire
   - **Implémentation Claude**: `/01-entreprise/memory/client/fred.md` + symlink `~/.claude/memory`

3. **Workflows Spécialisés** (remplace "5 Agents Spécialisés")
   - **Workflow Ingénieur** — Conformité produit, validation multi-pays, cartographie réglementaire
   - **Workflow Admin** — Documents, correspondance, templates, automation
   - **Workflow Introspection** — Patterns, forces, blocages, rituels qui marchent
   - **Workflow Coach** — Debriefs hebdo (jeudi 17h), mesure progrès par marché
   - **Workflow Sécurité** — Antiphishing, RGPD, responsabilité produit, transactions sécurisées
   - **Implémentation Claude**: SKILLs spécialisées + Agent invocations par session

4. **Tâches Programmées** ✅ Implémentable
   - Daily 6h30 (briefing)
   - Weekly jeudi 17h (debrief coach)
   - Monthly 1er du mois (conformité alert)
   - **Implémentation Claude**: `schedule` skill (cron-based) + remote agents

5. **Style "Fred Direct"** ✅ Implémentable
   - Direct, pragmatique, tableaux > texte, chiffres > théories
   - Brouillons relisibles, zéro bullshit
   - **Implémentation Claude**: CLAUDE.md + Memory avec exemples de style préféré

6. **Sécurité Activée** ✅ Implémentable
   - Antiphishing absolu (lecture seule sur fichiers sensibles)
   - RGPD stricte, zéro R&D public
   - Validation avant transactions
   - **Implémentation Claude**: Permissions dans settings.json + Security SKILL

## Why This Is The Standard
Fred's config is **hyper-spécifique** à son contexte réel (ingénieur inventeur, multi-pays, complexité administrative/réglementaire). Not generic "entrepreneur setup" but deeply personal and transformative for Fred's actual daily work.

## How to apply
Pour chaque client diagnostic:
- Comparer la config générée contre la densité et pertinence de Fred's config
- Poser la question: "Est-ce que c'est aussi transformateur pour ce client que Fred's config l'est pour Fred?"
- Si réponse = "non", creuser plus profondément dans le diagnostic (les blocs implicites n'ont pas tous été couverts)

## Implementation Guide for Claude (100% Code-Based, No UI)

⚠️ **Fred**: There is **NO "Custom Instructions" settings panel in Claude**. You configure everything via files:

### What Fred Actually Needs to Do in Claude

**File 1: `.claude/CLAUDE.md`** (in project root)
- Fred's working style + non-negotiables
- Preferred tone (direct, pragmatic, no BS)
- Security rules (antiphishing, RGPD)
- 3 priorities: export, compliance, commercial

**File 2: `.claude/settings.json`** (in project root)
```json
{
  "system_prompt": "You are working with Fred (Ingénieur Inventeur)...",
  "permissions": {
    "security": ["read-only on sensitive files"],
    "automation": ["schedule"]
  },
  "hooks": {
    "sessionStart": "Load ~/claude/memory/client/fred.md",
    "sessionEnd": "/memory-saver"
  }
}
```

**File 3: `~/.claude/memory/client/fred.md`** (in home directory)
- Current priorities + blockers
- Progress tracking by market
- Operational guidelines

**File 4: Scheduled Tasks** (via `schedule` skill)
- Daily 6h30: Briefing
- Weekly Thursday 17h: Coach debrief
- Monthly 1st: Compliance alert

### Files to Deliver to Fred
- **CLAUDE.md** — Project configuration (text file, NOT a settings UI)
- **settings.json** — Project hooks + permissions (text file)
- **~/claude/memory/client/fred.md** — Operational memory file

### ❌ DOES NOT EXIST in Claude
- Custom Instructions UI panel
- Settings → Instructions personnalisées (that's OpenAI)
- No settings UI at all for personalization → use CLAUDE.md instead
