# The 4 Flexible Integration Modes

This guide specifies the operational workflows for integrating new lecture materials, transcripts, or external research into the Politecnico di Torino "Large Language Models for Software Engineering" LaTeX study guide.

---

## Decision Flowchart

When new lecture material arrives, determine the target integration mode using the following decision tree:

```
                          [Incoming Material]
                                   |
         +-------------------------+-------------------------+
         |                                                   |
[Full Lecture / Topic Module?]                     [Subtopic / Addendum / Note?]
         |                                                   |
     (YES) -> MODE 1: New Chapter                            |
                                                             v
                                            +----------------+----------------+
                                            |                                 |
                                   [New Structural Heading?]         [Inline Enrichment?]
                                            |                                 |
                                        (YES) -> MODE 2:                  (YES) -> MODE 3:
                                                 New Section                       Deep Integration
                                                                              |
                                                                           (NO: Warning/Analogy/Citation?)
                                                                              |
                                                                              v
                                                                          MODE 4:
                                                                          Callout Box
```

---

## Mode 1: New Chapter Creation

### Trigger Condition
- Material represents an entire syllabus module or dedicated slide deck (e.g., Language Models Intro, Deep Learning Foundations, Word Embeddings, RNNs, Transformers, Alignment, LLM4SE) that does not yet exist as a standalone chapter file.

### Required File Hierarchy & Layout
- Target location:
  - Part 1 (Foundations): `chapters/part1_foundations/chXX_<slug>.tex` (or `XX_<slug>.tex` matching project convention)
  - Part 2 (LLM4SE): `chapters/part2_llm4se/chXX_<slug>.tex`
- Registered in: `main.tex` via `\subfile{...}` or `\include{...}`.
- Preamble contract:
  ```latex
  \documentclass[../../main.tex]{subfiles}
  \begin{document}
  ...
  \end{document}
  ```

### Standard Chapter Scaffolding Blueprint
Every newly created chapter must follow this standardized pedagogical structure:

```latex
\documentclass[../../main.tex]{subfiles}

\begin{document}

\chapter{<Chapter Title>}
\label{ch:<chapter_label>}

\begin{tcolorbox}[title=Chapter Overview \& Core Objectives, colback=blue!5!white, colframe=blue!75!black, fonttitle=\bfseries]
This chapter covers the foundational theory, mathematical derivations, architectural implementations, and practical trade-offs for \textbf{<Topic Name>}, as taught in the Master's course \textit{Large Language Models for Software Engineering} at Politecnico di Torino by Prof. Flavio Giobergia and Prof. Riccardo Coppola.

\begin{itemize}
    \item \textbf{Core Concepts}: <Bullet list of primary concepts>.
    \item \textbf{Mathematical Formulations}: <Key equations derived step-by-step>.
    \item \textbf{Architectural Mechanics}: <TikZ visualizations and tensor dimensions>.
    \item \textbf{Software Engineering Applications}: <Relevance to SE benchmarks, code generation, and repair>.
\end{itemize}
\end{tcolorbox}

\section{Historical Context \& Theoretical Motivation}
\label{sec:<slug>_motivation}
% Detailed conceptual motivation, limitations of predecessor architectures.

\section{Exhaustive Mathematical Formulation}
\label{sec:<slug>_mathematics}
% Unrolled derivations, step-by-step algebra, tensor dimensions.

\begin{intuition}[Geometric Perspective: <Intuition Title>]
% 3Blue1Brown-style intuitive explanation of the high-dimensional geometric transformation.
\end{intuition}

\section{Algorithmic Architectures \& Mechanics}
\label{sec:<slug>_architecture}
% Detailed component breakdown with native TikZ figure float.

\begin{figure}[htbp]
\centering
\begin{tikzpicture}
    % Native TikZ diagram
\end{tikzpicture}
\caption{Detailed architectural pipeline for <Topic>.}
\label{fig:<slug>_arch}
\end{figure}

\begin{deepdive}[Mechanistic Analysis: <Deep Dive Title>]
\textbf{Authority}: <Seminal Paper / Karpathy / Enkk Reference>
% Synthesized technical insights from literature or code walkthroughs.
\end{deepdive}

\section{Implementation Nuances \& PyTorch Mechanics}
\label{sec:<slug>_implementation}
% Syntax-highlighted code snippets using lstlisting with tensor shape comments.

\section{Exam Insights, Traps \& Pitfalls}
\label{sec:<slug>_exam_insights}

\begin{examinsight}[Exam Traps and Pitfalls: <Topic>]
% Recurrent exam questions, derivation traps, grading rubrics from professors.
\end{examinsight}

\section{Summary \& Practice Problems}
\label{sec:<slug>_summary}
% Comparative booktabs table, recap, and practice problems with full analytical solutions.

\end{document}
```

---

## Mode 2: New Section / Subsection Insertion

### Trigger Condition
- Material introduces a substantial sub-topic that belongs inside an existing chapter but represents a distinct thematic break requiring a dedicated `\section` or `\subsection` heading (e.g., adding "Negative Sampling and Noise Contrastive Estimation" into Chapter 3: Word Embeddings).

### Execution Protocol
1. **Locate Target Chapter**:
   View the target file using `view_file` to determine its current section outline and semantic flow.
2. **Anchor Identification**:
   Identify the preceding logical concept mathematically rather than relying on volatile line numbers (e.g., insert immediately after "Full Softmax Bottleneck" and before "GloVe").
3. **Draft Structural Insertion**:
   Include a retrospective bridge connecting to the previous section, the complete conceptual and mathematical breakdown, and a prospective bridge into the following section:
   ```latex
   \section{Negative Sampling and Noise Contrastive Estimation}
   \label{sec:negative_sampling}
   
   Having established the computational intractability of evaluating the full vocabulary denominator in Equation~(\ref{eq:softmax_vocab}), we now examine the negative sampling formulation introduced by Mikolov et al.~\citep{mikolov2013distributed}...
   
   % Exhaustive math and intuition
   
   With the negative sampling approximation established, we turn our attention to global co-occurrence matrix factorization methods...
   ```
4. **Compile & Verify**:
   Run `latexmk -pdf main.tex` to confirm table-of-contents alignment and label resolution.

---

## Mode 3: Deep Integration (In-Place Enrichment)

### Trigger Condition
- Material clarifies, deepens, or expands an existing paragraph, equation, or proof without introducing a new structural heading (e.g., expanding a 1-line cross-entropy loss into a full multi-step derivative, or adding explicit tensor dimensions to an RNN recurrence equation).

### Execution Protocol
1. **Target Identification**:
   Read the exact lines surrounding the target equation or narrative in the `.tex` file.
2. **In-Place Transformation**:
   - Convert single-line equations into multi-line `align` environments displaying every intermediate algebraic step.
   - Insert tensor dimensionalities under each matrix/vector multiplication using `\underbrace{...}_{[d \times 1]}`.
   - Weave in the operational intuition explaining *why* the mathematical operation produces the desired physical effect.
3. **Strict Non-Destructive Invariant**:
   Never delete existing technical information or invalidate existing `\label{...}` targets. Deep integration is strictly additive and enriching.
4. **Verify**:
   Run `git diff` or compare content to ensure all prior content and citations remain intact.

---

## Mode 4: Marginal / Callout Integration

### Trigger Condition
- Material contains an exam trap, past exam question, student misconception, geometric analogy, or seminal paper citation that enriches the text but would interrupt the linear narrative flow if placed directly in the main body.

### Environment Selection Matrix

| Content Type | LaTeX Environment | Visual Styling / Purpose |
|---|---|---|
| Exam traps, past exam questions, grading criteria, recurrent question patterns | `\begin{examinsight}[<Title>] ... \end{examinsight}` | Amber/Crimson accent. Highlights trick questions emphasized by Prof. Giobergia and Prof. Coppola. |
| 3Blue1Brown geometric metaphors, visual intuitions, mental models | `\begin{intuition}[<Title>] ... \end{intuition}` | Purple/Teal accent. Provides high-dimensional vector space visualizations and physical analogies. |
| Seminal paper citations, Karpathy code walkthroughs, Enkk benchmarks | `\begin{deepdive}[<Title>] ... \end{deepdive}` | Dark Teal/Indigo accent. Technical syntheses from literature and code mechanics. |
| Formal mathematical definitions | `\begin{definition}{<Title>}{<label>} ... \end{definition}` | Navy numbered box with formal conditions. |
| Core theorems and analytical proofs | `\begin{theorem}{<Title>}{<label>} ... \end{theorem}` | Green numbered box with rigorous proof. |

### Execution Protocol
1. Place the callout box immediately following the paragraph containing the anchor concept.
2. Ensure the callout is **self-contained**: a student reading only the box should grasp the full takeaway without needing adjacent sentences.
3. Keep the content focused, rigorous, and visually separated from the core derivation.
