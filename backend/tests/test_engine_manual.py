from skill_engine.engine import analyze_resume


tests = [
    {
        "name": "Python Fresher",
        "resume": """
        MCA student.
        Python developer intern.
        Built applications using Python, Flask, SQL and Git.
        """,
        "jd": """
        Python Developer required.
        Skills: Python, Flask, SQL, Git and Docker.
        """
    },
    {
        "name": "Java Candidate",
        "resume": """
        MCA student.
        Java developer intern.
        Skills: Java, Spring, MySQL and Git.
        """,
        "jd": """
        Python Developer required.
        Skills: Python, Flask, SQL, Docker.
        """
    },
    {
        "name": "Frontend Candidate",
        "resume": """
        Frontend Developer.
        Skills: React, JavaScript, HTML, CSS and Git.
        """,
        "jd": """
        Frontend Developer.
        Required skills: React, JavaScript, HTML, CSS and Git.
        """
    },
    {
        "name": "Empty Resume",
        "resume": "",
        "jd": """
        Python Developer required.
        Skills: Python, SQL and Docker.
        """
    },
    {
        "name": "Non IT Resume",
        "resume": """
        Bachelor of Commerce graduate.
        Worked in sales and customer service.
        Excellent communication and teamwork skills.
        """,
        "jd": """
        Python Developer required.
        Skills: Python, Flask, SQL and Docker.
        """
    }
]


for test in tests:

    print("\n" + "=" * 50)
    print(test["name"])
    print("=" * 50)

    result = analyze_resume(
        test["resume"],
        test["jd"]
    )

    print("Resume skills:", result["resume_skills"])
    print("JD skills:", result["jd_skills"])
    print("Matched:", result["matched_skills"])
    print("Missing:", result["missing_skills"])
    print("Experience:", result["experience"])
    print("Education:", result["education"])
    print("Metadata:", result["metadata"])