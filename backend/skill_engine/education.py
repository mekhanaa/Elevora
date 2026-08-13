import re


def extract_education(text):
    """
    Extract education information from resume text.

    Returns:
        {
            "degree": str or None,
            "institution": str or None,
            "year": int or None
        }
    """

    text_lower = text.lower()

    # --------------------------------------------------
    # 1. Detect degree
    # --------------------------------------------------

    degree_patterns = [
        (r'\bmaster of computer applications\b|\bmca\b', "MCA"),
        (r'\bmaster of technology\b|\bmtech\b', "MTech"),
        (r'\bbachelor of technology\b|\bbtech\b', "BTech"),
        (r'\bbachelor of computer applications\b|\bbca\b', "BCA"),
        (r'\bmaster of science\b|\bmsc\b', "MSc"),
        (r'\bbachelor of science\b|\bbsc\b', "BSc"),
        (r'\bmaster of arts\b|\bma\b', "MA"),
        (r'\bbachelor of arts\b|\bba\b', "BA"),
        (r'\bphd\b|\bph\.d\b', "PhD"),
    ]

    degree = None

    for pattern, degree_name in degree_patterns:
        if re.search(pattern, text_lower):
            degree = degree_name
            break

    # --------------------------------------------------
    # 2. Detect education section
    # --------------------------------------------------

    education_text = text

    education_match = re.search(
        r'EDUCATION(.*?)(?:INTERNSHIP EXPERIENCE|EXPERIENCE|PROJECTS|CERTIFICATIONS|LANGUAGES|$)',
        text,
        re.IGNORECASE | re.DOTALL
    )

    if education_match:
        education_text = education_match.group(1)

    # --------------------------------------------------
    # 3. Detect graduation year
    # --------------------------------------------------

    year_ranges = re.findall(
        r'\b(20\d{2})\s*[-–]\s*(20\d{2}|present|pursuing)\b',
        education_text,
        re.IGNORECASE
    )

    years = []

    for start, end in year_ranges:
        years.append(int(start))

        if end.isdigit():
            years.append(int(end))

    # Also find standalone years inside education section
    standalone_years = re.findall(
        r'\b20\d{2}\b',
        education_text
    )

    years.extend(int(year) for year in standalone_years)

    graduation_year = max(years) if years else None

    # --------------------------------------------------
    # 4. Detect institution
    # --------------------------------------------------

    institution = None

    institution_patterns = [
    r'([A-Z][A-Za-z ]+University(?:\s+of\s+[A-Za-z ]+)?(?:\s*\([^)]+\))?)',
    r'([A-Z][A-Za-z ]+College(?:\s+of\s+[A-Za-z ]+)?(?:\s*\([^)]+\))?)',
    r'([A-Z][A-Za-z ]+Institute(?:\s+of\s+[A-Za-z ]+)?(?:\s*\([^)]+\))?)',
]

    for pattern in institution_patterns:
        match = re.search(pattern, education_text)

        if match:
            institution = match.group(1).strip()
            break

    # --------------------------------------------------
    # 5. Return result
    # --------------------------------------------------

    return {
        "degree": degree,
        "institution": institution,
        "year": graduation_year
    }