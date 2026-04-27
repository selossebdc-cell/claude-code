"""Configuration centrale CS Agents."""

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Anthropic
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"

# Chemins
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = "/Users/cath/Projects/claude-skills/skills"
CLIENTS_DIR = "/Users/cath/Projects/claude-skills/clients"
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# Google Calendar
GCAL_TOKENS_PATH = os.path.expanduser(
    "~/.config/google-calendar-mcp/tokens.json"
)
GCAL_OAUTH_PATH = os.path.expanduser(
    "~/.config/google-calendar-mcp/gcp-oauth.keys.json"
)
GCAL_WRITE_CALENDAR = "catherine@csbusiness.fr"

# Notion
NOTION_SETTINGS_PATH = os.path.expanduser("~/.claude/settings.json")
NOTION_API_VERSION = "2022-06-28"
