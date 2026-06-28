from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.units import inch


def generate_pdf_report(
        candidate,
        output_file):

    doc = SimpleDocTemplate(
        output_file
    )

    styles = getSampleStyleSheet()

    story = []

    # Title

    title = Paragraph(
        "AI Resume ATS Report",
        styles["Title"]
    )

    story.append(title)
    story.append(
        Spacer(1, 0.2 * inch)
    )

    # Candidate Name

    story.append(
        Paragraph(
            f"<b>Candidate:</b> "
            f"{candidate['candidate']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> "
            f"{candidate['ats_score']}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Recommendation:</b> "
            f"{candidate['recommendation']}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 0.2 * inch)
    )

    # Matched Skills

    story.append(
        Paragraph(
            "<b>Matched Skills:</b>",
            styles["Heading2"]
        )
    )

    for skill in candidate[
            "matched_skills"]:

        story.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )

    story.append(
        Spacer(1, 0.1 * inch)
    )

    # Missing Skills

    story.append(
        Paragraph(
            "<b>Missing Skills:</b>",
            styles["Heading2"]
        )
    )

    for skill in candidate[
            "missing_skills"]:

        story.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )

    story.append(
        Spacer(1, 0.1 * inch)
    )

    # Sections

    story.append(
        Paragraph(
            "<b>Resume Sections Found:</b>",
            styles["Heading2"]
        )
    )

    for section in candidate[
            "present_sections"]:

        story.append(
            Paragraph(
                f"• {section}",
                styles["Normal"]
            )
        )

    doc.build(story)