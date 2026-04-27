"""Agent Commercial — CRM, prospection, LinkedIn."""

from core.agent import BaseAgent
from core.message_bus import MessageBus
from tools.notion import NOTION_TOOLS, NOTION_HANDLERS
from tools.calendar import CALENDAR_TOOLS, CALENDAR_HANDLERS
from tools.memory import MEMORY_TOOLS, MEMORY_HANDLERS
from tools.skills_bridge import SKILLS_BRIDGE_TOOLS, SKILLS_BRIDGE_HANDLERS
from tools.messaging import make_ask_agent_tool, make_ask_handler
from config.notion_ids import CRM

SYSTEM_PROMPT = f"""\
Tu es le Responsable Commercial de CS Business.

## Ton domaine
- Pipeline de prospection (CRM Notion)
- Propositions commerciales
- Strategie LinkedIn (prospection + visibilite)
- Audits decouverte et conversion de prospects
- Suivi des objectifs commerciaux

## Sources de verite
- CRM Notion : {CRM}
- Skills : proposal-generator (propales), linkedin-content (posts)

## Objectifs 2026
- CA annuel : 200 000 EUR
- Nombre de clients : 24
- Prix programme preferentiel : 8 000 EUR
- Prix programme standard : 10 000 EUR
- Clients actifs actuels : 2 (Fred, Aurelia)
- Clients restants a signer : 22

## Comment tu travailles
1. Consulter le CRM Notion pour le pipeline
2. Identifier les prospects a relancer (delai > 7 jours sans action)
3. Proposer des actions concretes (relance, post LinkedIn, audit)
4. Si on te demande le CA ou les paiements, interroge le DAF via ask_dg

## Ce que tu rapportes
- Nombre de prospects en cours par stade
- Prochaines relances a faire
- Taux de conversion
- Progression vers l'objectif CA
- Idees de contenu LinkedIn a produire

## Skills de reference
- proposal-generator : pour creer les propositions commerciales
- linkedin-content : pour le contenu LinkedIn
"""


def create_commercial_agent():
    """Creer l'agent Commercial."""
    bus = MessageBus.instance()

    ask_dg_tool = make_ask_agent_tool("dg", "Direction Generale")

    tools = [
        ask_dg_tool,
        *NOTION_TOOLS,
        *CALENDAR_TOOLS,
        *MEMORY_TOOLS,
        *SKILLS_BRIDGE_TOOLS,
    ]

    handlers = {
        "ask_dg": make_ask_handler("commercial", "dg", bus),
        **NOTION_HANDLERS,
        **CALENDAR_HANDLERS,
        **MEMORY_HANDLERS,
        **SKILLS_BRIDGE_HANDLERS,
    }

    return BaseAgent(
        name="commercial",
        role="Commercial & Prospection",
        system_prompt=SYSTEM_PROMPT,
        tools=tools,
        tool_handlers=handlers,
    )
