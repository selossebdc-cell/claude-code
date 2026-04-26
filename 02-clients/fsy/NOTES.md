---
name: Notes Client — Face Soul Yoga
description: Contexte client, équipe, contacts, patterns observés, citations clés
---

# Notes Client — Face Soul Yoga (FSY)

**Contact principal** : Aurélia (fondatrice/propriétaire)  
**Équipe opérationnelle** : Laurie (opérationnel), Anam (VA)  
**Statut** : Client — Projet Data/KPI/Automations (23/04/2026)

---

## Profil Client

**Entreprise** : Face Soul Yoga — plateforme de formations vidéo (yoga, sommeil, etc.)

**Marques/Produits** :
- **FSY Studio** : Formation vidéo (17€ mass-market)
- **MTM** : Mastering The Mind (formation)
- **Aurélia Del Sol** : Offre premium coaching Aurélia

**Équipe** :
- Aurélia = validation uniquement, pas d'opérationnel
- Laurie = connexions outils, automations, opérationnel
- Anam = migration vidéos Uscreen → Circle, VA générale

**Taille** : Brevo 13,302 contacts, 19 listes existantes, 2 membres Circle au départ

---

## Contexte du Projet

**Objectif** : Mettre en place une infrastructure data complète pour tracker le parcours client (source → conversion → rétention) sans dépendance Catherine.

**Scope** :
- Automations Brevo (22 templates + 9 workflows n8n)
- Migration Uscreen → Circle (avec subscription preservation)
- Chatbots : Telegram MTM + WhatsApp FSY
- eSignatures intégrées (0,49€/contrat)

**Architecture** :
- **Brevo** : CRM principal (13K+ contacts, segmentation par offre/intérêt/statut)
- **Circle** : Communauté (2 groupes: MTM + FSY Studio)
- **n8n** : Automations (webhooks Stripe → Brevo, Circle sync, email nurture)
- **Stripe** : Paiements
- **eSignatures.com** : Contrats B2B (automatisé)
- **Manychat** : Quiz prospects → Brevo segment
- **Telegram/WhatsApp** : Chatbots support/onboarding

---

## Patterns Observés

**Aurélia = Direction, pas opérationnel**
- Valide contenu, ne fait pas les connexions
- Besoin de processus délégables à Laurie + Anam
- Pense premium (Aurélia Del Sol), FSY pour scale (mass-market)

**Importance data** :
- Aurélia n'avait aucune visibilité sur conversions (13K contacts sans taux known)
- Veut tracker source → conversion → rétention en temps réel
- Intéressée par reporting automata (rapport hebdo validé + envoyé)

**Efficacité opérationnelle** :
- Laurie débordée = besoin d'automations max
- Anam en VA = tâches bien structurées et simples
- Besoin de documentation claire pour chaque outil

---

## Contexte Devis

**Service** : Mise en place infrastructure data + automations + formation  
**Durée** : Sprint serré (audit 06/04 → livraison 23/04 = 17 jours)  
**Livraison** : Jeudi 23 avril 18h (DEADLINE CRITIQUE)

---

## Points de Vigilance

🔴 **CRITIQUE - Deadline 23/04/2026 18h** : Sprint livraison finale en cours

🟠 **Dépendances critiques** :
- Laurie pour Stripe↔Circle connexion + UTM links
- Aurélia pour validation templates + contenu
- Mickaël pour chatbots (timeline très serrée)

🟠 **Escalade si bloquage** :
- Aurélia (validation contenu)
- Laurie (opérationnel Stripe/Circle)
- Catherine (infrastructure/n8n)

---

## Pépites LinkedIn

À extraire après chaque livrables (patterns intéressants pour audience dirigeants TPE).

---

## Historique Sessions

| RDV | Date | Étape | Décision | Livrables |
|-----|------|-------|----------|-----------|
| 1 | 06/04/2026 | Audit initial | Brevo core 9 attrs, 22 templates, 9 workflows n8n | Audit report |
| 2 | 20/04/2026 | Livraison + test | Validation tests, Stripe webhook, migration Uscreen | Planning interactif |
| 3 | 23/04/2026 | Livraison finale | Chatbots + formation équipe | Checklist validation |

