# Sebastian Raschka: "Build a Large Language Model (from Scratch)" — Chapter 2 Notes

Source: `STUDY_GUIDE/sources/shared/books/Build a Large Language Model from scratch (Sebastian Raschka).epub` (Chapter 2: *Working with text data*)

## Key Pedagogical Principles & Technical Insights

### 1. The Fundamental Motivation: Why Embeddings are Required
- **Core Premise**: Deep neural network models, including LLMs, cannot process raw text directly.
- **Mathematical Incompatibility**: Text is categorical/discrete and cannot participate in differential calculus, inner products, or backpropagation.
- **Definition of Embedding**: An embedding is fundamentally a mapping from discrete objects (words, characters, subwords, tokens) to points in a continuous vector space ($\phi: \mathcal{V} \to \mathbb{R}^d$, with $d \ll V$).
- The primary purpose of embeddings is to convert non-numeric, discrete categorical items into continuous dense vectors that neural networks can process and optimize.

### 2. The Algebraic Equivalence of One-Hot Vectors and Embedding Lookup Tables
In Section 2.7 (*"Creating token embeddings"*), Raschka highlights the direct mathematical equivalence between one-hot matrix multiplication and embedding lookups:
- Suppose a vocabulary has $V$ items, and we represent the $i$-th token as standard basis one-hot vector $\mathbf{e}_i \in \{0, 1\}^V$.
- Passing $\mathbf{e}_i$ through a linear neural network layer with weight matrix $\mathbf{W} \in \mathbb{R}^{V \times d}$:
  $$\mathbf{e}_i^\top \mathbf{W} = \mathbf{w}_i^\top \in \mathbb{R}^{1 \times d}$$
  extracts exactly the $i$-th row of $\mathbf{W}$.
- **Systems Engineering Reality**: In deep learning frameworks (e.g. PyTorch `torch.nn.Embedding(vocab_size, output_dim)`), the framework does not compute a dense matrix multiplication with thousands of multiplications by zero. Instead, it implements this exact linear layer via an $\mathcal{O}(1)$ pointer/integer lookup (`embedding_layer(torch.tensor([3]))` $\to$ row 3).
- **Trainable Parameters**: The rows of this matrix are initialized with small random values (`torch.manual_seed(123)`), and are updated during model training via gradient descent and backpropagation.

### 3. Data Preparation & Tokenization Pipeline
- **Step 1: Text to Tokens**: Splitting raw string into atomic tokens (word-level vs character-level vs subword BPE).
- **Step 2: Tokens to Token IDs**: Assigning unique integer indices $i \in \{0, \dots, V-1\}$ to vocabulary items.
- **Step 3: Sliding Window Sampling**: Creating input-target training pairs $(x, y)$ by sliding a context window across the tokenized sequence.
- **Step 4: Token IDs to Embedding Vectors**: Converting integer IDs into dense $d$-dimensional continuous vectors via the embedding layer lookup.
