# Multimedia Reference Notes: Chapter 04 (Enkk & Andrej Karpathy)

This document synthesizes key pedagogical takeaways and visual metaphors from top-tier educational multimedia integrated into Chapter 04.

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

---

## 3. Andrej Karpathy: "Let's build the GPT Tokenizer" (minbpe)
- **Source Video & Codebase**: YouTube Educational Lecture (2h 15m) & `minbpe` GitHub repository (2024).
- **Core Insights**:
  1. *The Naive BPE Category-Bleed Failure*:
     - Running unconstrained byte-level BPE directly on raw text induces disastrous cross-category merges across punctuation, numbers, and letters (e.g., `"dog."`, `"hello!"`, `"user123"`, `"model4"`).
     - Because `"dog."` becomes a completely separate token from `"dog"` and `"."`, the vocabulary $V$ gets diluted with redundant punctuation-fused duplicates, severely degrading out-of-distribution generalization.
  2. *The Regex Pre-tokenization Solution*:
     - Both GPT-2 and GPT-4 split raw text using a strict regular expression into isolated chunks *before* BPE pair frequency counting and merging.
     - **Crucial Invariant**: Merges are strictly forbidden from crossing regex chunk boundaries! Each chunk is tokenized into subwords independently, and the resulting token lists are concatenated.
     - **GPT-2 Regex Breakdown**:
       ```python
       r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
       ```
       - `'s|'t|'re|'ve|'m|'ll|'d`: Isolates common English contractions as atomic entities.
       - ` ?\p{L}+`: Groups letters (`\p{L}`) with an optional leading space, preserving word boundaries without bleeding into punctuation or numbers.
       - ` ?\p{N}+`: Groups contiguous digits (`\p{N}`), keeping numbers isolated.
       - ` ?[^\s\p{L}\p{N}]+`: Groups punctuation/symbols, keeping symbols like `!!!` or `---` together without fusing to words.
       - `\s+(?!\S)` and `\s+`: Groups runs of whitespaces (preserving indentation tabs/spaces).
     - **GPT-4 Regex Refinements**:
       ```python
       r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
       ```
       - Capping digits at 3 places (`\p{N}{1,3}`): Instead of arbitrary long digit merges (` ?\p{N}+`), GPT-4 caps number chunks at 3 digits (`123`, `456`, `789`). This mirrors the standard decimal comma notation ($1,000,000 \to [1, 000, 000]$), creating consistent place-value token representations that dramatically boost arithmetic reasoning.
       - Case-insensitive contractions (`'(?i:[sdmt]|ll|ve|re)`) handles capitalized forms like `'LL`, `'VE`.
  3. *Special Tokens & Injection Security*:
     - Special delimiters (`<|endoftext|>`, `<|fim_prefix|>`, `<|fim_middle|>`, `<|fim_suffix|>`) must bypass regex splitting and byte encoding, assigned designated IDs outside the learned BPE range.
     - Failing to sanitize or escape user-supplied `<|endoftext|>` strings causes tokenizer-level prompt injection, prematurely terminating generation or breaking out of instruction contexts.
  4. *Demystifying LLM Pathologies via Tokenization*:
     - **Spelling blindness**: `"strawberry"` is parsed as `["straw", "berry"]` (two integers). The model never sees the letter "r" unless forced to decompose words into byte-level tokens.
     - **Reversing strings**: Reversing `"hello"` requires mapping a single token ID (`15334`) to an inverted sequence of tokens, which is unnatural for an autoregressive sequence model.
     - **Token fertility disparity**: Non-Latin scripts (Japanese, Arabic, Cyrillic) require 3–4 UTF-8 bytes per character, resulting in 3–8$\times$ more tokens per sentence than English. This shrinks effective context windows, slows generation, and inflates API costs.
     - **Glitch tokens (*SolidGoldMagikarp*)**: Tokens present in the BPE vocabulary (due to Reddit/web scraping) but filtered out of the pretraining data. Their row vectors in $\mathbf{W}_{\text{in}}$ received zero gradient updates, leaving them at anomalous random initialization coordinates that cause wild activation spikes and hallucinations when triggered.
