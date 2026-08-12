from skill_engine.engine import analyze_resume


def test_python_candidate():
    resume = """
    Python Developer Intern

    I have experience with Python, Flask, SQL and Git.
    I completed my MCA.
    """

    jd = """
    Python Developer

    Requirements:
    Python, Flask, SQL, Git and Docker.
    """

    result = analyze_resume(resume, jd)

    assert result["metadata"]["resume_skill_count"] == 4
    assert result["metadata"]["jd_skill_count"] == 5

    assert "Python" in result["matched_skills"]
    assert "Flask" in result["matched_skills"]
    assert "SQL" in result["matched_skills"]
    assert "Git" in result["matched_skills"]

    assert "Docker" in result["missing_skills"]

    assert result["experience"]["internships"] >= 1
    assert result["education"]["degree"] == "MCA"


def test_java_candidate():
    resume = """
    Java Developer Intern

    Skills: Java, MySQL and Git.
    """

    jd = """
    Python Developer

    Required:
    Python, Flask, SQL and Docker.
    """

    result = analyze_resume(resume, jd)

    assert result["metadata"]["resume_skill_count"] == 3
    assert result["metadata"]["jd_skill_count"] == 4

    assert result["matched_skills"] == []

    assert len(result["missing_skills"]) == 4


def test_frontend_candidate():
    resume = """
    Frontend Developer

    JavaScript, React, HTML, CSS and Git.
    """

    jd = """
    Frontend Developer

    JavaScript, React, HTML, CSS and Git.
    """

    result = analyze_resume(resume, jd)

    assert len(result["matched_skills"]) == 5
    assert result["missing_skills"] == []

    assert result["metadata"]["matched_count"] == 5
    assert result["metadata"]["missing_count"] == 0


def test_empty_resume():
    resume = ""

    jd = """
    Python, SQL and Docker.
    """

    result = analyze_resume(resume, jd)

    assert result["metadata"]["resume_skill_count"] == 0
    assert result["matched_skills"] == []
    assert len(result["missing_skills"]) == 3


def test_engine_output_structure():
    resume = "Python Flask SQL"
    jd = "Python Flask SQL Docker"

    result = analyze_resume(resume, jd)

    required_keys = {
        "schema_version",
        "metadata",
        "resume_skills",
        "jd_skills",
        "matched_skills",
        "missing_skills",
        "unknown_skills",
        "experience",
        "education"
    }

    assert required_keys.issubset(result.keys())