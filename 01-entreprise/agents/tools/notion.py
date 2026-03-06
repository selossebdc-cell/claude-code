"""Wrapper API Notion — lecture de pages et databases."""

import json
import time
import urllib.request
import urllib.error
from config.settings import NOTION_SETTINGS_PATH, NOTION_API_VERSION

_token_cache = None


def _get_notion_token():
    global _token_cache
    if _token_cache:
        return _token_cache
    with open(NOTION_SETTINGS_PATH) as f:
        settings = json.load(f)
    _token_cache = settings["mcpServers"]["notion"]["env"]["NOTION_TOKEN"]
    return _token_cache


def _notion_request(method, url, body=None):
    token = _get_notion_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}


def _extract_text_from_blocks(blocks):
    lines = []
    for block in blocks:
        block_type = block.get("type", "")
        data = block.get(block_type, {})
        rich_texts = data.get("rich_text", []) if isinstance(data, dict) else []
        text = "".join(rt.get("plain_text", "") for rt in rich_texts)
        if text:
            prefix = ""
            if block_type.startswith("heading_"):
                level = block_type[-1]
                prefix = "#" * int(level) + " "
            elif block_type == "bulleted_list_item":
                prefix = "- "
            elif block_type == "numbered_list_item":
                prefix = "1. "
            elif block_type == "to_do":
                checked = data.get("checked", False)
                prefix = "[x] " if checked else "[ ] "
            lines.append(f"{prefix}{text}")
    return "\n".join(lines)


def _extract_db_row(page):
    props = page.get("properties", {})
    row = {"id": page.get("id", "")}
    for name, prop in props.items():
        ptype = prop.get("type", "")
        if ptype == "title":
            texts = prop.get("title", [])
            row[name] = "".join(t.get("plain_text", "") for t in texts)
        elif ptype == "rich_text":
            texts = prop.get("rich_text", [])
            row[name] = "".join(t.get("plain_text", "") for t in texts)
        elif ptype == "number":
            row[name] = prop.get("number")
        elif ptype == "select":
            sel = prop.get("select")
            row[name] = sel.get("name", "") if sel else ""
        elif ptype == "multi_select":
            row[name] = [s.get("name", "") for s in prop.get("multi_select", [])]
        elif ptype == "date":
            d = prop.get("date")
            row[name] = d.get("start", "") if d else ""
        elif ptype == "checkbox":
            row[name] = prop.get("checkbox", False)
        elif ptype == "status":
            s = prop.get("status")
            row[name] = s.get("name", "") if s else ""
        elif ptype == "url":
            row[name] = prop.get("url", "")
        elif ptype == "formula":
            f = prop.get("formula", {})
            ftype = f.get("type", "")
            row[name] = f.get(ftype)
    return row


def notion_read_page(page_id, page_name=""):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    resp = _notion_request("GET", url)
    if "error" in resp:
        return resp
    blocks = resp.get("results", [])
    text = _extract_text_from_blocks(blocks)
    return {"page_name": page_name, "content": text, "block_count": len(blocks)}


def notion_query_database(database_id, filter=None, sorts=None):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    body = {}
    if filter:
        body["filter"] = filter
    if sorts:
        body["sorts"] = sorts
    time.sleep(0.3)
    resp = _notion_request("POST", url, body)
    if "error" in resp:
        return resp
    results = resp.get("results", [])
    rows = [_extract_db_row(r) for r in results]
    return {"rows": rows, "count": len(rows)}


NOTION_TOOLS = [
    {
        "name": "notion_read_page",
        "description": (
            "Lire le contenu d'une page Notion (blocs enfants). "
            "Retourne le texte en markdown."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {
                    "type": "string",
                    "description": "ID de la page Notion (format UUID)",
                },
                "page_name": {
                    "type": "string",
                    "description": "Nom lisible de la page (pour le log)",
                },
            },
            "required": ["page_id"],
        },
    },
    {
        "name": "notion_query_database",
        "description": (
            "Interroger une database Notion avec des filtres optionnels. "
            "Retourne les lignes avec leurs proprietes."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "database_id": {
                    "type": "string",
                    "description": "ID de la database Notion",
                },
                "filter": {
                    "type": "object",
                    "description": "Filtre Notion API (optionnel)",
                },
                "sorts": {
                    "type": "array",
                    "description": "Tri Notion API (optionnel)",
                },
            },
            "required": ["database_id"],
        },
    },
]

NOTION_HANDLERS = {
    "notion_read_page": notion_read_page,
    "notion_query_database": notion_query_database,
}
