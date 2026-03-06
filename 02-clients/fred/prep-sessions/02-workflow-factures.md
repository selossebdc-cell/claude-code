# Workflow Automatisation Factures — Fred (FU Solutions)

## Problème actuel

- 4 boîtes mail avec des factures partout
- Factures papier en plus
- Pas de classement → tout en vrac
- L'assistante Admilink n'a pas de process clair
- Clôture mensuelle = cauchemar

## Vision cible : "La facture arrive → elle se range toute seule"

---

## WORKFLOW EN 4 ÉTAPES

```
┌─────────────────────────────────────────────────────────────┐
│                    ÉTAPE 1 : CAPTURE                        │
│                 "Toutes les factures arrivent au même endroit"│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📧 Gmail perso ──┐                                        │
│  📧 Fred V8 ─────┤   Filtre Gmail                         │
│  📧 Contact V8 ──┤── {facture invoice receipt reçu} ──→ 📧 V8 V8
│  📧 V8 V8 ───────┘   + Label "Facture" 🔴                 │
│                                                             │
│  📄 Factures papier → Photo → Email à V8 V8               │
│                       (ou scan direct dans OneDrive)        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   ÉTAPE 2 : TRI                             │
│                "Chaque facture va dans sa boîte"            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📧 V8 V8 (label Facture)                                  │
│       │                                                     │
│       ├── Objet contient "FU-Fight" ou fournisseur connu   │
│       │   → Label "Facture-FUF" 🔴                         │
│       │                                                     │
│       ├── Objet contient "V8" ou fournisseur Chine         │
│       │   → Label "Facture-V8" 🟢                          │
│       │                                                     │
│       └── Objet contient "Sourcing"                        │
│           → Label "Facture-Sourcing" 🟡                    │
│                                                             │
│  💡 Si pas identifiable → Label "Facture-A-TRIER" ⚪       │
│     (Fred trie 1x/semaine, 5 min)                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  ÉTAPE 3 : RANGEMENT                        │
│              "Le fichier est classé sur OneDrive"           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Option A : MANUELLE (Phase 1 — maintenant)                │
│  ─────────────────────────────────────────                  │
│  1x/semaine (vendredi, revue hebdo) :                      │
│  - Ouvrir Gmail V8 → Label "Facture"                       │
│  - Télécharger les PDF                                     │
│  - Renommer : 2026-02-27_Fournisseur_Montant.pdf           │
│  - Ranger dans OneDrive :                                  │
│    FU-FIGHT/Comptabilité/Factures Fournisseurs/2026/       │
│    ou V8/Comptabilité/Factures Fournisseurs/2026/          │
│  ⏱ Temps estimé : 10-15 min/semaine                       │
│                                                             │
│  Option B : AGENT IA (Phase 2 — mars-avril)               │
│  ──────────────────────────────────────────                 │
│  n8n (trigger) + Agent IA (cerveau) :                      │
│  - n8n détecte nouveau mail label "Facture"                │
│  - Agent IA lit la facture (OCR si scan)                   │
│  - Identifie : fournisseur, montant, date, entité         │
│  - Renomme + range dans le bon dossier OneDrive           │
│  - Met à jour le tableau récap mensuel                     │
│  - Alerte si montant anormal ou doublon                    │
│  ⏱ Setup : 1 jour | Puis 0 min/semaine                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                ÉTAPE 4 : CLÔTURE MENSUELLE                  │
│            "L'assistante Admilink a tout ce qu'il faut"     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Chaque fin de mois :                                      │
│                                                             │
│  📁 OneDrive/FU-FIGHT/Comptabilité/Factures.../2026/      │
│  📁 OneDrive/V8/Comptabilité/Factures.../2026/            │
│  📁 OneDrive/SOURCING/Comptabilité/Factures.../2026/      │
│       │                                                     │
│       ▼                                                     │
│  📊 Tableau récap mensuel (Excel ou Notion)                │
│  ┌──────────┬────────────┬─────────┬────────┬──────────┐   │
│  │ Date     │ Fournisseur│ Montant │ Entité │ Statut   │   │
│  ├──────────┼────────────┼─────────┼────────┼──────────┤   │
│  │ 01/02/26 │ Alibaba    │ 1 200€  │ V8     │ Payée    │   │
│  │ 03/02/26 │ UPS        │ 340€    │ V8     │ Payée    │   │
│  │ 15/02/26 │ Fournisseur│ 89€     │ FUF    │ A payer  │   │
│  └──────────┴────────────┴─────────┴────────┴──────────┘   │
│       │                                                     │
│       ▼                                                     │
│  ✉️  Envoi à Admilink : lien OneDrive + tableau récap      │
│  (1 mail, tout est dedans, rien à chercher)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## CALENDRIER DE DÉPLOIEMENT

| Phase | Quand | Quoi | Effort Fred |
|-------|-------|------|-------------|
| **Phase 1** | Session 5 (maintenant) | Filtres Gmail + labels + process manuel vendredi — on rode l'arborescence | 15 min/semaine |
| **Phase 2** | Mars-avril | n8n + Agent IA : lecture, tri, rangement, tableau récap — tout automatique | 0 min/semaine |

## CE QUE FRED DOIT RETENIR

> "Aujourd'hui tu fais 15 min le vendredi. Dans 1 mois, l'IA le fait pour toi."

---

## ACTIONS SESSION 5

1. ✅ Créer les filtres Gmail dans les 4 boîtes (pendant la session, en AnyDesk)
2. ✅ Créer l'arborescence OneDrive (pendant la session)
3. 📋 Fred : faire sa première "revue factures" vendredi prochain (test du process)
4. 📋 Fred : demander à Admilink son process actuel (pour l'intégrer)
5. 📋 Catherine : préparer la Phase 2 (n8n + Agent IA) pour session 7-8
