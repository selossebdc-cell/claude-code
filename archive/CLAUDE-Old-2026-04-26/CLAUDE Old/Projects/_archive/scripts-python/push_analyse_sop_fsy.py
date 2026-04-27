#!/usr/bin/env python3
"""Pousse l'analyse SOP Face Soul Yoga dans le Dashboard Production de Catherine."""

import json
import urllib.request

NOTION_TOKEN = "<SECRET-NOTION-TOKEN-REMOVED>"
DASHBOARD_PROD = "2f5c3a2f-4255-819d-8f33-ffbc33d6791f"
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

def numbered(*parts):
    return {"type": "numbered_list_item", "numbered_list_item": {"rich_text": list(parts)}}

def callout(emoji, *parts, color="default"):
    return {"type": "callout", "callout": {"rich_text": list(parts), "icon": {"type": "emoji", "emoji": emoji}, "color": color}}

def divider():
    return {"type": "divider", "divider": {}}

def toggle(title_parts, children):
    return {
        "type": "heading_3", "heading_3": {
            "rich_text": title_parts if isinstance(title_parts, list) else [text(title_parts)],
            "is_toggleable": True, "children": children,
        }
    }

def to_do(txt, checked=False):
    return {"type": "to_do", "to_do": {"rich_text": [text(txt)], "checked": checked}}

def table_block(rows, has_header=True):
    table_rows = []
    for row in rows:
        cells = [[text(cell)] for cell in row]
        table_rows.append({"type": "table_row", "table_row": {"cells": cells}})
    return {
        "type": "table", "table": {
            "table_width": len(rows[0]),
            "has_column_header": has_header,
            "has_row_header": False,
            "children": table_rows,
        }
    }


# === CRÉER LA PAGE ===

print("Création de la page analyse SOP...")

page = notion_post("pages", {
    "parent": {"page_id": DASHBOARD_PROD},
    "icon": {"type": "emoji", "emoji": "🔍"},
    "properties": {
        "title": {
            "title": [{"text": {"content": "Analyse SOP Face Soul Yoga — Proposition de travail"}}]
        }
    },
})

page_id = page["id"]
print(f"Page créée : {page_id}")

# === CONTENU ===

blocks = []

# En-tête
blocks.append(callout("📋",
    text("Document interne Catherine", bold=True),
    text(" — Analyse des 12 SOP documentées par Aurélia & Laurie. Base de travail pour structurer les sessions à venir."),
    color="gray_background"
))

blocks.append(paragraph(
    text("Rédigé le 25/02/2026 — CS Consulting Stratégique", italic=True, color="gray")
))

blocks.append(divider())

# === DIAGNOSTIC ===

blocks.append(heading1("Diagnostic"))

blocks.append(heading2("Ce qui est déjà posé"))

blocks.append(paragraph(
    text("La structure est là : 12 process identifiés, classés par département, avec RACI et potentiel d'automatisation. C'est un "),
    text("bon squelette", bold=True),
    text(". Mais les étapes sont quasi toutes \"à compléter en session\" — on est au stade "),
    text("cartographie", bold=True),
    text(", pas exécution."),
))

blocks.append(heading2("3 constats clés"))

# Constat 1
blocks.append(callout("🔴",
    text("Constat 1 — Aurélia est R+A sur quasi tout", bold=True),
    color="red_background"
))
blocks.append(paragraph(
    text("Elle est Responsable ET Approbatrice sur 10/12 process. Laurie est souvent Consultée ou absente. "),
    text("Tant que ça reste comme ça, la délégation est impossible.", bold=True),
    text(" C'est le nœud du problème."),
))

# Constat 2
blocks.append(callout("🟠",
    text("Constat 2 — Les process les plus douloureux sont les moins documentés", bold=True),
    color="orange_background"
))
blocks.append(bullet(
    text("Prospection (SOP 4)", bold=True),
    text(" : marquée \"inexistant\" — tout repose sur Instagram"),
))
blocks.append(bullet(
    text("Onboarding client (SOP 5)", bold=True),
    text(" : marquée \"flou\" — pas de parcours structuré"),
))
blocks.append(bullet(
    text("Publication RS (SOP 8)", bold=True),
    text(" : source principale d'épuisement, aucune étape formalisée"),
))

# Constat 3
blocks.append(callout("🟡",
    text("Constat 3 — Beaucoup d'outils marqués \"?\"", bold=True),
    color="yellow_background"
))
blocks.append(paragraph(
    text("Facturation, emailing, CRM, analytics — les outils ne sont pas encore choisis ou confirmés. Normal vu que la "),
    text("migration plateforme est en cours de décision", bold=True),
    text(" (vendredi 28/02)."),
))

blocks.append(divider())

# === PROPOSITION DE TRAVAIL ===

blocks.append(heading1("Proposition de travail — par ordre de priorité"))

# --- Phase 1 ---
blocks.append(heading2("Phase 1 — Stabiliser le quotidien (sessions 2-3)"))

blocks.append(callout("🎯",
    text("Objectif : ", bold=True),
    text("documenter les 3 process \"quick win\" qu'Aurélia et Laurie font déjà, pour que Laurie passe de Consultée à Responsable."),
    color="blue_background"
))

blocks.append(table_block([
    ["Process", "Pourquoi en premier", "Objectif"],
    ["SOP 8 — Publication RS", "C'est ce qui épuise le plus Aurélia", "Formaliser le workflow pour que Laurie prenne le relais sur la planification"],
    ["SOP 9 — Création contenu", "Le monteur est déjà recruté", "Clarifier le brief → livraison pour fluidifier la chaîne"],
    ["SOP 11 — Gestion Laurie", "Pas de système de brief/suivi", "Poser un cadre simple (brief hebdo + suivi) pour que tout le reste fonctionne"],
]))

blocks.append(paragraph())

blocks.append(toggle([text("Livrable Phase 1", bold=True)], [
    to_do("3 SOP complètes avec étapes concrètes et outils confirmés"),
    to_do("Laurie passe de \"C\" (Consultée) à \"R\" (Responsable) sur ces 3 process"),
    to_do("Rituel hebdo brief/suivi Aurélia-Laurie en place"),
]))

# --- Phase 2 ---
blocks.append(heading2("Phase 2 — Structurer le parcours client (sessions 4-5)"))

blocks.append(callout("🎯",
    text("Objectif : ", bold=True),
    text("une fois que l'opérationnel quotidien tourne mieux, structurer l'expérience client."),
    color="blue_background"
))

blocks.append(table_block([
    ["Process", "Pourquoi", "Objectif"],
    ["SOP 5 — Onboarding client", "\"Flou\" = perte de valeur perçue", "Créer un parcours d'accueil clair (J0 → J7 → J30)"],
    ["SOP 6 — Gestion emails/questions", "WhatsApp non cadré, week-ends", "Poser des règles + templates de réponse"],
    ["SOP 7 — Mailing Brevo", "Séquences inexistantes", "Créer les séquences de base (bienvenue, relance, upsell)"],
]))

blocks.append(paragraph())

blocks.append(toggle([text("Livrable Phase 2", bold=True)], [
    to_do("Parcours onboarding documenté (J0 → J7 → J30)"),
    to_do("Règles WhatsApp/email posées et communiquées aux clientes"),
    to_do("3 séquences Brevo créées (bienvenue, relance, upsell)"),
]))

# --- Phase 3 ---
blocks.append(heading2("Phase 3 — Après la décision plateforme (sessions 6+)"))

blocks.append(callout("⏳",
    text("En attente : ", bold=True),
    text("ces process dépendent de la décision migration du 28/02. Inutile de les formaliser avant."),
    color="yellow_background"
))

blocks.append(bullet(
    text("SOP 12 — Stack technique", bold=True),
    text(" → dépend de la décision Kajabi / Circle / Bunny"),
))
blocks.append(bullet(
    text("SOP 1 — Facturation", bold=True),
    text(" → dépend des outils de paiement choisis"),
))
blocks.append(bullet(
    text("SOP 3 — Benchmark coûts", bold=True),
    text(" → pertinent une fois la nouvelle stack en place"),
))

# --- Phase 4 ---
blocks.append(heading2("Phase 4 — Construire ce qui n'existe pas (mois 3-4)"))

blocks.append(callout("🚀",
    text("Objectif : ", bold=True),
    text("construire les leviers business une fois le quotidien stabilisé."),
    color="purple_background"
))

blocks.append(bullet(
    text("SOP 4 — Prospection hors RS", bold=True),
    text(" → le plus gros levier business, mais Aurélia n'est pas prête tant qu'elle est en mode pompier"),
))
blocks.append(bullet(
    text("SOP 2 — Relances paiements", bold=True),
    text(" → automatisable une fois l'outil de paiement choisi"),
))
blocks.append(bullet(
    text("SOP 10 — Planning/organisation semaine", bold=True),
    text(" → rituel à poser quand les autres process tournent"),
))

blocks.append(divider())

# === CE QU'ON NE FAIT PAS ===

blocks.append(heading1("Ce qu'on ne fait PAS maintenant"))

blocks.append(callout("⛔",
    text("Décisions délibérées", bold=True),
    text(" — pas par manque de temps, par choix stratégique."),
    color="red_background"
))

blocks.append(bullet(
    text("Ne pas tout documenter d'un coup", bold=True),
    text(" — ça ne tiendra pas, Aurélia est déjà saturée"),
))
blocks.append(bullet(
    text("Ne pas figer les outils", bold=True),
    text(" tant que la migration plateforme n'est pas décidée"),
))
blocks.append(bullet(
    text("Ne pas formaliser la prospection", bold=True),
    text(" tant que le quotidien n'est pas stabilisé"),
))
blocks.append(bullet(
    text("Ne pas chercher la perfection", bold=True),
    text(" — un process \"80% ok\" qu'on utilise vaut mieux qu'un process parfait qu'on ne suit pas"),
))

blocks.append(divider())

# === RÉSUMÉ ===

blocks.append(callout("💡",
    text("Logique globale : ", bold=True),
    text("stabiliser le quotidien → structurer le parcours client → migrer les outils → construire l'acquisition. Process par process, sans tout casser."),
    color="blue_background"
))

blocks.append(paragraph(
    text("Lien avec la feuille de route : ", bold=True),
    text("cette analyse alimente directement le Pilier 2 (Parcours Client & Organisation) et le Pilier 4 (Systèmes & Délégation) de l'accompagnement Clarté & Autonomie."),
))


# === PUSH ===
print(f"Envoi de {len(blocks)} blocs...")

for i in range(0, len(blocks), 100):
    batch = blocks[i:i+100]
    notion_patch(f"blocks/{page_id}/children", {"children": batch})
    print(f"  Batch {i//100 + 1}: {len(batch)} blocs")

print(f"Done — https://www.notion.so/{page_id.replace('-', '')}")
