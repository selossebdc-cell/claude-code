#!/usr/bin/env python3
"""CLI CS Consulting Strategique — point d'entree pour parler aux agents.

Usage:
    python3 cli.py dg "Bonjour, comment est ma journee?"
    python3 cli.py daf "Ou en sont les paiements?"
    python3 cli.py customer_success "Statut de Fred?"
    python3 cli.py commercial "Pipeline de prospection?"
    python3 cli.py growth "Revue scalabilite"
    python3 cli.py coo "Statut operations"

Mode interactif:
    python3 cli.py dg
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.message_bus import MessageBus
from dg.agent import create_dg_agent
from customer_success.agent import create_cs_agent
from commercial.agent import create_commercial_agent
from daf.agent import create_daf_agent
from growth.agent import create_growth_agent
from coo.agent import create_coo_agent


def init_agents():
    MessageBus.reset()
    bus = MessageBus.instance()

    cs = create_cs_agent()
    commercial = create_commercial_agent()
    daf = create_daf_agent()
    growth = create_growth_agent()
    coo = create_coo_agent()
    dg = create_dg_agent()

    bus.register_agent("customer_success", cs)
    bus.register_agent("commercial", commercial)
    bus.register_agent("daf", daf)
    bus.register_agent("growth", growth)
    bus.register_agent("coo", coo)
    bus.register_agent("dg", dg)

    return {
        "dg": dg,
        "coo": coo,
        "customer_success": cs,
        "commercial": commercial,
        "daf": daf,
        "growth": growth,
    }


def interactive_mode(agent):
    print(f"\n--- CS Consulting Strategique | Agent: {agent.role} ---")
    print("Tape 'quit' pour quitter.\n")

    while True:
        try:
            user_input = input("Catherine > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Au revoir!")
            break

        print(f"\n[{agent.role} reflechit...]\n")
        response = agent.run(user_input)
        print(response)
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 cli.py <agent> [message]")
        print()
        print("Agents disponibles:")
        print("  dg                 Direction Generale (orchestrateur)")
        print("  customer_success   Customer Success Manager")
        print("  commercial         Commercial & Prospection")
        print("  daf                DAF (Admin & Finance)")
        print("  growth             Growth Ops & Scalabilite")
        print("  coo                COO (Operations)")
        print()
        print("Exemples:")
        print('  python3 cli.py dg "Briefing du matin"')
        print('  python3 cli.py daf "Ou en sont les paiements?"')
        print("  python3 cli.py dg   (mode interactif)")
        sys.exit(1)

    agent_name = sys.argv[1]
    agents = init_agents()

    if agent_name not in agents:
        print(f"Agent inconnu: {agent_name}")
        print(f"Disponibles: {', '.join(agents.keys())}")
        sys.exit(1)

    agent = agents[agent_name]

    if len(sys.argv) >= 3:
        message = " ".join(sys.argv[2:])
        print(f"\n[{agent.role} reflechit...]\n")
        response = agent.run(message)
        print(response)
    else:
        interactive_mode(agent)


if __name__ == "__main__":
    main()
