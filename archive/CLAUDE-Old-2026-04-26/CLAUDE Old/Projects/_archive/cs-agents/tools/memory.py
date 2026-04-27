"""Lecture des fichiers memoire clients (markdown)."""

import os
from config.settings import CLIENTS_DIR


def memory_read_client(client_name):
    """Lire le fichier memoire d'un client."""
    path = os.path.join(CLIENTS_DIR, f"{client_name}.md")
    if not os.path.exists(path):
        return {"error": f"Fichier {client_name}.md introuvable dans {CLIENTS_DIR}"}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"client": client_name, "content": content}


def memory_list_clients():
    """Lister tous les clients ayant un fichier memoire."""
    if not os.path.isdir(CLIENTS_DIR):
        return {"error": f"Dossier {CLIENTS_DIR} introuvable"}
    files = [
        f.replace(".md", "")
        for f in sorted(os.listdir(CLIENTS_DIR))
        if f.endswith(".md") and not f.startswith("_")
    ]
    return {"clients": files}


# --- Schemas d'outils pour l'API Anthropic ---

MEMORY_TOOLS = [
    {
        "name": "memory_read_client",
        "description": (
            "Lire le fichier memoire d'un client (profil, audit, historique sessions, "
            "patterns observes). TOUJOURS lire avant toute question sur un client."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "client_name": {
                    "type": "string",
                    "description": (
                        "Nom du fichier sans extension "
                        "(ex: 'fred', 'face-soul-yoga')"
                    ),
                },
            },
            "required": ["client_name"],
        },
    },
    {
        "name": "memory_list_clients",
        "description": "Lister tous les clients ayant un fichier memoire.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]

MEMORY_HANDLERS = {
    "memory_read_client": memory_read_client,
    "memory_list_clients": memory_list_clients,
}
