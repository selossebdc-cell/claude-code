# Notion Inbox — LinkedIn Événements

## Principe

Catherine utilise une base de données Notion comme "boîte de réception" pour ses posts événements. Elle y dépose photos + notes depuis son téléphone (app Notion mobile), puis le skill traite les entrées en attente.

## Base de données Notion

**Nom** : LinkedIn Inbox
**ID** : `49a06f6a-5c72-4340-bdf4-d0b6410cc891`
**Emplacement** : workspace Notion CS Consulting Stratégique

### Propriétés de la base

| Propriété | Type | Valeurs / Description |
|-----------|------|----------------------|
| **Événement** | Titre | Nom de l'événement (ex: "Séminaire BPI Toulouse") |
| **Date** | Date | Date de l'événement |
| **Type** | Select | Séminaire, Conférence, Salon, Networking, Atelier, Autre |
| **Photos** | Fichiers | 1-5 photos prises sur place |
| **Notes** | Texte enrichi | Ce qui a marqué Catherine : ambiance, phrase clé, rencontre, idée forte. Quelques mots suffisent. |
| **Ton souhaité** | Select | Inspirant, Éducatif, Engagé, Coulisses, Drôle |
| **Personnes à taguer** | Texte | Noms LinkedIn des personnes à mentionner (optionnel) |
| **Statut** | Select | À traiter, En cours, Traité, Abandonné |
| **Post généré** | Texte enrichi | Le post final validé par Catherine (rempli par le skill) |
| **Date de publication** | Date | Date prévue de publication (remplie par le skill) |

### Vues recommandées

1. **À traiter** (vue par défaut) — Filtre : Statut = "À traiter", trié par Date décroissant
2. **Tous les posts** — Vue tableau complète
3. **Calendrier** — Vue calendrier par Date de publication

## Workflow depuis le téléphone

### Ce que Catherine fait (2 minutes max)

1. Ouvrir l'app Notion sur le téléphone
2. Aller dans "LinkedIn Inbox"
3. Appuyer sur "+" pour créer une entrée
4. Remplir :
   - **Événement** : nom rapide (ex: "Petit-dej CCI Lyon")
   - **Photos** : ajouter depuis la galerie du téléphone
   - **Notes** : taper quelques mots-clés ou une phrase (ex: "super échange avec un dirigeant artisan, il galère avec ses factures, moment authentique")
   - **Ton souhaité** : sélectionner dans la liste
5. Le statut se met automatiquement à "À traiter"

### Ce que le skill fait (sur VSCode/claude.ai)

Quand Catherine dit "traite mes posts événements" :

1. Lire la base Notion "LinkedIn Inbox" via l'API
2. Filtrer les entrées avec Statut = "À traiter"
3. Pour chaque entrée :
   - Analyser les photos (si accessibles) et les notes
   - Choisir le template événement approprié (8, 9 ou 10)
   - Rédiger le post avec 2-3 variantes de hooks
   - Suggérer les photos à utiliser et leur ordre
   - Proposer une date de publication
4. Catherine valide ou ajuste
5. Mettre à jour la page Notion : Statut → "Traité", coller le post dans "Post généré", renseigner la date de publication

## Accès API Notion

La config API Notion est dans le CLAUDE.md global (`~/Projects/CLAUDE.md`).
**Database ID** : `49a06f6a-5c72-4340-bdf4-d0b6410cc891`
La base doit être partagée avec l'intégration Notion existante.

## Astuce : Template rapide Notion mobile

Pour aller encore plus vite depuis le téléphone, Catherine peut créer un **template Notion** pré-rempli :
- Type : Séminaire (le plus fréquent)
- Ton souhaité : Inspirant
- Statut : À traiter

Comme ça, elle n'a qu'à ajouter le titre, les photos et les notes.
