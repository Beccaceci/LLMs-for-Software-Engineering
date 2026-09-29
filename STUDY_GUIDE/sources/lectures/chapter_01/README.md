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
- [Deep Learning](https://www.deeplearningbook.org/) (Ian Goodfellow, Yoshua Bengio, Aaron Courville — MIT Press, 2016)
  - **Chapter 10 (Section 10.1)**: Sequence Modeling: Discrete Sequence Modeling & N-gram Limits
  - **Why it matters**: Bridges statistical language modeling with neural architectures, proving why tabular $n$-grams scale exponentially ($\mathcal{O}(|V|^n)$) with context length.
  - **What it covers**: Tabular probability lookup tables, exponential parameter explosion, statistical statistical sparsity, and the necessity of distributed continuous representations.
- [Dive into Deep Learning (D2L.ai)](https://d2l.ai/) (Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola)
  - **Chapter 9 (Section 9.3)**: Language Models and the Dataset
  - **Why it matters**: Pairs statistical language model principles with concrete PyTorch dataset loading, token counting, and perplexity calculation routines.
  - **What it covers**: Word frequency distributions (Zipf's law), unigram/bigram/trigram count generation, and empirical perplexity evaluation.

## 2. Intuitive Masterclasses & Visual Walkthroughs
- Andrej Karpathy: ["Neural Networks: Zero to Hero — makemore Part 1: Bigram Language Models" (2022)](https://karpathy.github.io/)
  - **Why it matters**: Demonstrates the bridge between discrete statistical count matrices and neural parameter optimization.
  - **Key insights**: Visualizes a 27x27 2D bigram frequency table in PyTorch, extracts probability distributions via `torch.multinomial`, formalizes the Negative Log-Likelihood (NLL) loss, and contrasts matrix counts directly with a single-layer linear network trained via gradient descent.
  - **Companion code**: [`makemore` repository](https://github.com/karpathy/makemore) (`makemore.py`, ~200 LOC in pure PyTorch).
- 3Blue1Brown (Grant Sanderson): ["Information Theory and Entropy" (2020)](https://www.3blue1brown.com/)
  - **Why it matters**: Geometric and probabilistic intuition for Shannon information, entropy, and cross-entropy.
  - **Key insights**: Visualizes self-information as "surprise" ($I(w) = -\log_2 P(w)$), entropy as average surprise, and cross-entropy as the expected code length when using an imperfect model distribution.
- StatQuest with Josh Starmer: ["Cross-Entropy and Maximum Likelihood" (2021)](https://statquest.org/)
  - **Why it matters**: Step-by-step arithmetic breakdown of cross-entropy loss, clarifying the connection between likelihood maximization and entropy minimization.
  - **Key insights**: Details step-by-step log-likelihood computation, shows why minimizing negative log-likelihood is mathematically identical to minimizing cross-entropy under empirical data distributions, and demonstrates behavior under high-confidence misclassifications.

## 3. Landmark Seminal Papers (Primary Ground Truth)
- **Foundations of Information Theory**:
  - Shannon, C. E. (1948): [A Mathematical Theory of Communication](https://ieeexplore.ieee.org/document/6773024) — Formulates information entropy, discrete Markov chains, and statistical language modeling:
    - Information Entropy: $H(X) = -\sum_{x \in \mathcal{X}} P(x) \log_2 P(x)$
    - Joint Entropy & Chain Rule: $H(X, Y) = H(X) + H(Y \mid X)$ where $H(Y \mid X) = -\sum_{x, y} P(x, y) \log_2 P(y \mid x)$
    - Cross-Entropy: $H(P, Q) = -\sum_{x \in \mathcal{X}} P(x) \log_2 Q(x) = H(P) + D_{\text{KL}}(P \parallel Q)$
    - Relative Entropy (KL Divergence): $D_{\text{KL}}(P \parallel Q) = \sum_{x \in \mathcal{X}} P(x) \log_2 \frac{P(x)}{Q(x)}$
    - Perplexity Branching Factor: $\text{PPL}(W) = 2^{H(W)} = P(w_1, \dots, w_N)^{-1/N} = \exp\left(-\frac{1}{N} \sum_{i=1}^N \ln P(w_i \mid w_{1}^{i-1})\right)$
- **Statistical Smoothing & Sparse Data Estimation**:
  - Good, I. J. (1953): [The population frequencies of species and the estimation of population parameters](https://doi.org/10.1093/biomet/40.3-4.237) — The Good-Turing frequency estimator allocating probability mass to unseen events using singletons:
    - Adjusted frequency: $r^* = (r + 1) \frac{N_{r+1}}{N_r}$ where $N_r = |\{w : c(w) = r\}|$
    - Good-Turing probability: $P_{\text{GT}}(r) = \frac{r^*}{N}$ where $N = \sum_{r=1}^\infty r N_r$
    - Total probability mass of unseen events ($r=0$): $P_{\text{GT}}(0) = \frac{N_1}{N}$
  - Katz, S. M. (1987): [Estimation of Probabilities from Sparse Data for the Language Model Component of a Speech Recognizer](https://ieeexplore.ieee.org/document/1165341) — Formalized the Katz Back-off model using Turing's discounting formula:
    - Backoff formulation:
      $$P_{\text{bo}}(w_i \mid w_{i-n+1}^{i-1}) = \begin{cases} d_{c(w_{i-n+1}^i)} \frac{c(w_{i-n+1}^i)}{c(w_{i-n+1}^{i-1})} & \text{if } c(w_{i-n+1}^i) > 0 \\ \alpha(w_{i-n+1}^{i-1}) P_{\text{bo}}(w_i \mid w_{i-n+2}^{i-1}) & \text{if } c(w_{i-n+1}^i) = 0 \end{cases}$$
    - Normalization backoff weight: $\alpha(w_{i-n+1}^{i-1}) = \frac{1 - \sum_{w: c(w_{i-n+1}^{i-1}, w) > 0} P_{\text{bo}}(w \mid w_{i-n+1}^{i-1})}{1 - \sum_{w: c(w_{i-n+1}^{i-1}, w) > 0} P_{\text{bo}}(w \mid w_{i-n+2}^{i-1})}$
  - Kneser, R., & Ney, H. (1995): [Improved Backing-Off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) — Introduced Kneser-Ney smoothing based on continuation probabilities and absolute discounting:
    - Interpolated Kneser-Ney distribution:
      $$P_{\text{KN}}(w_i \mid w_{i-1}) = \frac{\max(c(w_{i-1}, w_i) - d, 0)}{c(w_{i-1})} + \lambda(w_{i-1}) P_{\text{cont}}(w_i)$$
    - Continuation probability: $P_{\text{cont}}(w_i) = \frac{|\{w' : c(w', w_i) > 0\}|}{\sum_{w} |\{w' : c(w', w) > 0\}|}$
    - Interpolation weight: $\lambda(w_{i-1}) = \frac{d}{c(w_{i-1})} |\{w : c(w_{i-1}, w) > 0\}|$ where $d \in (0, 1)$ is the absolute discount
  - Chen, S. F., & Goodman, J. (1996/1999): [An Empirical Study of Smoothing Techniques for Language Modeling](https://doi.org/10.1006/csla.1999.0128) — The definitive empirical benchmark proving Modified Kneser-Ney as the optimal statistical $n$-gram smoother with count-dependent discounts $d_1, d_2, d_{3+}$.
- **The Neural Transition**:
  - Bengio, Y., et al. (2003): [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html) — Replaces sparse $n$-gram lookup tables with continuous distributed word vector projections and MLPs:
    - Logit scoring: $\mathbf{y} = \mathbf{b} + \mathbf{W} \mathbf{x} + \mathbf{U} \tanh(\mathbf{d} + \mathbf{H} \mathbf{x})$
    - Distributed context: $\mathbf{x} = [\mathbf{C}(w_{t-1})^\top, \mathbf{C}(w_{t-2})^\top, \dots, \mathbf{C}(w_{t-n+1})^\top]^\top \in \mathbb{R}^{(n-1)d}$
    - Autoregressive conditional probability: $P(w_t = i \mid w_{t-n+1}^{t-1}) = \frac{\exp(y_i)}{\sum_j \exp(y_j)}$

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
- **Empirical Lecture Experiments**:
  - **Cat/Mouse Transition Frequency Matrix & Generative Loop**: Slides 5–16 introduce the toy corpus: *"The cat chased the mouse happily"*, *"The mouse ate the cheese"*. Constructs a 7x7 bigram transition frequency matrix with row normalization to conditional probabilities ($P(\text{mouse} \mid \text{chased}) = 1.0$, $P(\text{mouse} \mid \text{ate}) = 1.0$). Walks through the greedy/multinomial generative sampling loop starting from *"The"*, producing the cyclic degenerated sequence *"The mouse ate the mouse"* and demonstrating how unconditioned local bigram Markov approximations suffer from rapid semantic degradation.
  - **Zero-Probability Sparsity Collapse**: Slide 17 demonstrates the evaluation failure when an unseen test bigram (e.g., $c(\text{cat}, \text{ate}) = 0$) results in $P(\text{corpus}) = 0$ and $\text{PPL} = \infty$, compelling the mathematical derivation of Laplace, Good-Turing, and Kneser-Ney smoothing.
- [`slides/01-Language-Models-Intro.pdf`](slides/01-Language-Models-Intro.pdf): Course lecture slides (symlink to `SLIDES/01-Language-Models-Intro.pdf`).
- [`transcriptions/01-Language-Models-Intro.md`](transcriptions/01-Language-Models-Intro.md): Full lecture transcription (symlink to `TRANSCRIPTIONS/LECTURES/01-Language-Models-Intro.md`).
