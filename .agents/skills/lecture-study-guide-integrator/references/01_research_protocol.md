# Pre-Ingestion External Research Protocol

Before writing or integrating any lecture slide, transcript, or syllabus module into the study guide, the agent MUST execute targeted literature, textbook, and multimedia research to enrich the lecture content. Lecture slides are compressed by nature; academic excellence requires expanding slide points using seminal literature, local authoritative textbooks, and top-tier expert breakdowns.

---

## 1. The 8 Authority Vectors

Every concept must be triangulated across these eight authority vectors:

| Vector | Authority / Source | Primary Value & Pedagogical Focus | Target LaTeX Integration |
|---|---|---|---|
| **V1** | **Seminal Academic Papers**<br>(arXiv, NeurIPS, ICLR, ICML, ACL, EMNLP) | Canonical mathematical precision, formal definitions, proofs, objective functions, ablations, benchmark tables. | Inline body text, `theorem`, and numeric citations `[x]` |
| **V2** | **Andrej Karpathy**<br>(YouTube, nanoGPT, micrograd, makemore) | Code-level mechanics, tensor broadcasting nuances, autograd computational graphs, KV-cache plumbing, temperature sampling, BPE tokenization. | `deepdive` callout box, inline text, & listings |
| **V3** | **3Blue1Brown**<br>(Grant Sanderson & `3b1b/manim`) | High-dimensional geometric intuition, vector space transformations, spatial analogies, visual linear algebra, and Manim code harvesting. | `intuition` callout box, TikZ figures, & Manim 3D/video assets |
| **V4** | **Enkk**<br>(Enrico Mensa) | Tokenization mechanisms (word vs. char vs. subword), arithmetic digit blindness, token fertility disparities, unit hypersphere geometry (Cosine vs. $L_2$), vector DB indexing (HNSW, IVF-PQ) in RAG. | `deepdive` callout box, inline synthesis, & exam insights |
| **V5** | **Antirez**<br>(Salvatore Sanfilippo) | Architectural simplicity, LLM inference from scratch, token prediction mechanics, sampling algorithms (temperature, top-$k$, top-$p$), clean C/Python implementations without bloated frameworks. | `deepdive` callout box & practical engineering notes |
| **V6** | **Nello Cristianini**<br>(*La scorciatoia*, *Machina Sapiens*) | Foundational epistemology of AI, statistical learning theory, computational understanding vs. semantic understanding, shortcut learning, ethical boundaries. | Chapter / Section introductory bridges & exam insights |
| **V7** | **AI Explained**<br>(Ray) | Frontier LLM analysis, compute-optimal scaling laws, benchmark nuance, reasoning models, test-time compute scaling. | Modern perspective callouts & scaling analysis |
| **V8** | **Authoritative Textbooks**<br>(Goodfellow, Bishop, Prince, Jurafsky & Martin) | Rigorous statistical lemmas, PAC learnability bounds, Jacobian derivations, classical NLP linguistics, formal notation consistency. | Inline theorems, proofs, and definitions |

---

## 1.1 Pre-Writing Ingestion & Local Material Cache Protocol

Before a single paragraph or equation of LaTeX is authored, the agent MUST ensure that all required reference materials are gathered into the active context window or organized locally under `STUDY_GUIDE/sources/`:

```
STUDY_GUIDE/sources/
├── papers/         # PDF summaries, LaTeX equations, and BibTeX entries of seminal papers
├── books/          # Local textbook chapter excerpts and rigorous proofs (Bishop, Goodfellow, Prince)
└── multimedia/     # Timestamped notes and transcripts from Karpathy, 3B1B, Enkk, Antirez, Cristianini, Ray
```

### The Non-Negotiable Integration Invariant:
**The Professor Flow is the Golden Anchor, but External Triangulation is Mandatory.**
Even if the slides or the professor do NOT explicitly cite a paper, book, or video:
- If a slide covers **Transformers**, the agent MUST integrate Vaswani et al. (2017) *Attention Is All You Need* (multi-head projection, scaled dot-product attention, sinusoidal/rotary encodings) and 3Blue1Brown's attention geometry.
- If a slide covers **Tokenization**, the agent MUST integrate Sennrich et al. (2016) BPE, Radford et al. (2019) Byte-Level BPE, and Enkk's breakdown of arithmetic fragmentation and multilingual token fertility.
- If a slide covers **Sampling & Decoding**, the agent MUST integrate Karpathy's temperature sampling equations and Antirez's minimalist inference perspectives.
- If a slide covers **Scaling Laws**, the agent MUST integrate Kaplan et al. (2020), Chinchilla (Hoffmann et al., 2022), and AI Explained's compute-frontier analysis.
- If a slide covers **Fine-Tuning**, the agent MUST integrate LoRA (Hu et al., 2021) and QLoRA (Dettmers et al., 2023).

---

## 2. Topic-to-Authority Mapping & Query Templates

When assigned a specific course topic, execute targeted search queries using the structured templates below:

### Module 1: Language Modeling Foundations & N-grams
- **Seminal Literature**:
  - Claude Shannon (1948): *A Mathematical Theory of Communication* (Entropy, N-gram character approximations).
  - Jelinek & Mercer (1980): *Interpolated Estimation of Markov Source Parameters*.
  - Katz (1987): *Estimation of Probabilities from Sparse Data for the Language Model Component of a Speech Recognizer*.
  - Kneser & Ney (1995): *Improved Backing-Off for M-gram Language Modeling*.
  - Chen & Goodman (1996/1999): *An Empirical Study of Smoothing Techniques for Language Modeling*.
- **Karpathy Breakdown**:
  - *makemore Part 1: Building a bigram language model from scratch* (PyTorch 2D count matrices, `torch.multinomial`, negative log-likelihood loss, zero-count smoothing).
- **3Blue1Brown Perspective**:
  - Information theory, entropy, Shannon information measure $I(w) = -\log_2 P(w)$, cross-entropy as average surprise.
- **Search Query Templates**:
  - `site:arxiv.org "language model" "perplexity" "n-gram"`
  - `site:youtube.com "Andrej Karpathy" "makemore" "bigram"`
  - `"Kneser-Ney" smoothing derivation absolute discounting continuation probability`
  - `"Perplexity" "cross-entropy" language model evaluation proof`

### Module 2: Deep Learning Foundations & Optimization Landscapes
- **Seminal Literature**:
  - Rumelhart, Hinton, & Williams (1986): *Learning representations by back-propagating errors*.
  - Cybenko (1989) / Hornik (1991): *Approximation Capabilities of Multilayer Feedforward Networks* (Universal Approximation Theorem).
  - Glorot & Bengio (2010): *Understanding the difficulty of training deep feedforward neural networks* (Xavier initialization).
  - Kingma & Ba (2014): *Adam: A Method for Stochastic Optimization* (First/second moment tracking, bias correction).
  - He et al. (2015): *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification* (Kaiming initialization, ReLU/PReLU).
  - Hendrycks & Gimpel (2016): *Gaussian Error Linear Units (GELUs)*.
- **Karpathy Breakdown**:
  - *micrograd: Building micrograd (scalar-valued autograd engine)*; *makemore Part 2: MLP, activations, dead neurons, batch normalization*.
- **3Blue1Brown Perspective**:
  - *Essence of Neural Networks* (Gradient descent as ball rolling down high-dimensional valley, backpropagation chain rule calculus, weight space geometry).
- **Search Query Templates**:
  - `site:youtube.com "Andrej Karpathy" "micrograd" "backpropagation"`
  - `site:youtube.com "3blue1brown" "backpropagation" "calculus"`
  - `"Adam" optimizer "bias correction" derivation Kingma Ba`
  - `"Universal Approximation Theorem" Cybenko Hornik sigmoid compact set`

### Module 3: Word Embeddings & Vector Semantics
- **Seminal Literature**:
  - Bengio et al. (2003): *A Neural Probabilistic Language Model* (Distributed word representations).
  - Mikolov et al. (2013a): *Efficient Estimation of Word Representations in Vector Space* (CBOW and Skip-Gram).
  - Mikolov et al. (2013b): *Distributed Representations of Words and Phrases and their Compositionality* (Negative sampling, subsampling frequent words).
  - Pennington, Socher, & Manning (2014): *GloVe: Global Vectors for Word Representation* (Log-bilinear matrix factorization).
  - Bojanowski et al. (2017): *Enriching Word Vectors with Subword Information* (FastText, character n-grams).
- **3Blue1Brown Perspective**:
  - Visualizing high-dimensional embedding spaces, linear vector arithmetic ($\vec{v}_{\text{king}} - \vec{v}_{\text{man}} + \vec{v}_{\text{woman}} \approx \vec{v}_{\text{queen}}$), cosine similarity metric spaces.
- **Karpathy Breakdown**:
  - *makemore Part 2: Bengio 2003 neural language model lookup table, embedding layer indexing, batch dimension reshaping*.
- **Search Query Templates**:
  - `"Mikolov" "negative sampling" objective derivation`
  - `site:youtube.com "3blue1brown" "word embeddings"`
  - `"Word2Vec" skip-gram hierarchical softmax vs negative sampling`
  - `"FastText" subword n-grams out-of-vocabulary solution`

### Module 4: Recurrent Neural Networks & Sequence Modeling
- **Seminal Literature**:
  - Elman (1990): *Finding Structure in Time* (Simple Recurrent Networks).
  - Hochreiter & Schmidhuber (1997): *Long Short-Term Memory* (Constant error carousel, additive gradient highways).
  - Cho et al. (2014): *Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation* (GRU, reset/update gates).
  - Sutskever, Vinyals, & Le (2014): *Sequence to Sequence Learning with Neural Networks* (Encoder-decoder bottleneck, reversing input sequences).
  - Bahdanau, Cho, & Bengio (2014): *Neural Machine Translation by Jointly Learning to Align and Translate* (Additive attention mechanism).
  - Pascanu, Mikolov, & Bengio (2013): *On the difficulty of training Recurrent Neural Networks* (BPTT vanishing/exploding gradient eigenvalues).
- **Karpathy Breakdown**:
  - *The Unreasonable Effectiveness of Recurrent Neural Networks* (char-rnn PyTorch architecture, temperature sampling, hidden state dynamics).
- **Search Query Templates**:
  - `site:youtube.com "Andrej Karpathy" "recurrent neural networks"`
  - `"Pascanu" "vanishing gradients" Jacobian eigenvalue decomposition BPTT`
  - `"Hochreiter" "LSTM" constant error carousel derivation`
  - `"Bahdanau" additive attention alignment model equations`

### Module 5: Transformers & Modern LLM Architecture
- **Seminal Literature**:
  - Vaswani et al. (2017): *Attention Is All You Need* (Multi-Head Self-Attention, sinusoidal positional encodings).
  - Devlin et al. (2018): *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*.
  - Radford et al. (2019): *Language Models are Unsupervised Multitask Learners* (GPT-2, causal decoder-only transformer).
  - Kaplan et al. (2020): *Scaling Laws for Neural Language Models* (Compute, dataset size, parameter count power laws).
  - Hoffmann et al. (2022): *Training Compute-Optimal Large Language Models* (Chinchilla scaling laws, token-to-parameter ratio $20:1$).
  - Dao et al. (2022): *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness* (SRAM vs HBM tiling).
- **Karpathy Breakdown**:
  - *Let's build GPT: from scratch, in code, spelled out* (nanoGPT video, causal self-attention matrix masking, multi-head parallelization, residual connections, layer normalization).
- **3Blue1Brown Perspective**:
  - *Visualizing Attention and Transformers* (Attention as dot-product alignment, Query-Key matching, Value aggregation, geometric subspace projection).
- **Search Query Templates**:
  - `site:youtube.com "Andrej Karpathy" "Let's build GPT"`
  - `site:youtube.com "3blue1brown" "attention" "transformers"`
  - `site:arxiv.org "FlashAttention" Dao 2022`
  - `"Chinchilla" scaling laws compute-optimal Hoffmann 2022`

### Module 6: Parameter-Efficient Fine-Tuning (PEFT) & Alignment
- **Seminal Literature**:
  - Hu et al. (2021): *LoRA: Low-Rank Adaptation of Large Language Models* ($W + \frac{\alpha}{r} B A$).
  - Dettmers et al. (2023): *QLoRA: Efficient Finetuning of Quantized LLMs* (NF4 data type, double quantization, paged optimizers).
  - Ouyang et al. (2022): *Training language models to follow instructions with human feedback* (InstructGPT, 3-stage RLHF pipeline).
  - Rafailov et al. (2023): *Direct Preference Optimization: Your Language Model is Secretly a Reward Model* (DPO closed-form loss).
- **Enkk Breakdown**:
  - Practical open-source fine-tuning workflows, VRAM allocations for 4-bit/8-bit LoRA on consumer GPUs (RTX 3090/4090), throughput benchmarks, loss plateau debugging.
- **Search Query Templates**:
  - `site:arxiv.org "LoRA: Low-Rank Adaptation" Hu 2021`
  - `site:arxiv.org "Direct Preference Optimization" Rafailov 2023`
  - `site:youtube.com "Enkk" "LoRA" OR "fine-tuning"`
  - `"QLoRA" "NormalFloat4" NF4 information-theoretically optimal quantile`

### Module 7: LLMs for Software Engineering (LLM4SE)
- **Seminal Literature**:
  - Chen et al. (2021): *Evaluating Large Language Models Trained on Code* (OpenAI Codex, HumanEval pass@k metric).
  - Rozière et al. (2023): *Code Llama: Open Foundation Models for Code* (Infilling objective, long-context window).
  - Yao et al. (2022): *ReAct: Synergizing Reasoning and Acting in Language Models* (Thought-Action-Observation loop).
  - Yao et al. (2023): *Tree of Thoughts: Deliberate Problem Solving with Large Language Models* (BFS/DFS tree search on prompts).
  - Xia & Zhang (2022): *Less Training, More Repair: Template-based Program Repair with Pre-trained Code Models*.
- **Lex Fridman Podcast Context**:
  - Interview with Chris Lattner (LLVM, Swift, Mojo, modular compiler infrastructures for AI and code generation).
  - Interviews with Andrej Karpathy (Software 2.0/3.0, AI-assisted coding mental models).
- **Search Query Templates**:
  - `site:arxiv.org "Evaluating Large Language Models Trained on Code" Chen 2021 HumanEval`
  - `site:arxiv.org "ReAct: Synergizing Reasoning and Acting" Yao 2022`
  - `"Automated Program Repair" "Large Language Models" survey`
  - `"pass@k" unbiased estimator Chen 2021 formula derivation`

---

## 3. Synthesis Protocol

When integrating external research findings:

1. **Triangulate with Course Syllabus**:
   Never insert an external paper's thesis in isolation. Ground it directly in what Prof. Giobergia and Prof. Coppola emphasized in lecture. Use external sources to explain *why* the slide's claim is mathematically or practically true.
2. **Canonical Academic Attribution**:
   Always cite the paper formally using BibTeX keys (e.g. `\citep{mikolov2013efficient}`) and mention the authors and venue in text:
   *"In their landmark NeurIPS 2013 paper, Mikolov et al. demonstrated that..."*
3. **Dedicated Callout Packaging**:
   - Pack high-level code tricks, autograd nuances, or empirical benchmarks into a `deepdive` box:
     ```latex
     \begin{deepdive}[Mechanistic Insight: <Title>]
     \textbf{Author / Source}: Andrej Karpathy (\textit{Let's build GPT}) / Vaswani et al. (2017)
     
     <Technical synthesis with code/tensor explanation>
     \end{deepdive}
     ```
   - Pack 3Blue1Brown-style spatial intuitions into an `intuition` box:
     ```latex
     \begin{intuition}[Geometric Perspective: <Title>]
     <Spatial, high-dimensional vector visualization analogy>
     \end{intuition}
     ```
4. **Offline Fallback Guarantee**:
   If live web search is unavailable or restricted, utilize the canonical mathematical formulas, theorem proofs, and architectural details pre-indexed in this document and the master bibliography (`references.bib`). Never halt integration due to network latency.
