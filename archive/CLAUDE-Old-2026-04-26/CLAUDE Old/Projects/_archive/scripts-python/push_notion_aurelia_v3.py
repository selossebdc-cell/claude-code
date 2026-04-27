#!/usr/bin/env python3
"""Push comparatif plateformes — aide à la décision vendredi — portabilité au centre."""

import json
import urllib.request

NOTION_TOKEN = "<SECRET-NOTION-TOKEN-REMOVED>"
PAGE_ID = "30cc3a2f-4255-8146-a663-c656ed28b6a0"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def append_blocks(page_id, blocks):
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        data = json.dumps({"children": batch}).encode()
        req = urllib.request.Request(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            data=data, headers=HEADERS, method="PATCH"
        )
        with urllib.request.urlopen(req) as resp:
            json.loads(resp.read())
        print(f"  Batch {i//100 + 1}: {len(batch)} blocs")


def text(content, bold=False, italic=False, color="default", code=False, strikethrough=False):
    return {
        "type": "text", "text": {"content": content},
        "annotations": {"bold": bold, "italic": italic, "color": color, "code": code, "strikethrough": strikethrough},
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

def numbered(*parts):
    return {"type": "numbered_list_item", "numbered_list_item": {"rich_text": list(parts)}}

def todo(label, checked=False):
    return {"type": "to_do", "to_do": {"rich_text": [text(label)], "checked": checked}}

def callout(emoji, *parts, color="default"):
    return {"type": "callout", "callout": {"rich_text": list(parts), "icon": {"type": "emoji", "emoji": emoji}, "color": color}}

def divider():
    return {"type": "divider", "divider": {}}

def table_row(cells):
    return {"type": "table_row", "table_row": {"cells": [[text(c)] for c in cells]}}

def table_block(headers, rows, header_row=True):
    all_rows = [table_row(headers)] + [table_row(r) for r in rows]
    return {
        "type": "table", "table": {
            "table_width": len(headers), "has_column_header": header_row,
            "has_row_header": False, "children": all_rows,
        }
    }

def toggle(title_parts, children):
    return {
        "type": "heading_2", "heading_2": {
            "rich_text": title_parts if isinstance(title_parts, list) else [text(title_parts)],
            "is_toggleable": True, "children": children,
        }
    }

def toggle3(title_parts, children):
    return {
        "type": "heading_3", "heading_3": {
            "rich_text": title_parts if isinstance(title_parts, list) else [text(title_parts)],
            "is_toggleable": True, "children": children,
        }
    }


# === CONTENU V3 ===

blocks = []

# --- EN-TÊTE ---
blocks.append(callout("📋",
    text("Aide à la décision — Vendredi 28 février 2026", bold=True),
    text("\nComparatif plateformes pour la migration d'Aurélia hors d'Uscreen."),
    text("\nCritère n°1 : ne pas être bloquée. Pouvoir partir si ça ne va plus.", bold=True),
    color="blue_background"
))
blocks.append(paragraph(
    text("Catherine Selosse / CS Consulting Stratégique — Mis à jour le 24 février 2026", italic=True, color="gray"),
))
blocks.append(divider())

# ==========================================
# LE PROBLÈME USCREEN
# ==========================================

blocks.append(heading1("Le problème qu'on résout"))

blocks.append(callout("🔒",
    text("Uscreen = prison dorée.", bold=True),
    text(" Les vidéos, les membres, les paiements sont enfermés dans un seul outil. Quand on veut partir, tout est à refaire. "),
    text("On ne veut pas reproduire ça.", bold=True),
    color="red_background"
))

blocks.append(paragraph(
    text("Le principe directeur : ", bold=True),
    text("chaque brique doit pouvoir être remplacée indépendamment. Si un outil ne convient plus, on le change sans toucher au reste.")
))

blocks.append(divider())

# ==========================================
# LES 2 ARCHITECTURES POSSIBLES
# ==========================================

blocks.append(heading1("Les 2 architectures possibles"))

# --- Architecture A ---
blocks.append(toggle(
    [text("🧱 Architecture A — Modulaire (Circle + Bunny + Brevo)", bold=True)],
    [
        callout("💡", text("Philosophie : 3 outils spécialisés, chacun remplaçable indépendamment."), color="blue_background"),
        paragraph(),
        table_block(
            ["Rôle", "Outil", "Coût/mois", "Si on veut partir"],
            [
                ["📹 Vidéos", "Bunny.net", "5-15€", "Les vidéos restent, on change juste où elles s'affichent"],
                ["🏘️ Communauté + cours", "Circle.so Professional", "89$", "Export CSV membres. Vidéos pas touchées."],
                ["📧 Emails", "Brevo", "0-25€", "Export liste en 1 clic. Standard du marché."],
                ["TOTAL", "", "~110-130$/mois", "Chaque brique est indépendante"],
            ]
        ),
        paragraph(),
        paragraph(text("Forces :", bold=True)),
        bullet(text("Portabilité maximale", bold=True), text(" — les vidéos (l'actif le plus lourd) sont sur Bunny, pas sur Circle. Si Circle déçoit, on change Circle, les 500 vidéos ne bougent pas.")),
        bullet(text("Communauté = point fort de Circle", bold=True), text(" — meilleure expérience communautaire que Kajabi")),
        bullet(text("Coût maîtrisé", bold=True), text(" — Bunny facture à l'usage réel")),
        bullet(text("Emails indépendants", bold=True), text(" — Brevo est un standard, portable partout")),
        paragraph(),
        paragraph(text("Faiblesses :", bold=True)),
        bullet(text("3 outils à gérer", bold=True), text(" — 3 back-offices, 3 factures, 3 interfaces pour Laurie")),
        bullet(text("Pas de funnels ni de landing pages", bold=True), text(" — il faut un outil supplémentaire (ou garder Wix)")),
        bullet(text("Cours moins structurés que Kajabi", bold=True), text(" — Circle est communauté-first, les cours sont un ajout")),
        bullet(text("Frais de transaction Circle : 0.5 à 2%", bold=True)),
    ]
))

# --- Architecture B ---
blocks.append(toggle(
    [text("📦 Architecture B — Tout-en-un (Kajabi)", bold=True)],
    [
        callout("💡", text("Philosophie : un seul outil qui fait tout. Plus simple au quotidien, mais plus dur à quitter."), color="blue_background"),
        paragraph(),
        table_block(
            ["Rôle", "Outil", "Coût/mois", "Si on veut partir"],
            [
                ["📹 Vidéos", "Kajabi (via Wistia)", "Inclus", "⚠️ Téléchargement vidéo par vidéo. Pas d'export en masse."],
                ["🏘️ Communauté + cours", "Kajabi", "Inclus", "⚠️ Structure cours à recréer de zéro sur la nouvelle plateforme"],
                ["📧 Emails", "Kajabi", "Inclus", "⚠️ Export CSV contacts OK. Automations/séquences perdues."],
                ["🔗 Funnels + site", "Kajabi", "Inclus", "⚠️ Pages et funnels non portables"],
                ["TOTAL", "", "~199$/mois (Growth)", "Tout est lié. Partir = tout reconstruire."],
            ]
        ),
        paragraph(),
        paragraph(text("Forces :", bold=True)),
        bullet(text("Un seul outil", bold=True), text(" — Laurie n'a qu'un back-office à apprendre")),
        bullet(text("Formation structurée = point fort", bold=True), text(" — meilleur que Circle pour les parcours, évaluations, templates")),
        bullet(text("Vidéo illimitée incluse", bold=True), text(" — pas de coût supplémentaire pour 500 vidéos")),
        bullet(text("Email + funnels + site inclus", bold=True), text(" — pas besoin de Brevo ni de Wix")),
        bullet(text("0% de frais de transaction", bold=True)),
        paragraph(),
        paragraph(text("Faiblesses :", bold=True)),
        bullet(text("Lock-in élevé", bold=True, color="red"), text(" — si Kajabi augmente ses prix, change ses conditions, ou déçoit : extraire 500 vidéos une par une + recréer la structure cours + migrer les emails + reconstruire les funnels. C'est le scénario Uscreen bis.", color="red")),
        bullet(text("Export vidéos = manuel, une par une", bold=True), text(". Pas d'export en masse. Pour 500 vidéos, c'est des jours de travail.")),
        bullet(text("Communauté moins forte que Circle", bold=True)),
        bullet(text("Plus cher", bold=True), text(" : 199$/mois vs ~120$/mois modulaire")),
        bullet(text("Limite 15 produits (Growth)", bold=True), text(". Au-delà → Pro à 399$/mois.")),
    ]
))

# --- Architecture C (hybride) ---
blocks.append(toggle(
    [text("🔀 Architecture C — Hybride (Kajabi + Bunny.net)", bold=True)],
    [
        callout("💡", text("Philosophie : profiter de la simplicité Kajabi tout en sécurisant l'actif le plus critique (les vidéos) en externe."), color="blue_background"),
        paragraph(),
        table_block(
            ["Rôle", "Outil", "Coût/mois", "Si on veut partir"],
            [
                ["📹 Vidéos", "Bunny.net (embed dans Kajabi)", "5-15€", "✅ Vidéos intactes, on change juste la plateforme d'affichage"],
                ["🏘️ Communauté + cours", "Kajabi", "149-199$", "⚠️ Structure cours à recréer, mais vidéos pas touchées"],
                ["📧 Emails", "Kajabi", "Inclus", "⚠️ Export CSV OK, automations perdues"],
                ["🔗 Funnels + site", "Kajabi", "Inclus", "⚠️ Pages non portables"],
                ["TOTAL", "", "~165-215$/mois", "L'actif lourd (vidéos) est sécurisé"],
            ]
        ),
        paragraph(),
        paragraph(text("L'idée :", bold=True), text(" on ne stocke PAS les vidéos dans Kajabi. On les met sur Bunny.net et on les intègre par embed. Kajabi sert de vitrine (cours, communauté, paiements, emails) mais l'actif le plus lourd — les 500 vidéos — reste portable.")),
        paragraph(),
        paragraph(text("Forces :", bold=True)),
        bullet(text("Le meilleur des deux mondes", bold=True), text(" — simplicité Kajabi + portabilité vidéos")),
        bullet(text("Si Kajabi déçoit", bold=True), text(" : on migre la communauté/cours (léger) mais les vidéos ne bougent pas")),
        bullet(text("Si Bunny déçoit", bold=True), text(" : on peut toujours basculer les vidéos sur Kajabi natif")),
        paragraph(),
        paragraph(text("Faiblesses :", bold=True)),
        bullet(text("Un outil de plus à gérer (Bunny)", bold=True), text(" — mais interface très simple")),
        bullet(text("Coût un peu supérieur", bold=True), text(" au Kajabi pur")),
        bullet(text("Emails et funnels restent dépendants de Kajabi", bold=True)),
    ]
))

blocks.append(divider())

# ==========================================
# COMPARATIF PORTABILITÉ
# ==========================================

blocks.append(heading1("Le vrai sujet : la portabilité"))

blocks.append(callout("🔑",
    text("Si demain on veut partir, qu'est-ce qu'on peut emporter ?", bold=True),
    color="yellow_background"
))

blocks.append(table_block(
    ["Donnée à exporter", "Circle + Bunny", "Kajabi seul", "Kajabi + Bunny"],
    [
        ["500 vidéos", "✅ Bunny = rien à faire, elles sont déjà ailleurs", "🔴 Une par une, manuellement. Jours de travail.", "✅ Bunny = rien à faire"],
        ["Liste membres + emails", "✅ CSV (Circle) + CSV (Brevo)", "✅ CSV export", "✅ CSV export"],
        ["Automations email", "⚠️ À recréer (Brevo vers autre)", "🔴 Perdues (pas de format standard)", "🔴 Perdues"],
        ["Structure des cours", "⚠️ À recréer (textes + liens)", "🔴 À recréer de zéro", "⚠️ À recréer, mais vidéos intactes"],
        ["Funnels / landing pages", "N/A (pas dans Circle)", "🔴 Non portables", "🔴 Non portables"],
        ["Paiements Stripe", "✅ Stripe = indépendant", "✅ Stripe = indépendant", "✅ Stripe = indépendant"],
        ["Données communauté (posts, échanges)", "⚠️ Non exportable", "⚠️ Non exportable", "⚠️ Non exportable"],
    ]
))

blocks.append(paragraph())

blocks.append(callout("⚡",
    text("L'élément décisif : les 500 vidéos.", bold=True),
    text(" C'est l'actif le plus lourd, le plus long à migrer. Si les vidéos sont sur Bunny.net, on est libre. Si elles sont dans Kajabi, c'est des jours d'extraction manuelle pour partir."),
    color="red_background"
))

blocks.append(divider())

# ==========================================
# COMPARATIF PLATEFORMES DÉTAILLÉ
# ==========================================

blocks.append(heading1("Comparatif détaillé des plateformes"))

blocks.append(table_block(
    ["Critère", "Circle.so", "Kajabi", "Skool"],
    [
        ["Prix/mois", "89$ (Pro) — 199$ (Enterprise)", "149$ (Basic) — 199$ (Growth)", "99$ (Pro)"],
        ["Formation structurée", "✅ Bon (parcours, modules)", "✅ Excellent (templates, évaluations, IA)", "⚠️ Basique (pas de quiz, pas de certificat)"],
        ["Communauté", "✅ Excellent (conçu pour ça)", "✅ Correct (ajout récent)", "✅ Excellent (gamification forte)"],
        ["Vidéo native", "200GB-1TB (selon plan)", "Illimité (Wistia)", "Hébergement limité (renvoi YouTube/Vimeo)"],
        ["Email marketing", "❌ Outil tiers (Brevo, etc.)", "✅ Inclus", "❌ Outil tiers"],
        ["Funnels / landing pages", "❌ Outil tiers", "✅ Inclus", "❌ Non"],
        ["App mobile", "✅ Oui", "✅ Oui", "✅ Oui"],
        ["Frais de transaction", "0.5-2%", "0%", "2.9%"],
        ["Lives + replays", "✅ 30-1000 participants", "✅ Zoom intégré", "✅ 10 000 participants"],
        ["Export données", "✅ CSV membres", "✅ CSV contacts + vidéos (une par une)", "⚠️ Export très limité"],
        ["Export vidéos", "N/A (vidéos externes)", "⚠️ Manuelle, une par une", "N/A (vidéos externes)"],
        ["Lock-in global", "🟢 Faible (si vidéos sur Bunny)", "🔴 Élevé (tout est lié)", "🟠 Moyen (contenu non exportable)"],
    ]
))

blocks.append(divider())

# ==========================================
# SOLUTIONS ÉLIMINÉES
# ==========================================

blocks.append(toggle(
    [text("🚫 Solutions éliminées")],
    [
        bullet(text("YouTube Non-Référencé", bold=True, strikethrough=True), text(" — Sécurité illusoire, téléchargeable en 30s, risque suspension chaîne. Incompatible offre premium 299€/mois.")),
        bullet(text("Wistia (standalone)", bold=True, strikethrough=True), text(" — 500€+/mois pour 500 vidéos. Conçu B2B. Hors budget. (Mais inclus gratuitement dans Kajabi.)")),
        bullet(text("Wooskill", bold=True, strikethrough=True), text(" — Marketplace créateurs, pas plateforme formation. Commission 5%+9.5%. Portabilité quasi nulle.")),
        bullet(text("Skool", bold=True, strikethrough=True), text(" — Excellent en communauté mais pas de quiz/certificats, export quasi impossible, pas d'email ni funnel. Trop limité pour 500 vidéos de formation structurée.")),
    ]
))

blocks.append(divider())

# ==========================================
# RECOMMANDATION CATHERINE
# ==========================================

blocks.append(heading1("Recommandation Catherine"))

blocks.append(callout("🎯",
    text("Mon conseil : Architecture C — Kajabi + Bunny.net", bold=True),
    color="green_background"
))

blocks.append(paragraph())
blocks.append(paragraph(
    text("Pourquoi pas Kajabi seul ? ", bold=True),
    text("Parce qu'Aurélia sort d'Uscreen et sait ce que c'est d'être bloquée. Mettre 500 vidéos dans Kajabi, c'est refaire la même erreur. Si dans 2 ans Kajabi double ses prix ou change ses conditions, on est coincées avec des jours d'extraction manuelle."),
))

blocks.append(paragraph(
    text("Pourquoi pas Circle + Bunny seul ? ", bold=True),
    text("Parce qu'Aurélia a besoin de simplifier. 3 outils + un outil funnel + un outil email = 5 interfaces. À 50h/semaine dont 80% opérationnel, c'est trop."),
))

blocks.append(paragraph(
    text("Le compromis : ", bold=True),
    text("Kajabi pour la simplicité au quotidien (1 outil, cours structurés, email, funnels) "),
    text("+ Bunny.net pour la liberté (les vidéos restent portables, l'actif critique n'est jamais bloqué).", bold=True),
    text(" Le jour où Kajabi ne convient plus, les vidéos ne bougent pas — on reconstruit le reste."),
))

blocks.append(paragraph())
blocks.append(paragraph(
    text("Si la simplicité maximale prime sur tout", bold=True),
    text(" → Kajabi seul, en acceptant le risque de lock-in sur les vidéos."),
))
blocks.append(paragraph(
    text("Si la portabilité maximale prime sur tout", bold=True),
    text(" → Circle + Bunny + Brevo, en acceptant la complexité de 3+ outils."),
))

blocks.append(divider())

# ==========================================
# DÉCISION VENDREDI
# ==========================================

blocks.append(heading1("Décision à prendre vendredi"))

blocks.append(heading3("Question 1 — Où vivent les vidéos ?"))
blocks.append(bullet(text("Option A : dans Kajabi (simple, mais lock-in)", italic=True)))
blocks.append(bullet(text("Option B : sur Bunny.net, embedées dans la plateforme choisie (portable, un outil de plus)", italic=True)))

blocks.append(heading3("Question 2 — Quelle plateforme principale ?"))
blocks.append(bullet(text("Option A : Kajabi (tout-en-un, cours structurés, email + funnels inclus)", italic=True)))
blocks.append(bullet(text("Option B : Circle (meilleure communauté, mais besoin d'outils complémentaires)", italic=True)))

blocks.append(heading3("Question 3 — Quel niveau de complexité est acceptable pour Laurie ?"))
blocks.append(bullet(text("1 outil (Kajabi) → le plus simple", italic=True)))
blocks.append(bullet(text("2 outils (Kajabi + Bunny) → bon compromis", italic=True)))
blocks.append(bullet(text("3+ outils (Circle + Bunny + Brevo) → le plus portable mais le plus lourd", italic=True)))

blocks.append(divider())
blocks.append(paragraph(
    text("Document de travail Catherine Selosse — CS Consulting Stratégique", bold=True),
    text(" — À discuter en session vendredi 28 février", color="gray"),
))


# === PUSH ===
print(f"Envoi de {len(blocks)} blocs vers Notion...")
append_blocks(PAGE_ID, blocks)
print("✅ Page publiée.")
