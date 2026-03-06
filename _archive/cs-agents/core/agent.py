"""BaseAgent — boucle agentique avec tool use Anthropic."""

import json
import anthropic
from config.settings import ANTHROPIC_MODEL


class BaseAgent:
    """Agent IA avec boucle agentique (appel Claude + tool use + iteration)."""

    def __init__(
        self,
        name,
        role,
        system_prompt,
        tools=None,
        tool_handlers=None,
        model=None,
        max_iterations=15,
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.tool_handlers = tool_handlers or {}
        self.model = model or ANTHROPIC_MODEL
        self.max_iterations = max_iterations
        self.client = anthropic.Anthropic()

    def run(self, user_message):
        """Boucle agentique : envoie un message, gere les tool calls, itere."""
        messages = [{"role": "user", "content": user_message}]

        for _ in range(self.max_iterations):
            kwargs = {
                "model": self.model,
                "max_tokens": 4096,
                "system": self.system_prompt,
                "messages": messages,
            }
            if self.tools:
                kwargs["tools"] = self.tools

            response = self.client.messages.create(**kwargs)

            # Ajouter la reponse assistant
            messages.append({"role": "assistant", "content": response.content})

            # Si pas de tool use, on a fini
            if response.stop_reason != "tool_use":
                return self._extract_text(response.content)

            # Traiter les appels d'outils
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self._execute_tool(block.name, block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(
                                result, ensure_ascii=False, default=str
                            ),
                        }
                    )

            messages.append({"role": "user", "content": tool_results})

        return "[Agent a atteint la limite d'iterations]"

    def _execute_tool(self, tool_name, tool_input):
        """Dispatch un appel d'outil vers le handler correspondant."""
        handler = self.tool_handlers.get(tool_name)
        if not handler:
            return {"error": f"Outil inconnu: {tool_name}"}
        try:
            return handler(**tool_input)
        except Exception as e:
            return {"error": f"{tool_name} a echoue: {e}"}

    def _extract_text(self, content_blocks):
        """Extraire le texte des blocs de reponse."""
        texts = []
        for block in content_blocks:
            if hasattr(block, "text"):
                texts.append(block.text)
        return "\n".join(texts)
