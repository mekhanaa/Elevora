from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
from datetime import datetime

def generate_report(data):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.6*inch,
        bottomMargin=0.8*inch,
        leftMargin=0.7*inch,
        rightMargin=0.7*inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('title',
        fontSize=22, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1e3a5f'),
        spaceAfter=4, alignment=TA_CENTER)

    sub_style = ParagraphStyle('sub',
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#666666'),
        spaceAfter=2, alignment=TA_CENTER)

    section_style = ParagraphStyle('section',
        fontSize=12, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1e3a5f'),
        spaceBefore=14, spaceAfter=6)

    body_style = ParagraphStyle('body',
        fontSize=9.5, fontName='Helvetica',
        textColor=colors.HexColor('#333333'),
        spaceAfter=3, leading=14)

    small_style = ParagraphStyle('small',
        fontSize=8.5, fontName='Helvetica',
        textColor=colors.HexColor('#666666'),
        spaceAfter=2)

    footer_style = ParagraphStyle('footer',
        fontSize=8, fontName='Helvetica',
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER)

    story = []

    # Header
    story.append(Spacer(1, 20))
    story.append(Paragraph("SkillMap", title_style))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Resume Intelligence & Career Path Report", sub_style))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        sub_style
    ))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(
        width="100%", thickness=1.5,
        color=colors.HexColor('#1e3a5f'),
        spaceAfter=10
    ))

    # Match Score
    score = data.get("match_score", 0)
    score_color = (
        '#22c55e' if score >= 70 else
        '#f59e0b' if score >= 40 else
        '#ef4444'
    )
    score_label = (
        "Strong Match" if score >= 70 else
        "Partial Match" if score >= 40 else
        "Weak Match"
    )

    story.append(Paragraph("Match Score", section_style))
    story.append(Paragraph(
        f'<font color="{score_color}" size="28"><b>{score}%</b></font> &nbsp;&nbsp; {score_label}',
        body_style
    ))
    story.append(Spacer(1, 6))

    # Matched Skills
    story.append(Paragraph("Matched Skills", section_style))
    matched = data.get("matched_skills", [])
    if matched:
        story.append(Paragraph(", ".join(matched), body_style))
    else:
        story.append(Paragraph("No matched skills found.", small_style))

    # Missing Skills
    story.append(Paragraph("Missing Skills", section_style))
    missing = data.get("missing_skills", [])
    if missing:
        story.append(Paragraph(", ".join(missing), body_style))
    else:
        story.append(Paragraph("No missing skills - perfect match!", small_style))

    # All Resume Skills
    story.append(Paragraph("All Skills in Your Resume", section_style))
    resume_skills = data.get("resume_skills", [])
    if resume_skills:
        story.append(Paragraph(", ".join(resume_skills), body_style))

    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=colors.HexColor('#dddddd'),
        spaceBefore=10, spaceAfter=10
    ))

    # Career Readiness
    careers = data.get("careers", [])
    if careers:
        story.append(Paragraph("Career Readiness", section_style))

        table_data = [["Role", "Category", "Readiness", "Status"]]
        for c in careers[:6]:
            status = "Strong" if c["score"] >= 70 else "Partial" if c["score"] >= 40 else "Weak"
            table_data.append([
                c["role"],
                c["category"],
                f"{c['score']}%",
                status
            ])

        table = Table(table_data, colWidths=[
            2.2*inch, 1.4*inch, 1*inch, 1*inch
        ])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1),
             [colors.HexColor('#f8fafc'), colors.white]),
            ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dddddd')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('ALIGN', (2,0), (3,-1), 'CENTER'),
        ]))
        story.append(table)
        story.append(Spacer(1, 10))

    # Skill Gap Roadmap
    if careers:
        story.append(Paragraph("Skill Gap Roadmap", section_style))
        for c in careers[:3]:
            if c.get("roadmap"):
                story.append(Paragraph(
                    f"<b>{c['role']}</b>",
                    body_style
                ))
                for item in c["roadmap"][:2]:
                    story.append(Paragraph(
                        f"  • {item['skill']} - {item['path']}",
                        small_style
                    ))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=colors.HexColor('#dddddd'),
        spaceAfter=6
    ))

    # Footer — same as website
    story.append(Paragraph(
        "© SkillMap | Developed by Mekh",
        footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer