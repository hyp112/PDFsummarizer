# app/pdf_utils.py

import fitz  # PyMuPDF
from fastapi import UploadFile
import io

def extract_text_from_pdf(file: UploadFile) -> str:
    text = ""
    with fitz.open(stream=io.BytesIO(file.file.read()), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()
