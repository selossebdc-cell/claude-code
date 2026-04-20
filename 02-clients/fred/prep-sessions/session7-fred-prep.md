# Preparation Session 7 — Fred Funel
## Vendredi 14 mars 2026 — 8h00

> Cette session a ete decalee de 11h a 8h (Catherine a un coaching a 11h).
> Fred est en Thailande (decalage horaire a verifier — 8h France = 14h Thailande en hiver).

---

## Livrables Catherine a preparer AVANT la session

### 1. Tuto Dashlane — Import MDP + Installation
**Echeance : mercredi 12 mars au plus tard** (laisser a Fred le temps de faire avant vendredi)

Contenu du tuto :
- [ ] Creer un compte Dashlane (2 EUR/mois, plan Personnel)
- [ ] Exporter les mots de passe depuis Google Passwords (chrome://password-manager/settings → Exporter)
- [ ] Importer le CSV dans Dashlane
- [ ] Installer l'extension Dashlane sur **Chrome** ET **Firefox**
- [ ] Installer l'app Dashlane sur **iPhone** et **iPad**
- [ ] Desactiver la sauvegarde auto de Chrome (pour eviter les doublons)
- [ ] Montrer comment creer un groupe partage (ex: partager un MDP avec Agathe)

Format recommande : video screen recording (Fred retient mieux en voyant faire) + etapes ecrites en bullet points.

Envoyer par : WhatsApp (Fred l'a installe depuis session 5) + email FredGmail.

### 2. Screenshots / Video URSSAF
**Echeance : mercredi 12 mars au plus tard**

- [ ] Identifier ce que Fred doit faire sur URSSAF (declaration ? paiement ? creation compte ?)
- [ ] Faire les captures d'ecran etape par etape
- [ ] OU enregistrer une video screen recording du parcours URSSAF
- [ ] Envoyer a Fred avant la session pour qu'il puisse essayer seul d'abord

### 3. Cahier des charges Automatisation Factures (draft)
**Echeance : jeudi 13 mars**

Base : utiliser les notes de `04-notes-session7-factures.md` + architecture cible deja documentee.

Le draft doit couvrir :
- [ ] Perimetre : factures fournisseurs uniquement (confirmer avec Fred)
- [ ] Source : boite mail FU Solutions (en attente resolution 2FA) OU FredGmail en interim
- [ ] Workflow : Gmail trigger → extraction → classification (FU-Fight/V8/Sourcing) → rangement Drive → tableau recap → mail compta
- [ ] Stack : n8n + API Gmail + API Claude + API Google Drive + Google Sheets
- [ ] Questions ouvertes a valider avec Fred (voir section ci-dessous)
- [ ] Planning : dev apres resolution du blocage 2FA OVH

Format : requirements.md pour le pipeline Spec-to-Code Factory (dossier `03-developpement/agent-factures-fred/input/`).

### 4. Verifier si Fred a achete Claude
- [ ] Envoyer un rappel WhatsApp mardi 11 mars : "Fred, n'oublie pas d'acheter la licence Claude avant vendredi ! On configure ton agent perso en session."
- [ ] Si achete : preparer la configuration de l'agent (personnalite TDAH, recadrage, aide fichiers, competences V8)
- [ ] Si pas achete : pas grave, on reporte — ne pas insister

---

## Questions a poser en session 7

### Comptabilite (URGENT)
- [ ] As-tu contacte l'expert-comptable cette semaine ?
- [ ] Quel est le plan pour le rapprochement bancaire 2024 ? Et 2025 ?
- [ ] L'ancienne comptable (Admilink?) — c'est definitif que c'est termine ?

### Automatisation factures (pour finaliser le cahier des charges)
- [ ] Confirmer : factures fournisseurs uniquement, ou aussi factures clients ?
- [ ] Quels fournisseurs recurrents par entite ? (liste)
- [ ] La comptable actuelle — comment veut-elle recevoir les factures ? (lien Drive, mail, les deux ?)
- [ ] Frequence : mensuel ? Quelles infos elle a besoin ? (date, fournisseur, montant, entite, statut paiement)
- [ ] Fred OK pour Google Sheets (pas Excel) vu qu'on pousse vers Drive FU Solutions ?

### Configuration Outlook
- [ ] As-tu ajoute V8@v8-equipment.com et contact@v8-equipment.com ?
- [ ] Calendrier FU Solutions configure ?
- [ ] Outlook installe sur telephone et iPad ?

### Boite FU Solutions / OVH
- [ ] Gaetan a-t-il resolu le probleme 2FA ?
- [ ] Si oui : on configure tout de suite dans Outlook + on donne l'acces a Catherine

### Dashlane
- [ ] As-tu cree le compte et importe les MDP ?
- [ ] Extensions installees sur Chrome et Firefox ?

### Claude
- [ ] As-tu achete la licence ?
- [ ] Si oui : on configure ensemble l'agent personnalise

---

## Deroulement suggere (2h)

| Bloc | Duree | Sujet |
|------|-------|-------|
| 1 | 10 min | Check-in + point actions semaine (compta, Gaetan, Dashlane, Claude) |
| 2 | 20 min | URSSAF — parcours guide avec les screenshots/video prepares |
| 3 | 15 min | Dashlane — verification installation, import MDP, demo groupe partage |
| 4 | 15 min | Outlook — verification config (comptes ajoutes, calendrier) |
| 5 | 20 min | Automatisation factures — presenter le draft du cahier des charges, valider avec Fred |
| 6 | 20 min | Claude — si licence achetee : premiere config de l'agent personnalise |
| 7 | 10 min | Recap actions + prochaine session |

> **Rappel TDAH** : blocs de 20-25 min max, recadrer si Fred part dans les idees. Privilegier les actions concretes et immediates.

---

## Fichiers de reference
- CR session 6 : `session6-fred-cr.md`
- Notes factures : `04-notes-session7-factures.md`
- Memoire client : `../fred.md`
- Architecture factures : voir section "Architecture cible" dans `04-notes-session7-factures.md`
