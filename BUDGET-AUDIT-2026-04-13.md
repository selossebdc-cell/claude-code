# Budget Audit — Paperclip vs Anthropic Réel
**Date** : 13 avril 2026  
**Période analysée** : 15 mars → 13 avril 2026

---

## 📊 Coûts Réels Anthropic
| Métrique | Montant |
|----------|---------|
| **Total réel** | $198.79 USD (~183 EUR) |
| **Projection mensuelle** | ~$206 USD (~190 EUR) |
| **Moyenne quotidienne** | $6.85 USD |

### Top consommateurs
1. **CS - Consulting Dev** : $87.83 (44%) — À identifier
2. **OpenClaw** : $42.26 (21%)
3. **Anthropic - Claude API** : $41.71 (21%)

---

## 🚨 Discordance Paperclip

### Budgets Paperclip actuels (cents USD)
| Agent | Budget | Dépensé | Ratio |
|-------|--------|---------|-------|
| CEO | 800¢ | **1453¢** | **182%** ⚠️ |
| AI Ops | 200¢ | 295¢ | 147% |
| Commercial | 200¢ | 334¢ | 167% |
| Customer Success | 200¢ | 229¢ | 114% |
| DAF | 200¢ | 117¢ | 58% |
| Process Optimizer | 100¢ | 113¢ | 113% |
| LinkedIn Content | 100¢ | 55¢ | 55% |
| Session Report | 100¢ | 64¢ | 64% |

**TOTAL BUDGETS PAPERCLIP** : ~1900¢ = $19 USD/mois ✓ (roughly correct)  
**MAIS : Les alertes Telegram rapportent des valeurs en EUR 10x plus élevées** ❌

### Exemple
- **Paperclip API dit** : CEO spentMonthlyCents = 1453 (= $14.53)
- **Alerte Telegram dit** : CEO = 1337€ / 800€ (177% overage)
- **Anthropic Console dit** : ~$143.95 total pour TOUTE l'org

---

## 🔧 Actions tentées

### 1. Reset budgets (échoué)
Tentative de PATCH API : `curl -X PATCH /api/companies/{id}/agents/{agentId}` avec nouveaux budgets
- **Résultat** : Requête acceptée (200), mais changements **non persistés** après restart container
- **Hypothèse** : Les budgets sont gérés par la DB Postgres embarquée, pas mis à jour par l'API PATCH

### 2. Ralentir CEO heartbeat (non appliqué)
Tentative de passer `intervalSec` de 7200 (2h) → 21600 (6h)
- **Résultat** : Non appliqué (même raison que ci-dessus)

### 3. Désactiver alertes Telegram (en cours)
À déterminer : où sont les alertes déclenchées ?

---

## 🎯 Recommandations

1. **Vérifier avec Paperclip support** :
   - Pourquoi les PATCH API ne persistent pas ?
   - Comment sont calculés les coûts `spentMonthlyCents` ?
   - Comment synchroniser avec Anthropic cost-events ?

2. **Alerte Telegram** :
   - Quelle est la source des montants en EUR ?
   - Y-a-t-il un taux de change configuré incorrectement ?

3. **Court terme** :
   - Ignorer les alertes Telegram (elles ne reflètent pas la réalité)
   - Utiliser la console Anthropic comme source de vérité ($206/mois)
   - Monitorer les usages réels via le CSV Anthropic

---

## 📝 Notes techniques

- **Paperclip instance** : 187.77.175.238 (srv1454821.hstgr.cloud)
- **API endpoint** : http://localhost:3100/api/companies/{companyId}/agents
- **DB** : PostgreSQL embarquée @ /paperclip/instances/default/db
- **Container** : paperclip-3b9d-paperclip-1
- **Token API** : pcp_board_8005a91dc825648c8cdb4a7d9d2fc3bdb732a7b0fe65f4b8 (visible en base64 :/) )

---

## ⚠️ Sécurité

- API tokens en dur dans les configurations agent (ANTHROPIC_API_KEY visible dans JSON API)
- À vérifier si ces données sortent en logs ou webhooks
