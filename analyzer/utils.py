import fitz
from docx import Document

def extract_resume_text(file_path):
    text = ""

    # PDF
    if file_path.endswith(".pdf"):
        document = fitz.open(file_path)
        for page in document:
            text += page.get_text()
        document.close()

    # DOCX
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text