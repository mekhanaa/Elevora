from analyzers.gap import analyze_skill_gap


def test_skill_gap():

    engine_result = {
        "matched_skills": ["Python", "SQL", "Flask"],
        "missing_skills": ["Docker", "AWS"]
    }

    result = analyze_skill_gap(engine_result)

    assert result["matched_skills"] == ["Python", "SQL", "Flask"]
    assert result["missing_skills"] == ["Docker", "AWS"]
    assert result["gap_percentage"] == 40.0


def test_no_missing_skills():

    engine_result = {
        "matched_skills": ["Python", "SQL"],
        "missing_skills": []
    }

    result = analyze_skill_gap(engine_result)

    assert result["gap_percentage"] == 0


def test_all_skills_missing():

    engine_result = {
        "matched_skills": [],
        "missing_skills": ["Python", "Docker"]
    }

    result = analyze_skill_gap(engine_result)

    assert result["gap_percentage"] == 100.0


def test_empty_result():

    engine_result = {
        "matched_skills": [],
        "missing_skills": []
    }

    result = analyze_skill_gap(engine_result)

    assert result["gap_percentage"] == 0