---
name: laboratory-study-guide-integrator
description: >-
  Autonomously ingests laboratory notebook files (.ipynb), locates corresponding lecture slides
  and transcripts, executes external research (Andrej Karpathy video walkthroughs and codebases,
  3Blue1Brown visual intuition, PyTorch and Hugging Face official internals, seminal papers),
  preserves unabridged code snippets and complete verified solutions (Zero Omission), renders
  publication-grade TikZ diagrams and PGFPlots, and authors comprehensive laboratory chapters
  for Volume II: Laboratory Practicum (labs.pdf). Use this skill whenever converting or expanding
  lab notebooks into the study guide practicum.
---

# Laboratory Study Guide Integrator Skill

This skill governs the end-to-end ingestion, academic contextualization, code solution completion, and LaTeX authoring of laboratory assignments for the course "Large Language Models for Software Engineering" (Politecnico di Torino).

Volume II (`labs.pdf`) serves as a comprehensive, standalone **Hands-on Laboratory Practicum** that bridges high-level deep learning theory with production-grade engineering code.

---

## Core Principles

1. **Macro-to-Micro Pedagogical Scaffolding**:
   Never dive blindly into PyTorch syntax or library calls. Every laboratory chapter must open with the **overarching macro picture**:
   - Why does this lab exist in an LLM course?
   - Where do these operations fit into the broader LLM lifecycle (Data $\to$ Tokenization $\to$ Pretraining $\to$ Fine-Tuning / PEFT $\to$ Alignment $\to$ RAG / Agents $\to$ Evaluation)?
2. **Authority Triangulation & External Deep Dives**:
   Linearly weave high-signal insights from world-class AI educators and seminal papers:
   - **Andrej Karpathy Vector**: Reference *Micrograd* (autograd mechanics), *makemore* (language modeling from bigrams to MLP), *nanoGPT* (clean GPT-2/3 from scratch), and YouTube walkthroughs. Include Karpathy's clean code patterns and explanations.
   - **3Blue1Brown Vector**: Visual and geometric calculus intuition (e.g., viewing backpropagation as sensitivity nudges rippling backward through a computational DAG).
   - **Engineering Vector**: PyTorch C++ internals, CUDA/MPS memory management, Tensor Contiguity and strides, Hugging Face `transformers` abstractions (`AutoTokenizer`, `Trainer`, `DataCollator`).
3. **Zero Omission of Code, Solutions, and Outputs**:
   - Every single code block, helper function, dataset preparation step, and model definition from the notebook must appear in the chapter using `\begin{lstlisting}[language=Python]`.
   - All student exercises (`# TODO: ...`, ellipses `...`) must be replaced with **fully verified, production-grade solutions**.
   - Annotate code with step-by-step commentary, explicit tensor shapes (e.g., `[B, C, H, W] \to [B, 3072]`), and expected console outputs.
4. **Publication-Grade Vector Diagrams (TikZ & PGFPlots)**:
   - Replace raster screenshots and low-resolution `.png` files with native **TikZ** computational graphs, neural network architectures, and workflow pipelines.
   - Use **PGFPlots** to plot loss convergence curves, activation functions, and weight/bias trajectories using clean vector coordinates.
   - Strictly follow the course palette (`politoNavy`, `steelBlue`, `deepdiveTeal`, `intuitionPurple`, `examAmber`, `thmGreen`).
5. **Seamless Cross-Volume Linking (`xr-hyper`)**:
   - Reference foundational theorems and definitions from Volume I (`main.pdf`) using `\ref{th:eq:...}` or `\ref{th:sec:...}`.
   - Ensure the chapter compiles cleanly both as a standalone subfile (`\subfile{...}`) and within `labs.tex`.

---

## 6-Stage Laboratory Ingestion Pipeline

```
+-----------------------------------------------------------------------------+
| Stage 1: Input Triangulation                                                |
| -> Target lab notebook: LABS/labXX/*.ipynb                                  |
| -> Corresponding lecture slides: SLIDES/XX-*.pdf                            |
| -> Lecture transcripts: LECTURE_TRANSCRIPTIONS/XX-*.md                      |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| Stage 2: Code & Exercise Inventory Extraction                               |
| -> Parse all markdown headers, instructions, and theoretical explanations.  |
| -> Extract every code cell, import, model class, and training loop.         |
| -> Audit all TODOs and ellipses (...) and synthesize verified solutions.    |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| Stage 3: External Research & Authority Deep Dives                           |
| -> Search Karpathy repositories (Micrograd, nanoGPT, makemore).             |
| -> Extract 3Blue1Brown geometric / sensitivity perspectives.                |
| -> Check PyTorch/Hugging Face official documentation for internal mechanics.|
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| Stage 4: High-Level Macro Framework Drafting                                |
| -> Establish the general LLM pipeline context for the lab topic.            |
| -> Define why the student needs these specific primitives.                  |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| Stage 5: Chapter Authoring (Zero Omission & TikZ Generation)                |
| -> Write complete LaTeX subfile in STUDY_GUIDE/laboratories/chapters/       |
| -> Convert raster diagrams into publication-grade TikZ DAGs and flows.      |
| -> Insert full code listings with annotated line numbers and solutions.     |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| Stage 6: Compilation & Verification Gate                                     |
| -> Compile subfile: cd STUDY_GUIDE/laboratories/chapters && latexmk -pdf ...|
| -> Compile Volume II: cd STUDY_GUIDE/laboratories && latexmk -pdf labs.tex  |
| -> Verify 0 fatal errors and inspect visual rendering.                      |
+-----------------------------------------------------------------------------+
```

---

## Standard Chapter Architecture for Laboratories

Each laboratory chapter in `STUDY_GUIDE/laboratories/chapters/` follows this unified structure:

1. **Chapter Title & Learning Outcomes**:
   - `\chapter{Laboratory XX: [Topic in Sentence Case]}`
   - `\section{Laboratory overview and industrial context}`: High-level LLM pipeline role, prerequisites, learning outcomes checklist.
2. **Foundational Theory & Conceptual Intuition**:
   - The theoretical underpinnings (mathematical formulas, tensor shapes, gradient dynamics).
   - `\begin{intuition}[3Blue1Brown geometric view: ...]`
   - `\begin{deepdive}[Andrej Karpathy's code walkthrough: ...]`
3. **Step-by-Step Practical Walkthrough (Zero Omission)**:
   - Part-by-part breakdown matching the notebook flow.
   - Clear distinction between base framework code and completed exercise solutions.
   - Code listings formatted with syntax highlighting (`lstlisting`) and line numbers.
   - Annotated tensor dimensions before and after each critical transformation.
4. **Architectural & Vector Visualizations (TikZ)**:
   - Vector-rendered computational graphs with forward execution paths and backward adjoint gradient flows.
5. **Experimental Results & Trajectory Plots (PGFPlots)**:
   - Quantitative convergence curves, accuracy tables, and parameter tracking.
6. **Software Engineering Takeaways & Bridge to Next Lab**:
   - Summary of practical lessons, common pitfalls, debugging tips, and direct conceptual bridge to the next laboratory session.
