
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def generate_translation_pdf(translated_text):

    """Generate a downloadable PDF containing the English translation."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.8 * inch,
        leftMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "PDFTitle",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#1F77B4"),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    body_style = ParagraphStyle(
        "TranslationBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=17,
        alignment=TA_LEFT,
        spaceAfter=10
    )

    story = []

    story.append(
        Paragraph("BhashaSetu - English Translation", title_style)
    )

    story.append(Spacer(1, 0.2 * inch))

    # Preserve paragraph breaks and safely escape special characters.
    for paragraph in translated_text.splitlines():

        if paragraph.strip():
            story.append(
                Paragraph(escape(paragraph), body_style)
            )
        else:
            story.append(Spacer(1, 8))

    document.build(story)

    buffer.seek(0)

    return buffer
