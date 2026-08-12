import re


def extract_experience(text):
    """
    Extract basic work experience information from resume text.

    Returns:
        {
            "years": float,
            "internships": int,
            "roles": list
        }
    """

    text_lower = text.lower()

    # --------------------------------------------------
    # 1. Detect years of experience
    # --------------------------------------------------

    years = []

    year_patterns = [
        r'(\d+(?:\.\d+)?)\s*\+?\s*years?\s+(?:of\s+)?experience',
        r'(\d+(?:\.\d+)?)\s*\+?\s*years?\s+(?:as|in)',
    ]

    for pattern in year_patterns:
        matches = re.findall(pattern, text_lower)

        for match in matches:
            years.append(float(match))

    total_years = max(years) if years else 0


    # --------------------------------------------------
    # 2. Count internships
    # --------------------------------------------------

    internship_count = len(
        re.findall(r'\bintern(ship)?\b', text_lower)
    )


    # --------------------------------------------------
    # 3. Detect common job roles
    # --------------------------------------------------

    possible_roles = [
        "software developer",
        "software engineer",
        "python developer",
        "java developer",
        "web developer",
        "frontend developer",
        "backend developer",
        "full stack developer",
        "data analyst",
        "data scientist",
        "machine learning engineer",
        "intern",
    ]

    detected_roles = []

    for role in possible_roles:
        if role in text_lower:
            detected_roles.append(role.title())


    return {
        "years": total_years,
        "internships": internship_count,
        "roles": detected_roles
    }