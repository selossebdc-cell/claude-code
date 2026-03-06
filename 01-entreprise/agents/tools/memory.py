"""Lecture des fichiers memoire clients (markdown)."""

import os
from config.settings import CLIENTS_DIR


def memory_read_client(client_name):
    """Lire le fichier memoire d'un client.
    Cherche dans le dossier du client : 02-clients/{client_name}/{client_name}.md
    """
    path = os.path.join(CLIENTS_DIR, client_name, f"{client_name}.md")
    if not os.path.exists(path):
        return {"error": f"Fichier {client_name}.md introuvable dans {CLIENTS_DIR}/{client_name}/"}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"client": client_name, "content": content}


def memory_list_clients():
    """Lister tous les clients ayant un dossier avec fichier memoire."""
    if not os.path.isdir(CLIENTS_DIR):
        return {"error": f"Dossier {CLIENTS_DIR} introuvable"}
    clients = []
    for entry in sorted(os.listdir(CLIENTS_DIR)):
        if entry.startswith("_") or entry.startswith("."):
            continue
        client_dir = os.path.join(CLIENTS_DIR, entry)
        if os.path.isdir(client_dir):
            md_file = os.path.join(client_dir, f"{entry}.md")
            if os.path.exists(md_file):
                clients.append(entry)
    return {"clients": clients}


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
                        "Nom du dossier client "
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
