#!/usr/bin/env python3
"""Revue scalabilite hebdomadaire — Growth Ops analyse et recommande.

Cron : 0 10 * * 1 (lundi a 10h)
"""

import sys
import os
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import init_agents
from core.conversation_log import log_run


def notify_macos(title, message):
    preview = message[:200].replace('"', '\\"').replace("'", "\\'")
    subprocess.run(
        [
            "osascript",
            "-e",
            f'display notification "{preview}" with title "{title}"',
        ],
        capture_output=True,
    )


def save_review(content):
    review_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "logs",
        "growth-reviews",
    )
    os.makedirs(review_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(review_dir, f"{today}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Revue Scalabilite — {today}\n\n")
        f.write(content)
    return filepath


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{datetime.now().isoformat()}] Revue scalabilite hebdomadaire")

    try:
        agents = init_agents()
        growth = agents["growth"]

        message = (
            f"Nous sommes le {today}. Prepare la revue scalabilite hebdomadaire.\n\n"
            "Etapes :\n"
            "1. Lance growth_scalability_metrics pour les metriques globales\n"
            "2. Lance growth_analyze_patterns pour les patterns cross-clients\n"
            "3. Lance growth_sop_gap_analysis pour les SOPs manquantes\n"
            "4. Lance growth_content_pipeline pour les pepites disponibles\n"
            "5. Lance growth_delegation_analysis pour le suivi delegation Christelle\n"
            "6. Interroge le Commercial (ask_commercial) pour les stats Waalaxy et pipeline\n\n"
            "Format de la revue :\n"
            "## Dashboard Scalabilite\n"
            "- Score de standardisation : X% (SOPs existantes / process identifies)\n"
            "- Capacite : X clients actuels / X max estimee\n"
            "- CA : X EUR / 200 000 EUR objectif\n\n"
            "## Top 3 actions scalabilite cette semaine\n"
            "(quick wins priorises par impact/effort)\n\n"
            "## SOPs a creer\n"
            "(les 3 plus impactantes, avec estimation du temps economise)\n\n"
            "## Pipeline contenu\n"
            "(pepites disponibles, nombre de posts possible, prochains sujets)\n\n"
            "## Delegation Christelle\n"
            "(avancement, prochaine tache a deleguer)\n\n"
            "## Productisation\n"
            "(candidats identifies, prochaine etape)\n\n"
            "## Alertes\n"
            "(risques de saturation, process manuels critiques, pepites qui dorment)"
        )

        result = growth.run(message)

        filepath = save_review(result)
        log_run("weekly_growth_review", result, success=True)
        notify_macos("CS Consulting - Revue Scalabilite", result)

        print(f"\nRevue sauvegardee : {filepath}")
        print("\n" + result)

    except Exception as e:
        error_msg = f"Erreur revue scalabilite: {e}"
        log_run("weekly_growth_review", error_msg, success=False)
        notify_macos("CS Consulting - ERREUR", error_msg)
        print(error_msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
