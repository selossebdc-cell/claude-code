"""Bridge vers les skills existants — lecture des SKILL.md et references."""

import os
from config.settings import SKILLS_DIR

VALID_SKILLS = [
    "session-report",
    "invoice-generator",
    "proposal-generator",
    "client-onboarding",
    "roadmap-generator",
    "weekly-planner",
    "agenda-writer",
    "linkedin-content",
    "noble-ai",
    "brand-identity",
]


def read_skill_knowledge(skill_name, include_references=False):
    if skill_name not in VALID_SKILLS:
        return {"error": f"Skill inconnu: {skill_name}. Valides: {VALID_SKILLS}"}

    skill_dir = os.path.join(SKILLS_DIR, skill_name)
    skill_path = os.path.join(skill_dir, "SKILL.md")
    result = {"skill": skill_name}

    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf-8") as f:
            result["skill_md"] = f.read()
    else:
        return {"error": f"SKILL.md introuvable pour {skill_name}"}

    if include_references:
        refs_dir = os.path.join(skill_dir, "references")
        if os.path.isdir(refs_dir):
            result["references"] = {}
            for ref_file in sorted(os.listdir(refs_dir)):
                if ref_file.endswith(".md"):
                    ref_path = os.path.join(refs_dir, ref_file)
                    with open(ref_path, "r", encoding="utf-8") as f:
                        result["references"][ref_file] = f.read()

    return result


SKILLS_BRIDGE_TOOLS = [
    {
        "name": "read_skill_knowledge",
        "description": (
            "Lire les connaissances d'un skill existant (SKILL.md + references). "
            "Utilise quand tu as besoin de connaitre un process metier : "
            "facturation, CR de session, proposition commerciale, charte graphique, etc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "enum": VALID_SKILLS,
                    "description": "Nom du skill a lire",
                },
                "include_references": {
                    "type": "boolean",
                    "description": "Inclure les fichiers de reference (defaut: false)",
                },
            },
            "required": ["skill_name"],
        },
    },
]

SKILLS_BRIDGE_HANDLERS = {
    "read_skill_knowledge": read_skill_knowledge,
}
