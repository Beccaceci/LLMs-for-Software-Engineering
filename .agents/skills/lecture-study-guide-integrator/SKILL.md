---
name: lecture-study-guide-integrator
description: >-
  Autonomously ingests lecture videos (.mp4) via zero-token local Whisper transcription,
  lecture transcripts, and slides; executes pre-ingestion external research (seminal papers,
  Karpathy, 3B1B, Enkk, Lex Fridman), performs exhaustive mathematical derivations with explicit
  tensor dimensions, deploys a tri-tier visual framework (native TikZ architectures, exact PGFPlots
  analytical curves, and Manim 3D optimization landscapes / dynamic video companions), and
  seamlessly integrates content into the LaTeX study guide across 4 flexible modes (New Chapter,
  New Section/Subsection, Deep Integration, Marginal/Callout) while enforcing zero omission.
  Use this skill whenever processing lecture video files (.mp4), lecture slides, or transcripts,
  adding new chapters or sections to the study guide, expanding mathematical formulas, adding
  TikZ/PGFPlots/Manim diagrams, or enriching lecture notes with authoritative literature and video breakdowns.
---

# Lecture Study Guide Integrator Skill

This skill governs the end-to-end ingestion, academic expansion, visual diagramming,
and LaTeX integration of lecture materials for the Master's course "Large Language Models
for Software Engineering" (Politecnico di Torino, taught by Prof. Flavio Giobergia and Prof. Riccardo Coppola).

## Core Principles

1. **Zero Omission (Non-Negotiable)**:
   Every single concept, formula, code snippet, analogy, table, and exam warning present in the professor's slides or lecture transcripts must appear in the study guide. Never condense, summarize, or omit technical details for brevity.

2. **The Professor Flow is the Golden Anchor**:
   The study guide's primary structural spine, conceptual pacing, pedagogical metaphors, and section progression MUST strictly mirror the professor's lecture sequence. We never replace the professor's flow with an arbitrary textbook index.

3. **Mandatory Autonomous External Triangulation (The Core Requirement)**:
   While strictly anchored to the professor's flow, every topic MUST be deeply enriched by triangulating with the most authoritative academic papers, textbook chapters, and top-tier educational YouTube videos—**even when the slides or the professor do not explicitly cite them**:
   - *Seminal Academic Papers*: If discussing Transformers, the agent MUST integrate Vaswani et al. (2017) *Attention Is All You Need*; if discussing tokenization, Sennrich et al. (2016) BPE and Radford et al. (2019) Byte-level BPE; if discussing scaling, Kaplan et al. (2020) and Chinchilla (2022); if fine-tuning, LoRA (Hu et al., 2021).
   - *The 7 Expert Video Authorities*:
     1. **Andrej Karpathy**: *makemore* (lookup tables as linear layers, tensor plumbing, backpropagation through attention), *nanoGPT*, *The Unreasonable Effectiveness of RNNs*.
     2. **3Blue1Brown (Grant Sanderson)**: Geometric intuition, high-dimensional projections, dot-product attention alignment, 3D phase-space trajectories, and open-source Manim code harvesting.
     3. **Enkk (Enrico Mensa)**: Tokenization mechanisms (word vs. char vs. subword), arithmetic digit blindness, multilingual token fertility disparities, unit hypersphere geometry (Cosine vs. $L_2$ distance), vector database indexing (HNSW, IVF-PQ) in RAG pipelines.
     4. **Antirez (Salvatore Sanfilippo)**: Architecture simplicity, LLM inference from scratch, token prediction mechanics, sampling algorithms (temperature, top-$k$, top-$p$), lightweight C/Python implementations without bloated frameworks.
     5. **Nello Cristianini**: AI epistemology, statistical learning theory, computational vs. semantic understanding, shortcut learning, ethical boundaries (*La scorciatoia*, *Machina Sapiens*).
     6. **AI Explained (Ray)**: Frontier LLM analysis, compute-optimal scaling laws, benchmark nuance, reasoning models, test-time compute scaling.
     7. **Course Textbooks**: Goodfellow et al. (2016), Bishop & Bishop (2024), Simon Prince (2023), Jurafsky & Martin (2024).

4. **Pre-Writing Ingestion & Local Material Cache Protocol**:
   Before authoring or expanding any section, the agent MUST have all relevant source materials (papers, book excerpts, video transcripts/breakdowns) gathered in the active context window or organized locally in `STUDY_GUIDE/sources/` (`papers/`, `books/`, `multimedia/`). Writing only commences when both the professor's notes AND the external reference materials are fully present.

5. **Unified Numbered Bibliography with Clickable Link Enumerations**:
   - Maintain **one unique, comprehensive bibliography at the end of the document** (`STUDY_GUIDE/shared/references.bib` cited at the backmatter of `main.tex`).
   - Weave literature and multimedia citations directly into the continuous academic narrative using standard numeric brackets (`\cite{...}`) rendering as clickable hyperlinked numbers (`[1]`, `[2]`).
   - Every BibTeX entry must include complete metadata and official URLs so readers can jump directly to papers (arXiv) or videos.

6. **Exhaustive Mathematical Derivations & Explicit Tensor Shapes**:
   Never skip an algebraic step. Every equation must be derived step-by-step with explicit domain and tensor shape declarations (e.g., $\mathbf{x}_t \in \mathbb{R}^{d_{\text{in}}}$, $\mathbf{X} \in \mathbb{R}^{B \times T \times d}$, $\mathbf{W}_{hh} \in \mathbb{R}^{d_h \times d_h}$).

7. **Tri-Tier Geometric & Visual Intuition (TikZ, PGFPlots & 3Blue1Brown Manim)**:
   - **Tier 1 (Native TikZ)**: Neural network schematics, computational DAGs, decision trees, timelines, and topological hyperplanes.
   - **Tier 2 (Native PGFPlots)**: Exact 2D mathematical curves, activation functions ($\sigma, \tanh, \relu, \gelu$), analytical derivatives, and empirical scaling frontiers.
   - **Tier 3 (Manim Engine — 3Blue1Brown Style)**: 3D non-convex optimization surfaces, high-dimensional manifold transformations, attention subspace routing (exported as 4K stills to `STUDY_GUIDE/figures/manim/` for LaTeX, and dynamic 5--15s micro-animations to `STUDY_GUIDE/animations/` hyperlinked via `\faVideo` badges in callouts).

8. **Strict Sentence Case Convention**:
   All chapter titles, section headings, subsection titles, definition titles, theorem titles, and captions must strictly follow **sentence case** (e.g., *"Introduction to language models"*, *"The Bayes optimal decision boundary"*).

---

## Operational Workflow

When processing lecture materials (videos, slides, or transcripts), follow this sequential automated pipeline:

```
+-----------------------------------------------------------------------------------------+
| Step 0: Zero-Token Local Audio/Video Transcription                                      |
| -> Run: python3 scripts/transcribe_lecture.py <video.mp4>                               |
| -> Local Whisper decoding on Apple Silicon MPS (0 API tokens consumed)                  |
| -> Outputs timestamped Markdown to: TRANSCRIPTIONS/LECTURES/XX-<Topic>.md               |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Step 1: Slide & Transcript Inventory Extraction                                         |
| -> Extract all text, formulas, diagrams, tables, and analogies into an audit matrix     |
|    (Slide/Timestamp, Concepts, Equations, Pedagogical Metaphors).                       |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Step 2: Pre-Writing External Ingestion & Local Source Caching                           |
| -> Read: references/01_research_protocol.md                                             |
| -> Automatically identify required Seminal Papers (even if unmentioned by professor)    |
| -> Retrieve high-signal multimedia (Karpathy, 3B1B, Enkk, Antirez, Cristianini, Ray)    |
| -> Cache materials in context or local folders (STUDY_GUIDE/sources/)                   |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Step 3: Select Integration Mode & Architecture Alignment                               |
| -> Read: references/02_integration_modes.md                                             |
| -> Mode 1: New Chapter Creation (syllabus module scaffolding)                           |
| -> Mode 2: New Section / Subsection (sub-topic insertion preserving professor flow)     |
| -> Mode 3: Deep Integration (in-place algebraic & conceptual proof enrichment)          |
| -> Mode 4: Marginal / Callout Integration (examinsight, intuition, deepdive)            |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Step 4: Mathematical Derivation & Tensor Dimension Rigor                                |
| -> Read: references/04_math_expansion.md                                                |
| -> Step-by-step algebra in display math (`align`) with explicit tensor shapes           |
| -> Formal definitions, lemmas, and physical/geometric boundary behavior                 |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Step 5: Tri-Tier Visual Asset Generation (TikZ, PGFPlots & Manim)                       |
| -> Read: references/03_tikz_guidelines.md & references/06_manim_visualization_protocol.md|
| -> 2D Architectures & Trees: Render in clean native TikZ TeX code                       |
| -> Exact 2D Math Functions: Render via PGFPlots (`\begin{axis}`)                        |
| -> 3D Manifolds & 3B1B Animations: Render via Manim (`3b1b/manim` & `3b1b/videos`)      |
|    - 4K High-DPI stills (-s -qh) to `STUDY_GUIDE/figures/manim/`                        |
|    - Dynamic video clips (-qh --format=mp4) to `STUDY_GUIDE/animations/`                |
+-----------------------------------------------------------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------------+
| Step 6: Post-Integration Audit & Automated Verification                                 |
| -> Read: references/05_zero_omission_checklist.md                                       |
| -> Run: python3 scripts/verify_coverage.py                                              |
| -> Compile: latexmk -pdf main.tex                                                       |
+-----------------------------------------------------------------------------------------+
```

---

## Detailed Sub-Documentation Index

To preserve agent context windows under progressive disclosure, operational procedures are partitioned into focused reference documents. Read each document when entering the corresponding step:

- **Zero-Token Video Transcription Protocol**: [`references/00_video_transcription_protocol.md`](references/00_video_transcription_protocol.md)
  - Audio extraction via `ffmpeg`, local Whisper execution, timestamp chunking, and `.md` storage in `LECTURE_TRANSCRIPTIONS/`.
- **External Research Protocol**: [`references/01_research_protocol.md`](references/01_research_protocol.md)
  - Concrete query structures, 5 authority vectors, BibTeX keys, and literature triangulation guidelines.
- **The 4 Integration Modes**: [`references/02_integration_modes.md`](references/02_integration_modes.md)
  - Detailed algorithms, AST/text anchoring rules, transition bridges, and container specifications.
- **Visual & Diagram Enhancement Guidelines (TikZ)**: [`references/03_tikz_guidelines.md`](references/03_tikz_guidelines.md)
  - Color palettes, modern node styling, relative coordinate placement, and 4 canonical geometric patterns.
- **Mathematical Expansion & Dimensionality Guidelines**: [`references/04_math_expansion.md`](references/04_math_expansion.md)
  - "Never Skip a Step" algebraic proof templates, tensor dimensionality contracts, and physical intuition narratives.
- **Zero-Omission Verification Checklist & Audit Protocol**: [`references/05_zero_omission_checklist.md`](references/05_zero_omission_checklist.md)
  - Slide audit matrices, 6-category quality criteria, and post-generation verification gates.
- **Manim Visualization & Dynamic Companion Protocol**: [`references/06_manim_visualization_protocol.md`](references/06_manim_visualization_protocol.md)
  - 3D non-convex loss surfaces, geometric vector subspace projections, 3Blue1Brown (`3b1b/videos`) code harvesting, 4K still exports for LaTeX, and dynamic MP4/GIF micro-animations linked in `intuition` boxes.

---

## Tool Execution Protocols

When implementing or editing study guide files with this skill:

1. **File Reading**:
   - Always `view_file` on target LaTeX files before editing to confirm current structure and line positions.
2. **File Editing**:
   - Use `replace_file_content` for precise block modifications.
   - Never replace entire chapter files with wholesale generated text when performing Mode 2, Mode 3, or Mode 4 edits.
3. **Automated Verification**:
   - Execute the coverage auditor before reporting completion:
     ```bash
     python3 .agents/skills/lecture-study-guide-integrator/scripts/verify_coverage.py \
       --slide-json <extracted_slide.json> \
       --tex-file <chapter_path.tex>
     ```
4. **Document Compilation**:
   - Verify zero fatal compilation errors:
     ```bash
     latexmk -pdf -interaction=nonstopmode main.tex
     ```
