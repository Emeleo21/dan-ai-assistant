import io
from xml.sax.saxutils import escape

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer



def create_pdf(title: str, content: str, filename: str = "document.pdf") -> str:
    """Create a PDF document with a title and body text. Separate paragraphs
    with blank lines. Lines starting with '# ' become section headings.
    Use this whenever the user asks for a PDF, report, letter, CV or document.
    The user will get a download button automatically."""
    try:
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, title=title)
        styles = getSampleStyleSheet()

        story = [Paragraph(escape(title), styles["Title"]), Spacer(1, 12)]
        for block in content.split("\n\n"):
            block = block.strip()
            if not block:
                continue
            if block.startswith("# "):
                story.append(Paragraph(escape(block[2:]), styles["Heading2"]))
            else:
                story.append(Paragraph(escape(block).replace("\n", "<br/>"), styles["BodyText"]))
            story.append(Spacer(1, 8))

        doc.build(story)

        st.session_state.setdefault("pending_files", []).append(
            {"name": filename, "data": buffer.getvalue(), "mime": "application/pdf"}
        )
        return f"PDF '{filename}' created. Tell the user it is ready to download below."
    except Exception as e:
        return f"Error creating PDF: {e}"