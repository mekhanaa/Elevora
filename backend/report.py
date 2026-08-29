
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
import io
from datetime import datetime


def generate_report(data):
    """
    Generate an Elevora PDF report from analysis data.
    Handles resume skills represented as either strings or dictionaries.
    """

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.6 * inch,
        bottomMargin=0.8 * inch,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch
    )

    # --------------------------------------------------
    # Styles
    # --------------------------------------------------

    title_style = ParagraphStyle(
        "title",
        fontSize=22,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1e3a5f"),
        spaceAfter=4,
        alignment=TA_CENTER
    )

    sub_style = ParagraphStyle(
        "sub",
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#666666"),
        spaceAfter=2,
        alignment=TA_CENTER
    )

    section_style = ParagraphStyle(
        "section",
        fontSize=12,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1e3a5f"),
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "body",
        fontSize=9.5,
        fontName="Helvetica",
        textColor=colors.HexColor("#333333"),
        spaceAfter=3,
        leading=14
    )

    small_style = ParagraphStyle(
        "small",
        fontSize=8.5,
        fontName="Helvetica",
        textColor=colors.HexColor("#666666"),
        spaceAfter=2
    )

    footer_style = ParagraphStyle(
        "footer",
        fontSize=8,
        fontName="Helvetica",
        textColor=colors.HexColor("#999999"),
        alignment=TA_CENTER
    )

    story = []

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    story.append(Spacer(1, 20))

    story.append(
        Paragraph("Elevora", title_style)
    )

    story.append(Spacer(1, 14))

    story.append(
        Paragraph(
            "Resume Intelligence & Career Path Report",
            sub_style
        )
    )

    story.append(Spacer(1, 6))

    # --------------------------------------------------
    # Candidate Information
    # --------------------------------------------------

    candidate_name = data.get(
        "candidate_name",
        "Unknown"
    )

    candidate_email = data.get(
        "candidate_email",
        ""
    )

    story.append(
        Paragraph(
            f"Candidate: {candidate_name}",
            sub_style
        )
    )

    if candidate_email:
        story.append(
            Paragraph(
                f"Email: {candidate_email}",
                sub_style
            )
        )

    story.append(
        Paragraph(
            f"Generated on "
            f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            sub_style
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=colors.HexColor("#1e3a5f"),
            spaceAfter=10
        )
    )

    # --------------------------------------------------
    # Match Score
    # --------------------------------------------------

    score = data.get("match_score", 0)

    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0

    score_color = (
        "#22c55e"
        if score >= 70
        else "#f59e0b"
        if score >= 40
        else "#ef4444"
    )

    score_label = (
        "Strong Match"
        if score >= 70
        else "Partial Match"
        if score >= 40
        else "Weak Match"
    )

    story.append(
        Paragraph(
            "Match Score",
            section_style
        )
    )

    story.append(
        Paragraph(
            f'<font color="{score_color}" size="28">'
            f'<b>{score:g}%</b>'
            f'</font>'
            f' &nbsp;&nbsp; {score_label}',
            body_style
        )
    )

    story.append(Spacer(1, 6))

    # --------------------------------------------------
    # Matched Skills
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Matched Skills",
            section_style
        )
    )

    matched = data.get(
        "matched_skills",
        []
    )

    if matched:
        matched_names = []

        for skill in matched:

            if isinstance(skill, dict):
                skill_name = skill.get(
                    "skill",
                    ""
                )
            else:
                skill_name = str(skill)

            if skill_name:
                matched_names.append(skill_name)

        if matched_names:
            story.append(
                Paragraph(
                    ", ".join(matched_names),
                    body_style
                )
            )
        else:
            story.append(
                Paragraph(
                    "No matched skills found.",
                    small_style
                )
            )
    else:
        story.append(
            Paragraph(
                "No matched skills found.",
                small_style
            )
        )

    # --------------------------------------------------
    # Missing Skills
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Missing Skills",
            section_style
        )
    )

    missing = data.get(
        "missing_skills",
        []
    )

    if missing:

        missing_names = []

        for skill in missing:

            if isinstance(skill, dict):
                skill_name = skill.get(
                    "skill",
                    ""
                )
            else:
                skill_name = str(skill)

            if skill_name:
                missing_names.append(skill_name)

        if missing_names:
            story.append(
                Paragraph(
                    ", ".join(missing_names),
                    body_style
                )
            )
        else:
            story.append(
                Paragraph(
                    "No missing skills - perfect match!",
                    small_style
                )
            )

    else:
        story.append(
            Paragraph(
                "No missing skills - perfect match!",
                small_style
            )
        )

    # --------------------------------------------------
    # Resume Skills
    # --------------------------------------------------

    story.append(
        Paragraph(
            "All Skills in Your Resume",
            section_style
        )
    )

    resume_skills = data.get(
        "resume_skills",
        []
    )

    resume_skill_names = []

    for skill in resume_skills:

        if isinstance(skill, dict):

            skill_name = skill.get(
                "skill",
                ""
            )

        else:

            skill_name = str(skill)

        if skill_name:
            resume_skill_names.append(
                skill_name
            )

    if resume_skill_names:

        story.append(
            Paragraph(
                ", ".join(resume_skill_names),
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                "No resume skills detected.",
                small_style
            )
        )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor("#dddddd"),
            spaceBefore=10,
            spaceAfter=10
        )
    )

    # --------------------------------------------------
    # Career Readiness
    # --------------------------------------------------

    careers = data.get(
        "careers",
        []
    )

    if careers:

        story.append(
            Paragraph(
                "Career Readiness",
                section_style
            )
        )

        table_data = [
            [
                "Role",
                "Category",
                "Readiness",
                "Status"
            ]
        ]

        for career in careers[:6]:

            role = str(
                career.get(
                    "role",
                    "Unknown"
                )
            )

            category = str(
                career.get(
                    "category",
                    "General"
                )
            )

            try:
                career_score = float(
                    career.get(
                        "score",
                        0
                    )
                )
            except (TypeError, ValueError):
                career_score = 0

            status = (
                "Strong"
                if career_score >= 70
                else "Partial"
                if career_score >= 40
                else "Weak"
            )

            table_data.append(
                [
                    role,
                    category,
                    f"{career_score:g}%",
                    status
                ]
            )

        table = Table(
            table_data,
            colWidths=[
                2.2 * inch,
                1.4 * inch,
                1 * inch,
                1 * inch
            ]
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1e3a5f")
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.HexColor("#f8fafc"),
                            colors.white
                        ]
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.3,
                        colors.HexColor("#dddddd")
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "ALIGN",
                        (2, 0),
                        (3, -1),
                        "CENTER"
                    )
                ]
            )
        )

        story.append(table)

        story.append(
            Spacer(1, 10)
        )

    # --------------------------------------------------
    # Skill Gap Roadmap
    # --------------------------------------------------

    if careers:

        story.append(
            Paragraph(
                "Skill Gap Roadmap",
                section_style
            )
        )

        roadmap_found = False

        for career in careers[:3]:

            roadmap = career.get(
                "roadmap",
                []
            )

            if not roadmap:
                continue

            roadmap_found = True

            role = str(
                career.get(
                    "role",
                    "Career"
                )
            )

            story.append(
                Paragraph(
                    f"<b>{role}</b>",
                    body_style
                )
            )

            for item in roadmap[:2]:

                if isinstance(item, dict):

                    skill = str(
                        item.get(
                            "skill",
                            ""
                        )
                    )

                    path = str(
                        item.get(
                            "path",
                            ""
                        )
                    )

                else:

                    skill = str(item)
                    path = ""

                if skill and path:

                    story.append(
                        Paragraph(
                            f"- {skill} - {path}",
                            small_style
                        )
                    )

                elif skill:

                    story.append(
                        Paragraph(
                            f"- {skill}",
                            small_style
                        )
                    )

        if not roadmap_found:

            story.append(
                Paragraph(
                    "No skill-gap roadmap available.",
                    small_style
                )
            )

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    story.append(
        Spacer(1, 16)
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor("#dddddd"),
            spaceAfter=6
        )
    )

    story.append(
        Paragraph(
            "© Elevora | Developed by Mekh",
            footer_style
        )
    )

    # --------------------------------------------------
    # Build PDF
    # --------------------------------------------------

    doc.build(story)

    buffer.seek(0)

    return buffer
