# Sources Dossier: Chapter 01 (Introduction to Language Models)

This directory houses all required primary and external reference materials for Chapter 01, organized prior to chapter authoring to ensure zero omission and rigorous pedagogical grounding.

## 1. Definitive Graduate Textbooks
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) (Dan Jurafsky & James H. Martin — 3rd ed. draft)
  - **Chapter 3**: N-gram Language Models
  - **Why it matters**: The definitive modern reference for classical probabilistic language modeling and evaluation.
  - **What it covers**: The Chain Rule of Probability, the Markov assumption, Maximum Likelihood Estimation (MLE), zero-probability failure, Laplace add-1 smoothing, Interpolation, Backoff, Good-Turing discounting, Kneser-Ney smoothing, and Perplexity evaluation.
- [Foundations of Statistical Natural Language Processing](https://nlp.stanford.edu/fsnlp/) (Christopher D. Manning & Hinrich Schütze — MIT Press, 1999)
  - **Chapter 6**: Statistical Inference: N-gram Models over Sparse Data
  - **Why it matters**: Rigorous mathematical treatment of sparse estimators, Zipf's law, and validation protocols in discrete statistical NLP.
  - **What it covers**: Cross-validation of smoothing hyperparameters, deleted estimation, absolute discounting, and language model perplexity bounds.

## 2. Intuitive Masterclasses & Visual Walkthroughs
- Andrej Karpathy: ["Neural Networks: Zero to Hero — makemore Part 1: Bigram Language Models" (2022)](https://karpathy.github.io/)
  - **Why it matters**: Demonstrates the bridge between discrete statistical count matrices and neural parameter optimization.
  - **Key insights**: Visualizes a 27x27 2D bigram frequency table in PyTorch, extracts probability distributions via `torch.multinomial`, formalizes the Negative Log-Likelihood (NLL) loss, and contrasts matrix counts directly with a single-layer linear network trained via gradient descent.
  - **Companion code**: [`makemore`](https://github.com/karpathy/makemore) — Minimal character-level language model library in pure PyTorch.
- 3Blue1Brown (Grant Sanderson): ["Information Theory and Entropy" (2020)](https://www.3blue1brown.com/)
  - **Why it matters**: Geometric and probabilistic intuition for Shannon information, entropy, and cross-entropy.
  - **Key insights**: Visualizes self-information as "surprise" ($I(w) = -\log_2 P(w)$), entropy as average surprise, and cross-entropy as the expected code length when using an imperfect model distribution.
- StatQuest with Josh Starmer: ["Cross-Entropy and Maximum Likelihood" (2021)](https://statquest.org/)
  - **Why it matters**: Step-by-step arithmetic breakdown of cross-entropy loss, clarifying the connection between likelihood maximization and entropy minimization.

## 3. Landmark Seminal Papers (Primary Ground Truth)
- **Foundations of Information Theory**:
  - Shannon, C. E. (1948): [A Mathematical Theory of Communication](https://ieeexplore.ieee.org/document/6773024) — Formulates information entropy $H(X) = -\sum P(x) \log_2 P(x)$, discrete Markov chains, and $n$-gram statistical approximations of the English language.
- **Statistical Smoothing & Sparse Data Estimation**:
  - Good, I. J. (1953): [The population frequencies of species and the estimation of population parameters](https://doi.org/10.1093/biomet/40.3-4.237) — The Good-Turing frequency estimator allocating probability mass to unseen events using singletons ($N_1$).
  - Katz, S. M. (1987): [Estimation of Probabilities from Sparse Data for the Language Model Component of a Speech Recognizer](https://ieeexplore.ieee.org/document/1165341) — Formalized the Katz Back-off model using Turing's discounting formula.
  - Kneser, R., & Ney, H. (1995): [Improved Backing-Off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) — Introduced Kneser-Ney smoothing based on continuation probabilities and absolute discounting.
  - Chen, S. F., & Goodman, J. (1996/1999): [An Empirical Study of Smoothing Techniques for Language Modeling](https://doi.org/10.1006/csla.1999.0128) — The definitive empirical benchmark proving Modified Kneser-Ney as the optimal statistical $n$-gram smoother.
- **The Neural Transition**:
  - Bengio, Y., et al. (2003): [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html) — Replaces sparse $n$-gram lookup tables with continuous distributed word vector projections and MLPs.

## 4. University Video Lectures
- **Stanford CS224n (Natural Language Processing with Deep Learning)**:
  - Lecture 1: Introduction and Word Vectors (Christopher Manning). Motivation of statistical vs distributed representations.
  - Lecture 6: Language Models and Recurrent Neural Networks (Christopher Manning & Abigail See). Unigram/bigram baselines, perplexity calculations, and the curse of dimensionality.
- **MIT 6.S191 (Introduction to Deep Learning)**:
  - Lecture 2: Recurrent Neural Networks & Sequence Modeling (Alexander Amini). Sequential data dependencies and autoregressive sampling.

## 5. In This Workspace
You already have detailed materials synthesized in this repository:
- [`STUDY_GUIDE/lectures/chapters/part1_foundations/01_language_models_intro.tex`](../../lectures/chapters/part1_foundations/01_language_models_intro.tex): Chapter 1 of the course study guide, containing:
  - The definition and purpose of language modeling from first principles.
  - The Chain Rule of Probability and autoregressive sequence factorization.
  - Markov assumptions and $n$-gram models with transition count matrices.
  - The zero-probability problem and smoothing techniques (Laplace, Good-Turing, Kneser-Ney).
  - Mathematical formalization of Cross-Entropy and Perplexity as effective branching factors.
  - Comprehensive historical timeline across 5 distinct eras.
- [`slides/01-Language-Models-Intro.pdf`](slides/01-Language-Models-Intro.pdf): Course lecture slides (symlink to `SLIDES/01-Language-Models-Intro.pdf`).
- [`transcriptions/01-Language-Models-Intro.md`](transcriptions/01-Language-Models-Intro.md): Full lecture transcription (symlink to `TRANSCRIPTIONS/LECTURES/01-Language-Models-Intro.md`).
