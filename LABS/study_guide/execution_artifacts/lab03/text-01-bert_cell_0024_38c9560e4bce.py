# Load pre-trained BERT model
model_name = 'bert-base-uncased'
model = BertModel.from_pretrained(model_name)

# Position embeddings are stored in the embedding layer as 'position_embeddings.weight'
positional_encodings = model.embeddings.position_embeddings.weight.detach().cpu().numpy()

# Compute cosine similarity between positional encodings
cosine_sim = cosine_similarity(positional_encodings)

fig, ax = plt.subplot_mosaic("""
AAA
AAA
AAA
BBB""")

plt.tight_layout()

# Plot the cosine similarity heatmap
ax["A"].set_aspect('equal')
cbar = ax["A"].imshow(cosine_sim, cmap='viridis', vmin=-1, vmax=1)
ax["A"].set_xlabel('Vector 1')
ax["A"].set_ylabel('Vector 2')
ax["A"].axhline(100, c='r', lw=2)
# add colorbar
fig.colorbar(cbar, ax=ax["A"])


# Plot the cosine similarity for a specific row

ax["B"].plot(cosine_sim[100], c='r', lw=2)
ax["B"].set_xlabel('Vector 1')
ax["B"].set_ylabel('Cosine Similarity')
ax["B"].grid()