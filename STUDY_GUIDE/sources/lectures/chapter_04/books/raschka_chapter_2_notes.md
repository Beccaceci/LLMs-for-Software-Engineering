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
- **Step 1: Text to Tokens**: Splitting raw strings into atomic tokens (character-level vs. word-level vs. subword BPE).
- **Step 2: Tokens to Token IDs**: Assigning unique integer indices $i \in \{0, \dots, V-1\}$ to vocabulary items.
- **Step 3: Special Context Tokens**: Handling document boundaries (`<|endoftext|>`), unknown tokens (`<|unk|>`), and batch padding (`<|pad|>`).
- **Step 4: Byte Pair Encoding (BPE)**: Statistical pair merge algorithm; byte-level BPE on 256 UTF-8 bytes completely eliminating `<|unk|>` and preserving whitespace losslessly.
- **Step 5: Sliding Window Sampling**: Creating autoregressive input-target training pairs $(x, y)$ shifted by 1 token across context window $L$ with stride $s$.
- **Step 6: Token IDs to Embedding Vectors**: Converting integer IDs into dense $d$-dimensional continuous vectors via `torch.nn.Embedding`.
- **Step 7: Encoding Word Positions**: Combining token embeddings additively with learned absolute positional embeddings to overcome the permutation invariance of self-attention ($\mathbf{X}_{\text{in}} = \mathbf{E}_{\text{tok}} + \mathbf{E}_{\text{pos}}$).
