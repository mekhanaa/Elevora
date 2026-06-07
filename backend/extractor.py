import json
import re

with open("skills_master.json", "r") as f:
    SKILLS_DATA = json.load(f)

def build_skill_set():
    skills = {}
    for category in SKILLS_DATA:
        for skill in category["skills"]:
            normalized = skill.lower().strip()
            skills[normalized] = {
                "display": skill,
                "category": category["category"]
            }
            for alias in category.get("aliases", {}).get(skill, []):
                skills[alias.lower()] = {
                    "display": skill,
                    "category": category["category"]
                }
    return skills

SKILL_SET = build_skill_set()

def extract_skills(text):
    text_lower = text.lower()
    found = {}
    for skill_key, skill_data in SKILL_SET.items():
        pattern = r'\b' + re.escape(skill_key) + r'\b'
        if re.search(pattern, text_lower):
            found[skill_data["display"]] = skill_data["category"]
    return found

def calculate_match(resume_skills, jd_skills):
    resume_set = set(resume_skills.keys())
    jd_set = set(jd_skills.keys())
    matched = resume_set.intersection(jd_set)
    missing = jd_set - resume_set
    score = round((len(matched) / len(jd_set)) * 100, 1) if jd_set else 0
    return {
        "score": score,
        "matched": list(matched),
        "missing": list(missing)
    }