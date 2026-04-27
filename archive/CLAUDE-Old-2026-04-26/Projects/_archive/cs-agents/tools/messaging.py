"""Outils de communication inter-agents."""


def make_ask_agent_tool(target_name, target_role):
    """Creer le schema d'outil pour interroger un autre agent."""
    return {
        "name": f"ask_{target_name}",
        "description": (
            f"Envoyer une question ou demande a l'agent {target_role}. "
            f"Utilise cet outil quand tu as besoin d'informations ou d'actions "
            f"relevant du domaine de {target_role}."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "La question ou demande a envoyer",
                },
                "context": {
                    "type": "string",
                    "description": "Contexte supplementaire (optionnel)",
                },
            },
            "required": ["message"],
        },
    }


def make_ask_handler(from_name, to_name, bus):
    """Creer le handler pour un outil ask_agent."""

    def handler(message, context=None):
        response = bus.send_message(from_name, to_name, message, context)
        return {"from": to_name, "response": response}

    return handler
