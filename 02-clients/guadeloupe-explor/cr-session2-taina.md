---
client: Taina THARSIS
entreprise: Guadeloupe Explor
session: 2
date: 2026-04-07
duree: ~110 min (avec interruptions)
theme: Cartographie parcours client & structuration outils
prochaine_session: 2026-04-21 14h (8h Guadeloupe)
---

## SESSION 2 — Cartographie parcours client & structuration outils

Séance dense malgré les interruptions opérationnelles (problème guides au port, Vendredi Saint non anticipé, assistante marketing oubliée sur les documents). Ces interruptions illustrent parfaitement les blocages identifiés en S1.

### CÉLÉBRATIONS
- CS Digital Setup complété (ce matin entre deux RDV — motivation intacte)
- Claude Pro créé et actif
- Premier virement effectué le 04/04 (non reçu encore côté Shine — à surveiller)
- Actions cochées sur le portail client
- Fichier Excel de suivi Meurtre au Paradis en place (depuis 2024-2025)
- Mails types déjà préparés pour le flux contact@ (copier-coller structuré)
- Taina a déjà commencé à réfléchir aux instructions Claude (brouillon vs automatique)
- Décision prise de simplifier l'offre : 2 tours seulement l'an prochain (au lieu de 5-6)

### BLOCAGES CONFIRMÉS / NOUVEAUX
- **3 boîtes mail non centralisées** : contact@ (Meurtre au Paradis), info@ (site web), ttharsis@ (B2B/cartes de visite)
- **Emails en spam** : problème DNS identifié par Claude — double politique DMARC contradictoire. Correctif à envoyer au webmaster
- **Aucun calendrier numérique** : agenda papier depuis 2012 (trauma perte données iPad en Australie)
- **Aucun cloud** : seul Google Drive partagé avec collaborateurs. Pas de sauvegarde NAS ni iCloud
- **Roundcube** : interface mail archaïque, pas UX-friendly, pas d'automatisation possible
- **Pas de facturation individuelle** : une seule facture globale, pas envoyée aux clients → comptable demande facture par client
- **Relances manuelles** : 50% payé → relance manuelle (quand elle n'oublie pas)
- **Feedback clients** : alternante marketing fait les retours, mais dernière campagne le 13/03 — non systématique
- **Prestataires non fiables** : jours fériés Guadeloupe non anticipés, guide qui ne se lève pas, billets de bateau non confirmés → tout repose sur Taina pour vérifier
- **Crédit Mutuel bloquant** : ne répond pas, accès banque en ligne refusé pour l'analyste financier (Abdenasseir), pas de facturation auto

---

## CARTOGRAPHIE DES PARCOURS CLIENTS

### Parcours 1 — BtoC Meurtre au Paradis (via contact@)

**Flux actuel :**
1. Lead arrive via page Facebook "Caribbean Cruises" → mail contact@
2. Taina lit le mail, évalue l'urgence
3. Envoie catalogue Meurtre au Paradis (mail type copié-collé depuis fichier Excel de l'ex-employée)
4. Client choisit une excursion → Taina vérifie disponibilité prestataires (WhatsApp/appels)
5. Envoie lien de paiement Crédit Mutuel (100% ou 50% + solde plus tard)
6. Paiement reçu → copier-coller récap banque dans fichier Excel → classement mail par mois d'excursion
7. Confirmation envoyée via Canva (voucher/bon de réservation)
8. 1 mois avant : email choix de menu + relance 50% restant (quand elle n'oublie pas)
9. Bon de commande prestataires créé (guide, bus, restaurant, etc.)
10. Jour J : coordination opérationnelle
11. Post-excursion : feedback par assistante marketing (non systématique)

**Points de friction identifiés :**
- 4-5 jours de délai de réponse parfois → perte de clients
- Pas de relance automatique pour les 50%
- Pas de facturation individuelle
- Feedback post-excursion non automatisé

### Parcours 2 — BtoC Site Internet (via info@)

**Flux actuel :**
1. Lead arrive via site internet ou Google → mail info@
2. Taina répond à la main (pas de mail type — réponse personnalisée selon la demande)
3. Si séjour : appel téléphonique pour creuser la demande
4. Suite du process = similaire au parcours 1
5. Pas de relance systématique si pas de réponse ("mon cerveau attend la réponse")

**Aussi B2B** : des agences étrangères trouvent le site (en anglais) → mêmes flux

### Parcours 3 — BtoB Ponant / UCPA (via ttharsis@)

**Ponant :**
- Travail en amont avec siège Marseille : choix excursions, programmation, pré-réservation prestataires avant saison
- 15 jours avant : pré-chiffres remplissage → validation prestataires
- Redondant à chaque escale : 4 à 8 excursions par escale, 5 prestataires par excursion (guide, fort, bus, snacking, etc.)
- Process plus structuré que BtoC

**UCPA :**
- Séjours hebdo (vendredi → vendredi)
- Chiffres : dimanche soir pré-validation → lundi midi confirmation
- Taina envoie aux prestataires bus + soufrière dès validation
- Frustration : la nouvelle personne UCPA est moins réactive que l'ancienne

**Autres B2B (agence canadienne, etc.) :**
- 3 voyages/an, même logique de pré-réservation
- Demandes via info@ ou bouche-à-oreille

### Gestion des prestataires (transversal)

- ~50 prestataires (30 mentionnés en S1, corrigé en S2)
- Coordination principalement par WhatsApp + appels
- Pré-réservation des dates en début de saison pour les guides
- Problème récurrent : jours fériés Guadeloupe non anticipés par les prestataires
- Un guide (Yanis) nécessite un récap mensuel pour facturer → exception, les autres se débrouillent
- Automatisation prioritaire : **message de rappel automatique la veille de chaque excursion à chaque prestataire**

---

## DÉCISIONS PRISES

### 1. Parcours client — Catherine mappe, Taina valide
- Catherine va modéliser le parcours client complet à partir de cette séance
- Taina valide et complète

### 2. Automatisation prioritaire : leads entrants + réponses mail
- Traitement automatique des mails entrants (qualification + réponse)
- Phase 1 : brouillon (Taina envoie manuellement) → Phase 2 : automatique après 15 jours sans correction
- Taina avait déjà pensé à ce modèle brouillon/auto dans sa config Claude

### 3. Ezus comme hub central
- Plan Pro confirmé (API disponible)
- Objectif : centraliser clients + facturation individuelle + lien paiement
- Question ouverte : comment Ezus sait-il qu'un paiement via lien bancaire est reçu ? → à investiguer
- Garder le lien de paiement Crédit Mutuel (éviter les frais Stripe) mais utiliser Ezus pour la facturation

### 4. Migration vers Apple Mail + Calendrier
- Quitter Roundcube (lecture seule) → configurer Apple Mail avec les 3 boîtes
- Installer le calendrier Apple pour vision d'ensemble
- Catherine fait un tuto pas-à-pas

### 5. Passer au cloud (iCloud)
- Taina accepte (malgré le trauma de 2012)
- Premier niveau iCloud (~200 Go, 2,99€/mois)
- Synchronisation Mac + iPhone + Apple Watch

### 6. Simplification de l'offre Meurtre au Paradis
- 2 tours seulement l'an prochain (au lieu de 5-6 options)
- Full Experience (réduit si escale courte) + déjeuner chez Catherine limité aux 30 premiers

---

## ACTIONS TAINA (Semaine du 7 — 21 avril)

### Priorité 1 : Finir la configuration Claude
- [ ] Terminer l'intégration des instructions CS Digital Setup (style manquant)
- [ ] Demander à Claude d'intégrer les 50 prestataires (via fichier Excel, pas copier-coller dans les instructions)
- [ ] Configurer Claude avec les résultats complets

### Priorité 2 : Infrastructure de base
- [ ] Configurer Apple Mail avec les 3 boîtes (contact@, info@, ttharsis@) — tuto Catherine à venir
- [ ] Activer le calendrier Apple — commencer à y mettre les excursions
- [ ] Souscrire iCloud (premier niveau)
- [ ] Envoyer le correctif DNS (spam) au webmaster (Catherine envoie les instructions)

### Priorité 3 : Partager les données
- [ ] Donner accès Google Drive à Catherine (fichiers Excel + bons de commande)

### Paiement
- [ ] Vérifier le virement du 04/04 (non reçu côté Shine)

---

## ACTIONS CATHERINE

- [ ] Envoyer le diagnostic DNS email (correctif spam — double DMARC)
- [ ] Mapper le parcours client complet (schéma visuel)
- [ ] Faire un tuto configuration Apple Mail (3 boîtes, archivage Roundcube, durée synchro)
- [ ] Faire un tuto configuration calendrier Apple
- [ ] Regarder l'API Ezus en détail (gestion paiements, facturation, clients)
- [ ] Investiguer le lien paiement Crédit Mutuel → Ezus (comment synchroniser ?)
- [ ] Mettre à jour le portail client (actions S2)
- [ ] Envoyer invitation RDV 21 avril 14h
- [ ] Vérifier arrivée du virement sur Shine

---

## MINDSET & INSIGHTS

**Ce qui fonctionne :**
- Malgré le "bordel", Taina a des process implicites : classement mail par mois d'excursion, récap paiements hebdo, mails types pour contact@
- Elle a déjà intégré le concept brouillon → automatique dans sa réflexion Claude
- La simplification de l'offre (2 tours) montre une prise de recul stratégique
- Bons rapports avec prestataires (le chauffeur qui se rend dispo un jour férié)

**Prises de conscience :**
> "Je perds des clients. Il y en a que je relance pas forcément." — sur les 4-5 jours de délai

> "Je pense pour moi, je pense machin, je pense pas à l'agenda des autres." — sur l'oubli de l'assistante marketing

> "C'est tout dans le... suite à ce plantage. J'ai bloqué de partout." — sur le trauma iPad 2012 qui bloque encore l'adoption numérique

> "Je boycotte l'instantané sur ma banque professionnelle parce qu'ils me font payer." — le Crédit Mutuel comme frein permanent

**Dynamique de séance :**
- 3 interruptions opérationnelles majeures (guides au port, maman's friends, assistante) — illustrent parfaitement le problème "90% opérationnel"
- Taina est lucide sur ses blocages mais la charge opérationnelle empêche l'action
- La basse saison qui arrive = fenêtre critique pour tout mettre en place

---

## PROCHAINE SESSION
**Date :** Lundi 21 avril 2026, 14h (France) / 8h (Guadeloupe)
**Focus :** Validation parcours client mappé + premières automatisations (leads entrants)

---

## PÉPITES LINKEDIN

| Citation / situation | Angle | Hook potentiel | Anonymisable ? |
|---------------------|-------|----------------|----------------|
| Dirigeante interrompue 3 fois pendant la séance par des urgences opérationnelles | Coulisses | "Pendant notre séance de travail, elle a dû gérer un guide absent, un port bloqué et une assistante oubliée. C'est ça, 90% opérationnel." | Oui |
| "Je boycotte le virement instantané parce qu'ils me font payer" (banque pro) | Éducatif | "Sa banque lui fait payer le virement instantané pro mais pas le perso. Les TPE paient toujours plus." | Oui |
| Trauma iPad 2012 → 14 ans sans cloud ni calendrier numérique | Témoignage | "Elle a perdu ses données en 2012. Depuis, tout est sur papier. Aujourd'hui, elle accepte enfin de passer au cloud." | Oui (avec accord) |
| Process caché dans le "bordel" (mails classés par mois, récap hebdo) | Éducatif | "Elle dit que c'est le bordel. Mais quand on décortique, il y a déjà un process. Il faut juste le formaliser." | Oui |
