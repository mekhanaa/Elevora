from skill_engine.extractor import extract_skills


def test_extract_normal_skills():
    text = "I know Python, Flask, SQL and Docker."

    result = extract_skills(text)

    skills = [item["skill"] for item in result]

    assert "Python" in skills
    assert "Flask" in skills
    assert "SQL" in skills
    assert "Docker" in skills


def test_extract_aliases():
    text = "I use py, python3, js and es6."

    result = extract_skills(text)

    skills = [item["skill"] for item in result]

    assert "Python" in skills
    assert "JavaScript" in skills


def test_empty_text():
    result = extract_skills("")

    assert result == []


def test_unknown_skills():
    text = "I know Photoshop and Blender."

    result = extract_skills(text)

    assert result == []


def test_case_insensitive():
    text = "PYTHON FLASK docker"

    result = extract_skills(text)

    skills = [item["skill"] for item in result]

    assert "Python" in skills
    assert "Flask" in skills
    assert "Docker" in skills


def test_confidence_values():
    text = "Python Flask"

    result = extract_skills(text)

    for item in result:
        assert 0 <= item["confidence"] <= 1