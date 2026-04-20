---
title: Planning Livraison FSY — Lundi 20 au Jeudi 23 Avril
deadline: Jeudi 23 avril soir
---

# 🎯 Objectif
**Jeudi soir** : Automations + Migr. Uscreen→Circle prêtes + Aurélia peut lancer la comm et la formation

---

## LUNDI 20 AVRIL (AUJOURD'HUI)

### ✅ À FAIRE (4-5 heures)

**1. Laurie — UTMs (CRITIQUE)**
- [ ] Envoyer le mail avec le générateur UTM + tracker
- [ ] Demander les 3 liens UTM finalisés (FSY Studio, MTM, Licence MTM)
- [ ] Vérifier qu'elle les mette à jour dans :
  - Bio Instagram
  - Mails de promo
  - Landing pages

**2. Vidéo d'intro Circle** (Aurélia)
- [ ] Enregistrer 4-5 min max : "Bienvenue dans Circle, voilà comment naviguer"
- [ ] Upload dans Circle
- [ ] Lier dans le 1er email d'onboarding

**3. Vérifier Stripe → n8n Webhook**
- [ ] Aller dans Stripe Dashboard → Webhooks
- [ ] Vérifier que `charge.succeeded` envoie bien vers n8n
- [ ] Tester 1 paiement test Stripe → vérifier que Brevo reçoit l'update

**4. Config Circle — Calendrier/Événements**
- [ ] Créer structure : onglet "Programme" ou "Événements"
- [ ] Récupérer les URLs des vidéos du lundi (format Circle)
- [ ] Tester : mettre 1 vidéo test en tant qu'événement

---

## MARDI 21 AVRIL

### ✅ À FAIRE (5-6 heures)

**1. Relancer Laurie** (si pas de réponse)
- [ ] Check : les UTMs sont générés ?
- [ ] Check : ils sont mis à jour partout ?

**2. Tester PARCOURS COMPLET FSY Studio** (chemin critique)
- [ ] Créer contact test : `test.fsy.studio@mailinator.com`
- [ ] Cliquer sur lien UTM (depuis YouTube/Instagram)
- [ ] Remplir quiz Manychat → vérifier Brevo création
- [ ] Vérifier email nurture reçu
- [ ] Payer 17€ → vérifier :
  - [ ] Webhook Stripe → n8n OK
  - [ ] Brevo : `STATUT_MEMBRE=active`, `DATE_ACHAT` rempli
  - [ ] Email onboarding (Bienvenue + Tuto + Accès vidéo) reçu
  - [ ] Invitation Circle reçue
  - [ ] Accès Circle fonctionne

**3. Tester PARCOURS COMPLET MTM** (validation)
- [ ] Créer contact test : `test.mtm@mailinator.com`
- [ ] Quiz + Nurture
- [ ] Payer → vérifier :
  - [ ] eSignature workflow déclenché
  - [ ] Contrat reçu + signé OK
  - [ ] Invitation Circle différente (groupe MTM)

**4. Config Telegram/WhatsApp**
- [ ] Vérifier quelle option on choisit (coût + verrouillage)
- [ ] Commencer setup si possible

---

## MERCREDI 22 AVRIL

### ✅ À FAIRE (4-5 heures)

**1. Migration Uscreen → Circle** (si les accès sont dispo)
- [ ] Exporter CSV Uscreen (email, sub_id Stripe, date renouvellement)
- [ ] Importer contacts dans Circle
- [ ] **Stripe subscription update** :
  - [ ] Créer workflow n8n pour migrer les subscriptions
  - [ ] Tester sur 5 contacts
  - [ ] Vérifier : dates renouvellement conservées ✅

**2. Corriger bugs trouvés les jours précédents**
- [ ] Lister ce qui a échoué lors des tests
- [ ] Fixer les workflows n8n si besoin
- [ ] Mettre à jour les emails si besoin

**3. Mail du dimanche (Aurelia)**
- [ ] Récupérer historique mails du dimanche (derniers 3 mois)
- [ ] Faire analyser par Claude → générer template IA
- [ ] Tester : envoyer 1 version test dimanche

**4. Vérifier les listes Brevo** (blocage de Laurie)
- [ ] Confirmer : listes créées en tant que déclencheurs d'automations ?
- [ ] Si non, créer les listes et reconfigurer les automations

---

## JEUDI 23 AVRIL

### ✅ À FAIRE (2-3 heures)

**1. Dernière validation globale**
- [ ] Tester parcours FSY Studio 1x complètement (de zéro)
- [ ] Tester parcours MTM 1x complètement
- [ ] Vérifier : tous les mails arrivent à temps
- [ ] Vérifier : Circle access fonctionne

**2. Documentation finale pour Aurélia**
- [ ] Runbook clair : "Voilà c'est prêt, voici comment ça marche"
- [ ] Check-list avant lancer la comm :
  - [ ] Tous les liens UTM en place
  - [ ] Stripe webhook actif
  - [ ] Brevo automations OK
  - [ ] n8n workflows actifs
  - [ ] Circle accès fonctionne
  - [ ] Mails envoyés à temps

**3. Autorisation de lancer**
- [ ] Appel rapide Aurélia : "C'est bon, tu peux commencer"
- [ ] Elle peut lancer :
  - [ ] Comm FSY Studio
  - [ ] Comm MTM
  - [ ] Accueil sur Circle
  - [ ] Migration Uscreen (contacts + subscriptions)

---

## DÉPENDANCES CRITIQUES 🚨

1. **Laurie UTMs** → tout bloqué si pas fait lundi
2. **Stripe webhook live** → n8n ne reçoit rien sinon
3. **Test Parcours FSY** → valide le flux complet
4. **Circle access** → sinon les clients sont bloqués

---

## CHECKPOINT JEUDI 18H

- ✅ FSY Studio : test OK de bout en bout
- ✅ MTM : test OK de bout en bout
- ✅ Mails arrivent + Circle access fonctionne
- ✅ Laurie UTMs placés partout
- ✅ Doc pour Aurélia prête

→ **Feu vert pour lancer la comm**
