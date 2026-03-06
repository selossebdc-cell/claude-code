# LE CIRCUIT DE TES FACTURES
## (à montrer à Fred en session)

```
    AUJOURD'HUI ❌                          DEMAIN ✅
    ─────────────                          ─────────

    📧 Gmail         Factures              📧 Gmail ──┐
    📧 Fred V8       partout,              📧 Fred V8 ─┤  FILTRE AUTO
    📧 Contact V8    en vrac,              📧 Contact V8┤  "facture"
    📧 V8 V8         perdues...            📧 V8 V8 ◄──┘  → tout arrive ici
    📄 Papier                              📄 Papier → photo → email V8
         │                                      │
         ▼                                      ▼
    😰 "Je cherche                         📧 V8 V8
     mes factures                          Label 🔴 Facture
     pendant 2h"                                │
                                                ▼
                                     ┌──────────┼──────────┐
                                     │          │          │
                                   🔴 FUF    🟢 V8    🟡 Sourcing
                                     │          │          │
                                     ▼          ▼          ▼
                                   📁 OneDrive (rangé par entité)
                                                │
                                                ▼
                                     📊 Tableau récap mensuel
                                                │
                                                ▼
                                     ✉️ 1 mail à Admilink
                                        "Tout est là"
                                                │
                                                ▼
                                          ✅ Clôture OK
```

---

## LES 2 PHASES

```
MAINTENANT                          DANS 1 MOIS
──────────                          ───────────

📧 Filtre Gmail                     🧠 Agent IA
    +                               n8n détecte le mail
📁 Tu ranges le vendredi            → l'IA lit la facture
   (15 min)                         → classe + renomme + range
                                    → met à jour le tableau récap
                                    (0 min)

   PHASE 1                           PHASE 2
   "Tu rides le process"             "L'IA prend le relais"
```

---

## TA ROUTINE VENDREDI (15 min)

```
1. Ouvre Gmail V8 → clique sur label "Facture" 🔴
2. Pour chaque facture de la semaine :
   - Télécharge le PDF
   - Renomme : 2026-02-27_Fournisseur_Montant.pdf
   - Range dans OneDrive → Entité → Comptabilité → Factures → 2026
3. C'est fini. ☕
```
