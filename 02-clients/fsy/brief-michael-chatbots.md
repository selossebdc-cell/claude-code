---
title: Brief Mickaël — Chatbots FSY + MTM (Vendredi-Dimanche)
deadline: Dimanche 23 avril
---

# 📋 Brief Chatbots FSY + MTM

**Pour :** Mickaël
**Deadline :** Dimanche 23 avril (Catherine reprend dimanche)
**Contexte :** Catherine finit automations jeudi. Toi tu bosses vendredi/samedi sur chatbots. Dimanche validation.

---

## 🎯 Livrable 1 : MTM Chatbot Telegram

### État actuel
- ✅ Chatbot Telegram **prêt** (développé)
- ✅ Brevo + Circle intégrés
- ❌ Documentation manquante
- ❌ Guide "comment utiliser" pour Aurélia

### À faire (Vendredi)

**Spec technique :**
- [ ] Localiser le code chatbot MTM Telegram (dossier `03-developpement/chatbot-fsy/`)
- [ ] Documenter : architecture, où est la DB, comment elle se sync avec Brevo/Circle
- [ ] Clarifier : comment les réponses FAQ sont stockées/updatées

**Guide pour Aurélia + assistante :**
- [ ] Comment poster un nouveau contenu/exercice
- [ ] Comment modérer les questions
- [ ] Comment tracker les stats (nombre de messages, questions récurrentes)
- [ ] Escalade : quand contacter Mickaël

**Format :** HTML ou Markdown, lisible, avec screenshots

---

## 🎯 Livrable 2 : FSY WhatsApp Chatbot

### État actuel
- ✅ WhatsApp Business API configurée (Meta app "CS - Consulting WA", WABA 1553022859098901)
- ✅ Token permanent généré (utilisateur système "n8n")
- ❌ Chatbot pas encore développé
- 📍 Coûts réels : ~1.25€/mois (2-3 questions/jour à 0.017€/msg)

### Architecture cible
```
FSY Planning (Dimanche soir)
  ↓
WhatsApp Groupe (Aurélia poste manuellement)
  ↓
  
FSY Chatbot FAQ
  ↓
WhatsApp API (réponses auto)
  ↓
Brevo (capture interactions)
```

### À faire (Vendredi-Samedi)

**Chatbot Spec :**
- [ ] Créer webhooks Twilio/Vonage OU solution alternative pas chère (que tu identifieras)
- [ ] FAQ initiales (à récupérer depuis contexte FSY ou questions existantes)
- [ ] Intégration : comment réponses chatbot → Brevo
- [ ] Comment Aurélia modère/ajoute FAQ

**Code requis :**
- [ ] Webhook endpoint (Node.js / Python, hébergé où ?)
- [ ] Logique FAQ (match question → réponse)
- [ ] Brevo sync (contact reçoit tag FAQ_ASKED, etc.)

**Documentation :**
- [ ] Guide "comment ajouter une FAQ"
- [ ] Guide modération pour assistante
- [ ] Coûts/pricing expliqué

**Format :** Code + HTML guide

---

## 🎯 Livrable 3 : Guide Maintenance Aurélia

### À faire (Samedi-Dimanche)

**Pour Aurélia + future assistante**, comment mettre à jour les automations :

**Sections :**
1. **Mails Brevo**
   - Comment modifier un email existant
   - Comment ajouter un email à une séquence
   - Comment changer dates/timing
   - Tester avant d'activer

2. **UTMs**
   - Où sont les liens UTMs (bio Instagram, mails, etc.)
   - Comment ajouter nouveau lien UTM (Générateur tool)
   - Comment tracker les sources (Brevo report)
   - Substack : comment ajouter UTM (nouvelle source)

3. **Automations Brevo**
   - Comment activer/désactiver une séquence
   - Comment ajouter une liste comme déclencheur
   - Comment modifier les attributs capturés
   - Où voir les logs (Brevo automation history)

4. **Circle**
   - Comment inviter en masse
   - Comment modérer le groupe
   - Comment voir stats (membres actifs, messages, etc.)
   - Lien avec Brevo (qui a accès)

5. **Chatbots**
   - MTM Telegram : ajouter FAQ
   - FSY WhatsApp : ajouter FAQ
   - Voir les questions posées
   - Escalade (quand contacter qui)

6. **Suivi des clients**
   - Dashboard Brevo (source, engagement, statut)
   - Circle (qui s'active, qui dort)
   - Rapport hebdo (c'est automatique)

**Format :** Document HTML/Markdown avec liens directs + screenshots

---

## 📅 Timeline proposée

**Vendredi 21 avril**
- [ ] MTM Telegram : documentation technique + guide usage (3-4h)
- [ ] FSY WhatsApp : architecture + dev webhook (3h)

**Samedi 22 avril**
- [ ] FSY WhatsApp : FAQ + Brevo sync + guide modération (4h)
- [ ] Guide Maintenance Aurélia : brouillon (2h)

**Dimanche 23 avril**
- [ ] Review avec Catherine (1h)
- [ ] Finalisations + tests (2h)

---

## 🔗 Ressources / Contexte

### Fichiers clés
- Chatbot MTM Telegram : `03-developpement/chatbot-fsy/` (chemin à vérifier)
- WhatsApp config : Stripe/Meta WABA `1553022859098901`
- Brevo : 13K contacts, 35 templates, automations structure

### Contacts
- **Aurélia** : aurélia.delsol@gmail.com (elle verra les guides)
- **Catherine** : respons. finale (valide dimanche)
- **Toi** : dev/architecture

### Points clés à ne pas oublier
- ⚠️ **Aucune dépendance Catherine** : tout doit être autonome pour Aurélia
- ⚠️ **Coûts transparent** : expliquer pourquoi WhatsApp 1.25€ vs Telegram gratuit
- ⚠️ **Escalade claire** : quand Aurélia doit te contacter (pas 24/7)
- ✅ **MTM Telegram est prioritaire** : FSY WhatsApp en second (moins urgente)

---

## Questions à clarifier demain (Mardi 21) avec Catherine

- [ ] Où est le code MTM Telegram exact ?
- [ ] FAQ initiales FSY : tu les as ou faut les récupérer où ?
- [ ] WhatsApp solution alternative pas chère : tu as des pistes ? (Twilio, Vonage, autre ?)
- [ ] Hébergement chatbot : sur quel serveur (Vercel, Hostinger, autre) ?
- [ ] Brevo escalade : qui doit être contacté si problème (Catherine, Laurie, toi ?) ?

---

## Checkpoint Dimanche 18h

- ✅ MTM Telegram : doc + guide Aurélia OK
- ✅ FSY WhatsApp : chatbot fonctionnel + guide OK
- ✅ Guide Maintenance complet
- ✅ Tous les liens/docs en place
- ✅ Prêt pour Aurélia lancer semaine prochaine

→ **Catherine valide et vous êtes bons pour phase 2**
