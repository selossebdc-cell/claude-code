#!/usr/bin/env python3
"""Push le plan d'action migration Kajabi — Aurélia — v2 mise à jour."""

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
        "type": "text",
        "text": {"content": content},
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
        "type": "table",
        "table": {
            "table_width": len(headers),
            "has_column_header": header_row,
            "has_row_header": False,
            "children": all_rows,
        }
    }


def toggle(title_parts, children):
    return {
        "type": "heading_2",
        "heading_2": {
            "rich_text": title_parts if isinstance(title_parts, list) else [text(title_parts)],
            "is_toggleable": True,
            "children": children,
        }
    }


def toggle3(title_parts, children):
    return {
        "type": "heading_3",
        "heading_3": {
            "rich_text": title_parts if isinstance(title_parts, list) else [text(title_parts)],
            "is_toggleable": True,
            "children": children,
        }
    }


# === CONTENU V2 — RECENTRÉ KAJABI ===

blocks = []

# --- EN-TÊTE ---
blocks.append(callout("🎯",
    text("Migration plateforme Aurélia — "),
    text("Décision : Kajabi", bold=True),
    color="green_background"
))
blocks.append(paragraph(
    text("Mis à jour le 24 février 2026", italic=True, color="gray"),
    text(" — Catherine Selosse / CS Consulting Stratégique", italic=True, color="gray"),
))
blocks.append(divider())

# ==========================================
# DÉCISION PRISE
# ==========================================

blocks.append(heading1("Décision prise : Kajabi"))

blocks.append(callout("✅",
    text("Kajabi Growth (199$/mois)", bold=True),
    text(" est la solution retenue. La migration est en cours. Cette décision est la bonne pour le cas d'Aurélia."),
    color="green_background"
))

blocks.append(paragraph())
blocks.append(heading2("Pourquoi Kajabi est le bon choix"))

blocks.append(numbered(
    text("Stockage vidéo illimité inclus", bold=True),
    text(" — Kajabi héberge toutes les vidéos via Wistia, sans limite de stockage ni de bande passante. Pour 500 vidéos, c'est la solution la plus simple. Pas besoin de Bunny.net ni d'outil tiers.")
))
blocks.append(numbered(
    text("Tout-en-un = moins de charge mentale", bold=True),
    text(" — Cours, communauté, email marketing, funnels, paiements, site web : tout dans un seul outil. Aurélia est à 50h/semaine, 80% opérationnel. Réduire le nombre d'outils, c'est réduire la charge.")
))
blocks.append(numbered(
    text("Formation structurée", bold=True),
    text(" — Le cœur de métier d'Aurélia c'est la formation, pas la communauté. Kajabi excelle en cours structurés (templates, parcours, évaluations). Circle est meilleur en communauté, mais ce n'est pas la priorité n°1.")
))
blocks.append(numbered(
    text("Email marketing + funnels inclus", bold=True),
    text(" — Pas besoin de Brevo, pas besoin d'outil de funnels tiers. Moins de connecteurs = moins de points de rupture.")
))
blocks.append(numbered(
    text("0% de frais de transaction", bold=True),
    text(" — Circle prend 0.5 à 2%. Sur un membership à 299€/mois avec des centaines de membres, la différence est significative.")
))
blocks.append(numbered(
    text("Laurie n'a qu'un outil à maîtriser", bold=True),
    text(" — Un seul back-office à apprendre. Onboarding plus rapide, moins d'erreurs, autonomie plus vite.")
))

blocks.append(divider())

# ==========================================
# COMPARATIF COÛTS
# ==========================================

blocks.append(heading2("Comparatif des coûts"))

blocks.append(table_block(
    ["Stack", "Coût/mois", "Outils à gérer", "Vidéo incluse"],
    [
        ["✅ Kajabi Growth", "~199$", "1 seul", "Oui (illimité)"],
        ["Circle + Bunny + Brevo", "~130$", "3 outils", "Non (Bunny à part)"],
        ["Uscreen actuel + Wix + Planity", "~125$+", "3+ outils (fragmenté)", "Oui (limité)"],
    ]
))

blocks.append(paragraph(
    text("Les ~70$/mois de différence avec la stack Circle sont compensés par : ", italic=True),
    text("le temps gagné, la simplification pour Laurie, et 0% de frais de transaction.", bold=True, italic=True),
))

blocks.append(divider())

# ==========================================
# PLAN KAJABI RECOMMANDÉ
# ==========================================

blocks.append(heading2("Plan Kajabi recommandé : Growth"))

blocks.append(table_block(
    ["Caractéristique", "Growth (199$/mois)"],
    [
        ["Produits", "Jusqu'à 15 produits"],
        ["Stockage vidéo", "Illimité (via Wistia)"],
        ["Bande passante", "Illimitée"],
        ["Communauté", "Groupes d'accès illimités"],
        ["Email marketing", "Inclus"],
        ["Funnels / landing pages", "Inclus"],
        ["Site web / domaine custom", "Inclus"],
        ["App mobile", "Oui"],
        ["Frais de transaction", "0%"],
    ]
))

blocks.append(callout("💡",
    text("Astuce : ", bold=True),
    text("en paiement annuel, Kajabi Growth passe à ~159$/mois (-20%). À envisager une fois la migration validée."),
    color="yellow_background"
))

blocks.append(divider())

# ==========================================
# CE QUE KAJABI REMPLACE
# ==========================================

blocks.append(heading2("Ce que Kajabi remplace"))

blocks.append(table_block(
    ["Outil actuel", "Remplacé par", "Statut"],
    [
        ["Uscreen (vidéos + formation)", "Kajabi Courses + vidéo native", "À migrer"],
        ["Wix (site web)", "Kajabi Website Builder", "À migrer"],
        ["Outil email externe", "Kajabi Email Marketing", "À configurer"],
        ["Planity (réservations)", "À évaluer (Kajabi Coaching ou outil tiers)", "À décider"],
    ]
))

blocks.append(callout("⚠️",
    text("Point d'attention Planity : ", bold=True),
    text("Kajabi gère le coaching et les sessions 1-to-1, mais si Aurélia a des besoins spécifiques de prise de RDV en ligne (type Calendly), il faudra peut-être conserver un outil dédié ou utiliser l'intégration Kajabi."),
    color="orange_background"
))

blocks.append(divider())

# ==========================================
# PLAN DE MIGRATION
# ==========================================

blocks.append(heading1("Plan de migration"))

blocks.append(heading2("Phase 1 — Setup Kajabi (en cours)"))

blocks.append(heading3("👩 Laurie"))
blocks.append(todo("Configurer la structure Kajabi : produits, modules, parcours de formation"))
blocks.append(todo("Uploader les vidéos dans Kajabi (par batch — commencer par les 50 les plus vues)"))
blocks.append(todo("Recréer les pages de vente / landing pages dans Kajabi"))
blocks.append(todo("Configurer les emails automatiques (séquences de bienvenue, relances)"))
blocks.append(todo("Paramétrer le domaine custom et l'identité visuelle"))

blocks.append(heading3("🎯 Aurélia"))
blocks.append(todo("Valider l'architecture des produits et modules (avant que Laurie uploade tout)"))
blocks.append(todo("Tester le parcours membre : inscription → accès formation → communauté"))
blocks.append(todo("Décider : Planity reste ou on migre la prise de RDV dans Kajabi ?"))

blocks.append(divider())

blocks.append(heading2("Phase 2 — Migration des contenus"))

blocks.append(heading3("👩 Laurie"))
blocks.append(todo("Exporter toutes les vidéos d'Uscreen (téléchargement par batch)"))
blocks.append(todo("Uploader l'intégralité des vidéos dans Kajabi"))
blocks.append(todo("Migrer les contenus texte, PDF, cahiers d'exercices"))
blocks.append(todo("Recréer la structure communauté (groupes, espaces de discussion)"))
blocks.append(todo("Migrer la liste email dans Kajabi Email"))

blocks.append(heading3("🎯 Aurélia"))
blocks.append(todo("Valider la qualité de lecture des vidéos migrées"))
blocks.append(todo("Vérifier les parcours de formation complets (navigation, liens entre modules)"))
blocks.append(todo("Tester les emails automatiques en condition réelle"))

blocks.append(divider())

blocks.append(heading2("Phase 3 — Bascule"))

blocks.append(heading3("👩 Laurie"))
blocks.append(todo("Rediriger le domaine vers Kajabi"))
blocks.append(todo("Communiquer aux membres : nouvel accès, nouveau lien, mode d'emploi"))
blocks.append(todo("Supprimer / résilier Uscreen et Wix une fois la bascule validée"))

blocks.append(heading3("🎯 Aurélia"))
blocks.append(todo("Envoyer un email aux membres pour annoncer la migration"))
blocks.append(todo("Être disponible les 48h post-bascule pour les retours membres"))
blocks.append(todo("Valider la résiliation Uscreen + Wix"))

blocks.append(divider())

# ==========================================
# POINTS DE VIGILANCE
# ==========================================

blocks.append(heading1("Points de vigilance"))

blocks.append(callout("⚠️",
    text("Sécurité vidéo : ", bold=True),
    text("Kajabi héberge via Wistia — les vidéos ne sont pas téléchargeables facilement par les membres. C'est un niveau de protection correct pour un membership. Bien meilleur que YouTube non-référencé."),
    color="orange_background"
))

blocks.append(callout("⚠️",
    text("Portabilité : ", bold=True),
    text("si un jour Aurélia veut quitter Kajabi, les vidéos sont récupérables (téléchargement depuis le back-office). Les emails aussi (export CSV). C'est moins modulaire que Bunny + Circle, mais pas un lock-in total."),
    color="orange_background"
))

blocks.append(callout("⚠️",
    text("Limite produits : ", bold=True),
    text("le plan Growth permet 15 produits. Si Aurélia dépasse ce seuil à terme, il faudra passer au plan Pro (399$/mois). À anticiper dans la structuration des offres."),
    color="orange_background"
))

blocks.append(divider())

# ==========================================
# HISTORIQUE — ancien comparatif
# ==========================================

blocks.append(toggle(
    [text("📋 Historique : comparatif initial (février 2026)", italic=True)],
    [
        paragraph(text("Ce comparatif a été réalisé avant la décision Kajabi. Conservé pour mémoire.", italic=True, color="gray")),
        paragraph(),
        paragraph(text("Solutions éliminées :", bold=True)),
        bullet(text("🚫 YouTube Non-Référencé", bold=True), text(" — Sécurité illusoire, téléchargeable en 30s, risque suspension chaîne, image dégradée pour offre premium.")),
        bullet(text("🚫 Wistia (standalone)", bold=True), text(" — 500€+/mois pour 500 vidéos. Hors budget. Mais inclus gratuitement dans Kajabi.")),
        bullet(text("🚫 Wooskill", bold=True), text(" — Marketplace, pas plateforme formation. Commission élevée (5%+9.5%). Portabilité nulle.")),
        bullet(text("🟡 Bunny.net", bold=True), text(" — Excellente solution à 5-15€/mois, mais rendue inutile par Kajabi qui inclut le stockage illimité.")),
        bullet(text("🟡 Circle.so", bold=True), text(" — Meilleur en communauté, mais nécessite 2-3 outils complémentaires. Pas le bon choix pour simplifier.")),
        paragraph(),
        table_block(
            ["Critère", "Circle.so", "Skool", "Kajabi ✅"],
            [
                ["Prix/mois", "89-199$", "9$ ou 99$", "89-199$"],
                ["Vidéo incluse", "200GB-1TB (limité)", "Hébergement limité", "Illimité (Wistia)"],
                ["Communauté", "✅ Excellent", "✅ Excellent", "✅ Bon"],
                ["Formation structurée", "✅ Bon", "⚠️ Basique", "✅ Excellent"],
                ["Email marketing", "❌ Outil tiers", "❌ Outil tiers", "✅ Inclus"],
                ["Funnels", "❌ Outil tiers", "❌ Outil tiers", "✅ Inclus"],
                ["Frais transaction", "0.5-2%", "2.9-10%", "0%"],
                ["App mobile", "✅ Oui", "✅ Oui", "✅ Oui"],
            ]
        ),
    ]
))

blocks.append(divider())

blocks.append(paragraph(
    text("Document de travail Catherine Selosse — CS Consulting Stratégique", bold=True),
    text(" — Prochaine étape : valider l'architecture Kajabi avec Aurélia en session", color="gray"),
))


# === PUSH ===
print(f"Envoi de {len(blocks)} blocs vers Notion...")
append_blocks(PAGE_ID, blocks)
print("✅ Page mise à jour avec succès.")
