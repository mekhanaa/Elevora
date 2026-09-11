import json
import re
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_FILE = os.path.join(BASE_DIR, "config", "skills_master.json")


# Load skill database
with open(SKILLS_FILE, "r", encoding="utf-8") as f:
    SKILLS_DATA = json.load(f)


def build_skill_set():
    """
    Build a normalized lookup table containing
    skill names and their aliases.
    """

    skills = {}

    for category in SKILLS_DATA:
        category_name = category["category"]

        for skill in category["skills"]:

            # Store the actual skill name
            normalized = skill.lower().strip()

            skills[normalized] = {
                "display": skill,
                "category": category_name,
                "confidence": 1.0,
                "is_alias": False
            }

            # Store aliases
            aliases = category.get("aliases", {}).get(skill, [])

            for alias in aliases:
                skills[alias.lower().strip()] = {
                    "display": skill,
                    "category": category_name,
                    "confidence": 0.95,
                    "is_alias": True
                }

    return skills


# Build lookup table once when module loads
SKILL_SET = build_skill_set()


def extract_skills(text):
    """
    Extract recognized skills from a piece of text.

    Returns:
        [
            {
                "skill": "Python",
                "category": "Programming",
                "confidence": 1.0
            }
        ]
    """

    if not text or not text.strip():
        return []

    text_lower = text.lower()

    found = {}

    for skill_key, skill_data in SKILL_SET.items():

        # Skills containing special characters
        # Example: C++, Node.js
        if re.search(r"[^a-z0-9]", skill_key):
            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(skill_key)
                + r"(?![a-z0-9])"
            )

        # Short aliases such as:
        # js, py
        # The dot is treated as part of another technology name,
        # so "js" does not match the ".js" inside "Node.js".
        elif skill_data["is_alias"] and len(skill_key) <= 2:
            pattern = (
                r"(?<![a-z0-9.])"
                + re.escape(skill_key)
                + r"(?![a-z0-9.])"
            )

        # Normal skills such as:
        # Python, Docker, Flask, SQL
        else:
            pattern = (
                r"(?<![a-z0-9+#])"
                + re.escape(skill_key)
                + r"(?![a-z0-9+#])"
            )

        if re.search(pattern, text_lower):

            skill_name = skill_data["display"]

            # Prevent duplicates caused by aliases
            if skill_name not in found:
                found[skill_name] = {
                    "skill": skill_name,
                    "category": skill_data["category"],
                    "confidence": skill_data["confidence"]
                }

            # Prefer the exact skill name over an alias
            elif skill_data["confidence"] > found[skill_name]["confidence"]:
                found[skill_name]["confidence"] = skill_data["confidence"]

    return list(found.values())