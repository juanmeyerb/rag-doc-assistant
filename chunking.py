from pathlib import Path

import pymupdf


def clean_text(text):
    kept_lines = []
    for line in text.split("\n"):
        if any(character.isalnum() for character in line):
            kept_lines.append(line.strip())
    return "\n".join(kept_lines)


def load_pdf_chunks(pdf_path):
    pdf_path = Path(pdf_path)
    chunks = []
    doc = pymupdf.open(pdf_path)
    for page in doc:
        text = clean_text(page.get_text())
        if text:
            chunks.append({"source": pdf_path.name, "page": page.number + 1, "text": text})
    return chunks


def load_chunks(folder="static"):
    chunks = []
    for pdf_path in sorted(Path(folder).glob("*.pdf")):
        chunks.extend(load_pdf_chunks(pdf_path))
    return chunks