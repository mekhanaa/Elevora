def analyze_skill_gap(engine_result):
    """
    Analyze missing skills from Skill Engine output.

    Args:
        engine_result: Complete output from engine.py

    Returns:
        Dictionary containing matched skills, missing skills,
        and gap percentage.
    """

    matched = engine_result.get("matched_skills", [])
    missing = engine_result.get("missing_skills", [])

    total_skills = len(matched) + len(missing)

    gap_percentage = (
        round((len(missing) / total_skills) * 100, 1)
        if total_skills
        else 0
    )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "gap_percentage": gap_percentage
    }