import os
from PyPDF2 import PdfReader
from docx import Document


def extract_pdf_text(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file_path):

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        text.append(paragraph.text)

    return "\n".join(text)


def extract_txt_text(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def extract_resume_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    elif extension == ".txt":
        return extract_txt_text(file_path)

    else:
        raise ValueError(
            "Unsupported resume format."
        )




































