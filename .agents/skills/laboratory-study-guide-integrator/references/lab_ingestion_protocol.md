# Laboratory Ingestion & Pedagogy Protocol

This document establishes the operational procedures for triangulating course materials, conducting external research, and drafting laboratory chapters.

---

## 1. Triangulating Lecture and Laboratory Materials

When assigned a laboratory chapter (e.g., Lab $N$):
1. **Identify the Laboratory Files**:
   - Locate `LABS/labXX/` and identify all `.ipynb` notebooks and associated scripts/images.
   - Parse the JSON AST of the notebook to extract markdown instructions, exercise prompts, code cells, and output displays.
2. **Locate Corresponding Lecture Materials**:
   - Inspect `SLIDES/` for the matching presentation deck (e.g., `02-DL-Intro.pdf` for Lab 01, `05-Transformers.pdf` for Lab 02, etc.).
   - Inspect `LECTURE_TRANSCRIPTIONS/` for professor commentary, oral exam warnings, and conceptual analogies.
3. **Map Conceptual Synergies**:
   - Cross-reference theoretical definitions from Volume I (`main.pdf`) to code implementations in Volume II (`labs.pdf`).
   - Identify where the professor introduced a theoretical formula on slides, and where the student is asked to implement it in PyTorch / Hugging Face.

---

## 2. External Authority Triangulation

For every laboratory, query foundational external sources to enrich the narrative:

### The Karpathy Vector
- **Focus**: Transparent, from-scratch Python/PyTorch implementations that strip away library magic.
- **Reference Repositories**:
  - *Micrograd*: Scalar-level autograd engine in under 100 lines (`Value` class, DAG topological sort, multivariate chain rule).
  - *makemore*: Autoregressive character-level language modeling across Bigram, MLP (Bengio 2003), WaveNet, and Transformer.
  - *nanoGPT*: Minimalist, hackable PyTorch implementation of GPT-2 and GPT-3.
- **Integration Style**: Use `\begin{deepdive}[Andrej Karpathy's perspective: ...]` boxes with reproducible code patterns.

### The 3Blue1Brown Vector
- **Focus**: Geometric intuition, linear algebra transformations, and visual calculus.
- **Key Concepts**:
  - Viewing forward inference as continuous geometric coordinate warping through high-dimensional manifolds.
  - Viewing backpropagation as sensitivity nudges ($\Delta \theta \to \Delta \Loss$).
  - Attention mechanisms as soft database lookup / information routing across orthogonal semantic subspaces.
- **Integration Style**: Use `\begin{intuition}[Geometric intuition: ...]` boxes connecting formulas to spatial concepts.

### Official API & Engineering Vectors
- **Focus**: PyTorch and Hugging Face official internals.
- **Key Concepts**:
  - Tensor memory layouts (strides, contiguous storage, in-place operations vs out-of-place).
  - PyTorch autograd engine internals (`grad_fn`, `AccumulateGrad`, computation graph lifecycle).
  - Hugging Face abstractions (`PreTrainedModel`, `PreTrainedTokenizer`, `Trainer`, `peft.LoraConfig`).

---

## 3. Macro Framing: The General LLM Pipeline

Before diving into granular code or library syntax, every laboratory must place the topic within the global Large Language Model lifecycle:

```
[ Raw Web Text / Code Repositories ]
                 │
                 ▼
[ Data Preprocessing & Cleaning (PyMuPDF, filtering) ]
                 │
                 ▼
[ Subword Tokenization (BPE, WordPiece, SentencePiece) ]
                 │
                 ▼
[ Embedding Layer (Continuous Vector Representation) ]
                 │
                 ▼
[ Deep Neural Backbone (PyTorch Tensors, Transformer Blocks, Attention) ]
                 │
                 ▼
[ Pretraining Objective (Causal Language Modeling / Cross-Entropy) ]
                 │
                 ▼
[ Parameter-Efficient Fine-Tuning (LoRA, Quantization INT8/INT4) ]
                 │
                 ▼
[ Alignment & Instruction Tuning (Chat Templates, RLHF / DPO) ]
                 │
                 ▼
[ Downstream SE Systems (RAG, Agents, Code & Test Generation) ]
```
