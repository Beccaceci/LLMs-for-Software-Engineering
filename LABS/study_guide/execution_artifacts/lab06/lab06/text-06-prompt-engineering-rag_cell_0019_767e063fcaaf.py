import re
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity

# Keep the generation tokenizer separate from the BERT tokenizer. CPU BERT
# embeddings avoid occupying MPS memory needed by the 3B generation model.
embedding_device = torch.device("cpu")
model_embeddings = AutoModel.from_pretrained("bert-base-uncased").to(embedding_device).eval()
tokenizer_embeddings = AutoTokenizer.from_pretrained("bert-base-uncased")

def extract_abstract(document_text):
    # PDF text can split "Abstract" as "A b s t r a c t". Match either spelling,
    # then stop at the numbered Introduction or Keywords section.
    heading = r"(?im)^[ \t]*a[ \t]*b[ \t]*s[ \t]*t[ \t]*r[ \t]*a[ \t]*c[ \t]*t\b"
    intro = re.search(r"(?im)^\s*(?:(?:1|I)[.\s]+)?Introduction\b", document_text)
    prefix = document_text[:intro.start()] if intro else document_text
    headings = list(re.finditer(heading, prefix))
    if not headings:
        raise ValueError("No abstract heading found; inspect the source PDF instead of inventing an abstract.")
    # paper3 has a publisher cover sheet duplicating its abstract. Use the
    # article's final Abstract heading before the first Introduction.
    abstract_start = headings[-1]
    remainder = document_text[abstract_start.end():].lstrip(" :\n\t—-.")
    abstract_end = re.search(
        r"(?:\n\s*(?:(?:1|I)[.\s]+)?Introduction\b|\n\s*(?:Keywords|Key words|Index Terms|CCS CONCEPTS)\b)",
        remainder, re.IGNORECASE,
    )
    return (remainder[:abstract_end.start()] if abstract_end else remainder).strip()

abstracts_dict = {document_id: extract_abstract(document_text) for document_id, document_text in pdf_texts.items()}
for document_id, abstract in abstracts_dict.items():
    print(f"paper{document_id}.pdf abstract ({len(abstract.split())} words):\n{abstract}\n")

document_ids = list(abstracts_dict)
tokenized_inputs = tokenizer_embeddings(
    list(abstracts_dict.values()), return_tensors="pt", padding=True,
    truncation=True, max_length=512,
).to(embedding_device)
with torch.inference_mode():
    abstract_vectors = model_embeddings(**tokenized_inputs).last_hidden_state[:, 0].cpu()
print("Abstract vectors [documents, hidden size]:", abstract_vectors.shape)
assert abstract_vectors.shape == (10, 768)