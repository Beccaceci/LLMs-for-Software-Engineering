# Multimedia Reference Notes: Chapter 03 (Enkk & Andrej Karpathy)

This document synthesizes key pedagogical takeaways and visual metaphors from top-tier educational multimedia integrated into Chapter 03.

---

## 1. Enkk (Enrico Mensa): Embeddings and Tokenization Mechanics
- **Source Video**: *Embeddings e Tokenization: come i computer capiscono il testo* (2023).
- **Core Insights**:
  1. *The One-Hot Dilemma*: Explaining how one-hot encoding creates isolated orthogonal basis vectors with zero semantic overlap, and why this necessitates finding a continuous mapping $\phi: \mathcal{V} \to \mathbb{R}^d$.
  2. *Hypersphere Normalization*: Why cosine similarity and angular distance on the unit hypersphere $\mathbb{S}^{d-1}$ are preferred over Euclidean distance for high-dimensional semantic search:
     $$\cos(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u}^\top \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}$$
     Cosine similarity evaluates direction and semantic concept alignment, invariant to document/word length scaling.
  3. *Tokenization Granularity Trade-offs*: Comparing word-level (OOV catastrophe), character-level (context length explosion), and subword tokenization (BPE/Byte-level BPE). Highlighting tokenization pitfalls such as digit fragmentation and cross-lingual fertility disparities.

---

## 2. Andrej Karpathy: "Neural Networks: Zero to Hero" (makemore)
- **Source Series**: *Building makemore: Part 2 (MLP Language Model)* & *Part 3 (BatchNorm & Gradients)*.
- **Core Insights**:
  1. *Embedding Tables are Linear Layers*: Karpathy demonstrates that indexing into an embedding matrix `C[X]` is functionally identical to passing a one-hot vector into a linear layer with no bias `W @ x`, because:
     $$\mathbf{W}^\top \mathbf{e}_i = \mathbf{w}_i$$
     This demystifies embeddings: they are not mysterious lookup tables, but standard learnable synaptic weights of the network.
  2. *Gradient Flow to Embedding Weights*: When backpropagating, the gradient with respect to the input weights $\frac{\partial \mathcal{L}}{\partial \mathbf{W}}$ routes error signals directly to the rows corresponding to active tokens:
     $$\mathbf{W}_{i, :} \leftarrow \mathbf{W}_{i, :} - \eta \frac{\partial \mathcal{L}}{\partial \mathbf{h}_i}$$
     This visualizes the training process: backpropagation exerts "forces" on word coordinates, pulling words that appear in similar predictive contexts towards the same region of latent space.
