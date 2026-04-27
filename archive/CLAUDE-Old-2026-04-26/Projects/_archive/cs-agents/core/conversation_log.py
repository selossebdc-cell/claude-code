"""Logging des conversations agent pour transparence."""

import json
import os
from datetime import datetime
from config.settings import LOGS_DIR


def log_run(routine_name, result, success=True):
    """Logger l'execution d'une routine (cron)."""
    run_dir = os.path.join(LOGS_DIR, "runs")
    os.makedirs(run_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(run_dir, f"{today}.jsonl")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "routine": routine_name,
        "success": success,
        "result": result[:3000] if isinstance(result, str) else str(result)[:3000],
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_today_conversations():
    """Lire les conversations inter-agents d'aujourd'hui."""
    conv_dir = os.path.join(LOGS_DIR, "conversations")
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(conv_dir, f"{today}.jsonl")

    if not os.path.exists(log_file):
        return []

    entries = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries
