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
    # 2. Detect internship positions
    # --------------------------------------------------

    internship_roles = re.findall(
        r'([A-Za-z][A-Za-z &-]*?)\s+Intern\b',
        text,
        re.IGNORECASE
    )

    # Remove duplicates
    internship_roles = list(dict.fromkeys(
    role.strip().title() + " Intern"
    for role in internship_roles
))

    internship_count = len(internship_roles)


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
    ]

    detected_roles = []

    for role in possible_roles:
        if role in text_lower:
            detected_roles.append(role.title())

    # Add actual internship roles
    detected_roles.extend(internship_roles)

    # Remove duplicates while preserving order
    detected_roles = list(dict.fromkeys(detected_roles))


    return {
        "years": total_years,
        "internships": internship_count,
        "roles": detected_roles
    }