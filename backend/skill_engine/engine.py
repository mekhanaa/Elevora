import time

from .extractor import extract_skills
from .comparator import compare_skills
from .experience import extract_experience
from .education import extract_education


def analyze_resume(resume_text, jd_text):
    """
    Run the complete Skill Engine.

    Args:
        resume_text: Extracted text from the resume.
        jd_text: Job description text.

    Returns:
        A structured dictionary containing
        skills, comparison, experience,
        education, and metadata.
    """

    start_time = time.perf_counter()

    # -----------------------------------------
    # 1. Extract skills
    # -----------------------------------------

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    # -----------------------------------------
    # 2. Compare skills
    # -----------------------------------------

    comparison = compare_skills(
        resume_skills,
        jd_skills
    )

    # -----------------------------------------
    # 3. Extract experience
    # -----------------------------------------

    experience = extract_experience(resume_text)

    # -----------------------------------------
    # 4. Extract education
    # -----------------------------------------

    education = extract_education(resume_text)

    # -----------------------------------------
    # 5. Calculate execution time
    # -----------------------------------------

    elapsed_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2
    )

    # -----------------------------------------
    # 6. Build final Skill Engine output
    # -----------------------------------------

    result = {
        "schema_version": "2.0",

        "metadata": {
            "resume_skill_count": len(resume_skills),
            "jd_skill_count": len(jd_skills),
            "matched_count": len(comparison["matched_skills"]),
            "missing_count": len(comparison["missing_skills"]),
            "analysis_time_ms": elapsed_ms
        },

        "resume_skills": resume_skills,

        "jd_skills": jd_skills,

        "matched_skills": comparison["matched_skills"],

        "missing_skills": comparison["missing_skills"],

        "unknown_skills": [],

        "experience": experience,

        "education": education
    }

    return result