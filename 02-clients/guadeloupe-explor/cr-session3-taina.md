---
client: Taina THARSIS
entreprise: Guadeloupe Explor
session: 3
date: 2026-04-21
duree: ~2h30
theme: Infrastructure digitale, CRM ESUS & routines IA
lien_fathom: 
prochaine_session: 2026-04-28 14h (8h Guadeloupe)
---

## 🎯 SESSION 3 — Infrastructure digitale, coaching perfectionnisme & setup Playbook

Séance axée sur **3 fronts en parallèle** : finalisation configuration Apple (iCloud, mail, calendrier) + coaching profond sur le perfectionnisme + présentation du Playbook avec bug critique de permissions identifié.

### ✅ CÉLÉBRATIONS

- **Configuration iCloud réussie** : Bureau + Documents synchronisés, import mail complété
- **Calendrier Apple structuré** : multiples calendriers (CPA, Ponant, Structure & Finance, Alternance, personnel)
- **Prise de conscience en action** : Taina a commencé le nettoyage d'archives (suppression 2015-2016 mails, réflexion sur durée de conservation)
- **Coaching perfectionnisme engagé** : identification du pattern + travail en cours avec coach Julien (gratitude, fierté)
- **Playbook partagé** : 3 parcours clients visibles + 50 prestataires identifiés (vs "2 employés" annoncé en S1)
- **Skill "Stratégie" en création** : basée sur doc HTML généré par Claude (séminaire Business Max)
- **Modèles Claude intégrés** : Taina comprend la stratégie Haiku (data) → Opus 4.7 (analyse) = coût-efficace

### 🔄 BLOCAGES / BUGS IDENTIFIÉS

#### 🐛 **BUG CRITIQUE — Permissions Playbook**
- **Problème :** Taina voit les tâches d'autres clients (Aurélia, Laurie, Véa) dans "Mes tâches"
- **Impact :** problème de confidentialité/cloisonnement client grave
- **Cause probable :** erreur de configuration droits lors création Playbook
- **Action requise :** nettoyer permissions + vérifier l'isolation par client

#### ⚠️ **Tutos cassés**
- Les liens ressources ne fonctionnent pas depuis la resécurisation
- À corriger via Michael (développeur)

#### ⚠️ **ESUS + Paiement à vérifier**
- ESUS ne permet que Stripe ou peut-on connecter lien Crédit Mutuel actuel ?
- Comment ESUS sait qu'un paiement via lien bancaire est reçu ?
- À investiguer avec Michael

#### ⚠️ **Enregistrement appels téléphoniques**
- Solution native iOS à chercher ou utiliser Otter.ai
- Nécessaire pour feed Claude (transcription auto)

---

## 🛠️ DÉCISIONS PRISES

### 1️⃣ Infrastructure Apple validée
- ✅ iCloud (premier niveau ~200 Go, 2,99€/mois)
- ✅ Apple Mail (futur : intégrer 3 boîtes contact@ / info@ / ttharsis@)
- ✅ Apple Calendrier (pour vision d'ensemble opérationnelle)

### 2️⃣ Perfectionnisme — prise de conscience & défis
- **Pattern identifié :** besoin de tout garder (10 ans historique) + devis "parfait" = paralysie agence
- **Reframing clé :** "Il y a une marge de progression" ≠ "J'ai échoué"
- **Mantra :** "Mieux vaut une action imparfaite qu'une parfaite inaction"
- **Prochain défi :** identifier limites acceptables par domaine (mails : combien d'années ? Contrats : légal ? Historique client : 2 ans ?)
- **Travail en parallèle :** coach Julien pour gratitude + fierté (2 mois en cours)

### 3️⃣ Playbook B2C DIP — automatisations prioritaires
Le parcours BtoC "Meurtre au Paradis" peut être **massivement automatisé** :

| Étape | État Actuel | Automatisation |
|-------|------------|-----------------|
| Lead entrant | Multiple canaux (mail, WhatsApp, Instagram) | Inbox centralisée (email + chat) |
| Qualification | Manuel | Auto-extraction (nom, date, budget, type) + réponse type |
| Dispo prestataires | 45 min/excursion (appels + WhatsApp) | Chatbot WhatsApp (réponse 2h) |
| Devis | Manuel (Excel + mail) | ESUS génère automatique |
| Paiement | Lien Crédit Mutuel (client choisit montant) | À optimiser avec ESUS/Stripe |
| Choix menu | Mail 1 mois avant (manuel) | Formulaire + compilation auto |
| Relance 50% | Quand Taina n'oublie pas | Auto ESUS (1 mois avant excursion) |
| Bon commande prestataires | Manuel | Auto depuis ESUS |
| Veille avant | Email + SMS | Auto si data dans ESUS |
| Post-excursion | Formulaire alternante | Formulaire feedback + Claude recap |
| Fidélisation | Aucune | Email 6 mois après (offres adaptées) |

### 4️⃣ ESUS = CRM central
- Base données clients + colonne "Menu choisi"
- Tout centralisé (pas de base parallèle)
- Relances auto programmées
- À clarifier : connexion avec lien paiement Crédit Mutuel vs Stripe

### 5️⃣ Claude — stratégie modèles
- **Haiku :** lire documents/data (pas cher tokens)
- **Opus 4.7 :** analyser/synthétiser (le plus performant, tout récent)
- **Pattern :** Haiku lit les 96 pages séminaire → Opus 4.7 génère doc HTML stratégie
- **Résultat :** "Équipe 3 internes + 50 prestataires" (vs "2 employés" S1) → mise à jour mémoire Claude

### 6️⃣ Skill "Stratégie" en création
- Basée sur doc HTML du séminaire Business Max
- Claude recadre conversations dans stratégie globale
- V1 à tester en usage réel avant finalisation

---

## 📋 ACTIONS TAINA (Semaine du 21 — 28 avril)

### Priorité 1 — Nettoyage & structuration données
- [ ] Continuer nettoyage mails (historique : jusqu'où ?)
- [ ] Identifier règles de conservation par domaine (mails : 3 ans ? Contrats : légal ? Historique client : 2 ans ?)
- [ ] Migrer dossier Guadeloupe Explore vers Cloud (actuellement local)
- [ ] Valider doc "Stratégie/Valeurs" + demander à Claude d'intégrer dans mémoire

### Priorité 2 — Finaliser Skill Stratégie
- [ ] Relire doc HTML généré + challenger Claude si corrections nécessaires
- [ ] Créer Skill "Stratégie" via Skill Creator (utiliser doc HTML comme source)
- [ ] Tester V1 en conversation réelle

### Priorité 3 — Préparer ESUS
- [ ] Chercher solution enregistrement appels (native iOS ou Otter.ai)
- [ ] Clarifier ESUS + paiement (Stripe vs Crédit Mutuel)

### À Attendre
- [ ] Correction bug permissions Playbook (Michael / Catherine)
- [ ] Revérifier liens tutos (Michael)

---

## 🎤 ACTIONS CATHERINE

- [ ] **URGENT :** Corriger bug permissions Playbook (cloisonnement clients)
- [ ] **URGENT :** Revérifier liens tutos (resécurisation a cassé les chemins)
- [ ] Investiguer ESUS + paiement (Stripe vs Crédit Mutuel, sync paiements)
- [ ] Envoyer invite RDV #4 (28 avril 14h)

---

## 💭 MINDSET & INSIGHTS

### Le Pattern du Perfectionnisme
> "Tu t'infliges d'être parfaite, mais tu t'obliges aussi à te remettre en question. Parce que pour toi, c'est ça l'évolution. Mais la remise en question, ça veut dire que tu as mal fait. Tu vois le système dans lequel tu t'es mise ?"

**Origines :** Attachement sentimental transmis générationnellement (parents, grands-parents) → Taina en prend conscience et commence à "jeter/donner" plutôt que tout conserver.

**Parallèle pro :** Même pattern : attendre perfection avant d'envoyer un devis = bloquant pour l'agence. Elle le sait : "Ça me ralentit et ça réduit des choses."

### Le Mantra
> "Mieux vaut une action imparfaite qu'une parfaite inaction."

Taina doit le voir régulièrement. C'est là où elle va se libérer.

### Contexte Personnel
- Coach Julien travaille en parallèle (gratitude, fierté, perception)
- Mac ancien (Monterey) → pas Sonoma/Cowork
- iPhone peut nécessiter OS update pour app Claude
- Travaille souvent à la dernière minute (mode de fonctionnement accepté)

---

## 🐛 BUGS À CORRIGER (Priority Order)

| Bug | Severity | Owner | ETA |
|-----|----------|-------|-----|
| Permissions Playbook (voit autres clients) | 🔴 CRITICAL | Michael | ASAP |
| Tutos cassés | 🟡 HIGH | Michael | ASAP |
| ESUS + paiement (Stripe vs CM) | 🟡 HIGH | Catherine + Taina | 28/04 |
| Enregistrement appels | 🟢 MEDIUM | Taina | 28/04 |

---

## 📊 PROCHAINE SESSION
**Date :** Mardi 28 avril 2026, 14h (France) / 8h (Guadeloupe)  
**Focus :** Validation Skill Stratégie + résolution bugs ESUS + premiers tests automatisations

---

## ✨ RESSOURCES CRÉÉES CETTE SÉANCE

- `Perfectionnisme-Phrases-Cles.html` — extraction toutes phrases clés du coaching (à afficher/relire)
- `Compte-rendu-RDV2-avril2026.html` — synthèse complète session

