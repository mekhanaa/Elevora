from skill_engine.comparator import compare_skills


def test_all_skills_match():
    resume = [
        {"skill": "Python"},
        {"skill": "SQL"},
        {"skill": "Git"}
    ]

    jd = [
        {"skill": "Python"},
        {"skill": "SQL"},
        {"skill": "Git"}
    ]

    result = compare_skills(resume, jd)

    assert result["matched_skills"] == ["Python", "SQL", "Git"]
    assert result["missing_skills"] == []
    assert result["score"] == 100.0


def test_partial_match():
    resume = [
        {"skill": "Python"},
        {"skill": "SQL"}
    ]

    jd = [
        {"skill": "Python"},
        {"skill": "SQL"},
        {"skill": "Docker"}
    ]

    result = compare_skills(resume, jd)

    assert result["matched_skills"] == ["Python", "SQL"]
    assert result["missing_skills"] == ["Docker"]
    assert result["score"] == 66.7


def test_no_match():
    resume = [
        {"skill": "Java"}
    ]

    jd = [
        {"skill": "Python"},
        {"skill": "Docker"}
    ]

    result = compare_skills(resume, jd)

    assert result["matched_skills"] == []
    assert result["missing_skills"] == ["Python", "Docker"]
    assert result["score"] == 0.0


def test_empty_jd():
    resume = [
        {"skill": "Python"}
    ]

    jd = []

    result = compare_skills(resume, jd)

    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["score"] == 0


def test_case_insensitive_matching():
    resume = [
        {"skill": "python"},
        {"skill": "SQL"}
    ]

    jd = [
        {"skill": "Python"},
        {"skill": "sql"}
    ]

    result = compare_skills(resume, jd)

    assert len(result["matched_skills"]) == 2
    assert result["missing_skills"] == []
    assert result["score"] == 100.0