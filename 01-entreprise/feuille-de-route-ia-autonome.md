# Feuille de route — Entreprise IA autonome

> Document vivant. Derniere mise a jour : 10 avril 2026.
> Objectif : 80% autonomie CSC, 100% CSD. Trajectoire 1M€ CA.

---

## Protocole de securite — A APPLIQUER AVANT CHAQUE INSTALLATION

Avant d'installer un plugin, repo ou template depuis GitHub :

### Checklist obligatoire

| # | Verification | Comment |
|---|---|---|
| 1 | **Stars & activite** | Repo avec historique, contributors multiples, commits reguliers. Mefiance si < 10 stars et 1 seul contributor. |
| 2 | **Lire le code source** | Parcourir les fichiers principaux (index.js, main.py, etc.). Chercher : `eval()`, `exec()`, requetes HTTP vers des domaines inconnus, acces fichiers sensibles (`~/.ssh`, `~/.env`, credentials). |
| 3 | **Verifier les dependances** | Lire package.json / requirements.txt. Googler les packages inconnus. Chercher typosquatting (ex: `lodash` vs `lodas`). |
| 4 | **Issues & PR ouvertes** | Verifier les issues pour des signalements de securite. |
| 5 | **Licence** | MIT ou Apache 2.0 = OK. Pas de licence = mefiance. BSL 1.1 = lire les restrictions. |
| 6 | **Tester en isolation** | Installer d'abord sur un environnement de test (branch Docker separee ou VPS staging) avant de deployer en prod. |
| 7 | **Pas de secrets en clair** | Ne jamais commiter de cles API dans un repo. Verifier que les `.env.example` ne contiennent pas de vraies cles. |
| 8 | **Scanner automatique** | Lancer `npm audit` (Node) ou `pip audit` (Python) apres installation. |

### Signaux d'alerte (STOP immediate)

- Repo cree il y a < 7 jours avec beaucoup de stars (achat de stars)
- Demande de permissions excessives (acces SSH, root, tous les scopes OAuth)
- Obfuscation du code (variables incomprehensibles, code minifie sans source)
- Redirections vers des domaines hors du scope du projet
- Fork d'un repo populaire avec des modifications non documentees

---

## Phase 0 — Fondations & deblocage (Semaine 1)

**Objectif** : Rendre le systeme Paperclip fonctionnel. Agents capables d'executer des taches reelles.

### Actions

| # | Tache | Statut | Detail |
|---|---|---|---|
| 0.1 | Fixer les budgets agents | A FAIRE | CEO/DAF : 100€/mois. Autres : 50€/mois. Via `PATCH /api/agents/{id}`. |
| 0.2 | Verifier MCP Tools dans Docker | A FAIRE | SSH sur VPS. Tester Gmail, Calendar, Supabase depuis le container. Documenter ce qui fonctionne. |
| 0.3 | Creer 3 projets dans Paperclip | A FAIRE | "Clients Actifs", "Pipeline Commercial", "Ops Internes". Via l'API ou l'UI. |
| 0.4 | Debloquer les agents en erreur | A FAIRE | Heartbeat manuel sur les agents encore en status `error`. |
| 0.5 | Mettre a jour Paperclip | A EVALUER | Version actuelle : `2026.325.0`. Derniere : `v2026.403.0`. Evaluer si la mise a jour apporte des corrections critiques. |

### Indicateur de succes
- [ ] Au moins 1 agent (CEO) execute un heartbeat complet avec une action reelle (pas 0 turns).

---

## Phase 1 — Premier agent autonome : le CEO (Semaine 2-3)

**Objectif** : Le CEO produit un briefing quotidien utile, envoye sur Telegram, sans intervention humaine.

### Actions

| # | Tache | Statut | Detail |
|---|---|---|---|
| 1.1 | Configurer le SOUL.md du CEO | A FAIRE | S'inspirer du template [openclaw-starter-kit](https://github.com/jeffweisbein/openclaw-starter-kit) pour la structure. Adapter au contexte CS Consulting. |
| 1.2 | Connecter Paperclip → Telegram | A FAIRE | Utiliser le workflow n8n existant (`telegram-debrief-claude-supabase.json`) ou creer un webhook Paperclip → Telegram Bot. |
| 1.3 | Definir le heartbeat CEO | A FAIRE | Matin 8h : briefing clients + pipeline. Soir 18h : recap de la journee. S'inspirer de la philosophie "scripts are free, model time is expensive" du starter-kit. |
| 1.4 | Implementer la memoire persistante | A FAIRE | Creer `/paperclip/workspaces/csc/MEMORY.md` avec le pattern du starter-kit : fichiers daily + long-term curate. |
| 1.5 | Test cycle complet | A FAIRE | Lundi : laisser le CEO tourner 24h. Mardi : evaluer la qualite des briefings. Iterer. |

### Repos GitHub utiles pour cette phase

| Repo | Utilite | Securite |
|---|---|---|
| [jeffweisbein/openclaw-starter-kit](https://github.com/jeffweisbein/openclaw-starter-kit) | Patterns SOUL.md, HEARTBEAT.md, MEMORY.md | OK — MIT, 1 contributor mais code lisible, pas de dependances externes |
| [mergisi/awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) | 199 templates SOUL.md copier-coller | OK — MIT, templates statiques (pas de code execute) |

### Indicateur de succes
- [ ] Catherine recoit un briefing Telegram utile chaque matin pendant 5 jours consecutifs sans intervenir.

---

## Phase 2 — Equipe operationnelle CSC (Semaine 4-8)

**Objectif** : DAF, Commercial, Customer Success et Session Report fonctionnent en autonomie sur les taches repetitives.

### Sous-phase 2A : DAF (Semaine 4-5)

| # | Tache | Statut | Detail |
|---|---|---|---|
| 2A.1 | Connecter la facturation | A FAIRE | Agent DAF accede aux donnees Stripe/factures via MCP ou n8n. |
| 2A.2 | Automatiser le suivi paiements | A FAIRE | Relance automatique a J+14 impaye. Notification Catherine si > 500€. |
| 2A.3 | Dashboard financier | A FAIRE | Le fichier `dashboard-financier.html` existe deja — le connecter aux vraies donnees. |

### Sous-phase 2B : Commercial (Semaine 5-6)

| # | Tache | Statut | Detail |
|---|---|---|---|
| 2B.1 | Evaluer openclaw-crm | A FAIRE | [giorgosn/openclaw-crm](https://github.com/giorgosn/openclaw-crm) — Next.js + PostgreSQL. SECURITE : verifier les dependances, tester en local avant deploiement VPS. |
| 2B.2 | Configurer le pipeline commercial | A FAIRE | Etapes : Lead → Qualifie → Diagnostic propose → Signe → En cours. |
| 2B.3 | Automatiser la prospection | A EVALUER | [iPythoning/b2b-sdr-agent-template](https://github.com/iPythoning/b2b-sdr-agent-template) — template SDR B2B. SECURITE : 2 contributors dont "claude" (genere par IA), verifier chaque script shell manuellement. |
| 2B.4 | Connecter LinkedIn Content | A FAIRE | Agent LinkedIn produit du contenu → validation Catherine → publication. |

### Sous-phase 2C : Customer Success (Semaine 6-7)

| # | Tache | Statut | Detail |
|---|---|---|---|
| 2C.1 | Automatiser les CR de session | A FAIRE | Agent Session Report genere les CR apres chaque session coaching. Template existant dans `skills/session-report/`. |
| 2C.2 | Suivi satisfaction client | A FAIRE | Agent Customer Success envoie un check-in hebdomadaire aux clients actifs. |
| 2C.3 | Onboarding automatise | A FAIRE | Le skill `client-onboarding` existe — le connecter a Paperclip. |

### Repos GitHub utiles pour cette phase

| Repo | Utilite | Securite | Verdict |
|---|---|---|---|
| [giorgosn/openclaw-crm](https://github.com/giorgosn/openclaw-crm) | CRM self-hosted pour agents | MIT, 49 stars, stack connue (Next.js/PG) | A AUDITER avant deploiement |
| [MaestroAgent/maestro](https://github.com/MaestroAgent/maestro) | RevOps multi-agents, CRM SQLite | MIT, 11 stars, 1 contributor | PRUDENCE — tester en isolation d'abord |
| [iPythoning/b2b-sdr-agent-template](https://github.com/iPythoning/b2b-sdr-agent-template) | Template SDR B2B multi-canal | MIT, 26 stars, scripts shell | AUDIT APPROFONDI des scripts shell requis |

### Indicateur de succes
- [ ] 3 agents CSC produisent du travail utile par semaine sans intervention.
- [ ] Pipeline commercial visible avec au moins 5 leads en suivi actif.

---

## Phase 3 — Plugins Paperclip & infrastructure (Semaine 6-10)

**Objectif** : Enrichir Paperclip avec les plugins pertinents pour l'autonomie.

### Actions

| # | Tache | Statut | Detail |
|---|---|---|---|
| 3.1 | Lire le livre "Headcount Zero" | A FAIRE | [AnthonyDavidAdams/zero-employee-company-book](https://github.com/AnthonyDavidAdams/zero-employee-company-book) — 151 stars, open-source, pas de code a executer (texte uniquement). |
| 3.2 | Evaluer company-wizard | A EVALUER | [paperclip-plugin-company-wizard](https://github.com/yesterday-ai/paperclip-plugin-company-wizard) — 89 stars, MIT, 2 contributors. SECURITE : auditer le code TypeScript avant install. |
| 3.3 | Installer oh-my-paperclip | A EVALUER | Bundle de plugins. SECURITE : chaque plugin du bundle doit etre verifie individuellement. |
| 3.4 | Evaluer plugin Slack/Telegram | A EVALUER | Pour les notifications agents. Verifier les scopes OAuth demandes. |
| 3.5 | Etudier wshobson/agents | A FAIRE | [wshobson/agents](https://github.com/wshobson/agents) — 33k stars, 50 contributors. Strategie 3 tiers Opus/Sonnet/Haiku pour optimiser les couts. Applicable a nos 12 agents. |
| 3.6 | Optimiser les couts API | A FAIRE | Actuellement tous les agents sur claude-sonnet-4-6. Passer les taches simples (rappels, notifications) sur claude-haiku-4-5. |

### Decision d'architecture : Paperclip plugins vs n8n

| Critere | Plugin Paperclip natif | Workflow n8n |
|---|---|---|
| Integration | Directe dans le dashboard | Webhook externe |
| Flexibilite | Limitee au plugin | Totale (800+ nodes) |
| Maintenance | Dependante de la version Paperclip | Independante |
| Securite | Code execute dans le container | Isole sur sa propre instance |
| **Recommandation** | **Notifications simples** | **Workflows complexes (facturation, CRM, multi-etapes)** |

### Indicateur de succes
- [ ] Au moins 2 plugins Paperclip installes et fonctionnels.
- [ ] Strategie de couts API documentee (quel modele pour quel agent).

---

## Phase 4 — Produits scalables (Mois 3-4)

**Objectif** : Lancer l'etage 2 du modele economique — produits numeriques qui scalent sans temps Catherine.

### Actions

| # | Tache | Statut | Detail |
|---|---|---|---|
| 4.1 | Automatiser CS Digital Setup | A FAIRE | Le produit a 149€ doit etre delivrable a 90% par les agents. |
| 4.2 | Creer des playbooks vendables | A FAIRE | Packager les process internes (onboarding, audit IA, roadmap) en produits. S'inspirer de [slavingia/skills](https://github.com/slavingia/skills) pour le format skills. |
| 4.3 | Lancer Agent-as-a-Service | A EVALUER | Offre a 500€/mois : un agent configure et maintenu pour le client. Necessite une infra multi-tenant. |
| 4.4 | Explorer les marketplaces agents | A EVALUER | [ClipMarts](https://clipmarts.com/) vend des templates a 79€. Possibilite de vendre nos propres templates de consulting IA. |

### Repos GitHub utiles pour cette phase

| Repo | Utilite | Securite |
|---|---|---|
| [slavingia/skills](https://github.com/slavingia/skills) | Methodologie entrepreneur pour structurer les produits | OK — 7.6k stars, texte/prompts uniquement |
| [ertugrulakben/cashclaw](https://github.com/ertugrulakben/cashclaw) | Modele de monetisation autonome via marketplace | A AUDITER — 214 stars, connecte a HYRVE (API tierce) |
| [moltlaunch/cashclaw](https://github.com/moltlaunch/cashclaw) | Agent "prend travail → fait → se fait payer" | A AUDITER — 935 stars, connecte a Moltlaunch/Stripe |

### Indicateur de succes
- [ ] 1 produit scalable genere des ventes sans intervention Catherine.
- [ ] 10 CS Digital Setup livres en un mois.

---

## Phase 5 — CS Digital Apps autonome (Mois 4-5)

**Objectif** : CSD passe de coquille vide a company fonctionnelle et autonome a 100%.

### Actions

| # | Tache | Statut | Detail |
|---|---|---|---|
| 5.1 | Definir le produit CSD | A FAIRE | App/SaaS pour les clients consulting ? Portail client ? Outil interne vendu en marque blanche ? |
| 5.2 | Restructurer les 4 agents CSD | A FAIRE | Definir des SOUL.md precis pour CEO, Product Manager, Marketing, Developer. |
| 5.3 | Pipeline de dev autonome | A EVALUER | [ShunsukeHayashi/Miyabi](https://github.com/ShunsukeHayashi/Miyabi) — Issue GitHub → Code → Test → PR automatique. SECURITE : 21 stars, 5 contributors, code TypeScript a auditer. |
| 5.4 | Connecter au repo GitHub | A FAIRE | Les agents CSD poussent du code, creent des PRs, Catherine valide. |

### Indicateur de succes
- [ ] CSD livre un premier produit fonctionnel.
- [ ] Cycle Issue → PR → Deploy fonctionne sans intervention humaine.

---

## Phase 6 — Scale vers 1M€ (Mois 5-12)

**Objectif** : Activer l'etage 3 du modele economique. Revenus recurrents haute valeur.

### Actions

| # | Tache | Statut | Detail |
|---|---|---|---|
| 6.1 | Lancer les cohortes | A FAIRE | Groupes de 8-10 entrepreneurs, 8 000€/pers, anime par Catherine + agents IA pour le suivi. |
| 6.2 | Creer la licence CS Digital OS | A FAIRE | Systeme complet (agents + workflows + templates) a 2 000€/mois pour les entreprises. |
| 6.3 | Automatiser l'acquisition | A FAIRE | Tunnel complet : contenu LinkedIn (agent) → lead magnet → diagnostic auto → proposition. |
| 6.4 | Monitoring financier temps reel | A FAIRE | Dashboard qui suit CA, MRR, couts API, ROI par agent. |
| 6.5 | Documenter le modele | A FAIRE | Ecrire le "playbook CS Consulting" vendable comme produit. |

### Projection financiere

| Etage | Source | CA annuel cible |
|---|---|---|
| 1 | Consulting premium (Acceleration + Diagnostics) | 370 000€ |
| 2 | Produits scalables (Setup + Playbooks + AaaS) | 194 000€ |
| 3 | Recurrents haute valeur (Cohortes + Licences) | 464 000€ |
| **Total** | | **1 028 000€** |

### Indicateur de succes
- [ ] MRR > 30 000€.
- [ ] Temps Catherine < 20h/semaine sur l'operationnel (80% autonomie reelle).

---

## Suivi global

### Metriques cles a tracker

| Metrique | Actuel (10/04/2026) | Cible Phase 0 | Cible Phase 2 | Cible Phase 6 |
|---|---|---|---|---|
| Agents fonctionnels | 0/12 | 1/12 | 6/12 | 12/12 |
| Budgets configures | 0/12 | 12/12 | 12/12 | 12/12 |
| MCP Tools verifies | 0/3 | 3/3 | 3/3 | 3/3 |
| Clients actifs | 5 | 5 | 8 | 20+ |
| CA mensuel | ~12 500€ | ~12 500€ | ~18 000€ | ~85 000€ |
| Temps Catherine ops | 100% | 90% | 60% | 20% |
| Plugins Paperclip | 0 | 0 | 2+ | 5+ |
| Produits scalables | 0 | 0 | 0 | 3+ |

### Registre des installations (securite)

| Date | Repo/Plugin | Audit fait | Resultat | Installe |
|---|---|---|---|---|
| — | — | — | — | — |

> Chaque ligne ajoutee ici APRES verification du protocole de securite ci-dessus.

---

## Repos GitHub — Reference rapide

### Priorite haute (a explorer en premier)

| Repo | Stars | Utilite | Lien |
|---|---|---|---|
| Headcount Zero (livre) | 151 | Methodologie zero-employe | [GitHub](https://github.com/AnthonyDavidAdams/zero-employee-company-book) |
| awesome-paperclip | 234 | Catalogue plugins Paperclip | [GitHub](https://github.com/gsxdsm/awesome-paperclip) |
| company-wizard | 89 | Bootstrap company Paperclip | [GitHub](https://github.com/yesterday-ai/paperclip-plugin-company-wizard) |
| openclaw-crm | 49 | CRM pour agents IA | [GitHub](https://github.com/giorgosn/openclaw-crm) |
| wshobson/agents | 33k | 182 agents + strategie couts | [GitHub](https://github.com/wshobson/agents) |
| slavingia/skills | 7.6k | Methodologie entrepreneur | [GitHub](https://github.com/slavingia/skills) |

### Priorite moyenne (evaluer quand le socle fonctionne)

| Repo | Stars | Utilite | Lien |
|---|---|---|---|
| openclaw-starter-kit | — | Templates SOUL.md/MEMORY.md | [GitHub](https://github.com/jeffweisbein/openclaw-starter-kit) |
| awesome-openclaw-agents | — | 199 templates SOUL.md | [GitHub](https://github.com/mergisi/awesome-openclaw-agents) |
| b2b-sdr-agent-template | 26 | Pipeline commercial B2B | [GitHub](https://github.com/iPythoning/b2b-sdr-agent-template) |
| Maestro | 11 | RevOps multi-agents | [GitHub](https://github.com/MaestroAgent/maestro) |
| oh-my-claudecode | 26k | Orchestration Claude Code | [GitHub](https://github.com/Yeachan-Heo/oh-my-claudecode) |

### Priorite basse (inspiration / veille)

| Repo | Stars | Utilite | Lien |
|---|---|---|---|
| cashclaw (moltlaunch) | 935 | Agent freelance autonome | [GitHub](https://github.com/moltlaunch/cashclaw) |
| cashclaw (ertugrulakben) | 214 | Skills monetisation HYRVE | [GitHub](https://github.com/ertugrulakben/cashclaw) |
| SynthOrg | 4 | Framework orgs synthetiques | [GitHub](https://github.com/Aureliolo/synthorg) |
| Miyabi | 21 | Issue → PR automatique | [GitHub](https://github.com/ShunsukeHayashi/Miyabi) |
| awesome-ai-agents-2026 | — | Liste 340+ outils IA | [GitHub](https://github.com/caramaschiHG/awesome-ai-agents-2026) |

---

## Principes directeurs (rappel)

1. **Catherine garde le controle** : 100% relation client + strategie. Les agents gerent l'admin.
2. **Un agent a la fois** : Prouver la valeur du CEO avant d'activer les autres.
3. **Securite d'abord** : Aucune installation sans audit. Le protocole ci-dessus est non-negociable.
4. **Le consulting nourrit la machine** : Les revenus actuels financent l'infra IA. Les produits digitaux scalent.
5. **Pas de modif Paperclip sans validation Catherine** : Je propose, tu valides, j'execute.
6. **Iterer** : Cette feuille de route evolue. Chaque phase est validee avant de passer a la suivante.
