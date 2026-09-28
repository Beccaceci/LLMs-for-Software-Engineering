# Original User Request

## 2026-09-22T10:12:45Z

Build a comprehensive, publication-grade LaTeX study guide for the Master's course "Large Language Models for Software Engineering" at Politecnico di Torino (taught by Prof. Flavio Giobergia and Prof. Riccardo Coppola), together with a custom, highly flexible Antigravity skill that ingests lecture transcriptions and slides, autonomously retrieves external authoritative sources (seminal papers, top-tier video lectures from Andrej Karpathy, 3Blue1Brown, Enkk, Lex Fridman, etc.), deeply expands mathematical formulas, generates conceptual diagrams, and seamlessly integrates content into the study guide.

Working directory: /Users/nicolabeccaceci/Desktop/LLMs
Integrity mode: development

## Reference Materials
- Course Slides in `/Users/nicolabeccaceci/Desktop/LLMs/SLIDES`:
  - `01-Language-Models-Intro.pdf`: Probabilistic language modeling, N-grams, Markov assumptions, evaluation metrics (Perplexity, Cross-Entropy).
  - `02-DL-Intro.pdf`: Neural network foundations, perceptrons, activation functions, backpropagation, optimization landscapes.
  - `03-WordEmbeddings.pdf`: Limitations of one-hot representations, distributed representations, Word2Vec architectures (CBOW & Skip-gram), negative sampling, semantic vector spaces.
  - `04-RNN.pdf`: Recurrence mechanisms, vanishing/exploding gradients, gating mechanisms (LSTM, GRU), sequence-to-sequence pipelines.
- Politecnico di Torino / DBDMG Course Syllabus:
  - Part 1 (LLM Foundations): Introduction to LMs, Deep Learning Foundations, Word Embeddings, RNNs & Sequence Models, Transformer Architecture (Self-Attention, Multi-Head Attention, Positional Encoding), LLM History & Scaling Laws, Metrics, Tasks & Benchmarks, Instruction Tuning & Alignment (SFT, RLHF, DPO), Efficient Fine-tuning (LoRA, QLoRA, Prefix Tuning) & Inference Optimization (Quantization, KV Caching, Speculative Decoding).
  - Part 2 (LLMs for Software Engineering): AI in Software Engineering Foundations, Prompt Engineering & Prompt Chaining (Few-Shot, CoT, ToT, Self-Consistency), AI Agents & Multi-Agent Architectures (ReAct, Reflection, Multi-Agent SE Teams), Automated Test Generation & Test Repair, Requirements Engineering & Modeling, LLM-Assisted Code Refactoring & Maintainability, Evaluation Methodologies for SE Tasks, Safety, Bias & Ethical Considerations.

## Requirements

### R1. LaTeX Study Guide Architecture & Modular Framework
Design and implement a modular, extensible, publication-ready LaTeX study guide in the working directory:
- `main.tex`: Root document configuring book layout, clean modern typography, table of contents, and package inclusions (`amsmath`, `amssymb`, `mathtools`, `tcolorbox`, `hyperref`, `booktabs`, `listings`, `tikz`).
- `style/macros.sty`: Standardized mathematical notation, custom environments for definitions, theorems, and specialized callout boxes:
  - *Exam Insights*: Highlights recurrent question patterns, traps, and exam-relevant insights.
  - *Intuition & Analogy*: Visual and high-level conceptual explanations (inspired by 3Blue1Brown).
  - *External Deep Dive*: Citations and syntheses from seminal papers and authoritative multimedia.
- `chapters/`: Modular chapter hierarchy partitioned into syllabus-aligned modules across Part I (Foundations) and Part II (LLM4SE), each with intro, core sections, rigorous derivations, and practice problems.
- Standalone compilability: Ensure the document builds cleanly with standard TeX engines (`pdflatex`, `xelatex`, or `latexmk`).

### R2. Lecture Transcription Ingestion & External Research Skill
Develop an Antigravity workspace skill located at `.agents/skills/lecture-study-guide-integrator/SKILL.md`:
- **Pre-Ingestion External Research Protocol**: Before writing or integrating any transcription or slide deck, the skill must execute web and literature queries to collect:
  - Foundational and recent academic papers relevant to the topic (e.g., Attention Is All You Need, Word2Vec, LoRA, Chain-of-Thought, CoT Monitorability, ReAct).
  - High-signal educational multimedia and expert breakdowns (e.g., Andrej Karpathy, 3Blue1Brown, Enkk, Lex Fridman).
- **Flexible Multi-Mode Integration**: The skill must support 4 distinct integration targets:
  1. *New Chapter*: Complete chapter creation following the full syllabus order.
  2. *New Section / Subsection*: Targeted insertion into an existing chapter.
  3. *Deep Integration*: Enhancing and expanding existing paragraphs with new insights, proofs, or practical examples.
  4. *Marginal / Callout Integration*: Adding supplementary boxes without disrupting primary narrative flow.
- **Visual & Diagram Enhancement Guidelines**: Direct instructions to create TikZ code or generate conceptual visual diagrams whenever concepts involve geometric or architectural complexity.
- **Exhaustive Mathematical Derivations**: Mandate step-by-step expansion of every equation, explaining variable definitions, tensor dimensionality, and operational intuition.

### R3. Educational Completeness & Pedagogical Standards Enforcement
Enforce the global educational quality standards:
- **Zero Omission**: Every concept, code snippet, analogy, table, and technical detail from the professor's material must appear in the text; never condense for brevity.
- **Concept Verification**: Include an auditing checklist to verify 100% coverage against the source slides/transcriptions.
- **Smooth Narrative Flow**: Organize thorough explanations into structured sections with clear transitions rather than abbreviated bullet points.

## Verification Plan

### Automated / Programmatic Verification
- **LaTeX Compilation Check**: Verify that `main.tex` and all included chapter files compile cleanly without fatal syntax or package errors.
- **Skill Specification Validation**: Confirm that `.agents/skills/lecture-study-guide-integrator/SKILL.md` is registered, contains valid YAML frontmatter (`name`, `description`), and provides complete step-by-step instructions.
- **Syllabus Coverage Audit**: Verify that all syllabus topics from both LLM Foundations and LLM4SE have corresponding structured sections or chapters.

## Acceptance Criteria

### Project Deliverables
- [ ] Root `main.tex` and modular `chapters/` created in `/Users/nicolabeccaceci/Desktop/LLMs`.
- [ ] Preamble and `style/macros.sty` configured with mathematical environments, styling, and specialized callout boxes (`tcolorbox`).
- [ ] Antigravity skill `.agents/skills/lecture-study-guide-integrator/SKILL.md` fully specified with multi-source retrieval protocols, visual diagram rules, math expansion guides, and 4 flexible integration modes.
- [ ] Chapter files scaffolded for all core course topics across Foundations and LLM4SE modules.
- [ ] Initial chapters populated from available slides (`01-Language-Models-Intro`, `02-DL-Intro`, `03-WordEmbeddings`, `04-RNN`) demonstrating mathematical rigor, external research citations, and visual explanations.
- [ ] LaTeX project compiles cleanly to PDF.

## 2026-09-22T13:52:29Z

Build and enrich the Master's course study guide for "Large Language Models for Software Engineering" at Politecnico di Torino (taught by Prof. Flavio Giobergia and Prof. Riccardo Coppola). Comment out unpopulated chapters (05–16) in `main.tex` to focus exclusively on active lecture material (Chapters 01–04), implement one unique unified numbered bibliography at the end of the document (after the last active chapter) with standard in-text numeric citations ([1], [2]), integrate external research seamlessly into the main prose flow, and synthesize publication-grade TikZ and PGFPlots visual diagrams for neural foundations and mathematical concepts.

Working directory: /Users/nicolabeccaceci/Desktop/LLMs
Integrity mode: development

## Source Materials & Reference Storage
- Existing course slides in `/Users/nicolabeccaceci/Desktop/LLMs/SLIDES/` (`01-Language-Models-Intro.pdf`, `02-DL-Intro.pdf`, `03-WordEmbeddings.pdf`, `04-RNN.pdf`).
- Existing transcripts in `/Users/nicolabeccaceci/Desktop/LLMs/LECTURE_TRANSCRIPTIONS/` (`01-Language-Models-Intro.md`).
- **Source Material Handling**: All supplementary research papers, video transcripts, and external materials must be stored inside `STUDY_GUIDE/sources/` or `STUDY_GUIDE/references/` to preserve root directory cleanliness (`LECTURE_TRANSCRIPTIONS/`, `SLIDES/`, `STUDY_GUIDE/`).

---

## Requirements

### R1. Document Scope Configuration & Source Material Management
- In `STUDY_GUIDE/main.tex`, comment out unpopulated chapters 05 through 16 (`\subfile{chapters/part1_foundations/05_...}` through `16_...}`) so the compiled `main.pdf` focuses strictly on Chapters 01 to 04 and frontmatter.
- Create `STUDY_GUIDE/sources/` to house downloaded source papers, web summaries, and video references. Ensure the workspace root remains strictly uncluttered with only `LECTURE_TRANSCRIPTIONS`, `SLIDES`, and `STUDY_GUIDE` visible.

### R2. Unified Global Numbered Bibliography at Document End & Seamless Narrative Flow
- Maintain **one unique, comprehensive bibliography at the end of the document** (following the last active chapter, Chapter 04), listing all cited literature and multimedia sources with complete metadata (authors, title, venue/URL, year).
- Replace disruptive standalone external callout boxes with direct, coherent narrative synthesis in the main body text, linking to sources using standard numeric references (`[1]`, `[2]`, etc.) on first mention.
- Hyperlink all numeric citation markers directly to the corresponding entry in the unified end bibliography.

### R3. Chapter 01 Deepening: Markov Assumptions, Finite Horizon & Cross-Entropy
- **Markov Assumption Deep Dive**: Expand the mathematical intuition of $n$-gram Markov approximations, integrating pedagogical multimedia and authoritative literature (e.g., Shannon 1948, Jurafsky & Martin, StatQuest, 3Blue1Brown probability trees), demonstrating state-space reduction and transition probabilities with concrete step-by-step examples.
- **Finite Context Horizon Limitations**: Detail how fixed $n-1$ history induces semantic amnesia, demonstrating long-range grammatical agreement failures (e.g., subject-verb agreement across subordinate clauses) and how memory degradation scales with sentence complexity.
- **Cross-Entropy & Perplexity Formalization**: Provide an exhaustive step-by-step mathematical derivation connecting Empirical Cross-Entropy $H(P, Q)$, Kullback-Leibler divergence $D_{\text{KL}}(P \parallel Q)$, Shannon Entropy $H(P)$, and Perplexity $\text{PPL}(W) = 2^{H(W)}$, explicitly motivating why Perplexity is interpreted as the effective branching factor.

### R4. Chapter 02 Visual Architecture Diagrams & Mathematical Plots
Generate standalone, publication-grade TikZ / PGFPlots vector graphics directly in LaTeX:
1. **The Artificial Perceptron**: TikZ schematic showing inputs $x_i$, synaptic weights $w_i$, bias $b$, summation junction $\Sigma$, activation mapping $f(z)$, and output $y$, accompanied by a 2D hyperplane decision boundary diagram ($w_1 x_1 + w_2 x_2 + b = 0$).
2. **Fully Connected Linear Layers (Dense Layers)**: Detailed multi-layer bipartite/feed-forward TikZ diagram illustrating matrix projection $\vy = \mW^\top \vx + \vb$, with explicit tensor dimensions and weight indices.
3. **Activation Function Function Graphs (PGFPlots)**: Exact, beautifully rendered 2D function curves with axes, grid, and asymptotes for:
   - Logistic Sigmoid: $\sigma(z) = \frac{1}{1 + e^{-z}}$ and its derivative $\sigma'(z)$.
   - Hyperbolic Tangent: $\tanh(z)$ and its derivative.
   - Rectified Linear Unit (ReLU): $\max(0, z)$ and the dying ReLU regime.
   - Leaky ReLU: showing negative slope $\alpha = 0.01$.
   - Gaussian Error Linear Unit (GELU): smooth non-monotonic curvature $z \Phi(z)$.
   - Softmax: bar chart / vector transformation illustrating logit exponentiation and normalization onto the simplex.
4. **Task Formulations & Geometric Examples**:
   - *Binary Classification*: 2D feature space with a separating sigmoid boundary and worked example.
   - *Multi-Class Classification*: 2D feature space with 3-class Voronoi/linear partition, softmax probabilities, and worked example.
   - *Regression*: 1D feature vs target plot with fitted curve and residuals.
5. **Loss Function Profiles & Selection Criteria**:
   - Exact mathematical plots for MSE: $L(y, \hat{y}) = (y - \hat{y})^2$ (parabolic loss).
   - Exact mathematical plots for BCE: $-\log(\hat{y})$ for $y=1$ and $-\log(1 - \hat{y})$ for $y=0$, illustrating asymptotic penalty.
   - Exact mathematical plots / diagrams for Categorical Cross-Entropy (CCE).
   - In-depth theoretical justification: why MSE fails for classification (non-convex optimization, gradient saturation of sigmoid), and why Cross-Entropy is the maximum likelihood estimator under Bernoulli / Categorical likelihoods.

### R5. Chapter 02 Theoretical Foundations: Stacking Collapse & Universal Approximation
- **Linear Stacking Collapse & Activation Motivation**: Expand Section 2.3 to deeply motivate each of the three foundational reasons for activation functions (output bounding, non-linear manifold folding, gradient flow regulation) with geometric intuition.
- **Universal Approximation Theorem (UAT)**: Deep theoretical expansion referencing Cybenko (1989), Hornik (1989), and Leshno et al. (1993). Include an intuitive visual proof (step-function / bump construction: combining pairs of sigmoids to form localized box wavelets that approximate any continuous function $g \in C(I_n)$).
- **Skill Evolution**: Update `.agents/skills/lecture-study-guide-integrator/SKILL.md` to mandate unified global bibliography with numeric citations, narrative integration over isolated callout boxes, and PGFPlots/TikZ visualization standards.

---

## Verification Plan

### Automated / Programmatic Verification
- **LaTeX Compilation Check**: Compile `main.tex` with `latexmk -pdf -interaction=nonstopmode main.tex` to verify zero fatal errors, resolving all cross-references and PGFPlots compilations.
- **Bibliography Audit**: Verify that the document compiles with a single unified numbered bibliography at the end and that all numeric in-text citations `[x]` resolve correctly.
- **Diagram and Plot Verification**: Verify that perceptron, dense layers, activation graphs (Sigmoid, Tanh, ReLU, Leaky ReLU, GELU, Softmax), task examples, and loss function plots compile and render cleanly into the PDF.
- **Test Suite Execution**: Run `python3 -m pytest STUDY_GUIDE/tests/` to ensure all structural and coverage tests pass with the commented chapters and updated architecture.

---

## Acceptance Criteria

### Scope & Structure
- [ ] Unpopulated chapters (05–16) are cleanly commented out in `STUDY_GUIDE/main.tex`.
- [ ] Active document compiles cleanly with only Chapters 01–04 and frontmatter included.
- [ ] Directory cleanliness preserved: only `LECTURE_TRANSCRIPTIONS/`, `SLIDES/`, and `STUDY_GUIDE/` in root.

### Numbered Bibliography & Integrated Writing
- [ ] A single unique bibliography is placed at the end of the document after the last chapter.
- [ ] External sources are woven directly into the text narrative with numeric brackets `[x]` hyperlinked to the bibliography.

### Content Deepening & Visualizations
- [ ] Chapter 01 includes comprehensive mathematical expansions of Markov assumptions, finite context horizons, and cross-entropy/perplexity.
- [ ] Chapter 02 includes TikZ diagrams for the artificial perceptron (with 2D decision boundary) and fully connected layers.
- [ ] Chapter 02 includes exact PGFPlots/TikZ mathematical curves for Sigmoid, Tanh, ReLU, Leaky ReLU, GELU, and Softmax.
- [ ] Chapter 02 includes worked examples and diagrams for binary classification, multi-class classification, and regression.
- [ ] Chapter 02 includes mathematical plots for MSE, BCE, and CCE with rigorous comparative motivation.
- [ ] Chapter 02 includes a rigorous analysis of the Universal Approximation Theorem with seminal papers (Cybenko, Hornik) and intuitive bump-function derivation.
- [ ] `lecture-study-guide-integrator/SKILL.md` is updated to reflect unified bibliography standards, narrative integration, and visual diagram requirements.
- [ ] PDF builds cleanly to `STUDY_GUIDE/main.pdf` with zero syntax errors.
- [ ] All automated tests pass.
