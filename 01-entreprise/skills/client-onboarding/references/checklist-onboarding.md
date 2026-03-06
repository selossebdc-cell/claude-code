# Checklist d'onboarding — Nouveau client CS Consulting Stratégique

Source : Process d'onboarding Notion de Catherine + Questionnaire Fillout (https://feuillederoute.fillout.com/csbusiness)

## 1️⃣ Validation & engagement (J0)

**Objectif :** transformer la décision en engagement clair

### Actions
- [ ] Envoi du récap de proposition (PDF)
- [ ] Signature du devis / contrat
- [ ] Envoi et signature des CGV
- [ ] Paiement du 1er versement (ou acompte selon échéancier)
- [ ] Confirmer réception paiement / signature
- [ ] **☐ Prise en charge OPCO ?** → Si oui, voir encadré ci-dessous

### Si prise en charge OPCO

- [ ] Demander au client de fournir **sous 10 jours** :
  1. **Attestation de cotisation de formation** (à télécharger depuis leur profil URSSAF)
  2. **Nom et coordonnées de l'OPCO**
  3. **Montant estimé de prise en charge** (si connu)
- [ ] 1er versement demandé immédiatement (sans attendre le retour OPCO)
- [ ] Dès réception du montant OPCO confirmé → calculer le reste à charge client
- [ ] Facturer le solde au client selon l'échéancier convenu
- [ ] Facture séparée à émettre à l'OPCO (voir skill `invoice-generator`)

### Pack de documents à envoyer
1. **Devis / Proposition commerciale** (signée) — utiliser le skill `proposal-generator`
2. **CGV** — document standard CS Consulting Stratégique (CGV.docx dans Notion)
3. **Facture / échéancier** — montant, dates, moyens de paiement

**Règle d'or :** Ne jamais onboarder sans validation écrite + paiement (1er versement minimum).

## 2️⃣ Email de bienvenue (J0 — J1)

**Objectif :** rassurer + expliquer la suite

### Contenu de l'email
- Félicitations / remerciements
- Rappel de l'objectif de la collaboration
- Étapes à venir (synthétique)
- Liens vers :
  - Le questionnaire d'onboarding
  - L'agenda pour réserver Session #1
  - L'espace Notion (quand prêt)

### Template email

Objet : 🎉 Bienvenue [Prénom] — C'est parti !

---

Bonjour [Prénom],

Je suis ravie de vous accueillir et de démarrer notre accompagnement ensemble.

Afin de commencer dans les meilleures conditions, voici les premières informations utiles :

**Objectif de l'accompagnement**
[Personnaliser selon le diagnostic de l'audit]

**Déroulement**
- Durée : 6 mois (de [date] à [date])
- Format : visio / présentiel
- Fréquence : 1 séance de 1h30 par semaine (mois 1-3), puis espacé (mois 4-6)
- Crédit : 18 sessions à votre rythme

**Prochaine étape**
Avant notre première séance, merci de :
1. Remplir le questionnaire d'onboarding : https://feuillederoute.fillout.com/csbusiness
2. Réserver votre Session #1 (minimum 5 jours ouvrés après le questionnaire) : [lien Fantastical]

⏰ Pourquoi ce délai ? Pour que je puisse analyser vos réponses et vous préparer une feuille de route personnalisée avant notre rencontre.

**Communication entre les séances**
- Email : catherine@csbusiness.fr
- WhatsApp : 0661864016
- Délai de réponse : 24/48h

**Les règles du jeu :**
- Prévenir 24h avant pour annuler/reporter une session
- Appliquer les actions entre les sessions
- Poser vos questions à tout moment

Je me réjouis de travailler ensemble vers vos objectifs.

À très bientôt !

Catherine
CS — Consulting Stratégique

## 3️⃣ Questionnaire d'onboarding (envoyé J0-J1)

**Objectif :** récolter les infos clés sans allers-retours
**Format :** Formulaire Fillout

Le questionnaire d'onboarding est hébergé sur Fillout :
→ **URL : https://feuillederoute.fillout.com/csbusiness**

⚠️ **RÈGLE CRITIQUE — Délai questionnaire → Session #1 :**
Le client doit réserver sa Session #1 **minimum 5 jours ouvrés (= 7 jours calendaires) après avoir rempli le questionnaire**. Ce délai est nécessaire pour que Catherine puisse analyser les réponses et préparer la feuille de route personnalisée.

### Sections du questionnaire (7 sections) :
1. **Clarifier la vision** — Pourquoi cette entreprise, vie idéale, valeurs
2. **Simplifier la stratégie** — Client idéal, offres, positionnement
3. **Mapper le parcours client** — Marketing, vente, delivery
4. **Auditer la productivité** — Tâches détestées, meilleur usage du temps
5. **Problématiques** — Obstacles, défis, ce qui ne fonctionne pas
6. **Objectifs** — Résultats attendus, métriques de succès
7. **Revenus** — CA actuel, CA souhaité, résultats à 1 an

### Envoi au client
- Envoyer le lien Fillout dans l'email de bienvenue
- Le formulaire est générique (pas besoin de dupliquer/personnaliser)

## 4️⃣ Création du dashboard Notion (J1-J2)

**Objectif :** préparer l'espace de travail du client

### Structure du dashboard (basée sur le modèle Fred)

```
🎯 [Prénom] [Nom] - Dashboard Client

> Programme : Accompagnement Clarté & Autonomie - 6 mois
> Début : [date]
> Fin : [date + 6 mois]
> Votre crédit : 18 sessions

---

📊 Votre Parcours
- Rythme recommandé (Mois 1-3 : hebdo, Mois 4-6 : bi-mensuel)
- 📅 Réserver ma prochaine session
  - 👉 RDV 1h30 : [lien Fantastical]
  - 👉 RDV 1h : [lien Fantastical]

📥 INBOX - Capture Rapide (callout orange)
- Zone de capture avec règle des 2 minutes

[Colonnes]
Gauche — Ressources + Outils :
- 🎯 Feuille de route
- ⏱️ Tracker de temps
- 📋 Mes SOP & Process
- 📝 Mes Notes & Questions
- 🔧 Outils informatiques

Droite — Matériel :
- 📁 Administratif (CGV, factures)
- 📟 Meeting Agendas
- 📅 Mes 18 Sessions
- 👥 Accès Communauté Skool
- 🎁 Bonus & Ressources

📞 Contact Catherine
- Email, WhatsApp, délai réponse

🔔 Rappels importants
- Réserver régulièrement
- Préparer ses questions
- Appliquer les actions
- Utiliser les ressources Skool
```

### Actions
- [ ] Dupliquer le template dashboard depuis l'espace "Clients - Gestion des Missions & Projets"
- [ ] Personnaliser : prénom, dates, liens Fantastical
- [ ] Créer les sous-pages vides (Meeting Agendas, Feuille de route, etc.)
- [ ] Ajouter CGV signées dans Administratif
- [ ] Partager l'accès Notion au client

## 5️⃣ Document de bienvenue / Guide de collaboration (J1-J2)

**Objectif :** poser le cadre opérationnel et relationnel

### Contenu
- Présentation de la méthode CS Consulting Stratégique
- Rôles & responsabilités (ce que Catherine fait / ce que le client fait)
- Règles de communication
- Outils utilisés
- Bonnes pratiques collaboration

## 6️⃣ Process & roadmap de la mission (J1-J2)

**Objectif :** projection et clarté
**Format :** 1-2 pages dans le dashboard Notion

### Contenu
- Grandes étapes de la mission (Phase 1 + Phase 2)
- Livrables attendus
- Jalons clés
- Points de validation

## 7️⃣ Email kit de démarrage (J3)

**Objectif :** donner les accès et lancer

Objet : 🚀 Votre espace est prêt — [Prénom]

---

Bonjour [Prénom],

Votre espace personnel est prêt ! Voici vos accès :

👉 **Votre Dashboard** : [lien Notion]

Prenez 5 minutes pour :
1. Ouvrir le lien et explorer votre espace
2. Remplir le questionnaire de démarrage : https://feuillederoute.fillout.com/csbusiness
3. Réserver votre Session #1 (au moins 5 jours ouvrés après le questionnaire) : [lien Fantastical]

Pas de stress si ça semble beaucoup — on verra tout ça ensemble lors de notre première séance.

À bientôt !

Catherine
CS — Consulting Stratégique

## 8️⃣ Vérification pré-Session #1 (J5-J7)

- [ ] Le client a ouvert Notion
- [ ] Le questionnaire est rempli
- [ ] La Session #1 est réservée
- [ ] Si non → envoyer relance douce

## 9️⃣ Session #1 : Lancement

- [ ] Faire l'audit initial à partir du questionnaire + échange
- [ ] Créer le premier CR dans Meeting Agendas (utiliser le skill `session-report`)
- [ ] Remplir la feuille de route avec les premières priorités
- [ ] Définir les quick wins (semaine 1)
- [ ] Planifier Session #2
