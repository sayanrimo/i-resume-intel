import docx
from pypdf import PdfReader
from pathlib import Path
import logging

def parse_pdf(file_path: Path) -> str:
    try:
        reader = PdfReader(file_path)
        return "".join(page.extract_text() for page in reader.pages if page.extract_text())
    except Exception as e:
        logging.error(f"Error parsing PDF {file_path}: {e}")
        return ""

def parse_docx(file_path: Path) -> str:
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text])
    except Exception as e:
        logging.error(f"Error parsing DOCX {file_path}: {e}")
        return ""