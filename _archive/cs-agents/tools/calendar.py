"""Wrapper API Google Calendar — lecture d'evenements."""

import json
import time
import urllib.request
import urllib.error
import urllib.parse
from config.settings import GCAL_TOKENS_PATH, GCAL_OAUTH_PATH
from config.calendar_ids import ALL_CALENDARS

_access_token_cache = None


def _get_access_token():
    """Lire le token d'acces Google Calendar, refresh si expire."""
    global _access_token_cache
    with open(GCAL_TOKENS_PATH) as f:
        tokens = json.load(f)
    token_data = tokens.get("normal", {})
    expiry = token_data.get("expiry_date", 0)

    # Refresh si expire (ou dans les 5 prochaines minutes)
    if expiry < (time.time() + 300) * 1000:
        _refresh_token(tokens)
        with open(GCAL_TOKENS_PATH) as f:
            tokens = json.load(f)
        token_data = tokens.get("normal", {})

    _access_token_cache = token_data.get("access_token", "")
    return _access_token_cache


def _refresh_token(tokens):
    """Rafraichir le token OAuth Google."""
    with open(GCAL_OAUTH_PATH) as f:
        creds = json.load(f)
    client_info = creds.get("installed", creds.get("web", {}))
    data = urllib.parse.urlencode(
        {
            "client_id": client_info["client_id"],
            "client_secret": client_info["client_secret"],
            "refresh_token": tokens["normal"]["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req) as resp:
        new_tokens = json.loads(resp.read())
    tokens["normal"]["access_token"] = new_tokens["access_token"]
    tokens["normal"]["expiry_date"] = int(
        (time.time() + new_tokens.get("expires_in", 3600)) * 1000
    )
    with open(GCAL_TOKENS_PATH, "w") as f:
        json.dump(tokens, f, indent=2)


def _gcal_request(url):
    """Requete GET vers l'API Google Calendar."""
    token = _get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            # Force refresh et retry
            with open(GCAL_TOKENS_PATH) as f:
                tokens = json.load(f)
            _refresh_token(tokens)
            token = _get_access_token()
            headers = {"Authorization": f"Bearer {token}"}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        error_body = e.read().decode() if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}


def _format_event(event):
    """Formater un evenement en dict lisible."""
    start = event.get("start", {})
    end = event.get("end", {})
    return {
        "summary": event.get("summary", "(sans titre)"),
        "start": start.get("dateTime", start.get("date", "")),
        "end": end.get("dateTime", end.get("date", "")),
        "location": event.get("location", ""),
        "description": (event.get("description", "") or "")[:200],
        "status": event.get("status", ""),
    }


# --- Outils exposes aux agents ---

def calendar_list_events(date_start, date_end, calendar_ids=None):
    """Lister les evenements de tous les calendriers pour une periode."""
    if not calendar_ids:
        calendar_ids = [c["id"] for c in ALL_CALENDARS]

    all_events = []
    for cal_id in calendar_ids:
        cal_name = next(
            (c["name"] for c in ALL_CALENDARS if c["id"] == cal_id), cal_id
        )
        encoded_id = urllib.parse.quote(cal_id, safe="")
        url = (
            f"https://www.googleapis.com/calendar/v3/calendars/{encoded_id}/events"
            f"?timeMin={date_start}T00:00:00Z"
            f"&timeMax={date_end}T23:59:59Z"
            f"&singleEvents=true"
            f"&orderBy=startTime"
            f"&maxResults=50"
        )
        resp = _gcal_request(url)
        if "error" in resp:
            continue
        for event in resp.get("items", []):
            formatted = _format_event(event)
            formatted["calendar"] = cal_name
            all_events.append(formatted)

    # Trier par heure de debut
    all_events.sort(key=lambda e: e.get("start", ""))
    return {"events": all_events, "count": len(all_events)}


# --- Schemas d'outils pour l'API Anthropic ---

CALENDAR_TOOLS = [
    {
        "name": "calendar_list_events",
        "description": (
            "Lister les evenements Google Calendar pour une periode donnee. "
            "Scanne TOUS les calendriers de Catherine (12 calendriers, 3 comptes). "
            "Dates au format YYYY-MM-DD."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "date_start": {
                    "type": "string",
                    "description": "Date debut au format YYYY-MM-DD",
                },
                "date_end": {
                    "type": "string",
                    "description": "Date fin au format YYYY-MM-DD",
                },
                "calendar_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "IDs des calendriers a scanner (defaut: tous)",
                },
            },
            "required": ["date_start", "date_end"],
        },
    },
]

CALENDAR_HANDLERS = {
    "calendar_list_events": calendar_list_events,
}
