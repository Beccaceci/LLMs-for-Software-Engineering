# Project: Politecnico di Torino "Large Language Models for Software Engineering" Study Guide & Antigravity Skill

## Architecture
- **Document Root**: `main.tex` (One-sided A4 layout, Palatino `newpxtext` + `newpxmath`, `sourcecodepro`, `microtype`, `subfiles` modularity).
- **Styling & Macros**: `style/macros.sty` (Standardized mathematical operators, `tcolorbox` definition & theorem boxes, and three distinct callout boxes: `examinsight`, `intuition`, `deepdive`).
- **Bibliography Database**: `references.bib` (12+ seminal papers referenced in course material; compiled via `bibtex` with `natbib` or `backend=bibtex`).
- **Build Automation**: `Makefile` and `.latexmkrc` (`latexmk -pdf` standalone and whole-book compilation).
- **Modular Directory Organization**:
  - `chapters/part1_foundations/`: 8 core foundation chapters (Decks 01-04 fully implemented with zero omission, Decks 05-08 scaffolded).
  - `chapters/part2_llm4se/`: 8 core software engineering application chapters (scaffolded with detailed learning outcomes and reading lists).
- **Antigravity Custom Skill**: `.agents/skills/lecture-study-guide-integrator/`
  - `SKILL.md`: Root progressive-disclosure skill definition with YAML frontmatter.
  - `references/`: Modular execution guides for research protocol, 4 integration modes, TikZ visual guidelines, math expansion, zero-omission checklist.
  - `scripts/verify_coverage.py`: Automated verification script for slide-to-LaTeX concept coverage.

---

## Feature Inventory
Every feature identified during the Survey phase is mapped to an implementation milestone. No feature is unassigned.

| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | TeX Book Layout & Typography | `main.tex`, Palatino fonts, 25mm margins, `book` class, `subfiles` setup | M1 | Survey (LaTeX Explorer) |
| 2 | Macro & Math Foundation | `style/macros.sty`, standard notation ($\mathbb{E}, \operatorname{softmax}, \mathcal{L}$), theorems | M1 | Survey (LaTeX Explorer) |
| 3 | Specialized Callout Boxes | `examinsight` (amber), `intuition` (purple), `deepdive` (teal) `tcolorbox` | M1 | Survey (LaTeX Explorer) |
| 4 | Build Engine & Automation | `Makefile`, `.latexmkrc` configured for clean `latexmk -pdf` with `bibtex` | M1 | Survey (LaTeX Explorer) |
| 5 | Master Bibliography | `references.bib` containing Shannon, Bengio, Mikolov, Hochreiter, Cho, etc. | M1 | Survey (LaTeX Explorer & Slide Miner) |
| 6 | Directory & Chapter Scaffolding | Complete `chapters/part1_foundations/` & `chapters/part2_llm4se/` structure | M1 | Survey (LaTeX Explorer) |
| 7 | Antigravity Skill Frontmatter | `SKILL.md` with valid YAML frontmatter (`name`, `description`) | M2 | Survey (Skill Spec Miner) |
| 8 | Pre-Ingestion Research Protocol | `references/01_research_protocol.md` (ArXiv, Karpathy, 3B1B, Enkk, Fridman) | M2 | Survey (Skill Spec Miner) |
| 9 | 4-Mode Integration Workflows | `references/02_integration_modes.md` (New Chapter, New Section, Deep, Callout) | M2 | Survey (Skill Spec Miner) |
| 10 | TikZ Diagram Guidelines | `references/03_tikz_guidelines.md` (Color palette, positioning, neural layouts) | M2 | Survey (Skill Spec Miner) |
| 11 | Math Derivation Guidelines | `references/04_math_expansion.md` (Step-by-step algebra, tensor dimensions) | M2 | Survey (Skill Spec Miner) |
| 12 | Zero-Omission Audit Matrix | `references/05_zero_omission_checklist.md` (6-point criteria, chapter template) | M2 | Survey (Skill Spec Miner) |
| 13 | Coverage Verification Script | `scripts/verify_coverage.py` (Slide concept to LaTeX text auditor) | M2 | Survey (Skill Spec Miner) |
| 14 | Deck 01: Language Models Intro | Probabilistic LMs, joint probability chain rule, Markov assumptions | M3 | Survey (Slide Miner: Deck 01) |
| 15 | Deck 01: N-gram Counting & Trace | Cat/Mouse transition matrix, bigram conditional probs, generation trace | M3 | Survey (Slide Miner: Deck 01) |
| 16 | Deck 01: N-gram Pathologies & History | Sparsity $V^n$, context loss, lack of semantics; Shannon $\to$ Bengio $\to$ GPT | M3 | Survey (Slide Miner: Deck 01) |
| 17 | Deck 01: Evaluation Metrics | Perplexity and Cross-Entropy derivation ($PPL = 2^{H(P, Q)}$) | M3 | Survey (Slide Miner: Deck 01) |
| 18 | Deck 02: Perceptron & Activations | Biological neuron, linear regression, ReLU, Sigmoid, Tanh, GeLU, Softmax | M3 | Survey (Slide Miner: Deck 02) |
| 19 | Deck 02: Multi-Layer Perceptron | Linear layer stacking collapse ($W'^T x$), Universal Approximation Theorem | M3 | Survey (Slide Miner: Deck 02) |
| 20 | Deck 02: Loss & Gradient Descent | MSE, BCE, CCE, optimization landscapes, momentum, Adam update rules | M3 | Survey (Slide Miner: Deck 02) |
| 21 | Deck 02: Backprop Computational DAG | Adjoint trace, chain rule, forward/backward equations ($\hat{y} = \theta_1 \theta_2 x$) | M3 | Survey (Slide Miner: Deck 02) |
| 22 | Deck 03: One-Hot Limits & Embeddings | Sparsity, curse of dimensionality, orthogonal distance ($\sqrt{2}$), dense vs sparse | M3 | Survey (Slide Miner: Deck 03) |
| 23 | Deck 03: Word2Vec CBOW & Skip-Gram | Objective functions, input/output matrices ($W_{\text{in}}, W_{\text{out}}$), softmax | M3 | Survey (Slide Miner: Deck 03) |
| 24 | Deck 03: Softmax Scaling & Negative Sampling | Hierarchical Softmax $O(\log V)$, Negative Sampling binary logistic loss | M3 | Survey (Slide Miner: Deck 03) |
| 25 | Deck 03: FastText & Vector Arithmetic | Subword n-grams, OOV solving, cosine similarity, vector arithmetic | M3 | Survey (Slide Miner: Deck 03) |
| 26 | Deck 04: Sequential Data & RNN Limits | FCNN failure modes on sequences, recurrent cell equations, weight sharing | M3 | Survey (Slide Miner: Deck 04) |
| 27 | Deck 04: BPTT & Gradient Pathology | BPTT unrolling, Jacobian product $\prod W_{hh}^T$, vanishing/exploding gradients | M3 | Survey (Slide Miner: Deck 04) |
| 28 | Deck 04: Gating Mechanisms (LSTM & GRU) | Forget, Input, Output gates, cell state highway, GRU reset/update gates | M3 | Survey (Slide Miner: Deck 04) |
| 29 | Deck 04: Sequence-to-Sequence Models | Encoder-Decoder architecture, context vector bottleneck, teacher forcing | M3 | Survey (Slide Miner: Deck 04) |
| 30 | Syllabus Scaffolding (Chapters 05-16) | Scaffolded outline, learning objectives, and reading lists for full syllabus | M3 | Survey (LaTeX Explorer & Syllabus) |
| 31 | Full LaTeX Compilation & PDF Output | Programmatic build verification with `pdflatex` / `latexmk`, 0 fatal errors | M4 | Survey & Verification Plan |
| 32 | E2E Requirement & Skill Verification | Antigravity skill syntax, YAML, test tiers 1-4 validation | M4 | Survey & Verification Plan |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | LaTeX Framework & Architecture | `main.tex`, `style/macros.sty`, `references.bib`, `.latexmkrc`, `Makefile`, and chapter directory skeleton | none | PLANNED |
| M2 | Antigravity Skill Implementation | `.agents/skills/lecture-study-guide-integrator/` (`SKILL.md`, `references/01-05`, `scripts/verify_coverage.py`) | none | PLANNED |
| M3 | Chapter Content Authoring & Scaffolding | Chapters 01-04 fully implemented with mathematical derivations, TikZ diagrams, external deep dives, exam insights; Chapters 05-16 scaffolded | M1 | PLANNED |
| M4 | E2E Testing, Compilation & Verification | Opaque-box E2E testing suite, full PDF compilation, zero-omission verification, and adversarial hardening | M1, M2, M3 | PLANNED |

---

## Interface Contracts

### M1 (LaTeX Framework) ↔ M3 (Chapter Content)
- **Document Inclusion**: Chapters must use `\documentclass[../../main.tex]{subfiles}` at the top, followed by `\begin{document} ... \end{document}`.
- **Environment Names**:
  - `\begin{examinsight}[<Title>] ... \end{examinsight}` (Amber left-bar box)
  - `\begin{intuition}[<Title>] ... \end{intuition}` (Purple left-bar box)
  - `\begin{deepdive}[<Title>] ... \end{deepdive}` (Teal left-bar box)
  - `\begin{definition}{<Title>}{<label>} ... \end{definition}` (Navy numbered box)
  - `\begin{theorem}{<Title>}{<label>} ... \end{theorem}` (Green numbered box)
- **Math Macros**: `\E`, `\softmax`, `\sigmoid`, `\relu`, `\gelu`, `\L`, `\transpose`, `\R`, `\vx`, `\vh`, `\vy`, `\mW`.
- **Bibliography**: All citations must use `\citep{...}` or `\citet{...}` pointing to keys in `references.bib`.

### M2 (Antigravity Skill) ↔ Study Guide Project
- **Skill Location**: `.agents/skills/lecture-study-guide-integrator/SKILL.md`.
- **Reference Document References**: All relative links in `SKILL.md` must resolve to files under `.agents/skills/lecture-study-guide-integrator/references/`.
- **Validation Script**: `scripts/verify_coverage.py` must take `--slides-dir` and `--chapters-dir` arguments and return exit code 0 when all concepts are present.

---

## Code Layout
```
/Users/nicolabeccaceci/Desktop/LLMs/
├── main.tex
├── Makefile
├── .latexmkrc
├── references.bib
├── style/
│   └── macros.sty
├── frontmatter/
│   ├── titlepage.tex
│   ├── preface.tex
│   └── notation.tex
├── chapters/
│   ├── part1_foundations/
│   │   ├── 01_language_models_intro.tex
│   │   ├── 02_deep_learning_foundations.tex
│   │   ├── 03_recurrent_neural_networks.tex
│   │   ├── 04_word_embeddings.tex
│   │   ├── 05_transformer_architecture.tex
│   │   ├── 06_scaling_laws_pretraining.tex
│   │   ├── 07_instruction_tuning_alignment.tex
│   │   └── 08_peft_inference_optimization.tex
│   └── part2_llm4se/
│       ├── 09_ai_in_software_engineering.tex
│       ├── 10_prompt_engineering_chaining.tex
│       ├── 11_ai_agents_multiagent.tex
│       ├── 12_automated_test_generation_repair.tex
│       ├── 13_requirements_engineering_modeling.tex
│       ├── 14_code_refactoring_maintainability.tex
│       ├── 15_evaluation_metrics_benchmarks_se.tex
│       └── 16_safety_bias_ethics_ip.tex
├── scripts/
│   └── compile.sh
└── .agents/
    └── skills/
        └── lecture-study-guide-integrator/
            ├── SKILL.md
            ├── references/
            │   ├── 01_research_protocol.md
            │   ├── 02_integration_modes.md
            │   ├── 03_tikz_guidelines.md
            │   ├── 04_math_expansion.md
            │   └── 05_zero_omission_checklist.md
            └── scripts/
                └── verify_coverage.py
```
