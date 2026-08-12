def compare_skills(resume_skills, jd_skills):
    """
    Compare resume skills against job-description skills.

    Args:
        resume_skills: List of skill dictionaries from extractor.py
        jd_skills: List of skill dictionaries from extractor.py

    Returns:
        Dictionary containing matched skills,
        missing skills, and overall match score.
    """

    resume_map = {
        item["skill"].lower(): item["skill"]
        for item in resume_skills
    }

    jd_map = {
        item["skill"].lower(): item["skill"]
        for item in jd_skills
    }

    matched = []
    missing = []

    for skill_key, display_name in jd_map.items():
        if skill_key in resume_map:
            matched.append(display_name)
        else:
            missing.append(display_name)

    total_jd_skills = len(jd_map)

    score = (
        round((len(matched) / total_jd_skills) * 100, 1)
        if total_jd_skills
        else 0
    )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "score": score
    }