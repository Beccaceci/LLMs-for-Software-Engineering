# Zero-Omission Verification Checklist & Audit Protocol

This protocol enforces the non-negotiable global educational standard: every concept, equation, table, code snippet, and professor's emphasis present in the course slides or transcripts must appear in the final study guide. Never summarize or omit details for brevity.

---

## 1. The Slide Inventory Matrix

For every lecture slide deck processed, construct and maintain an explicit audit matrix:

| Slide # | Slide Title / Topic | Source Concept / Formula | Target Chapter & Section | Target LaTeX Label | Verification Status |
|---|---|---|---|---|---|
| 01-02 | What is a Language Model? | Probabilistic model $P(w_1, \dots, w_m)$, plausible vs implausible sentences | Ch 1, Sec 1.1 | `sec:lm_definition` | [x] Verified |
| 01-03 | Formal Definition | Chain rule of probability $P(w_1, \dots, w_m) = \prod P(w_t \mid w_1, \dots, w_{t-1})$ | Ch 1, Sec 1.2 | `eq:prob_chain_rule` | [x] Verified |
| 01-04 | N-gram Models | Markov assumption $P(w_t \mid w_1, \dots, w_{t-1}) \approx P(w_t \mid w_{t-n+1}, \dots, w_{t-1})$ | Ch 1, Sec 1.3 | `sec:ngram_models` | [x] Verified |
| 01-05 | Cat/Mouse Transition Matrix | Frequency counting trace ("The cat chased the mouse happily") | Ch 1, Sec 1.4 | `tab:cat_mouse_counts` | [x] Verified |
| 01-11 | Generating from N-grams | Greedy sampling vs multinomial sampling, end-of-sequence token | Ch 1, Sec 1.5 | `sec:ngram_generation` | [x] Verified |
| 01-16 | Limitations of N-grams | Sparsity $V^n$, exponential context growth, lack of semantic similarity | Ch 1, Sec 1.6 | `sec:ngram_pathology` | [x] Verified |
| 01-22 | Evaluation Metrics | Perplexity $PPL = 2^{H(P, Q)}$ and Cross-Entropy derivation | Ch 1, Sec 1.7 | `eq:ppl_derivation` | [x] Verified |

---

## 2. Systematic 6-Category Audit Checklist

Before marking any chapter or section complete, systematically verify all six categories:

### A. Conceptual Completeness
- [ ] Every slide headline is represented by a dedicated section, subsection, or explicit narrative heading.
- [ ] Every bullet point on every slide is thoroughly unpacked and explained with academic depth (never summarized as a single sentence).
- [ ] Every conversational remark, intuition, or historical anecdote shared by Prof. Giobergia or Prof. Coppola in lecture is woven into the narrative or an `intuition` callout box.

### B. Mathematical Completeness
- [ ] Every formula appearing on any slide is reproduced in display math mode (`align`, `equation`).
- [ ] All intermediate algebraic derivation steps omitted on the slides are fully unrolled and annotated.
- [ ] Every scalar, vector, matrix, and tensor has explicit Euclidean space and dimensional annotations ($\mathbb{R}^{d_{\text{in}}}$, $\mathbb{R}^{B \times T \times d_{\text{model}}}$).
- [ ] Operational intuitions, architectural rationales, and boundary condition behaviors ($\tau \to 0$, $\tau \to \infty$) are articulated.

### C. Code & Algorithmic Completeness
- [ ] Every code snippet or algorithmic workflow on the slides is reproduced in syntax-highlighted Python/PyTorch code using the `lstlisting` environment.
- [ ] Code listings include line-by-line comments detailing tensor shape mutations (e.g., `# [B, T, d] -> [B, h, T, d_k]`).
- [ ] Implementation subtleties (e.g. PyTorch `F.cross_entropy` combining `LogSoftmax` and `NLLLoss`) are highlighted.

### D. Tables & Comparisons Completeness
- [ ] Every comparison table on the slides is reproduced using publication-quality LaTeX `booktabs` (`\toprule`, `\midrule`, `\bottomrule`).
- [ ] Computational and memory complexities (Big-O time and space) are formally contrasted across models.

### E. Exam Insights & Traps
- [ ] Common exam traps, tricky multiple-choice questions, and recurrent derivation pitfalls are captured inside `examinsight` callout boxes.
- [ ] Past exam questions discussed in class are transcribed and accompanied by complete analytical solutions.

### F. External Triangulation
- [ ] Seminal academic papers are cited formally (`\citep{...}`) and synthesized with author and year in text.
- [ ] High-signal insights from Andrej Karpathy (code autograd/nanoGPT), 3Blue1Brown (geometric intuition), and Enkk (practical engineering) are embedded in dedicated `deepdive` and `intuition` boxes.

---

## 3. Automated Pre-Submission Verification Gate

Prior to reporting any milestone or chapter as complete, execute the automated verification suite:

1. **Slide Concept Coverage Verification**:
   ```bash
   python3 .agents/skills/lecture-study-guide-integrator/scripts/verify_coverage.py \
     --slides-dir SLIDES/extracted/ \
     --chapters-dir chapters/
   ```
   *Requirement: Exit code 0, 0 unmapped slides.*

2. **LaTeX Compilation Gate**:
   ```bash
   latexmk -pdf -interaction=nonstopmode main.tex
   ```
   *Requirement: Exit code 0, 0 undefined citations, 0 undefined cross-references.*
