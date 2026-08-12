import re


def extract_education(text):
    """
    Extract basic education information from resume text.

    Returns:
        {
            "degree": str or None,
            "institution": str or None,
            "year": int or None
        }
    """

    # --------------------------------------------------
    # 1. Detect degree
    # --------------------------------------------------

    degree_patterns = [
        (r'\bmca\b', "MCA"),
        (r'\bbtech\b', "BTech"),
        (r'\bmtech\b', "MTech"),
        (r'\bbca\b', "BCA"),
        (r'\bbsc\b', "BSc"),
        (r'\bmsc\b', "MSc"),
        (r'\bba\b', "BA"),
        (r'\bma\b', "MA"),
        (r'\bphd\b', "PhD")
    ]

    degree = None

    text_lower = text.lower()

    for pattern, degree_name in degree_patterns:
        if re.search(pattern, text_lower):
            degree = degree_name
            break

    # --------------------------------------------------
    # 2. Detect graduation year
    # --------------------------------------------------

    years = re.findall(r'\b(20\d{2})\b', text)

    graduation_year = int(years[-1]) if years else None

    # --------------------------------------------------
    # 3. Detect institution
    # --------------------------------------------------

    institution = None

    institution_patterns = [
        r'(?:university|college|institute)\s+of\s+[A-Za-z ]+',
        r'[A-Za-z ]+\s+(?:university|college|institute)'
    ]

    for pattern in institution_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            institution = match.group().strip()
            break

    return {
        "degree": degree,
        "institution": institution,
        "year": graduation_year
    }