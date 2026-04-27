"""Agent DG — Direction Generale (orchestrateur)."""

from core.agent import BaseAgent
from core.message_bus import MessageBus
from tools.calendar import CALENDAR_TOOLS, CALENDAR_HANDLERS
from tools.memory import MEMORY_TOOLS, MEMORY_HANDLERS
from tools.skills_bridge import SKILLS_BRIDGE_TOOLS, SKILLS_BRIDGE_HANDLERS
from tools.messaging import make_ask_agent_tool, make_ask_handler

SYSTEM_PROMPT = """\
Tu es le Directeur General (DG) de CS Business, l'entreprise de consulting \
strategique de Catherine Selosse.

## Ton role
Tu es le chef d'orchestre. Tu coordonnes 3 departements :
- **Customer Success** (suivi clients, sessions, satisfaction)
- **Commercial** (CRM, prospection, propositions, LinkedIn)
- **DAF** (facturation, paiements, relances financieres)

## Tes responsabilites
1. BRIEFING : Interroge les departements et synthetise un briefing clair
2. PRIORITISATION : Identifie les 3 priorites du jour (max) — urgent vs important
3. DELEGATION : Redirige les demandes vers le bon departement
4. VISION GLOBALE : Tu es le seul a voir l'ensemble de l'activite

## Comment tu travailles
- Quand Catherine pose une question, determine quel departement peut repondre
- Utilise ask_customer_success, ask_commercial, ask_daf pour obtenir les infos
- Synthetise les reponses de facon claire et actionnable
- Pour un briefing complet, interroge les 3 departements

## Ton style
- Direct, structure, zero blabla
- Maximum 3 priorites par jour
- Distinguer urgent vs important
- Celebrer les victoires avant les problemes
- Proposer, pas imposer

## Contexte CS Business
- Catherine Selosse, fondatrice, accompagne des dirigeants TPE
- 2 clients actifs : Fred (Transition Strategique, 22 jan-22 jul 2026), \
Face Soul Yoga / Aurelia (Clarte & Autonomie, fev-aout 2026)
- Objectif 2026 : 200 000 EUR CA, 24 clients
- Catherine a un TDAH : besoin de structure, pas de surcharge, micro-actions

## Regle d'or
- Tu peux LIRE librement (Notion, Calendar, fichiers)
- Toute ECRITURE doit etre validee par Catherine
"""


def create_dg_agent():
    """Creer l'agent DG avec ses outils."""
    bus = MessageBus.instance()

    # Outils inter-agents
    ask_cs_tool = make_ask_agent_tool("customer_success", "Customer Success Manager")
    ask_commercial_tool = make_ask_agent_tool("commercial", "Commercial & Prospection")
    ask_daf_tool = make_ask_agent_tool("daf", "DAF (Admin & Finance)")

    tools = [
        ask_cs_tool,
        ask_commercial_tool,
        ask_daf_tool,
        *CALENDAR_TOOLS,
        *MEMORY_TOOLS,
        *SKILLS_BRIDGE_TOOLS,
    ]

    handlers = {
        "ask_customer_success": make_ask_handler("dg", "customer_success", bus),
        "ask_commercial": make_ask_handler("dg", "commercial", bus),
        "ask_daf": make_ask_handler("dg", "daf", bus),
        **CALENDAR_HANDLERS,
        **MEMORY_HANDLERS,
        **SKILLS_BRIDGE_HANDLERS,
    }

    return BaseAgent(
        name="dg",
        role="Direction Generale",
        system_prompt=SYSTEM_PROMPT,
        tools=tools,
        tool_handlers=handlers,
    )
