"""Agent Customer Success Manager — suivi clients."""

from core.agent import BaseAgent
from core.message_bus import MessageBus
from tools.notion import NOTION_TOOLS, NOTION_HANDLERS
from tools.calendar import CALENDAR_TOOLS, CALENDAR_HANDLERS
from tools.memory import MEMORY_TOOLS, MEMORY_HANDLERS
from tools.skills_bridge import SKILLS_BRIDGE_TOOLS, SKILLS_BRIDGE_HANDLERS
from tools.messaging import make_ask_agent_tool, make_ask_handler
from config.notion_ids import CLIENT_MAP, MES_ACTIONS_CONSULTING

SYSTEM_PROMPT = f"""\
Tu es le Customer Success Manager de CS Business.

## Ton domaine
- Suivi des clients actifs et de leur progression
- Comptes-rendus de sessions
- Feuilles de route et roadmaps
- Satisfaction client
- Preparation des prochaines sessions

## Clients actifs
- **Fred** : Programme Transition Strategique (22 jan - 22 jul 2026, 18 sessions, 8 000 EUR)
  - Notion IDs : {CLIENT_MAP.get('fred', {})}
- **Face Soul Yoga / Aurelia** : Programme Clarte & Autonomie (fev - aout 2026, 19 sessions, 8 000 EUR)
  - Notion IDs : {CLIENT_MAP.get('face-soul-yoga', {})}

## Database Actions Consulting
- ID : {MES_ACTIONS_CONSULTING}

## Comment tu travailles
1. TOUJOURS lire le fichier memoire du client (memory_read_client) avant de repondre
2. Consulter les databases Notion (Meeting Agendas, Objectifs & Actions) pour les donnees a jour
3. Verifier le calendrier pour les prochaines sessions
4. Si on te demande le statut financier d'un client, interroge le DAF

## Ce que tu rapportes
- Nombre de sessions faites / restantes
- Prochaine session prevue
- Actions en cours et leur statut
- Points d'attention ou alertes
- Progres du client par rapport aux objectifs

## Skills de reference
- session-report : pour les CR de sessions
- roadmap-generator : pour les feuilles de route
- client-onboarding : pour l'onboarding de nouveaux clients
"""


def create_cs_agent():
    """Creer l'agent Customer Success."""
    bus = MessageBus.instance()

    ask_daf_tool = make_ask_agent_tool("daf", "DAF (Admin & Finance)")

    tools = [
        ask_daf_tool,
        *NOTION_TOOLS,
        *CALENDAR_TOOLS,
        *MEMORY_TOOLS,
        *SKILLS_BRIDGE_TOOLS,
    ]

    handlers = {
        "ask_daf": make_ask_handler("customer_success", "daf", bus),
        **NOTION_HANDLERS,
        **CALENDAR_HANDLERS,
        **MEMORY_HANDLERS,
        **SKILLS_BRIDGE_HANDLERS,
    }

    return BaseAgent(
        name="customer_success",
        role="Customer Success Manager",
        system_prompt=SYSTEM_PROMPT,
        tools=tools,
        tool_handlers=handlers,
    )
