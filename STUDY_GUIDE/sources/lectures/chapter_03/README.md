# Sources Dossier: Chapter 03 (Distributed Word Representations and Word2Vec)

This directory houses all required primary and external reference materials for Chapter 03, organized prior to chapter authoring to ensure zero omission and rigorous pedagogical grounding.

## 1. Definitive Graduate Textbooks
- [Build a Large Language Model (from Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch) (Sebastian Raschka — Manning Publications, 2024)
  - **Chapter 2**: Working with Text Data (Tokenization, Vocabulary Mapping, Embedding Layers)
  - **Why it matters**: Demonstrates the mathematical and implementation equivalence between one-hot matrix multiplication ($\mathbf{W}^\top \mathbf{e}_i$) and direct embedding lookup tables (`nn.Embedding`).
  - **What it covers**: BPE tokenizers, special tokens, discrete token-to-ID mapping, weight matrix initialization, embedding layer lookups, and positional embedding injection.
  - **Local resource**: [`../../shared/books/Build a Large Language Model from scratch (Sebastian Raschka).epub`](../../shared/books/Build a Large Language Model from scratch (Sebastian Raschka).epub), notes in [`books/raschka_chapter_2_notes.md`](books/raschka_chapter_2_notes.md).
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) (Dan Jurafsky & James H. Martin — 3rd ed. draft)
  - **Chapter 6**: Vector Semantics and Embeddings
  - **Why it matters**: The canonical theoretical text on lexical semantics, distributional hypothesis, and dense vectors.
  - **What it covers**: Term-document matrices, PPMI, TF-IDF, Word2Vec Skip-Gram with Negative Sampling (SGNS), cosine distance metrics, and semantic analogy evaluations.
- [Deep Learning](https://www.deeplearningbook.org/) (Ian Goodfellow, Yoshua Bengio, Aaron Courville — MIT Press, 2016)
  - **Chapter 14**: Autoencoders and Representation Learning
  - **Why it matters**: Formalizes distributed representations as continuous manifold discovery, contrasting local vs. distributed capacity scaling ($\mathcal{O}(V)$ vs. $\mathcal{O}(2^d)$).

## 2. Intuitive Masterclasses & Visual Walkthroughs
- Enkk (YouTube): ["Embeddings e Tokenization: come i computer capiscono il testo" (2023)](https://www.youtube.com/watch?v=5sYkC8aVv1k)
  - **Why it matters**: Visual and intuitive walkthrough of how discrete tokens map to continuous semantic vector coordinates.
  - **Key insights**: Demonstrates how token embeddings create geometric neighborhoods, why cosine similarity measures semantic closeness, and why subword representations solve the out-of-vocabulary barrier.
  - **Local notes**: [`multimedia/enkk_karpathy_notes.md`](multimedia/enkk_karpathy_notes.md).
- Andrej Karpathy: ["Neural Networks: Zero to Hero — makemore Part 2: MLP"](https://karpathy.github.io/)
  - **Why it matters**: Unveils the mechanics of Bengio's 2003 neural language model and embedding lookup tables.
  - **Key insights**: Explicitly demystifies `C = torch.randn((27, 2))` as a linear layer weight matrix without bias, showing `C[X]` as equivalent to $\mathbf{X} \mathbf{C}$ when $\mathbf{X}$ is one-hot encoded, and traces gradient backpropagation directly into embedding rows.
  - **Companion code**: [`makemore` repository](https://github.com/karpathy/makemore) (Part 2 MLP script, ~150 LOC in pure PyTorch).
- 3Blue1Brown (Grant Sanderson): ["Word Embeddings and Vector Arithmetic"](https://www.3blue1brown.com/)
  - **Why it matters**: Provides visual geometric intuition for high-dimensional hyperspheres, cosine angular separation, and linear relational translation vectors.
  - **Key insights**: Illustrates high-dimensional vector spaces, why dot products measure alignment on the hypersphere, and how linear offsets represent semantic relations.

## 3. Landmark Seminal Papers (Primary Ground Truth)
- **Foundations of the Distributional Hypothesis**:
  - Harris, Z. S. (1954): [Distributional Structure](https://www.tandfonline.com/doi/abs/10.1080/00437956.1954.11659520) — Formulates that words occurring in similar linguistic environments have similar meanings.
  - Firth, J. R. (1957): [A Synopsis of Linguistic Theory 1930-1955](https://cir.nii.ac.jp/crid/1570572700346337664) — Established the famous aphorism: *"You shall know a word by the company it keeps"*.
- **The Word2Vec Breakthrough**:
  - Mikolov, T., et al. (2013a): [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781) — Introduces Continuous Bag-of-Words (CBOW) and Continuous Skip-gram:
    - CBOW projection: $\mathbf{h} = \frac{1}{2C} \sum_{-C \le j \le C, j \ne 0} \mathbf{v}_{w_{t+j}}$
    - Skip-Gram log-likelihood objective: $\mathcal{L}_{\text{SG}} = \sum_{t=1}^T \sum_{-C \le j \le C, j \ne 0} \log P(w_{t+j} \mid w_t)$ where $P(w_O \mid w_I) = \frac{\exp(\mathbf{u}_{w_O}^\top \mathbf{v}_{w_I})}{\sum_{w=1}^V \exp(\mathbf{u}_w^\top \mathbf{v}_{w_I})}$
  - Mikolov, T., et al. (2013b): [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546) — Formulates Skip-Gram with Negative Sampling (SGNS), subsampling of frequent words, and demonstrates emergent linear relational analogies ($\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} + \mathbf{v}_{\text{woman}} \approx \mathbf{v}_{\text{queen}}$):
    - SGNS objective: $\mathcal{L}_{\text{SGNS}}(\mathbf{v}_w, \mathbf{u}_c, \{\mathbf{u}_{n,k}\}_{k=1}^K) = \log \sigma(\mathbf{u}_c^\top \mathbf{v}_w) + \sum_{k=1}^K \log \sigma(-\mathbf{u}_{n,k}^\top \mathbf{v}_w)$
    - Unigram noise distribution: $P_n(w) \propto U(w)^{3/4}$
- **Softmax Scaling & Morphology**:
  - Morin, F., & Bengio, Y. (2005): [Hierarchical Probabilistic Neural Network Language Model](http://proceedings.mlr.press/v5/morin05a/morin05a.pdf) — Replaces full Softmax with a binary Huffman hierarchical tree, reducing cost from $\mathcal{O}(V)$ to $\mathcal{O}(\log_2 V)$:
    - Path probability: $P(w \mid \mathbf{h}) = \prod_{j=1}^{L(w)-1} \sigma\left([\![ \text{ch}(n(w, j)) = n(w, j+1) ]\!] \cdot \mathbf{v}'^\top_{n(w, j)} \mathbf{h}\right)$
  - Bojanowski, P., et al. (2017): [Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) — Formulates FastText subword character $n$-gram representations:
    - Subword vector sum: $\mathbf{v}_w = \sum_{g \in \mathcal{G}_w} \mathbf{z}_g$, scoring target token via $s(w, c) = \sum_{g \in \mathcal{G}_w} \mathbf{z}_g^\top \mathbf{u}_c$, solving the Out-Of-Vocabulary (OOV) bottleneck and rare morphological variations.

## 4. University Video Lectures
- **Stanford CS224n (Natural Language Processing with Deep Learning)**:
  - Lecture 1: Introduction and Word Vectors (Christopher Manning). Focuses on discrete word representations, the one-hot collapse, Word2Vec objective, and analytical gradient derivations ($\frac{\partial J}{\partial \mathbf{v}_c}$).
  - Lecture 2: Neural Classifiers and Word Vectors (Christopher Manning). Focuses on Negative Sampling optimization, continuous Skip-Gram objective, and intrinsic evaluations.

## 5. In This Workspace
You already have detailed materials synthesized in this repository:
- [`STUDY_GUIDE/lectures/chapters/part1_foundations/03_word_embeddings.tex`](../../lectures/chapters/part1_foundations/03_word_embeddings.tex): Chapter 3 of the course study guide, structured in 10 linear causal sections (3.1 to 3.10):
  - Section 3.1: The Representation Problem: Why Continuous Embeddings are Mandatory.
  - Section 3.2: The Baseline Approach: Local One-Hot Encodings and Why They Fail (proof of $\mathbf{W}^\top \mathbf{e}_i = \mathbf{w}_i$ and Figure `fig:onehot_orthogonality_geometry`).
  - Section 3.3: Distributed Representations and the Distributional Hypothesis.
  - Section 3.4: The Embedding Training Loop & Semantic Geometry Evolution (with Figure `fig:embedding_training_loop`).
  - Section 3.5: Word2Vec Continuous Bag-of-Words (CBOW) and context dilution.
  - Section 3.6: Word2Vec Continuous Skip-Gram and the full Softmax $\mathcal{O}(V)$ computational wall.
  - Section 3.7: Scaling Softmax: Hierarchical Softmax Huffman trees and SGNS binary logistic regressions.
  - Section 3.8: Limitations of Word2Vec & The Out-Of-Vocabulary (OOV) Barrier.
  - Section 3.9: FastText: Subword Character $n$-gram Embeddings.
  - Section 3.10: Emergent Vector Space Geometry: Clustering, Metrics & Relational Analogies.
- **Empirical Lecture Experiments**:
  - **The 5-Word Toy Vocabulary & Metric Collapse**: Slide 5 introduces vocabulary $W = \{\text{dog}, \text{cat}, \text{fish}, \text{pen}, \text{pencil}\}$. Under standard basis one-hot encoding, every pair $(w_i, w_j)$ has Euclidean distance $d_E(\mathbf{e}_i, \mathbf{e}_j) = \sqrt{2}$ and cosine similarity $\cos(\mathbf{e}_i, \mathbf{e}_j) = 0$, exposing the total metric collapse of discrete orthogonal representations.
  - **Prof. Flavio Giobergia's Gist Demo**: The live empirical Python walkthrough (`giobergia2024gist`, `https://gist.github.com/fgiobergia/b3a20e097f9b697d0a02fb17685cfd5a`) demonstrating training word embeddings from scratch on real text corpora using Gensim Word2Vec, showing how continuous gradient updates map words to semantic coordinates.
  - **3-Category FastText PCA Projection**: Slide 14 visualizes a 2D PCA projection of subword embeddings across three distinct semantic domains (Household items, Mammals, Birds), proving that unsupervised training discovers clustered semantic neighborhoods.
  - **Country-Capital Relational Analogy Vector Arithmetic**: Slide 15 demonstrates emergent linear relational offsets: $\mathbf{v}_{\text{Rome}} - \mathbf{v}_{\text{Italy}} + \mathbf{v}_{\text{France}} \approx \mathbf{v}_{\text{Paris}}$, confirming that vector addition and subtraction operate as meaningful semantic relations.
- [`slides/03-WordEmbeddings.pdf`](slides/03-WordEmbeddings.pdf): Course lecture slides (symlink to `SLIDES/03-WordEmbeddings.pdf`).
- [`transcriptions/03-04-Word-Embeddings-And-RNNs.md`](transcriptions/03-04-Word-Embeddings-And-RNNs.md): Full lecture transcription (symlink to `TRANSCRIPTIONS/LECTURES/03-04-Word-Embeddings-And-RNNs.md`).
