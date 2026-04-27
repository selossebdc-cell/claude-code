#!/usr/bin/env python3
"""Check hebdomadaire des factures — DAF verifie les paiements.

Cron : 0 9 * * 5 (vendredi a 9h)
"""

import sys
import os
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import init_agents
from core.conversation_log import log_run


def notify_macos(title, message):
    """Notification macOS."""
    preview = message[:200].replace('"', '\\"').replace("'", "\\'")
    subprocess.run(
        [
            "osascript",
            "-e",
            f'display notification "{preview}" with title "{title}"',
        ],
        capture_output=True,
    )


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{datetime.now().isoformat()}] Check factures hebdomadaire")

    try:
        agents = init_agents()
        daf = agents["daf"]

        message = (
            f"Nous sommes le {today}. Fais le point facturation hebdomadaire.\n\n"
            "1. Lis les fichiers memoire de chaque client pour les details contractuels\n"
            "2. Consulte les pages Factures dans Notion pour chaque client\n"
            "3. Identifie :\n"
            "   - Factures emises et payees\n"
            "   - Factures emises en attente de paiement\n"
            "   - Factures a emettre (selon echeancier)\n"
            "   - Retards de paiement (>7 jours)\n"
            "4. Calcule le CA cumule 2026\n"
            "5. Synthetise avec des recommandations d'action\n\n"
            "IMPORTANT : Ne propose PAS d'envoyer de factures ou relances. "
            "Fais juste l'etat des lieux pour Catherine."
        )

        result = daf.run(message)

        log_run("weekly_invoice_check", result, success=True)
        notify_macos("CS Business - Facturation", result)

        print("\n" + result)

    except Exception as e:
        error_msg = f"Erreur check factures: {e}"
        log_run("weekly_invoice_check", error_msg, success=False)
        notify_macos("CS Business - ERREUR", error_msg)
        print(error_msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
