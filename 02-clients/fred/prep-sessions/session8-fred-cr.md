# CR Session 8 — Fred Funel
**Date :** 17 mars 2026, 8h
**Duree :** ~3h30
**Format :** Visio Google Meet

---

## 🎯 SESSION 8 - Claude Pro, Cowork & Automatisation Factures

### ✅ CELEBRATIONS
- **Lacher-prise en action** 🔥 : panne voiture, pas assure depuis 1 an, weekend ski improvise avec ses enfants — Fred a tout gere sereinement sans anticiper. "Chaque fois j'ai du cul, chaque fois j'ai du cul"
- **Agathe a dormi chez lui** pour la premiere fois depuis l'achat de la maison — moment familial fort, Fred etait tres emu
- **Tournage video avec Marion (CM)** reussi malgre zero preparation — "on a ete hyper efficaces, en 2-2 ca s'est fait"
- **Portail client retrouve et utilise** : Fred a navigue dans son espace, cocher/decocher les actions, comprend la logique
- **Outlook FU Solutions configure** par Fred lui-meme — "moins boomer que prevu"
- **A reproduire** : le lacher-prise fonctionne — Fred valide que "les ressources sont la" meme quand rien n'est prepare

### 🔄 BLOCAGES IDENTIFIES
- **Formation Simon (WhatsApp)** : Fred sature — pas de plateforme centralisee, tout passe par WhatsApp, info impossible a retrouver, replays perdus. "J'y arrive plus, c'est trop brouillon". N'assiste a aucun atelier.
- **Factures = point de douleur critique** : "putain ces factures, j'en peux plus" — la compta (Annie Link/Virginie) ne fait pas le travail attendu, Fred est tres decu. Pas de tableau de suivi, pas de visibilite.
- **Plantages techniques en session** : Firefox/Claude a plante plusieurs fois (micro vocal bloque, fenetres non fermables), fuseau horaire Outlook decale (codes de verification expires)
- **Acces Drive via Claude Cowork** : lent, autorisations multiples, fichier Excel difficile a importer

---

## 🛠️ DECISIONS PRISES

### 1️⃣ Migration Botnation → Claude Pro
- Compte Claude cree (fu@fusolutions.fr), plan Pro 20$/mois
- Memoire importee depuis l'ancien chatbot (export + prompt structure)
- Securite configuree : Claude ne stocke PAS noms clients, CB, MDP, donnees perso en memoire
- App desktop installee + epinglee en barre de taches
- Botnation : export memoire fait, desabonnement en cours

### 2️⃣ Claude = nouveau binome de travail
- Projet "Strategie entreprise" cree dans Claude
- Google Drive connecte (dossier "Claude" cree)
- Google Calendar connecte (fu@fusolutions.fr)
- Gmail connecte (fred@v8-equipment.com)
- Tache planifiee "Daily Briefing" configuree : tous les matins 7h, resume agenda + mails + alertes urgences (modele Haiku)
- Demo Cowork sur fichier Excel FooFight (taekwondo) → Claude detecte des bugs critiques dans les formules, Fred est bluffe

### 3️⃣ Automatisation factures lancee
- Process actuel : factures arrivent sur v8@v8equipment.com (Gmail) → Fred les met dans "scan facture" (Dropbox) → compta vide le dossier → Fred perd la trace
- Decision : Catherine construit une automatisation (n8n) qui extrait les factures automatiquement et remplit un tableau de suivi
- Fred envoie 2-3 factures d'exemple pour calibrer l'extraction
- Outil pour Fred uniquement, pas partage avec la compta

---

## 🎯 ACTIONS FRED (Semaine du 17-23 mars)

### ⚡ Priorite 1 : Dashlane + Microsoft 365 🔴
- [ ] Installer l'extension Dashlane dans Firefox et commencer l'import des mots de passe
- [ ] Acheter Microsoft 365 sous FU Solutions (lien dans le portail client)

### ⚡ Priorite 2 : Explorer Claude 🟠
- [ ] Travailler avec Claude sur le projet "Strategie entreprise" — continuer l'analyse du fichier FooFight et challenger les chiffres

### ⚡ Priorite 3 : Factures 🟡
- [ ] Envoyer 2-3 factures d'exemple a Catherine (depuis scan facture) ✅ FAIT

---

## 📝 ACTIONS CATHERINE
- [ ] Construire l'automatisation factures Fred (n8n + Claude API + Google Sheets) — PRD + specs faites
- [ ] Mettre a jour le portail client Fred (V2 en cours, corrections UX)
- [ ] Preparer des skills Claude pour Fred (publication, reponse clients V8, TDAH)

---

## 🧘 MINDSET & INSIGHTS

### **Ce qui fonctionne** ✅
- Le lacher-prise : Fred passe d'un mode "anticiper 3 mois a l'avance" a "j'arrive, on verra" — et ca marche mieux
- L'etat d'esprit de developpement (livre "Oser reussir") : de chaque echec, faire une force
- Fred commence a chercher par lui-meme au lieu de demander qu'on fasse pour lui — "je suis moins boomer"

### **Prises de conscience** 💡
- "Chaque fois j'ai du cul" → Fred realise qu'il a les ressources, meme sans anticipation
- "J'ai les epaules qui se liberent, les sacs de platre qui tombent" → reaction a la demo Claude sur les factures
- "Catherine, tu me regales. J'adore." → premiere fois que Fred exprime autant d'enthousiasme pour un outil digital
- "J'ai vraiment envie d'avancer, mais ce qui me manque c'est la premiere action pour lancer le truc" → Fred identifie son blocage TDAH : c'est le demarrage qui coince, pas l'execution
- Sur la compta : "je comptais vachement sur Annie Link/Virginie, et j'ai pas du tout cette sensation" → deception, Fred prend conscience qu'il doit garder le controle lui-meme

---

## 📅 PROCHAINE SESSION
**Date :** Mardi 18 mars 2026, 8h (si Fred n'est pas a Strasbourg, sinon a replanifier)
**Focus :** Retour Dashlane + M365, skills Claude, point factures
