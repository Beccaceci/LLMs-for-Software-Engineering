from pathlib import Path
import pymupdf

def extract_text_from_pdf(pdf_path):
    with pymupdf.open(pdf_path) as pdf:
        return "\n".join(page.get_text("text") for page in pdf)

# The RAG corpus is the ten numbered papers; example2.pdf is the prompting example.
pdf_texts = {i: extract_text_from_pdf(f"paper{i}.pdf") for i in range(10)}
assert all(document.strip() for document in pdf_texts.values())
for document_id, document_text in pdf_texts.items():
    print(f"paper{document_id}.pdf: {len(document_text):,} extracted characters")
    print(document_text[:500], "\n")