# Questions & Clarifications — BREAK Phase

## Q-001: Structure des 9 blocs
**Statut**: RÉPONDU  
**Hypothèse**: Garder en arrière-plan comme checklist implicite  
**Réponse utilisateur**: Garder en arrière-plan (checklist implicite) — L'assistant se pose la question en interne 'ai-je exploré tous les thèmes?' mais ne suit pas un ordre linéaire. Garantit la couverture.  
**Implication**: Le prompt diagnostic ne mentionne pas les 9 blocs explicitement, mais l'assistant les utilise comme mental model pour s'assurer qu'on explore tout.

---

## Q-002: Modèle pour diagnostic
**Statut**: RÉPONDU  
**Hypothèse**: Opus 4.7 (~2-3x coût de Sonnet)  
**Réponse utilisateur**: Envisager Sonnet 4.6 (compromis qualité/coût)  
**Implication**: Upgrader diagnostic de Sonnet 4-5 à Sonnet 4.6 pour meilleure analyse et adaptation. Coût modéré, qualité améliorée.

---

## Décisions intégrées dans les specs

| Décision | Impact |
|----------|--------|
| 9 blocs en arrière-plan | Prompt diagnostic plus conversationnel, pas de structure rigide visible |
| Sonnet 4.6 vs Opus | Diagnostic reste intelligent et adaptatif, coût acceptable |
| Métadonnées enrichies | pain_points, patterns_detected, claude_opportunities tracker en temps réel |
| Synthèse stratégique | Pas juste "résumé" mais "analyse + où Claude change la donne" |

---

**Phase BREAK**: ✅ Complétée  
**Prochaine étape**: Phase MODEL avec `/factory-spec`
