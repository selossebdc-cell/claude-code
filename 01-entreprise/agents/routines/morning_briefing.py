#!/usr/bin/env python3
"""Briefing matinal — lance le DG qui interroge les 3 departements.

Cron : 30 7 * * 1-5 (lun-ven a 7h30)
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


def save_briefing(content):
    briefing_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "logs",
        "briefings",
    )
    os.makedirs(briefing_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(briefing_dir, f"{today}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Briefing du {today}\n\n")
        f.write(content)
    return filepath


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{datetime.now().isoformat()}] Briefing matinal CS Consulting Strategique")

    try:
        agents = init_agents()
        dg = agents["dg"]

        message = (
            f"Nous sommes le {today}. Prepare le briefing matinal de Catherine.\n\n"
            "1. Interroge le Customer Success pour le statut de chaque client actif "
            "(sessions faites/restantes, prochaine session, actions en cours)\n"
            "2. Interroge le DAF pour les paiements en attente ou en retard\n"
            "3. Interroge le Commercial pour le pipeline de prospection et stats Waalaxy\n"
            "4. Lis le Google Calendar du jour pour voir les RDV\n"
            "5. Synthetise tout en un briefing structure avec les 3 priorites du jour\n\n"
            "Format du briefing :\n"
            "- Victoires d'abord\n"
            "- 3 priorites max (urgent/important)\n"
            "- Alertes si necessaire\n"
            "- Agenda du jour\n"
            "- Pepites LinkedIn disponibles (rappel si non publiees)"
        )

        result = dg.run(message)

        filepath = save_briefing(result)
        log_run("morning_briefing", result, success=True)
        notify_macos("CS Consulting - Briefing", result)

        print(f"\nBriefing sauvegarde : {filepath}")
        print("\n" + result)

    except Exception as e:
        error_msg = f"Erreur briefing: {e}"
        log_run("morning_briefing", error_msg, success=False)
        notify_macos("CS Consulting - ERREUR", error_msg)
        print(error_msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
