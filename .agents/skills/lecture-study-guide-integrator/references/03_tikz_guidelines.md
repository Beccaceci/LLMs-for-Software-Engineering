# Visual & Diagram Enhancement Guidelines (TikZ)

All architectural and geometric diagrams in the study guide must be rendered natively in TikZ. This ensures publication-quality vector rendering, seamless font matching with the Palatino text, infinite scalability without raster pixelation, and zero external image asset dependencies.

---

## 1. Global TikZ Configuration & Style Standards

### Required Libraries
Every diagram must compile cleanly under standard LaTeX engines (`pdflatex`, `xelatex`) using the TikZ packages and libraries configured in `main.tex`:

```latex
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc, shapes.geometric, backgrounds, decorations.pathreplacing, matrix, fit}
```

### Semantic Color Palette
Use the standard semantic colors defined in `style/macros.sty`:

| Color Name | LaTeX Definition | Semantic Purpose |
|---|---|---|
| `poblue` | `blue!75!black` | Inputs, forward activations, embeddings, Query vectors |
| `pogreen` | `green!60!black` | Key vectors, hidden memory states, cell states, recurrent latents |
| `porange` | `orange!90!black` | Value vectors, attention weights, gating signals ($\mathbf{f}_t, \mathbf{i}_t, \mathbf{o}_t$) |
| `popurple` | `purple!80!black` | Output projections, predictions, logits, loss functions |
| `pored` | `red!80!black` | Backprop gradients ($\partial \mathcal{L} / \partial h_t$), negative samples, error signals |

### Node Styling Rules
- **Fill Tints**: Use light background tints (`5%` to `15%` opacity) with crisp, solid borders:
  ```latex
  \tikzset{
      neuralnode/.style={circle, draw=poblue, fill=poblue!10, thick, minimum size=8mm, inner sep=0pt, font=\small},
      statebox/.style={rectangle, rounded corners=3pt, draw=pogreen, fill=pogreen!10, thick, minimum height=10mm, minimum width=22mm, align=center, font=\small},
      gatebox/.style={circle, draw=porange, fill=porange!15, semithick, inner sep=1pt, font=\footnotesize\bfseries},
      vecarrow/.style={-{Stealth[scale=1.1]}, thick, draw=gray!70!black},
      gradarrow/.style={-{Stealth[scale=1.1]}, thick, dashed, draw=pored}
  }
  ```
- **Typography**: Labels must be `\small` or `\footnotesize`. Mathematical variables must be wrapped in math mode (e.g., `$\mathbf{h}_t$`, `$W_{xh}$`).
- **Relative Positioning**: Never use brittle absolute coordinates (`at (3.4, 2.1)`) for connected multi-node topologies. Always use relative anchors: `right=1.5cm of node1`, `above=1.0cm of node2`.
- **Figure Wrapping**: Always enclose inside a standard `figure` float with an informative caption explaining the tensor flow and dimensions:
  ```latex
  \begin{figure}[htbp]
    \centering
    \begin{tikzpicture}[node distance=1.5cm and 2.0cm]
      ...
    \end{tikzpicture}
    \caption{Informative caption describing architectural flow and tensor dimensions.}
    \label{fig:<unique_slug>}
  \end{figure}
  ```

---

## 2. The 4 Canonical Geometric & Architectural Patterns

### Pattern A: High-Dimensional Semantic Vector Space & Analogy Parallelogram

Illustrates embedding spaces, word vector arithmetic, and directional cosine angles:

```latex
\begin{tikzpicture}[scale=1.2, >=Stealth]
  % Axes
  \draw[->, thin, gray!60] (-0.5, 0) -- (6.0, 0) node[right, font=\footnotesize] {Semantic Dimension 1};
  \draw[->, thin, gray!60] (0, -0.5) -- (0, 5.0) node[above, font=\footnotesize] {Semantic Dimension 2};
  
  % Base Word Nodes
  \coordinate (man) at (1.0, 1.2);
  \coordinate (woman) at (2.2, 3.8);
  \coordinate (king) at (3.5, 1.5);
  \coordinate (queen) at (4.7, 4.1);
  
  % Plot Points
  \fill[poblue] (man) circle (2.5pt) node[below left, font=\small\bfseries] {$\mathbf{v}_{\text{man}}$};
  \fill[popurple] (woman) circle (2.5pt) node[above left, font=\small\bfseries] {$\mathbf{v}_{\text{woman}}$};
  \fill[poblue] (king) circle (2.5pt) node[below right, font=\small\bfseries] {$\mathbf{v}_{\text{king}}$};
  \fill[popurple] (queen) circle (2.5pt) node[above right, font=\small\bfseries] {$\mathbf{v}_{\text{queen}}$};
  
  % Gender Transformation Vectors (Dashed Offset)
  \draw[->, very thick, pogreen] (man) -- (woman) node[midway, left=2pt, font=\footnotesize] {$\vec{d}_{\text{gender}}$};
  \draw[->, very thick, pogreen] (king) -- (queen) node[midway, right=2pt, font=\footnotesize] {$\vec{d}_{\text{gender}}$};
  
  % Royalty Transformation Vectors
  \draw[->, thick, dashed, poblue!70] (man) -- (king) node[midway, below, font=\footnotesize] {$\vec{d}_{\text{royalty}}$};
  \draw[->, thick, dashed, popurple!70] (woman) -- (queen) node[midway, above, font=\footnotesize] {$\vec{d}_{\text{royalty}}$};
\end{tikzpicture}
```

### Pattern B: Recurrent Unrolling Across Time & BPTT Gradient Backpropagation

Illustrates unrolled hidden state transitions and backward gradient decay:

```latex
\begin{tikzpicture}[
    cell/.style={rectangle, rounded corners=4pt, draw=pogreen, fill=pogreen!10, thick, minimum width=18mm, minimum height=12mm, align=center, font=\small},
    inout/.style={circle, draw=poblue, fill=poblue!10, thick, minimum size=8mm, font=\small},
    outnode/.style={circle, draw=popurple, fill=popurple!10, thick, minimum size=8mm, font=\small},
    forwardarr/.style={-{Stealth[scale=1.1]}, thick, draw=gray!80!black},
    backarr/.style={-{Stealth[scale=1.1]}, thick, dashed, draw=pored}
  ]
  
  % Time Steps: t-1, t, t+1
  \node[cell] (ht_prev) at (0, 0) {$\mathbf{h}_{t-1}$};
  \node[cell] (ht) [right=2.2cm of ht_prev] {$\mathbf{h}_t$};
  \node[cell] (ht_next) [right=2.2cm of ht] {$\mathbf{h}_{t+1}$};
  
  % Inputs
  \node[inout] (xt_prev) [below=1.2cm of ht_prev] {$\mathbf{x}_{t-1}$};
  \node[inout] (xt) [below=1.2cm of ht] {$\mathbf{x}_t$};
  \node[inout] (xt_next) [below=1.2cm of ht_next] {$\mathbf{x}_{t+1}$};
  
  % Outputs
  \node[outnode] (yt_prev) [above=1.2cm of ht_prev] {$\hat{\mathbf{y}}_{t-1}$};
  \node[outnode] (yt) [above=1.2cm of ht] {$\hat{\mathbf{y}}_t$};
  \node[outnode] (yt_next) [above=1.2cm of ht_next] {$\hat{\mathbf{y}}_{t+1}$};
  
  % Forward Connections
  \draw[forwardarr] (xt_prev) -- (ht_prev) node[midway, right, font=\footnotesize] {$W_{xh}$};
  \draw[forwardarr] (xt) -- (ht) node[midway, right, font=\footnotesize] {$W_{xh}$};
  \draw[forwardarr] (xt_next) -- (ht_next) node[midway, right, font=\footnotesize] {$W_{xh}$};
  
  \draw[forwardarr] (ht_prev) -- (ht) node[midway, above, font=\footnotesize] {$W_{hh}$};
  \draw[forwardarr] (ht) -- (ht_next) node[midway, above, font=\footnotesize] {$W_{hh}$};
  
  \draw[forwardarr] (ht_prev) -- (yt_prev) node[midway, right, font=\footnotesize] {$W_{hy}$};
  \draw[forwardarr] (ht) -- (yt) node[midway, right, font=\footnotesize] {$W_{hy}$};
  \draw[forwardarr] (ht_next) -- (yt_next) node[midway, right, font=\footnotesize] {$W_{hy}$};
  
  % BPTT Backward Gradient Arrows
  \draw[backarr] ($(ht_next.south west)+(0, 2pt)$) -- ($(ht.south east)+(0, 2pt)$) node[midway, below, font=\footnotesize, text=pored] {$\frac{\partial \mathcal{L}}{\partial \mathbf{h}_t}$};
  \draw[backarr] ($(ht.south west)+(0, 2pt)$) -- ($(ht_prev.south east)+(0, 2pt)$) node[midway, below, font=\footnotesize, text=pored] {$W_{hh}^\top \mathbf{J}_t$};
\end{tikzpicture}
```

### Pattern C: LSTM Constant Error Carousel & Gating Highway

Illustrates the uninterrupted cell state conveyor belt with multiplicative gating:

```latex
\begin{tikzpicture}[
    box/.style={rectangle, rounded corners=3pt, draw=poblue, fill=poblue!10, thick, minimum width=12mm, minimum height=8mm, font=\small},
    op/.style={circle, draw=porange, fill=porange!20, thick, inner sep=1pt, font=\small\bfseries},
    arr/.style={-{Stealth[scale=1.1]}, thick, draw=gray!80!black}
  ]
  
  % Cell State Highway (Top)
  \node (c_prev) at (-2.5, 3.0) {$C_{t-1}$};
  \node[op] (c_mult) at (0.0, 3.0) {$\odot$};
  \node[op] (c_add) at (2.5, 3.0) {$\oplus$};
  \node (c_next) at (5.0, 3.0) {$C_t$};
  
  \draw[arr, very thick, pogreen] (c_prev) -- (c_mult);
  \draw[arr, very thick, pogreen] (c_mult) -- (c_add);
  \draw[arr, very thick, pogreen] (c_add) -- (c_next);
  
  % Hidden State Input & Input Vector (Bottom)
  \node (h_prev) at (-2.5, 0.0) {$\mathbf{h}_{t-1}$};
  \node (x_curr) at (-2.5, -1.0) {$\mathbf{x}_t$};
  
  % Gates
  \node[box] (f_gate) at (0.0, 1.2) {$\sigma (\mathbf{f}_t)$};
  \node[box] (i_gate) at (1.5, 1.2) {$\sigma (\mathbf{i}_t)$};
  \node[box] (c_cand) at (2.5, 0.4) {$\tanh (\tilde{C}_t)$};
  \node[op] (cand_mult) at (2.5, 1.8) {$\odot$};
  \node[box] (o_gate) at (3.8, 1.2) {$\sigma (\mathbf{o}_t)$};
  
  % Gate Operations
  \draw[arr] (f_gate) -- (c_mult);
  \draw[arr] (i_gate) |- (cand_mult);
  \draw[arr] (c_cand) -- (cand_mult);
  \draw[arr] (cand_mult) -- (c_add);
  
  % Output State
  \node[box] (tanh_out) at (3.8, 2.2) {$\tanh$};
  \node[op] (h_mult) at (4.5, 1.2) {$\odot$};
  \node (h_next) at (5.5, 1.2) {$\mathbf{h}_t$};
  
  \draw[arr] (c_add) -| (tanh_out);
  \draw[arr] (tanh_out) |- (h_mult);
  \draw[arr] (o_gate) -- (h_mult);
  \draw[arr, very thick, poblue] (h_mult) -- (h_next);
\end{tikzpicture}
```

### Pattern D: Scaled Dot-Product Attention & Causal Lower-Triangular Masking

Illustrates Query-Key multiplication, causal $-\infty$ masking, and Value weighted projection:

```latex
\begin{tikzpicture}[
    mat/.style={matrix of math nodes, left delimiter=[, right delimiter=], nodes={minimum width=7mm, minimum height=7mm, anchor=center, font=\small}},
    block/.style={rectangle, draw=gray!70, fill=gray!10, rounded corners=3pt, thick, align=center, font=\small, minimum height=8mm},
    arr/.style={-{Stealth[scale=1.1]}, thick, draw=gray!80!black}
  ]
  
  % Query and Key
  \node[block, draw=poblue, fill=poblue!10] (q) at (0, 3.5) {$Q \in \mathbb{R}^{T \times d_k}$};
  \node[block, draw=pogreen, fill=pogreen!10] (k) at (3, 3.5) {$K^\top \in \mathbb{R}^{d_k \times T}$};
  
  % Matmul Box
  \node[block] (matmul1) at (1.5, 2.2) {MatMul ($Q K^\top$)};
  \draw[arr] (q) -- (matmul1);
  \draw[arr] (k) -- (matmul1);
  
  % Scale
  \node[block] (scale) at (1.5, 1.0) {Scale ($\frac{1}{\sqrt{d_k}}$)};
  \draw[arr] (matmul1) -- (scale);
  
  % Mask
  \node[block, draw=porange, fill=porange!10] (mask) at (1.5, -0.2) {Causal Mask (Upper Tri $-\infty$)};
  \draw[arr] (scale) -- (mask);
  
  % Softmax
  \node[block, draw=popurple, fill=popurple!10] (sm) at (1.5, -1.4) {Softmax (Row-wise)};
  \draw[arr] (mask) -- (sm);
  
  % Value and Output
  \node[block, draw=porange, fill=porange!10] (v) at (4.5, -1.4) {$V \in \mathbb{R}^{T \times d_v}$};
  \node[block] (matmul2) at (3.0, -2.6) {MatMul ($A V$)};
  \draw[arr] (sm) -- (matmul2);
  \draw[arr] (v) -- (matmul2);
  
  \node[block, draw=popurple, fill=popurple!20, very thick] (out) at (3.0, -3.8) {Context Output $O \in \mathbb{R}^{T \times d_v}$};
  \draw[arr] (matmul2) -- (out);
\end{tikzpicture}
```

---

## 3. Standalone Verification & Troubleshooting

When embedding TikZ diagrams:
1. **Math Mode Protection**: Never write raw unescaped math underscores in node labels (e.g. write `$W_{xh}$`, not `W_xh`).
2. **Matrix Delimiters**: When using `matrix of math nodes`, verify that `\usetikzlibrary{matrix}` is loaded in `main.tex`.
3. **Bounding Boxes**: Ensure nodes do not overflow the text width ($160\text{mm}$). If a diagram is wide, use `[scale=0.9, every node/.transform shape]` or resize using `\resizebox{\textwidth}{!}{\begin{tikzpicture}...}`.
4. **Compile Test**: Always verify syntax via `latexmk -pdf main.tex`.

---

## 4. The Tri-Tier Visualization Framework & Manim Integration

While TikZ handles 2D block diagrams and architectural flowcharts natively, the study guide integrates a specialized **three-tier visualization pipeline**:

1. **Tier 1 (Native TikZ)**: 2D neural architectures, block diagrams, DAGs, decision trees, timelines, token graphs.
2. **Tier 2 (Native PGFPlots)**: 2D analytical mathematical functions, activation curves, loss function profiles, empirical scaling frontiers.
3. **Tier 3 (Manim Engine)**: 3D non-convex optimization surfaces (saddle points, ravines), high-dimensional manifold folding, attention subspace projections, and dynamic 5--15s video companions linked via `\href` in `\begin{intuition}` callout boxes.

For complete details on Manim scene creation, high-res still export (`-s -qh`), and video clip integration, consult:
- [`references/06_manim_visualization_protocol.md`](06_manim_visualization_protocol.md)

