# Manim Visualization & Dynamic Companion Protocol

This reference document establishes the operational standards for leveraging **Manim** (Mathematical Animation Engine) as a specialized 3D geometric and dynamic video companion engine for the *Large Language Models for Software Engineering* study guide at Politecnico di Torino.

---

## 1. The Tri-Tier Visual Architecture

The study guide employs a three-tier visualization framework that balances native LaTeX compilation speed with publication-grade geometric intuition:

```
+---------------------------------------------------------------------------------------+
| TIER 1: Native TikZ (2D Structural & Topological Flowcharts)                           |
| -> Use for: Block architectures, DAGs, decision trees, timelines, state machines,    |
|    token dependency graphs, and neural bipartite layers.                             |
| -> Advantage: 100% native LaTeX compilation, infinite vector zoom, zero dependencies. |
+---------------------------------------------------------------------------------------+
                                           |
+---------------------------------------------------------------------------------------+
| TIER 2: Native PGFPlots (Exact 2D Mathematical Functions)                             |
| -> Use for: Analytical activation curves (Sigmoid, Tanh, ReLU, GELU), derivative      |
|    profiles, loss landscapes (MSE, BCE, CCE), and empirical scaling laws (Chinchilla).|
| -> Advantage: Exact coordinate evaluation, native axis styling, zero rasterization.   |
+---------------------------------------------------------------------------------------+
                                           |
+---------------------------------------------------------------------------------------+
| TIER 3: Manim Engine (3D Manifolds, Optimization Surfaces & Video Companions)        |
| -> Use for: 3D non-convex loss surfaces with saddle points/ravines, high-dimensional   |
|    semantic manifold folding, attention subspace geometric projections, and 5-15s   |
|    dynamic micro-animations embedded via hyperlinks in `intuition` boxes.             |
| -> Advantage: 3D camera controls, depth shading, particle flows, and video rendering. |
+---------------------------------------------------------------------------------------+
```

---

## 2. Decision Matrix: When to Select Manim

Always consult this decision matrix before generating a visual asset:

| Visual Requirement | Recommended Engine | Output Format | Integration Mechanism |
|---|---|---|---|
| **2D Model Architecture** (e.g. Bengio NPLM, Transformer, BERT vs GPT) | **TikZ** | Native TeX code | Inline `\begin{tikzpicture}` |
| **Discrete State Transitions / Trees** (e.g. Markov chains, Decision trees) | **TikZ** | Native TeX code | Inline `\begin{tikzpicture}` |
| **Historical Timelines & Roadmaps** | **TikZ** | Native TeX code | Inline `\begin{tikzpicture}` |
| **1D / 2D Analytical Functions** (e.g. $\sigma(z)$, $\tanh(z)$, $\gelu(z)$) | **PGFPlots** | Native TeX code | Inline `\begin{axis}` |
| **1D / 2D Loss Function Comparisons** (e.g. MSE vs. Cross-Entropy) | **PGFPlots** | Native TeX code | Inline `\begin{axis}` |
| **Empirical Iso-FLOP Contours** (e.g. Chinchilla loss frontier) | **PGFPlots** | Native TeX code | Inline `\begin{axis}` |
| **3D Non-Convex Optimization Surfaces** (Saddle points, ravines, SGD vs Adam) | **Manim** | High-Res PNG Still | `\includegraphics[width=...]{figures/manim/...}` |
| **High-Dimensional Manifold Folding** (Activation space bending) | **Manim** | High-Res PNG Still | `\includegraphics[width=...]{figures/manim/...}` |
| **Dynamic Vector Arithmetic Shift** ($\vec{v}_{\text{king}} - \vec{v}_{\text{man}} + \vec{v}_{\text{woman}}$) | **Manim** | 10s MP4 Companion | Hyperlink badge in `\begin{intuition}` |
| **Self-Attention Softmax Scaling Dynamics** ($Q K^T / \sqrt{d_k} \to \text{softmax}$) | **Manim** | 12s MP4 Companion | Hyperlink badge in `\begin{intuition}` |

---

## 3. Directory Layout & Workspace Integrity

To preserve workspace cleanliness, all Manim assets are organized within `STUDY_GUIDE/`:

```
STUDY_GUIDE/
├── manim/                        # Standalone Python Manim scene scripts
│   ├── scene_loss_landscape.py   # 3D optimization surface and trajectory scene
│   ├── scene_attention_geo.py    # Geometric attention subspace projection
│   └── scene_embeddings.py       # High-dimensional token clustering
├── figures/
│   └── manim/                    # Rendered 4K PNG stills for LaTeX inclusion
│       ├── scene_loss_landscape.png
│       └── scene_attention_geo.png
├── animations/                   # Rendered MP4/GIF video companion clips
│       ├── scene_loss_landscape.mp4
│       └── scene_attention_geo.mp4
└── scripts/
    └── render_manim.sh           # Automated batch rendering script
```

---

## 4. Standard Color Palette Mapping

Manim scripts must strictly follow the official Politecnico di Torino course palette defined in `style/macros.sty`:

```python
# Politecnico di Torino LLM4SE Course Palette
POLITO_NAVY      = "#002D62"   # Primary brand, axis lines, input tokens
STEEL_BLUE       = "#2364A0"   # Secondary accent, links, projections
DEEPDIVE_TEAL    = "#0F7364"   # Mathematical deep dives, shared embeddings
INTUITION_PURPLE = "#5F2D8C"   # Intuitive analogies, hidden states, attention
EXAM_AMBER       = "#B9550F"   # Warnings, high-variance paths, SGD oscillations
THM_GREEN        = "#14783C"   # Optimal trajectories (Adam), converging states
SKY_BLUE         = "#E6F0FA"   # Shading backgrounds
DARK_BG          = "#0F1117"   # Video dark background (for web viewing)
LIGHT_BG         = "#FDFDFE"   # Textbook light background (for PDF export)
```

---

## 5. Dual Production Pipelines

### Pipeline A: High-Resolution Static Still Export for LaTeX Figures

1. **Python Script Configuration**:
   Use `ThreeDScene` or `Scene`. Configure the camera angle and construct all Mobjects statically:
   ```python
   class NonConvexOptimization3D(ThreeDScene):
       def construct(self):
           self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
           # Build axes, surface, trajectories, and annotations
           ...
   ```

2. **Render Command**:
   Render exclusively the final high-definition still frame using the `-s` (save last frame) and `-qh` (high 1080p/4K quality) flags:
   ```bash
   manim -s -qh scene_loss_landscape.py NonConvexOptimization3D -o loss_surface.png
   cp .manim_cache/images/.../loss_surface.png STUDY_GUIDE/figures/manim/
   ```

3. **LaTeX Inclusion**:
   Embed the image using standard `figure` environment with sentence case caption and `fig:` label:
   ```latex
   \begin{figure}[htbp]
   \centering
   \includegraphics[width=0.88\linewidth]{figures/manim/loss_surface.png}
   \caption{Three-dimensional non-convex optimization surface illustrating saddle-point escape trajectories.}
   \label{fig:manim_loss_surface}
   \end{figure}
   ```

---

### Pipeline B: Dynamic Video Companion for Intuition Callout Boxes

1. **Python Script Configuration**:
   Add camera motion, morphing animations, and smooth transitions:
   ```python
   self.begin_ambient_camera_rotation(rate=0.15)
   self.play(Create(sgd_curve), run_time=3)
   self.play(Create(adam_curve), run_time=2)
   self.wait(2)
   ```

2. **Render Command**:
   Render the full video clip in high definition:
   ```bash
   manim -qh --format=mp4 scene_loss_landscape.py NonConvexOptimization3D -o loss_surface.mp4
   cp .manim_cache/videos/.../loss_surface.mp4 STUDY_GUIDE/animations/
   ```

3. **LaTeX Companion Badge in `intuition` Callout Box**:
   Provide a direct, hyperlinked callout inside the conceptual text:
   ```latex
   \begin{intuition}[Navigating non-convex saddle points]
   In high-dimensional parameter spaces, local minima are rare; saddle points and ravines dominate the landscape...
   \begin{center}
       \href{https://polito-llm4se.github.io/animations/loss_surface.mp4}{%
           \textcolor{steelBlue}{\faVideo\enspace \textbf{\textsf{Watch 10-second geometric animation of saddle-point optimization}}}%
       }
   \end{center}
   \end{intuition}
   ```

---

## 6. Deep Code Harvesting from 3Blue1Brown (`3b1b/videos` & `3b1b/manim`)

Grant Sanderson's open-source repositories [`3b1b/manim`](https://github.com/3b1b/manim) (the rendering engine) and [`3b1b/videos`](https://github.com/3b1b/videos) (the actual production scripts) provide the gold standard for communicating neural and mathematical intuition.

### 6.1 Core Architectural Motifs in `3b1b/videos/_2024/transformer/`
When generating visual assets for LLM architectures, inspect and replicate these specific files and classes:

1. **Embedding Geometry (`_2024/transformer/embedding.py`)**:
   - *Relational Vector Arithmetic*: Uses `Vector` and `DashedLine` with `Transform` to illustrate word offsets (e.g., $\vv_{\text{King}} - \vv_{\text{Man}} + \vv_{\text{Woman}} \approx \vv_{\text{Queen}}$) in continuous space.
   - *Unembedding Logit Projection*: Demonstrates matrix multiplication $\mW_U \ve$ mapping the final contextual state onto the vocabulary simplex.

2. **Attention Routing & Dot-Product Alignment (`_2024/transformer/attention.py`)**:
   - *Query-Key Subspace Projections*: Renders projection matrices $\mW_Q$ and $\mW_K$ mapping high-dimensional token representations into a shared low-dimensional metric space.
   - *Dot Product as Angular Alignment*: Uses animated unit circles and vector projections to show how $\vq^\top \vk$ measures semantic agreement.
   - *Softmax Temperature Scaling*: Shows how division by $\sqrt{d_k}$ prevents gradient saturation in extreme logit regimes.
   - *Value Vector Routing*: Visualizes attention weights $\alpha_{ij}$ as dynamic particle beams or opacity weights routing context features into the residual stream.

3. **The Residual Stream as a Central Highway (`_2024/transformer/mlp.py`)**:
   - Visualizes the continuous sequence of token states $[\vx_1, \dots, \vx_T]$ flowing along a multi-lane highway. Attention heads and MLP sublayers read from the stream via projections and write back into it additively: $\vx^{(l+1)} = \vx^{(l)} + \operatorname{Sublayer}(\vx^{(l)})$.

4. **Multi-Head Subspace Specialization (`_2024/transformer/multi_head.py`)**:
   - Visualizes multiple heads operating concurrently, each attending to distinct linguistic phenomena (syntactic dependencies, long-range coreference, code indentation structure).

### 6.2 Standalone Python Manim Recipe: Self-Attention Alignment Scene
Below is a turnkey template based on 3Blue1Brown patterns, tailored for the Politecnico di Torino course:

```python
from manim import *

class SelfAttentionProjection(Scene):
    def construct(self):
        # 1. Politecnico Palette
        POLITO_NAVY = "#002D62"
        STEEL_BLUE  = "#2364A0"
        INTUITION_P = "#5F2D8C"
        EXAM_AMBER  = "#B9550F"

        # 2. Text Labels
        title = Text("Self-Attention: Query-Key Alignment", font="sans-serif", weight=BOLD).scale(0.8)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # 3. Coordinate System
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1}
        )
        self.add(plane)

        # 4. Query and Key Vectors
        q_vec = Arrow(start=ORIGIN, end=[2.5, 1.5, 0], color=STEEL_BLUE, buff=0, stroke_width=5)
        k_vec = Arrow(start=ORIGIN, end=[1.8, 2.2, 0], color=INTUITION_P, buff=0, stroke_width=5)
        q_lbl = MathTex(r"\mathbf{q}_i = \mathbf{W}_Q \mathbf{x}_i", color=STEEL_BLUE).next_to(q_vec.get_end(), RIGHT)
        k_lbl = MathTex(r"\mathbf{k}_j = \mathbf{W}_K \mathbf{x}_j", color=INTUITION_P).next_to(k_vec.get_end(), UP)

        self.play(GrowArrow(q_vec), Write(q_lbl))
        self.play(GrowArrow(k_vec), Write(k_lbl))
        self.wait(1)

        # 5. Projection line (Dot product)
        proj_point = np.dot([2.5, 1.5, 0], [1.8, 2.2, 0]) / np.linalg.norm([1.8, 2.2, 0])**2 * np.array([1.8, 2.2, 0])
        proj_line = DashedLine(start=[2.5, 1.5, 0], end=proj_point, color=EXAM_AMBER, stroke_width=3)
        dot_score = MathTex(r"e_{ij} = \frac{\mathbf{q}_i^\top \mathbf{k}_j}{\sqrt{d_k}}", color=EXAM_AMBER).scale(0.85).to_corner(DR)

        self.play(Create(proj_line), Write(dot_score))
        self.wait(2)
```

### 6.3 Automated Rendering Protocol
To render Manim scenes for the study guide:
1. **High-Resolution Static Still (for LaTeX `\includegraphics`)**:
   ```bash
   manim -s -qh scene_attention.py SelfAttentionProjection -o attention_projection.png
   cp .manim_cache/images/.../attention_projection.png STUDY_GUIDE/figures/manim/
   ```
2. **Dynamic Micro-Animation (for Web/Digital Companion `\faVideo`)**:
   ```bash
   manim -qh --format=mp4 scene_attention.py SelfAttentionProjection -o attention_projection.mp4
   cp .manim_cache/videos/.../attention_projection.mp4 STUDY_GUIDE/animations/
   ```

