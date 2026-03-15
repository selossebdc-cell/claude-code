# Session 3 — Face Soul Yoga
**Date** : a planifier (semaine du 11-14 mars 2026)
**Participantes** : Aurelia + Laurie
**Duree** : 1h
**Session** : 3 / 19

---

## 1. Suivi actions session 2 (5 min)

- [ ] Migration Uscreen → Kajabi + Bunny.net : ou en est Laurie ?
  - Combien de videos transferees ?
  - Timeline estimee ?
- [ ] Antoine : premiers reels livres ? Calendrier de publication ?
- [ ] Aurelia utilise Claude AI ? Retours ? Besoins ?

---

## 2. Chatbot Telegram — Mise en service (30 min)

### Ce qui est pret (demo rapide)
- 8 workflows n8n fonctionnels (commandes slash, FAQ, accueil, anti-spam, escalade, cadrage horaires)
- Bot cree : @facesoulyoga_bot
- VPS Hostinger operationnel
- Mode mention obligatoire (decision 6 mars)

### Ce dont j'ai besoin pour lancer

**BLOQUANT — A fournir par Laurie/Aurelia :**

1. **FAQ (20-30 questions/reponses)**
   - Categories : Acces/Tech, Programmes, Planning, Tarifs, Communaute, Pratique
   - Format simple : Question → Reponse
   - **Demander a Laurie** : "Les 20 questions qu'on te pose le plus sur WhatsApp, avec tes reponses types"
   - Deadline : sous 1 semaine

2. **Planning hebdo**
   - Quelle est la source ? Kajabi ? Google Sheet ? Manuel ?
   - Le bot doit pouvoir repondre `/planning` avec le planning de la semaine
   - Comment il est mis a jour ? Par qui ?

3. **Creer le vrai groupe Telegram**
   - Laurie cree le groupe
   - Ajouter @facesoulyoga_bot comme administrateur
   - Me donner le chat_id du groupe

4. **Chat_id de Laurie**
   - Pour les escalades (quand le bot ne sait pas repondre → notification Laurie)
   - Laurie doit envoyer un message au bot en prive, je recupere son chat_id

**A VALIDER :**

5. **Message d'accueil nouveau membre** — valider le texte
6. **Horaires du bot** — 9h-18h lun-ven, c'est toujours OK ?
7. **Nom du bot** dans les reponses — "le bot FSY" ? autre ?

### Planning de mise en service

| Etape | Quoi | Qui | Quand |
|-------|------|-----|-------|
| 1 | Fournir FAQ + planning | Laurie/Aurelia | Semaine 12 |
| 2 | Creer groupe Telegram + ajouter bot | Laurie | Semaine 12 |
| 3 | Charger FAQ + fix escalade + mode mention | Catherine | Semaine 12-13 |
| 4 | Test sur vrai groupe (Laurie + Aurelia + Catherine) | Toutes | Semaine 13 |
| 5 | Ouverture aux membres | Laurie (communication) | Semaine 14 |

---

## 3. Point process & organisation (20 min)

- [ ] CEO time 2h/semaine : Aurelia l'a bloque ?
- [ ] Delegation Laurie : quoi de plus a deleguer ?
- [ ] Architecture offre FSY vs Aurelia Del Sol : avancees ?

---

## 4. Actions a assigner

### Laurie
- [ ] Lister 20-30 FAQ (questions + reponses) — deadline : vendredi prochain
- [ ] Creer le groupe Telegram FSY
- [ ] Envoyer un message prive au bot pour escalade

### Aurelia
- [ ] Valider message accueil + horaires bot
- [ ] Fournir source planning hebdo
- [ ] Bloquer 2h CEO time/semaine

### Catherine
- [ ] Fix workflow escalade (chat_id)
- [ ] Passer en mode mention obligatoire
- [ ] Desactiver attribution n8n
- [ ] Charger FAQ des reception
- [ ] Deployer sur vrai groupe Telegram

---

## Notes de session
_(a remplir pendant la session)_
