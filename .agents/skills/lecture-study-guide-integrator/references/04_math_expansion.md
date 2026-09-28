# Mathematical Expansion & Dimensionality Guidelines

This document establishes the mandatory standards for all mathematical derivations, equations, and tensor specifications in the study guide.

---

## 1. The "Never Skip a Step" Invariant

Lecture slides frequently state only the starting loss function and the final gradient, leaving students to guess the algebraic intermediate steps. In this study guide, skipping intermediate derivation steps is strictly forbidden.

### Derivation Protocol
1. **State the Initial Premise**:
   State the exact loss function, probability distribution, or objective function in display math.
2. **Show Every Intermediate Algebraic Manipulation**:
   - Applying logarithmic transformations.
   - Splitting summations or products.
   - Expanding vector and matrix products.
   - Applying calculus rules (chain rule, product rule, quotient rule, Leibniz integral rule).
   - Substituting analytical identities (e.g., $\sigma'(z) = \sigma(z)(1 - \sigma(z))$, $\frac{\partial}{\partial z_j}\text{softmax}(\mathbf{z})_i = S_i(\delta_{ij} - S_j)$).
   - Collecting like terms and factoring out common scalar or vector terms.
3. **Annotate Every Line**:
   Use `\intertext{...}` or trailing `\quad \text{(...)}` to explicitly state the mathematical principle applied between consecutive lines.

---

## 2. Canonical Worked Derivation Examples

### Example A: Cross-Entropy Loss with Softmax Output Layer

```latex
\begin{align}
\mathcal{L}_{\text{CE}} &= - \sum_{k=1}^{|\mathcal{V}|} y_k \log \hat{y}_k \label{eq:ce_loss} \\
\intertext{where $\hat{y}_k = \operatorname{softmax}(\mathbf{z})_k = \frac{e^{z_k}}{\sum_{j=1}^{|\mathcal{V}|} e^{z_j}}$, and $\mathbf{y}$ is a one-hot ground-truth target vector ($y_c = 1$ for true class $c$, and $y_k = 0$ for $k \neq c$). To compute the gradient with respect to logit $z_i$, we apply the multivariable chain rule:}
\frac{\partial \mathcal{L}_{\text{CE}}}{\partial z_i} &= - \sum_{k=1}^{|\mathcal{V}|} \frac{y_k}{\hat{y}_k} \frac{\partial \hat{y}_k}{\partial z_i} \label{eq:ce_chain} \\
\intertext{We differentiate the softmax function with respect to logit $z_i$ by considering two cases. When $k = i$:}
\frac{\partial \hat{y}_i}{\partial z_i} &= \frac{\partial}{\partial z_i} \left( \frac{e^{z_i}}{\sum_{j} e^{z_j}} \right) = \frac{e^{z_i}\sum_{j} e^{z_j} - e^{z_i}e^{z_i}}{\left( \sum_{j} e^{z_j} \right)^2} = \hat{y}_i(1 - \hat{y}_i) \label{eq:sm_case1} \\
\intertext{When $k \neq i$:}
\frac{\partial \hat{y}_k}{\partial z_i} &= \frac{\partial}{\partial z_i} \left( \frac{e^{z_k}}{\sum_{j} e^{z_j}} \right) = \frac{0 \cdot \sum_{j} e^{z_j} - e^{z_k}e^{z_i}}{\left( \sum_{j} e^{z_j} \right)^2} = -\hat{y}_k \hat{y}_i \label{eq:sm_case2} \\
\intertext{Combining Equations (\ref{eq:sm_case1}) and (\ref{eq:sm_case2}) using the Kronecker delta $\delta_{ki}$ yields $\frac{\partial \hat{y}_k}{\partial z_i} = \hat{y}_k (\delta_{ki} - \hat{y}_i)$. Substituting this identity back into Equation (\ref{eq:ce_chain}):}
\frac{\partial \mathcal{L}_{\text{CE}}}{\partial z_i} &= - \sum_{k=1}^{|\mathcal{V}|} \frac{y_k}{\hat{y}_k} \left[ \hat{y}_k (\delta_{ki} - \hat{y}_i) \right] \notag \\
&= - \sum_{k=1}^{|\mathcal{V}|} y_k (\delta_{ki} - \hat{y}_i) \notag \\
&= - y_i + \hat{y}_i \sum_{k=1}^{|\mathcal{V}|} y_k \label{eq:ce_sub} \\
\intertext{Since $\mathbf{y}$ is a probability distribution summing to unity ($\sum_{k=1}^{|\mathcal{V}|} y_k = 1$), Equation (\ref{eq:ce_sub}) collapses to the remarkably elegant residual error formulation:}
\frac{\partial \mathcal{L}_{\text{CE}}}{\partial z_i} &= \hat{y}_i - y_i \label{eq:ce_final}
\end{align}
```

### Example B: Word2Vec Skip-Gram with Negative Sampling (SGNS)

```latex
\begin{align}
\mathcal{L}_{\text{NEG}} &= \log \sigma(\mathbf{v}_{w_O}'^\top \mathbf{v}_{w_I}) + \sum_{i=1}^K \mathbb{E}_{w_i \sim P_n(w)} \left[ \log \sigma(-\mathbf{v}_{w_i}'^\top \mathbf{v}_{w_I}) \right] \label{eq:sgns_objective} \\
\intertext{We differentiate with respect to the input center word vector $\mathbf{v}_{w_I}$ using the identity $\frac{d}{dz}\log \sigma(z) = 1 - \sigma(z)$ for the positive context term:}
\frac{\partial}{\partial \mathbf{v}_{w_I}} \log \sigma(\mathbf{v}_{w_O}'^\top \mathbf{v}_{w_I}) 
&= \left[ 1 - \sigma(\mathbf{v}_{w_O}'^\top \mathbf{v}_{w_I}) \right] \mathbf{v}_{w_O}' \label{eq:sgns_pos_grad} \\
\intertext{For each negative sample $w_i$, utilizing the identity $\frac{d}{dz}\log \sigma(-z) = -\sigma(z)$:}
\frac{\partial}{\partial \mathbf{v}_{w_I}} \log \sigma(-\mathbf{v}_{w_i}'^\top \mathbf{v}_{w_I})
&= -\sigma(\mathbf{v}_{w_i}'^\top \mathbf{v}_{w_I}) \mathbf{v}_{w_i}' \label{eq:sgns_neg_grad} \\
\intertext{Summing Equations (\ref{eq:sgns_pos_grad}) and (\ref{eq:sgns_neg_grad}) produces the complete analytical gradient:}
\frac{\partial \mathcal{L}_{\text{NEG}}}{\partial \mathbf{v}_{w_I}} 
&= \left[ 1 - \sigma(\mathbf{v}_{w_O}'^\top \mathbf{v}_{w_I}) \right] \mathbf{v}_{w_O}' - \sum_{i=1}^K \sigma(\mathbf{v}_{w_i}'^\top \mathbf{v}_{w_I}) \mathbf{v}_{w_i}' \label{eq:sgns_full_grad}
\end{align}
```

### Example C: Backpropagation Through Time (BPTT) Jacobian Product

```latex
\begin{align}
\frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_t} &= \frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_T} \frac{\partial \mathbf{h}_T}{\partial \mathbf{h}_t} = \frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_T} \prod_{k=t+1}^T \frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}} \label{eq:bptt_chain} \\
\intertext{For a standard recurrent cell $\mathbf{h}_k = \tanh(W_{hh}\mathbf{h}_{k-1} + W_{xh}\mathbf{x}_k + \mathbf{b}_h)$, the single-step temporal Jacobian is:}
\mathbf{J}_k &= \frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}} = \operatorname{diag}\left( 1 - \mathbf{h}_k^2 \right) W_{hh}^\top \label{eq:bptt_jacobian} \\
\intertext{Consequently, the compounding temporal sensitivity matrix over $T - t$ steps evaluates to:}
\frac{\partial \mathbf{h}_T}{\partial \mathbf{h}_t} &= \prod_{k=t+1}^T \operatorname{diag}\left( 1 - \mathbf{h}_k^2 \right) W_{hh}^\top \label{eq:bptt_compounded}
\end{align}
```

---

## 3. Mandatory Tensor Dimensionality Tracking

Every introduced mathematical symbol representing a scalar, vector, matrix, or multi-dimensional tensor MUST be explicitly declared in its Euclidean space:

### Space Declaration Rules
1. **Never write**: "Let $W$ be weights and $x$ be input."
2. **Always write**: "Let $\mathbf{x}_t \in \mathbb{R}^{d_{\text{in}}}$ denote the input token embedding at time step $t$, $W_{xh} \in \mathbb{R}^{d_h \times d_{\text{in}}}$ denote the input projection matrix, $W_{hh} \in \mathbb{R}^{d_h \times d_h}$ denote the recurrent hidden transition matrix, and $\mathbf{b}_h \in \mathbb{R}^{d_h}$ denote the bias vector."

### Underbrace Annotations
Annotate key structural equations with underbraced dimensions:

```latex
\begin{equation}
\underbrace{\mathbf{h}_t}_{[d_h \times 1]} = \tanh \left( 
  \underbrace{W_{xh}}_{[d_h \times d_{\text{in}}]} \underbrace{\mathbf{x}_t}_{[d_{\text{in}} \times 1]} + 
  \underbrace{W_{hh}}_{[d_h \times d_h]} \underbrace{\mathbf{h}_{t-1}}_{[d_h \times 1]} + 
  \underbrace{\mathbf{b}_h}_{[d_h \times 1]} 
\right)
\end{equation}
```

### Transformer Batched Dimensions Reference

| Tensor Symbol | Name / Role | Mathematical Shape |
|---|---|---|
| $X$ | Input Token Batch | $\mathbb{R}^{B \times T \times d_{\text{model}}}$ |
| $W_Q, W_K, W_V$ | Projection Weights | $\mathbb{R}^{d_{\text{model}} \times d_{\text{model}}}$ |
| $Q, K, V$ | Multi-Head Reshaped Tensors | $\mathbb{R}^{B \times h \times T \times d_k}$ (where $d_k = d_{\text{model}} / h$) |
| $S = \frac{QK^\top}{\sqrt{d_k}}$ | Scaled Attention Logits | $\mathbb{R}^{B \times h \times T \times T}$ |
| $M$ | Causal Lower-Triangular Mask | $\mathbb{R}^{T \times T}$ ($M_{ij} = 0$ for $i \ge j$; $-\infty$ otherwise) |
| $A = \operatorname{softmax}(S + M)$ | Attention Probabilities | $\mathbb{R}^{B \times h \times T \times T}$ |
| $O = A V$ | Multi-Head Contextual Output | $\mathbb{R}^{B \times h \times T \times d_k}$ |
| $W_O$ | Output Linear Projection | $\mathbb{R}^{d_{\text{model}} \times d_{\text{model}}}$ |

---

## 4. Operational & Physical Intuition

Every derived mathematical equation must be paired with an operational narrative answering three fundamental questions:

1. **Geometric/Physical Meaning**:
   What does this transformation physically do to the vector geometry?
   *(e.g., "The dot product $\mathbf{q}_i^\top \mathbf{k}_j$ measures the collinear alignment between the query's information demand and the key's content offering in their shared latent subspace.")*
2. **Architectural Rationale**:
   Why this specific functional form instead of a naive alternative?
   *(e.g., "We scale by $1/\sqrt{d_k}$ because for independent zero-mean unit-variance components, the variance of the dot product grows linearly with dimension $d_k$. For large dimensions ($d_k = 64$ or $128$), the variance reaches $64$, pushing the softmax function into saturating regions with near-zero gradients.")*
3. **Boundary Condition Behavior**:
   What happens at extreme limits?
   *(e.g., "Under temperature scaling $\operatorname{softmax}(\mathbf{z}/\tau)$, as $\tau \to 0^+$, the distribution collapses to a one-hot argmax vector. As $\tau \to \infty$, the distribution smoothly converges to a uniform distribution $\mathcal{U}(1/|\mathcal{V}|)$ with maximal Shannon entropy.")*
