# Cahier des Charges — Automatisation Factures Fred (DRAFT)

> **Version** : Draft v1 — a revoir avec Fred en session 7 (14 mars 2026)
> **Redige par** : Catherine Selosse — CS Consulting Strategique
> **Client** : Fred Funel — FU Solutions / V8 Equipment / FU-Fight

---

## 1. Contexte & Probleme

### Situation actuelle

Fred gere **4 boites mail** qui recoivent des factures :
- **FredGmail** (perso/pro melange)
- **V8@v8-equipment.com**
- **contact@v8-equipment.com**
- **FU Solutions** (actuellement bloquee — probleme 2FA OVH)

Les factures arrivent en **pieces jointes** (PDF, parfois photos/scans) dans ces boites, sans tri, sans classement, sans nomenclature.

### Les entites de Fred

Fred opere sous **une structure holding** avec plusieurs branches :

| Entite | Code couleur | Activite |
|--------|-------------|----------|
| **FU-Fight** | Rouge | Activite principale |
| **V8 Equipment** | Vert | Import/distribution produits Chine |
| **Sourcing** | Jaune | Sourcing fournisseurs |
| **SCI** | - | Immobilier (a confirmer) |
| **Perso** | - | Factures personnelles |

### Le probleme en une phrase

> Les factures sont eparpillees dans 4 boites mail, il n'y a pas de process de classement, la comptabilite 2024 n'a pas de rapprochement bancaire, et 2025 n'est pas traite.

### Impact concret
- **Risque fiscal** : pas de rapprochement bancaire 2024 = l'ancien comptable a failli provoquer un controle Tracfin
- **Stress** : "Putain ces factures... j'en peux plus" (Fred, session 6)
- **Temps perdu** : Virginie (assistante) envoie les documents au comptable mais sans process clair
- **Changement de comptable** en cours = opportunite de repartir sur de bonnes bases

---

## 2. Objectifs

### Objectif principal
**Transformer le chaos factures en un systeme automatise ou chaque facture se range toute seule, avec un tableau recap pret pour le comptable.**

### Objectifs mesurables

| # | Objectif | Indicateur de succes |
|---|----------|---------------------|
| 1 | Zero facture perdue | 100% des factures recues sont dans le systeme |
| 2 | Classement automatique par entite | Tri correct dans > 90% des cas (les cas ambigus = validation humaine) |
| 3 | Tableau recap mensuel genere automatiquement | Le comptable recoit un fichier exploitable chaque mois |
| 4 | Temps Fred = quasi zero | Maximum 10 min/semaine de validation (vs 1h+ aujourd'hui en theorie, en pratique il ne le fait pas) |
| 5 | Virginie autonome sur le process | Elle sait ou trouver les factures et le recap |

---

## 3. Perimetre

### V1 — Ce qu'on fait (MVP)

| Fonctionnalite | Detail |
|----------------|--------|
| **Capture emails** | Surveillance des boites mail configurees (Gmail en priorite, les autres quand accessibles) |
| **Extraction PJ** | Recuperation automatique des pieces jointes (PDF) des mails identifies comme "facture" |
| **Classification IA** | Claude analyse la facture et identifie : fournisseur, date, montant HT/TTC, entite (FU-Fight / V8 / Sourcing / SCI / Perso) |
| **Renommage** | Convention : `AAAA-MM-JJ_Fournisseur_MontantTTC.pdf` |
| **Rangement cloud** | Depot automatique dans le bon dossier Dropbox (ou Drive FU Solutions — a confirmer) |
| **Tableau recap** | Ajout d'une ligne dans Google Sheets : date, fournisseur, montant HT, TVA, TTC, entite, statut, lien fichier |
| **Validation humaine** | Fred (ou Virginie) recoit une notification et valide avant rangement definitif |
| **Email comptable** | En fin de mois, preparation automatique d'un email avec lien dossier + lien Sheets |

### V1 — Factures fournisseurs uniquement (entrantes)

Le MVP traite les **factures fournisseurs** (les factures que Fred recoit). Les factures clients (emises par Fred) sont en V2.

### Hors perimetre V1

| Element | Raison |
|---------|--------|
| Factures clients (emises) | Process different, a traiter en V2 |
| Rapprochement bancaire automatique | Necessite acces API banques (HSBC, Revolut) — trop complexe pour V1 |
| OCR avance sur factures papier | V1 = PDF numeriques. Les scans seront traites si lisibles, sinon flag "a verifier" |
| Boite FU Solutions | Bloquee (2FA OVH). Sera ajoutee des qu'elle est debloquee |
| Traitement retroactif 2024-2025 | Le rattrapage sera un chantier a part avec le nouveau comptable |
| Paiement automatique des factures | Hors scope — on classe, on ne paie pas |

---

## 4. Workflow cible

### Vue d'ensemble

```
ETAPE 1 — CAPTURE
   Les 4 boites mail de Fred
         |
         v
   Filtres Gmail : detecte les mails contenant des factures
   (mot-cles : facture, invoice, receipt, avoir, recu)
         |
         v
   Label automatique "Facture" dans Gmail
         |
         v

ETAPE 2 — EXTRACTION & ANALYSE (n8n + Claude)
   n8n detecte un nouveau mail avec label "Facture"
         |
         v
   Telechargement de la piece jointe (PDF)
         |
         v
   Envoi a Claude API pour analyse :
   - Fournisseur (nom)
   - Date de la facture
   - Montant HT / TVA / TTC
   - Numero de facture
   - Entite destinataire (FU-Fight / V8 / Sourcing / SCI / Perso)
   - Type (facture, avoir, acompte)
         |
         v
   Si l'IA n'est pas sure de l'entite → flag "A TRIER"
         |
         v

ETAPE 3 — VALIDATION HUMAINE (obligatoire)
   Notification a Fred (email ou message)
   avec resume : "Facture Alibaba — 1 200 EUR TTC — V8 — OK ?"
         |
    +---------+
    |         |
  [OK]    [Corriger]
    |         |
    v         v
  Suite    Fred corrige l'entite / le montant
    |         |
    +---------+
         |
         v

ETAPE 4 — RANGEMENT & ARCHIVAGE
   Renommage du fichier : 2026-03-15_Alibaba_1200.pdf
         |
         v
   Depot dans le bon dossier cloud :
   /[ENTITE]/Comptabilite/Factures Fournisseurs/2026/03-Mars/
         |
         v
   Ajout d'une ligne dans Google Sheets :
   Date | Fournisseur | N. Facture | HT | TVA | TTC | Entite | Statut | Lien fichier
         |
         v

ETAPE 5 — CLOTURE MENSUELLE (automatisee)
   Fin de mois → n8n genere un email pre-rempli :
   - Destinataire : comptable (+ Virginie en copie)
   - Objet : "[ENTITE] Factures fournisseurs — Mars 2026"
   - Corps : lien vers le dossier cloud + lien vers le Google Sheets
   - Fred valide et envoie (un clic)
```

### Regles de classification par entite

L'IA utilisera une **table de mapping fournisseurs → entites** que Fred remplira au fur et a mesure :

| Fournisseur | Entite | Confiance |
|-------------|--------|-----------|
| Alibaba | V8 | Haute |
| UPS/DHL (colis Chine) | V8 | Haute |
| OVH | FU Solutions (admin) | Haute |
| EDF local | SCI | Haute |
| ... | ... | ... |

Les fournisseurs inconnus seront marques **"A TRIER"** et Fred les attribuera manuellement. L'IA apprendra de ses corrections.

---

## 5. Outils & Stack technique

### Architecture

| Composant | Outil | Role |
|-----------|-------|------|
| **Orchestration** | n8n (self-hosted, deja en place) | Declenchement, enchainement des etapes, notifications |
| **Intelligence** | Claude API (Anthropic) | Analyse des factures, extraction des donnees, classification |
| **Email** | API Gmail | Lecture des mails, detection des factures, envoi email comptable |
| **Stockage fichiers** | Dropbox ou Google Drive FU Solutions (a confirmer) | Rangement des PDF classes |
| **Tableau recap** | Google Sheets | Base de donnees des factures, vue mensuelle |
| **Validation** | Email (ou webhook n8n) | Fred valide chaque facture avant rangement |

### Pourquoi ces choix ?

- **n8n** : Catherine l'utilise deja pour d'autres projets (chatbot FSY, agent email Jade). Pas de code a ecrire pour Fred, tout est visuel.
- **Claude API** : comprend le francais, lit les PDF, classifie avec precision. Deja dans la stack CS Consulting.
- **Gmail API** : Fred est sur Gmail pour FredGmail et V8. Les filtres existent deja (poses en session 4-5).
- **Google Sheets** : Fred commence a connaitre (Drive FU Solutions), c'est partageable avec le comptable et Virginie.

### Couts estimes

| Poste | Cout mensuel estime |
|-------|-------------------|
| n8n (deja heberge) | 0 EUR (inclus dans infra CS Consulting) |
| Claude API (~50 factures/mois) | ~5-10 EUR |
| Gmail API | Gratuit |
| Google Sheets | Gratuit (inclus dans Google Workspace) |
| **Total** | **~5-10 EUR/mois** |

> A noter : le developpement est inclus dans le programme d'accompagnement de Fred (1 automatisation incluse dans la formule).

---

## 6. Questions ouvertes pour Fred (Session 7)

### Priorite haute — A trancher absolument

- [ ] **Cloud de rangement** : on utilise **Dropbox** (cloud principal actuel) ou **Google Drive FU Solutions** pour les factures ? Quel acces pour le comptable ?
- [ ] **Nouveau comptable** : qui est-ce ? Comment il/elle veut recevoir les documents ? (lien cloud, mail avec PJ, portail comptable ?)
- [ ] **Entites completes** : confirmer la liste exacte. FU-Fight, V8, Sourcing — et la SCI ? Et les factures perso, on les traite ou on les exclut ?
- [ ] **Boite FU Solutions** : Gaetan a-t-il resolu le probleme 2FA OVH ? Si non, on demarre sans et on l'ajoutera apres.
- [ ] **Virginie** : quel est son role exact dans le process ? Elle envoie au comptable ? Elle valide les factures ? Elle a acces a quoi ?

### Priorite moyenne — Pour affiner le systeme

- [ ] **Factures clients (emises)** : Fred emet des factures ? Avec quel outil ? Faut-il aussi les tracker ? (V2)
- [ ] **Frequence d'envoi au comptable** : mensuel ? Ou le comptable veut recevoir au fil de l'eau ?
- [ ] **Fournisseurs recurrents** : Fred peut-il lister ses 10-15 fournisseurs principaux par entite ? (pour pre-configurer le mapping)
- [ ] **Montant alerte** : a partir de quel montant Fred veut etre alerte specifiquement ? (ex : > 5 000 EUR = notification immediate)
- [ ] **Doublons** : ca arrive souvent qu'une meme facture arrive dans plusieurs boites ?
- [ ] **Factures papier** : il en recoit encore beaucoup ? Comment les traiter ? (photo avec le telephone → email a soi-meme ?)

### Questions techniques (Catherine gere, mais Fred doit valider)

- [ ] **Arborescence cloud** : confirmer la structure de dossiers par entite
  ```
  /FU-FIGHT/Comptabilite/Factures Fournisseurs/2026/01-Janvier/
  /V8/Comptabilite/Factures Fournisseurs/2026/01-Janvier/
  /SOURCING/Comptabilite/Factures Fournisseurs/2026/01-Janvier/
  ```
- [ ] **Google Sheets** : une feuille par entite ou tout dans un meme fichier avec un onglet par entite ?
- [ ] **Acces Gmail API** : Fred doit autoriser l'acces (OAuth). Catherine le guidera en session.

---

## 7. Planning previsionnel

### Phase 1 — Preparation (semaines du 10 au 21 mars)

| Etape | Quoi | Qui | Quand |
|-------|------|-----|-------|
| 1.1 | Valider ce cahier des charges avec Fred | Catherine + Fred | Session 7 (14 mars) |
| 1.2 | Fred liste ses fournisseurs recurrents par entite | Fred | Avant le 21 mars |
| 1.3 | Fred confirme le nouveau comptable + son process | Fred | Avant le 21 mars |
| 1.4 | Creer le Google Sheets template | Catherine | Semaine du 17 mars |
| 1.5 | Creer l'arborescence comptable dans le cloud | Catherine + Fred | Session 8 |

### Phase 2 — Developpement (semaines du 24 mars au 4 avril)

| Etape | Quoi | Qui | Quand |
|-------|------|-----|-------|
| 2.1 | Developper le workflow n8n (trigger Gmail + extraction) | Catherine | Semaine du 24 mars |
| 2.2 | Configurer le prompt Claude (analyse facture + classification) | Catherine | Semaine du 24 mars |
| 2.3 | Connecter le rangement cloud (Dropbox ou Drive) | Catherine | Semaine du 31 mars |
| 2.4 | Connecter Google Sheets (ajout de ligne auto) | Catherine | Semaine du 31 mars |
| 2.5 | Ajouter la validation humaine (notification + bouton OK/Corriger) | Catherine | Semaine du 31 mars |

### Phase 3 — Test & Lancement (semaine du 7 avril)

| Etape | Quoi | Qui | Quand |
|-------|------|-----|-------|
| 3.1 | Test avec 10 factures reelles (Fred valide les resultats) | Catherine + Fred | Session 9 ou 10 |
| 3.2 | Ajustements (mapping fournisseurs, precision IA) | Catherine | Apres tests |
| 3.3 | Mise en production | Catherine | Mi-avril |
| 3.4 | Formation Virginie sur le process | Catherine + Fred | Session suivante |

### Phase 4 — V2 (mai-juin, si pertinent)

- Ajout boite FU Solutions (quand debloquee)
- Factures clients (emises par Fred)
- Alertes doublons et anomalies de montant
- Rapprochement bancaire (si acces API banque)

---

## 8. Criteres de validation

### Le systeme est considere comme valide quand :

| # | Critere | Comment on le mesure |
|---|---------|---------------------|
| 1 | **Les factures sont detectees automatiquement** | Un mail avec PJ "facture" dans Gmail declenche le workflow en < 5 min |
| 2 | **L'extraction est correcte** | Fournisseur, date, montant extraits correctement dans > 95% des cas |
| 3 | **La classification par entite est fiable** | Entite correcte dans > 90% des cas (fournisseurs connus = 100%) |
| 4 | **Le fichier est range au bon endroit** | PDF renomme et dans le bon dossier cloud apres validation |
| 5 | **Le tableau recap est a jour** | Chaque facture validee = une ligne dans Google Sheets |
| 6 | **La validation humaine fonctionne** | Fred recoit une notification claire et peut valider ou corriger en 1 clic |
| 7 | **L'email comptable est pret** | En fin de mois, un brouillon d'email est genere avec les bons liens |
| 8 | **Fred comprend le systeme** | Fred peut expliquer le process a Virginie en 5 min |

### Test de recette (Phase 3)

On testera avec **10 factures reelles** couvrant :
- Au moins 3 entites differentes (FU-Fight, V8, Sourcing)
- Au moins 1 fournisseur inconnu (test du flag "A TRIER")
- Au moins 1 scan/photo (test de la qualite OCR)
- Au moins 1 doublon volontaire (test de la detection)

Fred validera chaque resultat. Si > 8/10 sont corrects du premier coup, on lance en production.

---

## Annexes

### A. Rappel du contexte comptable

- **Ancien comptable** : a failli provoquer un controle Tracfin
- **Situation 2024** : pas de rapprochement bancaire
- **Situation 2025** : pieces envoyees par Virginie mais non traitees
- **Nouveau comptable** : en cours d'integration (a confirmer avec Fred)
- **Urgence** : ce projet d'automatisation ne resout pas le retard 2024-2025, mais empechera que ca se reproduise pour 2026

### B. Boites mail et statut

| Boite | Statut | Dans le perimetre V1 ? |
|-------|--------|----------------------|
| FredGmail | Active, configuree dans Outlook | Oui |
| V8@v8-equipment.com | Active, a configurer dans Outlook | Oui |
| contact@v8-equipment.com | Active, a configurer dans Outlook | Oui |
| FU Solutions | Bloquee (2FA OVH) | Non (ajoutee des que debloquee) |

### C. Methode de developpement

Ce projet sera developpe selon la methode **Spec-to-Code Factory** :
- Pipeline : BREAK > MODEL > ACT > DEBRIEF
- Fichiers dans : `03-developpement/agent-factures-fred/`
- Gates de validation : Gate 0 (intake) → Gate 5 (production)

---

> **Prochaine etape** : revoir ce document avec Fred en session 7 (14 mars), trancher les questions ouvertes, puis lancer le developpement.
