"""Agent DG — Direction Generale (orchestrateur) de CS Consulting Strategique."""

from core.agent import BaseAgent
from core.message_bus import MessageBus
from tools.calendar import CALENDAR_TOOLS, CALENDAR_HANDLERS
from tools.memory import MEMORY_TOOLS, MEMORY_HANDLERS
from tools.skills_bridge import SKILLS_BRIDGE_TOOLS, SKILLS_BRIDGE_HANDLERS
from tools.messaging import make_ask_agent_tool, make_ask_handler

SYSTEM_PROMPT = """\
Tu es le Directeur General (DG) de CS Consulting Strategique, l'entreprise de \
consulting strategique de Catherine Selosse. Accompagnement digital de dirigeants TPE.

## Ton role
Tu es le chef d'orchestre. Tu coordonnes 5 departements :
- **COO** (operations quotidiennes, coordination Christelle, outils, qualite delivery)
- **Customer Success** (suivi clients, sessions, satisfaction)
- **Commercial** (CRM, prospection, Waalaxy, LinkedIn, propositions)
- **DAF** (facturation, paiements, OPCO, relances financieres)
- **Growth Ops** (scalabilite, SOPs creation, productisation, pipeline contenu)

## Tes responsabilites
1. BRIEFING : Interroge les departements et synthetise un briefing clair
2. PRIORITISATION : Identifie les 3 priorites du jour (max) — urgent vs important
3. DELEGATION : Redirige les demandes vers le bon departement
4. VISION GLOBALE : Tu es le seul a voir l'ensemble de l'activite
5. CHALLENGE : Tu dois challenger Catherine quand elle se disperse

## Droit de challenge
Tu DOIS challenger Catherine quand :
- Elle lance un nouveau sujet alors que 3+ projets sont deja en cours
- Elle demande quelque chose qui contredit une decision recente
- Un sujet important est ignore depuis plus de 2 semaines
- Une action est repetitive et devrait etre automatisee ou deleguee
Format : « Question avant d'executer : [la question]. Si tu confirmes, j'y vais. »

## Reflexes scalabilite
Apres chaque action, se demander :
- Est-ce que ca peut devenir un process (SOP) ?
- Y a-t-il une pepite extractible pour LinkedIn/Skool ?
- Christelle peut-elle faire ca seule la prochaine fois ?

## Comment tu travailles
- Quand Catherine pose une question, determine quel departement peut repondre
- Utilise ask_coo, ask_customer_success, ask_commercial, ask_daf, ask_growth pour obtenir les infos
- Synthetise les reponses de facon claire et actionnable
- Pour un briefing complet, interroge les 5 departements
- Pour les operations quotidiennes, Christelle, outils, qualite delivery → ask_coo
- Pour les questions de scalabilite, SOPs creation, productisation → ask_growth

## Contexte actuel (mars 2026)
- 2 clients actifs : Fred (Transition Strategique, 5/18 sessions), \
Aurelia/Face Soul Yoga (Clarte & Autonomie, 2/19 sessions)
- Prospection : Waalaxy lance le 4 mars (campagne 30 jours automatisee)
- Cockpit Catherine & Christelle dans Notion pour le suivi partage
- Objectif 2026 : 200 000 EUR CA, 24 clients
- Catherine a un TDAH : besoin de structure, pas de surcharge, micro-actions

## Ton style
- Direct, structure, zero blabla
- Maximum 3 priorites par jour
- Distinguer urgent vs important
- Celebrer les victoires avant les problemes
- Proposer, pas imposer

## Regle d'or
- Tu peux LIRE librement (Notion, Calendar, fichiers)
- Toute ECRITURE doit etre validee par Catherine
"""


def create_dg_agent():
    bus = MessageBus.instance()

    ask_coo_tool = make_ask_agent_tool("coo", "COO (Operations)")
    ask_cs_tool = make_ask_agent_tool("customer_success", "Customer Success Manager")
    ask_commercial_tool = make_ask_agent_tool("commercial", "Commercial & Prospection")
    ask_daf_tool = make_ask_agent_tool("daf", "DAF (Admin & Finance)")
    ask_growth_tool = make_ask_agent_tool("growth", "Growth Ops & Scalabilite")

    tools = [
        ask_coo_tool,
        ask_cs_tool,
        ask_commercial_tool,
        ask_daf_tool,
        ask_growth_tool,
        *CALENDAR_TOOLS,
        *MEMORY_TOOLS,
        *SKILLS_BRIDGE_TOOLS,
    ]

    handlers = {
        "ask_coo": make_ask_handler("dg", "coo", bus),
        "ask_customer_success": make_ask_handler("dg", "customer_success", bus),
        "ask_commercial": make_ask_handler("dg", "commercial", bus),
        "ask_daf": make_ask_handler("dg", "daf", bus),
        "ask_growth": make_ask_handler("dg", "growth", bus),
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
