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
