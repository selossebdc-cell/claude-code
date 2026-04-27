#!/usr/bin/env python3
"""Push le plan d'action migration plateforme Aurélia dans Notion — format natif optimisé."""

import json
import urllib.request

NOTION_TOKEN = "<SECRET-NOTION-TOKEN-REMOVED>"
PAGE_ID = "30cc3a2f-4255-8146-a663-c656ed28b6a0"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def notion_request(endpoint, data=None, method="GET"):
    url = f"https://api.notion.com/v1/{endpoint}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method if data is None else "PATCH" if "pages" in endpoint else "POST")
    if data and "blocks" in endpoint and "children" not in endpoint:
        req.method = method
    if data:
        req.method = "PATCH" if method == "PATCH" else "POST"
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")
        raise


def append_blocks(page_id, blocks):
    """Append blocks in batches of 100 (Notion limit)."""
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        result = notion_request(f"blocks/{page_id}/children", {"children": batch}, method="PATCH")
        print(f"  Batch {i//100 + 1}: {len(batch)} blocs ajoutés")
    return result


# === HELPERS NOTION BLOCKS ===

def text(content, bold=False, italic=False, color="default", code=False):
    return {
        "type": "text",
        "text": {"content": content},
        "annotations": {"bold": bold, "italic": italic, "color": color, "code": code},
    }


def heading1(txt):
    return {"type": "heading_1", "heading_1": {"rich_text": [text(txt)], "color": "default"}}


def heading2(txt):
    return {"type": "heading_2", "heading_2": {"rich_text": [text(txt)], "color": "default"}}


def heading3(txt):
    return {"type": "heading_3", "heading_3": {"rich_text": [text(txt)], "color": "default"}}


def paragraph(*parts):
    return {"type": "paragraph", "paragraph": {"rich_text": list(parts)}}


def bullet(*parts):
    return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": list(parts)}}


def todo(label, checked=False):
    return {"type": "to_do", "to_do": {"rich_text": [text(label)], "checked": checked}}


def callout(emoji, *parts, color="default"):
    return {"type": "callout", "callout": {"rich_text": list(parts), "icon": {"type": "emoji", "emoji": emoji}, "color": color}}


def divider():
    return {"type": "divider", "divider": {}}


def table_row(cells):
    return {
        "type": "table_row",
        "table_row": {
            "cells": [[text(c)] for c in cells]
        }
    }


def table_block(headers, rows, header_row=True):
    all_rows = [table_row(headers)] + [table_row(r) for r in rows]
    return {
        "type": "table",
        "table": {
            "table_width": len(headers),
            "has_column_header": header_row,
            "has_row_header": False,
            "children": all_rows,
        }
    }


def toggle(title_parts, children):
    """Toggle heading 2 with children."""
    return {
        "type": "heading_2",
        "heading_2": {
            "rich_text": title_parts if isinstance(title_parts, list) else [text(title_parts)],
            "is_toggleable": True,
            "children": children,
        }
    }


def toggle3(title_parts, children):
    """Toggle heading 3 with children."""
    return {
        "type": "heading_3",
        "heading_3": {
            "rich_text": title_parts if isinstance(title_parts, list) else [text(title_parts)],
            "is_toggleable": True,
            "children": children,
        }
    }


# === CONTENU ===

blocks = []

# --- EN-TÊTE ---
blocks.append(callout("🎯", text("Clarifier les décisions clés pour migrer la plateforme d'Aurélia hors d'Uscreen. "), text("Trois axes : ", bold=True), text("stockage vidéo, choix de plateforme communautaire, plan d'action."), color="blue_background"))
blocks.append(paragraph(text("Document de travail — Catherine Selosse / CS Consulting Stratégique — Février 2026", italic=True, color="gray")))
blocks.append(divider())

# ==========================================
# PARTIE 1 — STOCKAGE VIDÉO
# ==========================================

blocks.append(heading1("Stockage vidéo : la décision clé"))
blocks.append(paragraph(text("Avant de choisir la plateforme communautaire, il faut trancher : "), text("où vont physiquement vivre les 500 vidéos ?", bold=True), text(" Ce choix conditionne les coûts, la sécurité et la portabilité future.")))

# YouTube éliminé
blocks.append(toggle3(
    [text("🚫 YouTube Non-Référencé — ÉLIMINÉ", bold=True)],
    [
        callout("⚠️",
            text("Sécurité illusoire", bold=True),
            text(" — Un lien non listé reste une URL publique. Des outils gratuits (yt-dlp, Video DownloadHelper) téléchargent les vidéos en 30 secondes."),
            color="red_background"
        ),
        bullet(text("Risque légal : ", bold=True), text("YouTube peut suspendre la chaîne pour utilisation abusive de l'API. 500 vidéos disparaissent sans préavis.")),
        bullet(text("Image dégradée : ", bold=True), text("Un membre qui paie 299€/mois découvre ses cours sur YouTube gratuit → sentiment d'arnaque, demande de remboursement.")),
    ]
))

# Wistia éliminé
blocks.append(toggle3(
    [text("🚫 Wistia — ÉLIMINÉ", bold=True)],
    [
        paragraph(text("Outil B2B (lead gen, capture emails). Pas conçu pour la formation.")),
        table_block(
            ["Plan Wistia", "Vidéos incluses", "Prix/mois"],
            [
                ["Plus", "50 vidéos", "79$/mois"],
                ["Advanced", "250 vidéos", "319$/mois — INSUFFISANT"],
                ["Enterprise (500 vidéos)", "Sur devis", "500€+/mois estimé"],
            ]
        ),
        paragraph(text("Hors budget et inadapté à l'échelle d'Aurélia.", italic=True, color="gray")),
    ]
))

# Bunny.net recommandé
blocks.append(callout("✅",
    text("RECOMMANDÉ : Bunny.net", bold=True),
    text(" — Spécialiste streaming vidéo sécurisé. CDN mondial (119 points). Portabilité totale."),
    color="green_background"
))

blocks.append(toggle3(
    [text("Pourquoi Bunny.net change tout")],
    [
        bullet(text("Protection DRM réelle : ", bold=True), text("restriction par domaine, token d'accès, impossible à télécharger")),
        bullet(text("CDN mondial : ", bold=True), text("lecture fluide partout (France et international)")),
        bullet(text("Portabilité totale : ", bold=True), text("les vidéos s'intègrent par embed dans n'importe quelle plateforme. Changement de plateforme = 0 migration vidéo")),
        bullet(text("Transcoding + sous-titres auto inclus", bold=True)),
        paragraph(),
        table_block(
            ["Composant", "Coût/mois"],
            [
                ["Stockage (~500 vidéos / 100-200 GB)", "1-2€"],
                ["Streaming (bande passante)", "3-10€"],
                ["TOTAL Bunny.net", "~5-15€ vs ~125€ sur Uscreen"],
            ]
        ),
    ]
))

blocks.append(divider())

# ==========================================
# PARTIE 2 — COMPARATIF PLATEFORMES
# ==========================================

blocks.append(heading1("Comparatif plateformes communautaires"))
blocks.append(paragraph(text("Avec Bunny.net pour les vidéos, la plateforme n'a plus besoin de gérer le stockage. Son rôle : "), text("communauté, modules de formation, interactions, paiements.", bold=True)))

# Tableau comparatif principal
blocks.append(heading2("Vue d'ensemble"))
blocks.append(table_block(
    ["Critère", "Circle.so", "Skool", "Wooskill", "Kajabi"],
    [
        ["Prix/mois", "89-199$", "9$ ou 99$", "Abo + 5-9.5% commission", "89-199$"],
        ["Communauté", "✅ Excellent", "✅ Excellent", "⚠️ Limité", "✅ Bon"],
        ["Gamification", "✅ Oui", "✅ Fort (points, niveaux)", "❌ Non", "⚠️ Limité"],
        ["App mobile", "✅ Oui", "✅ iOS + Android", "⚠️ Web mobile", "✅ Oui"],
        ["Frais transaction", "0.5-2%", "2.9-10%", "5% + 9.5%", "0%"],
        ["Lives + replays", "✅ 30-1000p + replay", "✅ 10 000p + replay", "✅ 250p max", "✅ Zoom intégré"],
        ["Export données", "✅ CSV membres", "⚠️ Basique", "❌ Dépendance", "✅ CSV"],
        ["Verdict", "✅ TOP CHOIX", "✅ Alternative", "🚫 Éliminé", "⚠️ Trop large"],
    ]
))

# Détail par plateforme
blocks.append(toggle(
    [text("🟢 Circle.so — Le choix recommandé")],
    [
        paragraph(text("Référence pour les créateurs qui combinent communauté premium et formation structurée. Interface propre, professionnelle.")),
        bullet(text("Professional (89$/mois) : ", bold=True), text("200 GB stockage. Avec Bunny.net, largement suffisant.")),
        bullet(text("Enterprise (199$/mois) : ", bold=True), text("1 TB. Option si Bunny non retenu.")),
        bullet(text("Migration : ", bold=True), text("Circle propose une aide à la migration sur plans Business/Enterprise.")),
        bullet(text("Frais : ", bold=True), text("2% (Professional) ou 0.5% (Enterprise).")),
        bullet(text("Domaine custom, couleurs, logo — aspect pro garanti.")),
        callout("💡", text("Seule faiblesse : ", bold=True), text("customisation avancée de la marque moins flexible que Kajabi."), color="yellow_background"),
    ]
))

blocks.append(toggle(
    [text("🟡 Skool — L'alternative communauté-first")],
    [
        paragraph(text("Philosophie : la communauté au centre, le cours en soutien. Pertinent si l'engagement et la rétention sont la priorité absolue.")),
        bullet(text("Pro (99$/mois) : ", bold=True), text("illimité en membres et cours, 2.9% de frais, app mobile.")),
        bullet(text("Gamification native très forte : ", bold=True), text("points, niveaux, classements.")),
        callout("⚠️", text("Points critiques : ", bold=True), text("contenu des cours non exportable en format structuré (risque lock-in). Pas d'email marketing intégré → outils tiers nécessaires."), color="orange_background"),
        paragraph(text("Verdict : ", bold=True), text("excellent pour communauté engagée. Moins adapté si la priorité est la formation structurée.")),
    ]
))

blocks.append(toggle(
    [text("🔴 Wooskill — Éliminé")],
    [
        paragraph(text("Marketplace française pour créateurs. Pas une plateforme de formation structurée.")),
        bullet(text("Commission cumulée élevée (5% + 9.5%)")),
        bullet(text("Dépendance marketplace : si on quitte, on perd l'audience")),
        bullet(text("Portabilité quasi nulle — modèle conçu pour garder les créateurs captifs")),
        paragraph(text("À éliminer sans hésitation.", bold=True, color="red")),
    ]
))

blocks.append(toggle(
    [text("🟠 Kajabi — En réserve (12-18 mois)")],
    [
        paragraph(text("Tout-en-un très puissant mais surdimensionné et coûteux à ce stade.")),
        bullet(text("89$ (Basic, 3 produits) à 199$ (Growth). 0% de frais.")),
        bullet(text("Courbe d'apprentissage élevée.")),
        paragraph(text("À reconsidérer dans 12-18 mois si besoin de tout centraliser.", italic=True)),
    ]
))

blocks.append(divider())

# ==========================================
# STACK RECOMMANDÉE
# ==========================================

blocks.append(heading1("Stack recommandée"))
blocks.append(callout("💡", text("Principe directeur : la modularité avant tout. ", bold=True), text("Un outil qui fait tout = un outil qui bloque de partout. Chaque brique doit être remplaçable indépendamment."), color="blue_background"))

blocks.append(table_block(
    ["Rôle", "Outil", "Coût/mois", "Portabilité"],
    [
        ["📹 Stockage vidéo", "Bunny.net", "5-15€", "Embed universel. Migration = 0 travail"],
        ["🏘️ Communauté + cours", "Circle.so Professional (ou Skool Pro)", "89-99$", "Export CSV membres"],
        ["📧 Email marketing", "Brevo (ex Sendinblue)", "0-25€", "Export liste en 1 clic"],
        ["TOTAL", "", "~100-140€/mois", "vs 125€ Uscreen, sans blocage"],
    ]
))

blocks.append(divider())

# ==========================================
# PLAN D'ACTION
# ==========================================

blocks.append(heading1("Plan d'action"))

blocks.append(heading2("Décisions à prendre (dans l'ordre)"))

blocks.append(heading3("Décision 1 — Valider Bunny.net"))
blocks.append(paragraph(text("Aurélia valide-t-elle après test que la qualité de lecture est suffisante ?")))
blocks.append(bullet(text("Si OUI → ", bold=True), text("on intègre Bunny à la plateforme choisie")))
blocks.append(bullet(text("Si NON → ", bold=True), text("on opte pour Circle Enterprise (1TB natif) à 199$/mois")))

blocks.append(heading3("Décision 2 — Circle ou Skool ?"))
blocks.append(paragraph(text("Quelle est la priorité n°1 pour Aurélia ?")))
blocks.append(bullet(text("« Je veux un espace de formation structuré et professionnel » → ", bold=True), text("Circle.so")))
blocks.append(bullet(text("« Je veux une communauté vivante et engagée au quotidien » → ", bold=True), text("Skool")))
blocks.append(paragraph(text("Les deux sont valables avec Bunny.net. Tester les deux pendant l'essai gratuit (14 jours).", italic=True)))

blocks.append(divider())

blocks.append(heading2("Actions immédiates"))

blocks.append(heading3("👩 Laurie"))
blocks.append(todo("Créer un compte Bunny.net (gratuit). Uploader 5 vidéos test (variété : courte, longue, HD). Générer les embeds."))
blocks.append(todo("Lancer les 2 essais gratuits (Circle Professional + Skool Pro). Créer une structure basique dans chacun."))
blocks.append(todo("Intégrer les embeds Bunny.net dans une page de test Circle ET Skool."))

blocks.append(heading3("🎯 Aurélia"))
blocks.append(todo("Tester en tant que MEMBRE les 2 plateformes démo. Répondre : (1) Laquelle me ressemble ? (2) Laquelle pour mes clientes ?"))
blocks.append(todo("Valider la qualité de lecture Bunny.net sur les 5 vidéos test."))
blocks.append(todo("Lancer l'extraction des vidéos Uscreen en parallèle — priorité : les 50 vidéos les plus vues."))

blocks.append(divider())

# Récap décisions éliminées
blocks.append(toggle(
    [text("📋 Récapitulatif des décisions éliminées")],
    [
        table_block(
            ["Outil éliminé", "Raison principale"],
            [
                ["🚫 YouTube Non-Référencé", "Sécurité illusoire, téléchargeable en 30s, risque suspension, image dégradée pour 299€/mois"],
                ["🚫 Wistia", "500€+/mois pour 500 vidéos. Conçu B2B, pas formation. Hors budget."],
                ["🚫 Wooskill", "Marketplace, pas plateforme formation. Commission élevée. Portabilité nulle."],
                ["⏳ Kajabi", "Trop complexe et cher à ce stade. En réserve 12-18 mois."],
            ]
        ),
    ]
))

blocks.append(paragraph())
blocks.append(paragraph(text("Deadline actions Laurie : vendredi", bold=True), text(" — Prochaine étape : session de décision avec Aurélia", color="gray")))

# === PUSH ===

print(f"Envoi de {len(blocks)} blocs vers Notion...")
append_blocks(PAGE_ID, blocks)
print("✅ Contenu publié dans Notion avec succès.")
