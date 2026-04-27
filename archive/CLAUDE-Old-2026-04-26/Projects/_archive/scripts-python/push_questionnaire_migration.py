#!/usr/bin/env python3
"""Crée le questionnaire migration plateforme pour Aurélia ET Laurie dans Notion."""

import json
import urllib.request

NOTION_TOKEN = "<SECRET-NOTION-TOKEN-REMOVED>"
FSY_DASHBOARD = "304c3a2f-4255-80da-b8b2-fef4e17f7243"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def notion_post(endpoint, data):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{endpoint}",
        data=json.dumps(data).encode(), headers=HEADERS, method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def notion_patch(endpoint, data):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{endpoint}",
        data=json.dumps(data).encode(), headers=HEADERS, method="PATCH"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def text(content, bold=False, italic=False, color="default"):
    return {
        "type": "text", "text": {"content": content},
        "annotations": {"bold": bold, "italic": italic, "color": color},
    }

def heading1(txt):
    return {"type": "heading_1", "heading_1": {"rich_text": [text(txt)]}}

def heading2(txt):
    return {"type": "heading_2", "heading_2": {"rich_text": [text(txt)]}}

def heading3(txt):
    return {"type": "heading_3", "heading_3": {"rich_text": [text(txt)]}}

def paragraph(*parts):
    return {"type": "paragraph", "paragraph": {"rich_text": list(parts)}}

def bullet(*parts):
    return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": list(parts)}}

def callout(emoji, *parts, color="default"):
    return {"type": "callout", "callout": {"rich_text": list(parts), "icon": {"type": "emoji", "emoji": emoji}, "color": color}}

def divider():
    return {"type": "divider", "divider": {}}

def column_list(columns):
    return {"type": "column_list", "column_list": {"children": columns}}

def column(children):
    return {"type": "column", "column": {"children": children}}

def toggle(title_parts, children):
    return {
        "type": "heading_3", "heading_3": {
            "rich_text": title_parts if isinstance(title_parts, list) else [text(title_parts)],
            "is_toggleable": True, "children": children,
        }
    }

def quote(*parts):
    return {"type": "quote", "quote": {"rich_text": list(parts)}}


# === QUESTIONS (identiques pour les deux) ===

def question_block(numero, question, sous_texte=None):
    """Génère un bloc question numéroté."""
    blocks = [
        paragraph(
            text(f"Q{numero}. ", bold=True, color="orange"),
            text(question, bold=True),
        )
    ]
    if sous_texte:
        blocks.append(paragraph(text(sous_texte, italic=True, color="gray")))
    # Zone de réponse vide
    blocks.append(quote(text("  ", color="gray")))
    blocks.append(paragraph())
    return blocks


# === CRÉER LA PAGE ===

print("Création de la page questionnaire...")

page = notion_post("pages", {
    "parent": {"page_id": FSY_DASHBOARD},
    "icon": {"type": "emoji", "emoji": "📋"},
    "properties": {
        "title": {
            "title": [{"text": {"content": "Questionnaire migration plateforme — Aurélia & Laurie"}}]
        }
    },
})

page_id = page["id"]
print(f"Page créée : {page_id}")

# === CONTENU ===

blocks = []

# En-tête
blocks.append(callout("🎯",
    text("Objectif : ", bold=True),
    text("recueillir vos retours AVANT la session de vendredi 28 février pour prendre la meilleure décision sur la nouvelle plateforme. "),
    text("Répondez chacune de votre côté", bold=True),
    text(", sans vous concerter — c'est important d'avoir vos deux visions."),
    color="blue_background"
))

blocks.append(callout("⏰",
    text("Deadline : jeudi 27 février au soir", bold=True),
    text(" — Catherine lira vos réponses avant la session de vendredi."),
    color="yellow_background"
))

blocks.append(paragraph(
    text("Préparé par Catherine Selosse — CS Consulting Stratégique", italic=True, color="gray")
))

blocks.append(divider())

# === SECTION AURÉLIA ===

blocks.append(heading1("🎯 Réponses Aurélia"))

blocks.append(callout("💡",
    text("Aurélia, réponds avec ta casquette de dirigeante. "),
    text("Ce qui compte : ta vision, l'expérience de tes clientes, tes ambitions business.", bold=True),
    color="purple_background"
))

blocks.append(paragraph())

# --- Partie 1 : Uscreen aujourd'hui ---
blocks.append(heading2("Partie 1 — Uscreen aujourd'hui"))

for b in question_block(1, "Qu'est-ce qui fonctionne bien sur Uscreen aujourd'hui ?",
    "Ce que tu veux absolument retrouver sur la nouvelle plateforme."):
    blocks.append(b)

for b in question_block(2, "Qu'est-ce qui ne fonctionne pas ou te frustre sur Uscreen ?",
    "Ce qui t'a poussée à vouloir partir."):
    blocks.append(b)

for b in question_block(3, "Qu'est-ce qui te manque sur Uscreen et que tu n'as jamais eu ?",
    "Fonctionnalités que tu voudrais mais qui n'existent pas."):
    blocks.append(b)

for b in question_block(4, "Combien paies-tu par mois pour Uscreen ? Et pour quoi exactement ?",
    "Détailler si possible : abonnement, frais de transaction, stockage..."):
    blocks.append(b)

blocks.append(divider())

# --- Partie 2 : Besoins ---
blocks.append(heading2("Partie 2 — Ce dont tu as besoin"))

for b in question_block(5, "Classe ces fonctionnalités par ordre de priorité pour toi (1 = le plus important) :",
    "Mets un numéro devant chaque ligne."):
    blocks.append(b)

blocks.append(bullet(text("__ Héberger et diffuser mes vidéos de formation (500+ vidéos)")))
blocks.append(bullet(text("__ Communauté / espace d'échange entre les membres")))
blocks.append(bullet(text("__ Parcours de formation structuré (modules, progression, évaluations)")))
blocks.append(bullet(text("__ Paiements récurrents (abonnements, membership)")))
blocks.append(bullet(text("__ Email marketing (séquences automatiques, newsletters)")))
blocks.append(bullet(text("__ Lives / webinaires avec replay")))
blocks.append(bullet(text("__ Site web / landing pages")))
blocks.append(bullet(text("__ App mobile pour les membres")))
blocks.append(bullet(text("__ Analytics / suivi de la progression des membres")))
blocks.append(bullet(text("__ Gamification (points, badges, niveaux)")))
blocks.append(paragraph())

for b in question_block(6, "Y a-t-il des fonctionnalités dont tu auras besoin dans les 12 prochains mois et que tu n'utilises pas encore ?",
    "Pense à tes projets : B2B, certification, nouveau programme, upsells..."):
    blocks.append(b)

for b in question_block(7, "Quelle est LA chose la plus importante pour l'expérience de tes clientes ?",
    "Si tu ne pouvais choisir qu'un seul critère."):
    blocks.append(b)

blocks.append(divider())

# --- Partie 3 : Critères non-négociables ---
blocks.append(heading2("Partie 3 — Tes critères non-négociables"))

for b in question_block(8, "Si dans 2 ans tu veux changer de plateforme, qu'est-ce qui doit être facilement récupérable ?",
    "Vidéos, liste membres, emails, contenus de formation, données de paiement..."):
    blocks.append(b)

for b in question_block(9, "Quel est ton budget maximum par mois pour la plateforme (tout compris) ?",
    "Inclure : abonnement + stockage + email + éventuels frais de transaction."):
    blocks.append(b)

for b in question_block(10, "Préfères-tu un seul outil qui fait tout ou plusieurs outils spécialisés ?",
    "Et pourquoi ?"):
    blocks.append(b)

for b in question_block(11, "Qu'est-ce qui serait un DEALBREAKER absolu pour toi ?",
    "Le truc qui te ferait dire non immédiatement."):
    blocks.append(b)

blocks.append(divider())

# --- Partie 4 : Vision ---
blocks.append(heading2("Partie 4 — Ta vision"))

for b in question_block(12, "Dans 12 mois, à quoi ressemble ton écosystème digital idéal ?",
    "Imagine que tout fonctionne parfaitement. Décris ce que tu vois."):
    blocks.append(b)

for b in question_block(13, "Qu'est-ce qui t'a plu dans Kajabi quand tu as commencé à tester ?",
    "Et qu'est-ce qui t'a fait douter ou t'a manqué ?"):
    blocks.append(b)

for b in question_block(14, "Y a-t-il autre chose que tu veux que Catherine sache avant vendredi ?"):
    blocks.append(b)

blocks.append(divider())

# === SECTION LAURIE ===

blocks.append(heading1("👩 Réponses Laurie"))

blocks.append(callout("💡",
    text("Laurie, réponds avec ta casquette opérationnelle. "),
    text("Ce qui compte : ton quotidien, ce qui te fait gagner ou perdre du temps, ce qui est simple ou compliqué.", bold=True),
    color="green_background"
))

blocks.append(paragraph())

# --- Partie 1 : Uscreen ---
blocks.append(heading2("Partie 1 — Uscreen aujourd'hui"))

for b in question_block(1, "Qu'est-ce qui fonctionne bien sur Uscreen aujourd'hui ?",
    "Ce que tu veux absolument retrouver sur la nouvelle plateforme."):
    blocks.append(b)

for b in question_block(2, "Qu'est-ce qui ne fonctionne pas ou te frustre sur Uscreen ?",
    "Ce qui te fait perdre du temps ou te complique la vie."):
    blocks.append(b)

for b in question_block(3, "Qu'est-ce qui te manque sur Uscreen et que tu n'as jamais eu ?",
    "Fonctionnalités que tu voudrais mais qui n'existent pas."):
    blocks.append(b)

for b in question_block(4, "Combien de temps par semaine passes-tu à gérer Uscreen ?",
    "Upload vidéos, support membres, config, bugs..."):
    blocks.append(b)

blocks.append(divider())

# --- Partie 2 : Besoins ---
blocks.append(heading2("Partie 2 — Ce dont tu as besoin"))

for b in question_block(5, "Classe ces fonctionnalités par ordre de priorité pour toi (1 = le plus important) :",
    "Mets un numéro devant chaque ligne."):
    blocks.append(b)

blocks.append(bullet(text("__ Héberger et diffuser les vidéos de formation (500+ vidéos)")))
blocks.append(bullet(text("__ Communauté / espace d'échange entre les membres")))
blocks.append(bullet(text("__ Parcours de formation structuré (modules, progression, évaluations)")))
blocks.append(bullet(text("__ Paiements récurrents (abonnements, membership)")))
blocks.append(bullet(text("__ Email marketing (séquences automatiques, newsletters)")))
blocks.append(bullet(text("__ Lives / webinaires avec replay")))
blocks.append(bullet(text("__ Site web / landing pages")))
blocks.append(bullet(text("__ App mobile pour les membres")))
blocks.append(bullet(text("__ Analytics / suivi de la progression des membres")))
blocks.append(bullet(text("__ Gamification (points, badges, niveaux)")))
blocks.append(paragraph())

for b in question_block(6, "Quelles tâches quotidiennes aimerais-tu que la nouvelle plateforme simplifie ?",
    "Upload, gestion membres, réponse support, envoi emails, stats..."):
    blocks.append(b)

for b in question_block(7, "Quelle est LA chose la plus importante pour que tu puisses bien travailler au quotidien ?",
    "Si tu ne pouvais choisir qu'un seul critère."):
    blocks.append(b)

blocks.append(divider())

# --- Partie 3 : Critères non-négociables ---
blocks.append(heading2("Partie 3 — Tes critères non-négociables"))

for b in question_block(8, "Si dans 2 ans on veut changer de plateforme, qu'est-ce qui doit être facilement récupérable ?",
    "Vidéos, liste membres, emails, contenus de formation, données de paiement..."):
    blocks.append(b)

for b in question_block(9, "Combien d'outils différents es-tu prête à gérer au quotidien ?",
    "1 seul outil ? 2-3 outils spécialisés ? Peu importe tant que ça marche ?"):
    blocks.append(b)

for b in question_block(10, "Quel est ton niveau de confort pour apprendre un nouvel outil ?",
    "Très à l'aise / Ça va si c'est bien documenté / J'ai besoin d'être formée"):
    blocks.append(b)

for b in question_block(11, "Qu'est-ce qui serait un DEALBREAKER absolu pour toi ?",
    "Le truc qui te ferait dire non immédiatement."):
    blocks.append(b)

blocks.append(divider())

# --- Partie 4 : Vision ---
blocks.append(heading2("Partie 4 — Ta vision"))

for b in question_block(12, "Dans 12 mois, à quoi ressemble ton quotidien idéal sur la plateforme ?",
    "Imagine que tout fonctionne parfaitement. Décris ce que tu fais et comment."):
    blocks.append(b)

for b in question_block(13, "Qu'est-ce qui t'a plu dans Kajabi quand tu as commencé à tester ?",
    "Et qu'est-ce qui t'a fait douter ou t'a manqué ?"):
    blocks.append(b)

for b in question_block(14, "Y a-t-il autre chose que tu veux que Catherine sache avant vendredi ?"):
    blocks.append(b)

blocks.append(divider())

blocks.append(callout("📌",
    text("Merci à toutes les deux ! ", bold=True),
    text("Vos réponses permettront de prendre la décision vendredi en toute connaissance de cause. Pas de bonne ou mauvaise réponse — c'est votre vécu et vos besoins qui comptent."),
    color="green_background"
))


# === PUSH ===
print(f"Envoi de {len(blocks)} blocs...")

for i in range(0, len(blocks), 100):
    batch = blocks[i:i+100]
    notion_patch(f"blocks/{page_id}/children", {"children": batch})
    print(f"  Batch {i//100 + 1}: {len(batch)} blocs")

print(f"✅ Questionnaire publié : https://www.notion.so/{page_id.replace('-', '')}")
