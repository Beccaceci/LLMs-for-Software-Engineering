# Code Listing, Tensor Dimension, and TikZ Standards

This document establishes the typographic and visual standards for code, tensor shapes, and vector diagrams in Volume II (`labs.pdf`).

---

## 1. Code Listing Standards (`listings`)

All code blocks must use the unified `lstlisting` environment configured in `style/macros.sty`:

```latex
\begin{lstlisting}[language=Python, caption={Step-by-step description of the implementation.}, label={lst:unique_label}]
# Code with explicit comments
\end{lstlisting}
```

### Mandatory Rules for Code Listings:
1. **Unabridged Code**: Never truncate with `# ... remaining code same`. Always include the complete executable function or training loop.
2. **Explicit Tensor Dimensions**:
   In comments and text, always declare input and output tensor dimensions:
   ```python
   # x: [B, C, H, W] -> flattened: [B, 3072]
   x = x.view(x.size(0), -1)
   # x: [B, 3072] -> fc1: [B, 512]
   x = F.relu(self.fc1(x))
   ```
3. **Verified Solutions**:
   Student exercises from notebooks (`# TODO: ...`) must be fully implemented with verified, working code.
4. **Console Output Displays**:
   When an exercise produces a key numerical output, terminal print, or evaluation accuracy, provide the exact output in a formatted listing or table.

---

## 2. TikZ Computational Graph Standards

Computational graphs and neural network architectures must be drawn in native **TikZ** rather than including low-resolution raster images:

### Standard Styles:
```latex
\begin{tikzpicture}[
    scale=0.95,
    varnode/.style={circle, draw=politoNavy, fill=skyBlue!40, thick, minimum size=10mm, font=\small\bfseries},
    opnode/.style={circle, draw=deepdiveTeal, fill=deepdiveTealBg, very thick, minimum size=12mm, font=\large\bfseries},
    fwdarr/.style={-{Stealth[scale=1.0]}, thick, draw=bodyDark},
    bwdarr/.style={-{Stealth[scale=1.0]}, thick, dashed, draw=pored!80!black}
]
```

### Visual Convention:
- **Forward edges**: Solid dark arrows pointing left-to-right (`fwdarr`).
- **Backward adjoint edges**: Dashed red/crimson arrows pointing right-to-left (`bwdarr`) labeled with the symbolic partial derivative (e.g., $\frac{\partial \Loss}{\partial \theta_1}$).
- **Operations**: Displayed in circular or square operator nodes (`\times`, `+`, `-`, `\text{sq}`, `\text{ReLU}`).
