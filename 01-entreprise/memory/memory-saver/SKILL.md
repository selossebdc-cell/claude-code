# Memory Saver: End-of-Session Auto-Memory

## Vue d'ensemble
Ce skill s'exécute automatiquement en fin de session (via hook Claude Code) et:
1. **Analyse la conversation** pour identifier ce qui mérite d'être mémorisé
2. **Vérifie les mémoires existantes** et leur fraîcheur
3. **Propose des mises à jour** intelligentes (ajouts, modifications, suppressions)
4. **Sauvegarde automatiquement** les changements

## Processus

### Phase 1: Scanner la conversation
- Extraire les patterns de:
  - Ce que l'utilisateur a dit sur lui-même (rôle, expertise, préférences)
  - Feedback que l'utilisateur a donné sur mon approche
  - État des projets / initiatives mentionnées
  - Ressources externes (outils, systèmes, URLs)

### Phase 2: Analyser les mémoires existantes
Pour chaque mémoire trouvée dans `.claude/memory/`:
- Lire le frontmatter (name, description, type, date)
- Extraire la date de dernière modification
- **ALERTER** si:
  - Mémoire non mise à jour depuis > 6 mois (probablement périmée)
  - Contenu contredit ce qu'on vient d'apprendre
  - Références à des outils/fichiers qui n'existent plus

### Phase 3: Proposer les mises à jour
Pour chaque élément détecté:
- Si nouvelle information → créer une mémoire
- Si met à jour une mémoire existante → proposer la modification
- Si contredit une mémoire → signaler et proposer correction
- Si suppression recommandée → notifier

### Phase 4: Sauvegarder
- Créer/modifier les fichiers mémoire avec nouveau timestamp
- Mettre à jour MEMORY.md si structure change
- Afficher un résumé final: "✓ N mémoires créées/mises à jour, M mémoires périmées détectées"

## Format des mémoires

**Frontmatter obligatoire:**
```markdown
---
name: Nom court
description: Une ligne — hook pour relevance future
type: user | feedback | project | reference
updated: 2026-04-26
---

Contenu de la mémoire
```

**Structure recommandée pour feedback/project:**
- Énoncé du fait/règle
- **Why:** la raison (passée, contrainte, préférence)
- **How to apply:** quand/où utiliser

## Cas d'alerte

- 🔴 **Contradiction détectée** — une mémoire dit X mais conversation dit Y
- 🟡 **Potentiellement périmée** — pas mise à jour depuis 6+ mois
- 🟢 **À créer** — nouvelle information sans mémoire correspondante
- 🗑️ **À supprimer** — référence à quelque chose qui n'existe plus

## Résumé de sortie

Afficher:
```
📝 Mémoires: résumé des changements
─────────────────────────────
✓ 2 créées
✓ 1 mise à jour
🟡 1 potentiellement périmée (last updated: 2025-10-15)
🔴 0 contradictions
```

Si l'utilisateur confirme, appliquer et sauvegarder. Sinon, montrer les propositions en attente.
