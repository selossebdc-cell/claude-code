"""Outils Growth Ops — scalabilite CS Consulting Strategique.

Analyse cross-clients, suivi SOPs, pipeline contenu, delegation.
"""

import json
import os
from datetime import datetime
from config.settings import CLIENTS_DIR, SKILLS_DIR, LOGS_DIR
from config.notion_ids import (
    MES_SOP_PROCESS, FACTURATION_GLOBAL, CLIENT_MAP,
    COCKPIT_PROJETS, CRM,
)
from tools.notion import notion_query_database


# ---------------------------------------------------------------------------
#  1. Analyse cross-clients — detection de patterns repetitifs
# ---------------------------------------------------------------------------

def growth_analyze_patterns():
    """Lire TOUS les fichiers memoire clients et extraire les patterns communs.

    Retourne les themes recurrents, outils utilises, blocages frequents.
    """
    if not os.path.isdir(CLIENTS_DIR):
        return {"error": f"Dossier {CLIENTS_DIR} introuvable"}

    clients_data = {}
    for entry in sorted(os.listdir(CLIENTS_DIR)):
        if entry.startswith("_") or entry.startswith("."):
            continue
        md_file = os.path.join(CLIENTS_DIR, entry, f"{entry}.md")
        if os.path.exists(md_file):
            with open(md_file, "r", encoding="utf-8") as f:
                clients_data[entry] = f.read()

    # Lire aussi les prep-sessions si disponibles
    for client in list(clients_data.keys()):
        prep_dir = os.path.join(CLIENTS_DIR, client, "prep-sessions")
        if os.path.isdir(prep_dir):
            preps = []
            for prep_file in sorted(os.listdir(prep_dir)):
                if prep_file.endswith(".md"):
                    path = os.path.join(prep_dir, prep_file)
                    with open(path, "r", encoding="utf-8") as f:
                        preps.append({"file": prep_file, "content": f.read()})
            if preps:
                clients_data[f"{client}__preps"] = preps

    return {
        "client_count": len([k for k in clients_data if "__" not in k]),
        "clients": clients_data,
        "instruction": (
            "Analyse ces donnees pour identifier : "
            "1) Themes recurrents entre clients (ex: organisation cloud, facturation, CRM) "
            "2) Outils configures chez plusieurs clients "
            "3) Blocages types (resistance, manque temps, peur techno) "
            "4) Sequences d'actions replicables (candidats SOP) "
            "5) Pepites extractibles pour contenu LinkedIn/Skool"
        ),
    }


# ---------------------------------------------------------------------------
#  2. SOP Tracker — suivi des process standardises
# ---------------------------------------------------------------------------

def growth_list_sops():
    """Lister les SOPs existantes dans le dossier skills + Notion."""
    sops = {"from_skills": [], "from_notion": None}

    # SOPs dans les skills (templates, references)
    if os.path.isdir(SKILLS_DIR):
        for skill in sorted(os.listdir(SKILLS_DIR)):
            skill_dir = os.path.join(SKILLS_DIR, skill)
            refs_dir = os.path.join(skill_dir, "references")
            if os.path.isdir(refs_dir):
                refs = [f for f in os.listdir(refs_dir) if f.endswith(".md")]
                if refs:
                    sops["from_skills"].append({
                        "skill": skill,
                        "references": refs,
                    })

    # SOPs dans Notion
    if MES_SOP_PROCESS:
        result = notion_query_database(MES_SOP_PROCESS)
        if "error" not in result:
            sops["from_notion"] = result

    return sops


def growth_sop_gap_analysis():
    """Identifier les process repetitifs qui n'ont PAS encore de SOP.

    Compare ce qui est fait manuellement chez les clients vs les SOPs existantes.
    """
    # Lister les SOPs existantes
    existing = set()
    if os.path.isdir(SKILLS_DIR):
        for skill in os.listdir(SKILLS_DIR):
            existing.add(skill)
            refs_dir = os.path.join(SKILLS_DIR, skill, "references")
            if os.path.isdir(refs_dir):
                for ref in os.listdir(refs_dir):
                    existing.add(ref.replace(".md", ""))

    return {
        "existing_sops": sorted(existing),
        "notion_sop_db": MES_SOP_PROCESS,
        "instruction": (
            "Compare les SOPs existantes avec les patterns identifies chez les clients. "
            "Identifie les gaps : quels process sont faits manuellement a chaque client "
            "mais n'ont pas de SOP ? Propose les 3 SOPs les plus impactantes a creer. "
            "Format : nom_sop | description | frequence | temps economise estime"
        ),
    }


# ---------------------------------------------------------------------------
#  3. Content Pipeline — pepites sessions -> LinkedIn -> leads
# ---------------------------------------------------------------------------

def growth_content_pipeline():
    """Scanner les fichiers clients pour les pepites extractibles.

    Cherche dans les CR de sessions et prep-sessions.
    """
    pipeline = {"clients": {}, "total_nuggets": 0}

    if not os.path.isdir(CLIENTS_DIR):
        return {"error": "Dossier clients introuvable"}

    for entry in sorted(os.listdir(CLIENTS_DIR)):
        if entry.startswith("_") or entry.startswith("."):
            continue
        client_dir = os.path.join(CLIENTS_DIR, entry)
        if not os.path.isdir(client_dir):
            continue

        client_content = []

        # Fichier memoire principal
        md_file = os.path.join(client_dir, f"{entry}.md")
        if os.path.exists(md_file):
            with open(md_file, "r", encoding="utf-8") as f:
                client_content.append({"source": "memoire", "content": f.read()})

        # Prep sessions
        prep_dir = os.path.join(client_dir, "prep-sessions")
        if os.path.isdir(prep_dir):
            for pf in sorted(os.listdir(prep_dir)):
                if pf.endswith(".md"):
                    with open(os.path.join(prep_dir, pf), "r", encoding="utf-8") as f:
                        client_content.append({"source": pf, "content": f.read()})

        if client_content:
            pipeline["clients"][entry] = client_content

    return {
        **pipeline,
        "instruction": (
            "Pour chaque client, identifie les pepites : "
            "1) Problemes concrets resolus (avant/apres) "
            "2) Phrases marquantes du dirigeant "
            "3) Resultats chiffres (temps gagne, erreurs evitees) "
            "4) Patterns universels (applicable a tout dirigeant TPE) "
            "Classe chaque pepite : post LinkedIn, carrousel, temoignage, lead magnet. "
            "Indique si deja utilisee ou disponible."
        ),
    }


# ---------------------------------------------------------------------------
#  4. Delegation Tracker — ce que Christelle peut reprendre
# ---------------------------------------------------------------------------

def growth_delegation_analysis():
    """Analyser les taches et projets pour identifier ce qui est delegable.

    Lit le Cockpit Projets et les taches Catherine/Christelle.
    """
    result = {"cockpit_projets": None, "skills_delegables": []}

    # Projets en cours
    if COCKPIT_PROJETS:
        projets = notion_query_database(COCKPIT_PROJETS)
        if "error" not in projets:
            result["cockpit_projets"] = projets

    # Skills qui pourraient etre delegues a Christelle
    delegable_skills = [
        "client-onboarding",
        "session-report",
        "invoice-generator",
        "agenda-writer",
    ]
    for skill_name in delegable_skills:
        skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
        if os.path.exists(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                result["skills_delegables"].append({
                    "skill": skill_name,
                    "content": f.read(),
                })

    return {
        **result,
        "instruction": (
            "Analyse les projets et skills pour proposer un plan de delegation : "
            "1) Taches deja delegables a Christelle (formation minimale) "
            "2) Taches delegables apres formation (1-2 sessions) "
            "3) Taches qui restent Catherine uniquement (expertise, relation client) "
            "4) Estimation du temps libere par semaine si delegation effective "
            "Format : tache | delegable_a | formation_requise | temps_libere"
        ),
    }


# ---------------------------------------------------------------------------
#  5. Metriques de scalabilite
# ---------------------------------------------------------------------------

def growth_scalability_metrics():
    """Calculer les metriques cles de scalabilite.

    - Ratio temps/client
    - Capacite restante
    - Taux de reutilisation des process
    - Progression vers objectif CA
    """
    metrics = {
        "objectif_ca_annuel": 200000,
        "prix_programme_pref": 8000,
        "prix_programme_std": 10000,
        "objectif_clients": 24,
    }

    # Compter les clients actifs
    if os.path.isdir(CLIENTS_DIR):
        clients = [
            d for d in os.listdir(CLIENTS_DIR)
            if not d.startswith("_") and not d.startswith(".")
            and os.path.isdir(os.path.join(CLIENTS_DIR, d))
            and os.path.exists(os.path.join(CLIENTS_DIR, d, f"{d}.md"))
        ]
        metrics["clients_actifs"] = len(clients)
        metrics["clients_restants"] = max(0, 24 - len(clients))

    # SOPs existantes
    sop_count = 0
    if os.path.isdir(SKILLS_DIR):
        for skill in os.listdir(SKILLS_DIR):
            refs_dir = os.path.join(SKILLS_DIR, skill, "references")
            if os.path.isdir(refs_dir):
                sop_count += len([f for f in os.listdir(refs_dir) if f.endswith(".md")])
    metrics["sops_existantes"] = sop_count

    # Facturation Notion
    if FACTURATION_GLOBAL:
        factures = notion_query_database(FACTURATION_GLOBAL)
        if "error" not in factures:
            metrics["factures"] = factures

    return {
        **metrics,
        "instruction": (
            "Calcule et presente : "
            "1) CA realise vs objectif (200k) "
            "2) Nombre de clients actifs vs objectif (24) "
            "3) Capacite : combien de clients Catherine peut gerer en parallele "
            "   (estimer sur base du rythme actuel : sessions/semaine) "
            "4) Score de scalabilite : SOPs existantes / process identifies "
            "5) Temps de Catherine : heures client vs heures admin vs heures prospection "
            "6) Recommandations pour augmenter la capacite"
        ),
    }


# ---------------------------------------------------------------------------
#  6. Productisation — modules autonomes extractibles
# ---------------------------------------------------------------------------

def growth_productization_scan():
    """Identifier les bouts d'accompagnement qui peuvent devenir des produits autonomes.

    Analyse les skills, SOPs et patterns clients pour trouver des candidats.
    """
    products = {"skills_as_products": [], "client_patterns": []}

    # Chaque skill est un candidat produit
    if os.path.isdir(SKILLS_DIR):
        for skill in sorted(os.listdir(SKILLS_DIR)):
            skill_path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
            if os.path.exists(skill_path):
                with open(skill_path, "r", encoding="utf-8") as f:
                    products["skills_as_products"].append({
                        "skill": skill,
                        "content_preview": f.read()[:500],
                    })

    # Patterns clients communs = candidats formation/template
    for entry in sorted(os.listdir(CLIENTS_DIR)):
        if entry.startswith("_") or entry.startswith("."):
            continue
        md_file = os.path.join(CLIENTS_DIR, entry, f"{entry}.md")
        if os.path.exists(md_file):
            with open(md_file, "r", encoding="utf-8") as f:
                products["client_patterns"].append({
                    "client": entry,
                    "content_preview": f.read()[:800],
                })

    return {
        **products,
        "instruction": (
            "Identifie les candidats a la productisation : "
            "1) Templates vendables (ex: guide organisation cloud pour dirigeant) "
            "2) Mini-formations autonomes (ex: 'Securite numerique en 5 etapes') "
            "3) Outils/checklists partageables sur Skool ou en lead magnet "
            "4) Modules d'accompagnement packageables (ex: 'Sprint Facturation 2 semaines') "
            "Pour chaque candidat : nom | format | prix suggere | effort de creation | "
            "potentiel de vente recurrente"
        ),
    }


# ---------------------------------------------------------------------------
#  Export TOOLS + HANDLERS
# ---------------------------------------------------------------------------

GROWTH_TOOLS = [
    {
        "name": "growth_analyze_patterns",
        "description": (
            "Analyser TOUS les clients pour detecter les patterns repetitifs, "
            "themes communs, et sequences replicables. Utilise pour identifier "
            "ce qui peut devenir un process standardise (SOP)."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "growth_list_sops",
        "description": (
            "Lister toutes les SOPs existantes (skills + Notion). "
            "Vue d'ensemble de ce qui est deja standardise."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "growth_sop_gap_analysis",
        "description": (
            "Identifier les process repetitifs qui n'ont PAS de SOP. "
            "Compare le travail reel avec les process documentes."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "growth_content_pipeline",
        "description": (
            "Scanner les donnees clients pour extraire les pepites de contenu. "
            "Alimente le pipeline LinkedIn/Skool/lead magnets."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "growth_delegation_analysis",
        "description": (
            "Analyser ce qui peut etre delegue a Christelle. "
            "Projets, taches, skills — avec estimation du temps libere."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "growth_scalability_metrics",
        "description": (
            "Calculer les metriques de scalabilite : CA vs objectif, capacite clients, "
            "score de standardisation, ratio temps client/admin/prospection."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "growth_productization_scan",
        "description": (
            "Identifier les bouts d'accompagnement qui peuvent devenir des produits "
            "autonomes : templates, mini-formations, modules packages, lead magnets."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
]

GROWTH_HANDLERS = {
    "growth_analyze_patterns": growth_analyze_patterns,
    "growth_list_sops": growth_list_sops,
    "growth_sop_gap_analysis": growth_sop_gap_analysis,
    "growth_content_pipeline": growth_content_pipeline,
    "growth_delegation_analysis": growth_delegation_analysis,
    "growth_scalability_metrics": growth_scalability_metrics,
    "growth_productization_scan": growth_productization_scan,
}
