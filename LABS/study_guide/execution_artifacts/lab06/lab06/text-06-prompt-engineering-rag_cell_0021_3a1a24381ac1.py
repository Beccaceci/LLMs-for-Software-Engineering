def get_top_k_similar_indices(query_vector, abstract_vectors, k):
    if not 1 <= k <= len(abstract_vectors):
        raise ValueError("k must be between 1 and the number of documents")
    similarities = cosine_similarity(
        query_vector.cpu().detach().numpy(), abstract_vectors.cpu().detach().numpy()
    )
    return np.argsort(-similarities, axis=1, kind="stable")[:, :k]


def retrieve_documents(indices, documents_dict):
    selected_ids = [document_ids[int(index)] for index in np.asarray(indices).reshape(-1)]
    return "\n\n".join(f"[paper{document_id}.pdf]\n{documents_dict[document_id]}" for document_id in selected_ids)


def embed_query(query):
    encoded_query = tokenizer_embeddings(query, return_tensors="pt", truncation=True, max_length=512).to(embedding_device)
    with torch.inference_mode():
        return model_embeddings(**encoded_query).last_hidden_state[:, 0].cpu()

query = "How does DynamoLLM improve energy efficiency while meeting latency service-level objectives?"
query_vector = embed_query(query)
top_indices = get_top_k_similar_indices(query_vector, abstract_vectors, k=3)
retrieved_documents = retrieve_documents(top_indices, pdf_texts)
scores = cosine_similarity(query_vector.numpy(), abstract_vectors.numpy())[0]
print("Query vector shape:", query_vector.shape)
print("Top three documents:", [(f"paper{document_ids[int(i)]}.pdf", float(scores[i])) for i in top_indices[0]])
print("Retrieved full-text characters:", len(retrieved_documents))
print(retrieved_documents[:1000])