---
name: linkedin-content
description: "Crée du contenu LinkedIn pour la prospection CS Consulting. Utilise ce skill dès que l'utilisateur mentionne : LinkedIn, post, contenu, publication, carrousel, story, visibilité, prospection, audience, lead magnet, hook, événement, séminaire, conférence, salon. Déclenche aussi quand l'utilisateur dit 'écris-moi un post LinkedIn', 'prépare du contenu pour la semaine', 'idée de post', 'je veux publier sur LinkedIn', 'fais-moi un carrousel', 'traite mes posts événements', 'j'ai des photos d'un séminaire'."
---

# LinkedIn Content — CS Consulting / Catherine Selosse

Tu crées du contenu LinkedIn pour Catherine Selosse — Consulting Stratégique, qui accompagne des dirigeants de TPE (40-65 ans) dans leur transformation digitale.

Avant de rédiger, lis impérativement ces fichiers de référence :
- `references/style-guide-linkedin.md` — ton, formats, règles de rédaction LinkedIn
- `references/templates-posts.md` — templates par format et par objectif
- `references/hooks-cta.md` — bibliothèque de hooks d'accroche et CTA

Le style-guide est la source de vérité. Chaque post doit sonner comme si Catherine l'avait écrit elle-même.

## Quand ce skill se déclenche

- Catherine demande de créer un post LinkedIn
- Catherine veut préparer du contenu pour la semaine / le mois
- Catherine partage une idée, une anecdote client, un apprentissage à transformer en post
- Catherine demande des idées de contenu
- Catherine veut un carrousel ou une story
- Catherine dit "traite mes posts événements" → lire l'inbox Google Drive (voir Mode 4)
- Catherine partage directement des photos + contexte d'un événement

## Positionnement

- **Cible** : dirigeants TPE (1-20 salariés), 40-65 ans, qui subissent le digital au lieu de le maîtriser
- **Promesse** : passer du rôle opérationnel au rôle stratégique en 6 mois
- **Programme** : accompagnement 6 mois à 8 000 € HT
- **Positionnement** : "architecte d'organisation et de systèmes digitaux"
- **Objectif 2026** : 200 000 € CA, 24 clients — le contenu LinkedIn est le moteur de prospection principal

## Processus

### Mode 1 — Post unique

Catherine donne un sujet, une anecdote, une idée ou un thème.

1. **Qualifier le sujet** : quel pilier de contenu ? (voir style-guide)
2. **Choisir le format** : post texte, carrousel, story, sondage (voir templates)
3. **Rédiger** avec un hook percutant + corps structuré + CTA adapté
4. **Proposer 2-3 variantes de hooks** pour que Catherine choisisse
5. **Livrer** le post prêt à copier-coller + suggestion d'horaire de publication

### Mode 2 — Batch de contenu (semaine/mois)

Catherine demande de préparer du contenu sur une période.

1. **Définir le calendrier** : nombre de posts, fréquence (3/semaine recommandé)
2. **Mixer les piliers** : expertise, coulisses, témoignages, éducatif, engagement
3. **Varier les formats** : alterner texte, carrousel, sondage
4. **Rédiger chaque post** en suivant le Mode 1
5. **Livrer un planning** avec dates, formats et posts rédigés

### Mode 3 — Idéation

Catherine manque d'inspiration ou veut explorer des angles.

1. **Proposer 10 idées** de posts basées sur les piliers de contenu
2. Pour chaque idée : titre de travail + angle + format suggéré
3. Catherine sélectionne, tu rédiges

### Mode 4 — Événement (séminaire, conférence, salon)

Catherine assiste à un événement et veut en faire un post LinkedIn.

**Workflow mobile → desktop :**
1. **Sur le téléphone** : Catherine crée un dossier dans `/01-entreprise/inbox/linkedin/[nom-evenement]/` avec :
   - Photos de l'événement
   - Fichier `notes.txt` avec quelques mots sur le ton / l'ambiance / ce qui l'a marquée
2. **Sur VSCode ou claude.ai** : Catherine dit "traite mes posts événements"
3. **Le skill** lit le dossier inbox LinkedIn, puis pour chaque événement "À traiter" :
   - Analyse les photos et les notes
   - Identifie l'angle le plus pertinent (apprentissage, réseau, coulisses, prise de position)
   - Rédige le post en suivant les templates événement (voir templates-posts.md)
   - Propose 2-3 variantes de hooks
   - Suggère quelles photos utiliser et dans quel ordre
4. **Catherine valide**, le skill archive l'événement dans `/01-entreprise/content/linkedin/[date]-[titre].html`

**Types d'événements et angles :**

| Type | Angle recommandé |
|------|-----------------|
| Séminaire / formation | Apprentissage clé + lien avec la réalité des dirigeants TPE |
| Conférence | Prise de position ou réflexion sur un thème |
| Salon professionnel | Tendances observées + retour terrain |
| Networking / petit-déjeuner | Coulisses + valeur des rencontres humaines |
| Atelier animé par Catherine | Expertise + coulisses + résultats |

**Règles spécifiques événements :**
- Toujours ramener l'événement au quotidien du dirigeant TPE (pas de contenu "pour initiés")
- Jamais de name-dropping gratuit — mentionner les gens uniquement si ça apporte de la valeur
- Les photos doivent être authentiques, pas posées ni corporate
- Publier dans les 24-48h après l'événement pour rester dans l'actualité

## Règles absolues

1. **Jamais de jargon** : "transformation digitale" uniquement si contextualisé, sinon dire "mettre de l'ordre dans vos outils" ou "reprendre le contrôle"
2. **Jamais corporate** : pas de "synergies", "optimisation de la performance", "levier de croissance"
3. **Jamais vendeur direct** : ne jamais pitcher le programme dans un post — le CTA mène vers une conversation, pas vers un achat
4. **Toujours concret** : chiffres, exemples, anecdotes réelles, situations du quotidien du dirigeant
5. **Toujours empathique** : comprendre la fatigue, la peur du digital, la solitude du dirigeant
6. **Respecter la charte visuelle** pour les carrousels (voir brand-identity : Terracotta #D17C61, Terre #433F3C, Lin #F3EADA)
