"""MessageBus — communication inter-agents avec logging."""

import json
import os
from datetime import datetime
from config.settings import LOGS_DIR


class MessageBus:
    """Bus de messages synchrone pour la communication entre agents."""

    _instance = None

    def __init__(self):
        self._agents = {}
        self._log_dir = os.path.join(LOGS_DIR, "conversations")
        os.makedirs(self._log_dir, exist_ok=True)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None

    def register_agent(self, name, agent):
        self._agents[name] = agent

    def send_message(self, from_agent, to_agent, message, context=None):
        target = self._agents.get(to_agent)
        if not target:
            return f"[Erreur] Agent '{to_agent}' non disponible."

        formatted = f"[Message de {from_agent}]\n"
        if context:
            formatted += f"Contexte: {context}\n"
        formatted += f"\n{message}"

        response = target.run(formatted)
        self._log_exchange(from_agent, to_agent, message, response)
        return response

    def _log_exchange(self, from_agent, to_agent, message, response):
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self._log_dir, f"{today}.jsonl")

        entry = {
            "timestamp": datetime.now().isoformat(),
            "from": from_agent,
            "to": to_agent,
            "message": message[:1000],
            "response": response[:2000],
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def list_agents(self):
        return list(self._agents.keys())
