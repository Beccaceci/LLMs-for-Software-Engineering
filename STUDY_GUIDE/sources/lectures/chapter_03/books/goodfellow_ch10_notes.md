# Ian Goodfellow, Yoshua Bengio, & Aaron Courville: "Deep Learning" — Chapter 10 Notes

Source: [Deep Learning (MIT Press, 2016)](https://www.deeplearningbook.org/), Chapter 10: *Sequence Modeling: Recurrent and Recursive Nets*.

## Key Pedagogical Principles & Technical Insights

### 1. The Parameter Sharing Principle in Sequence Modeling
- **The Core Problem**: Standard feedforward networks have fixed input dimensions and independent parameters for each input position. They cannot generalize across variable-length sequences or transfer learned statistical rules (such as morphological agreement or syntax) from one temporal position to another.
- **The Recurrent Solution**: Parameter sharing across time. A recurrent neural network processes sequential tokens $\mathbf{x}_1, \dots, \mathbf{x}_T$ by repeatedly applying the same parameter matrices ($\mathbf{W}_{xh}, \mathbf{W}_{hh}, \mathbf{W}_{hy}$) at every step:
  $$\mathbf{h}_t = f(\mathbf{h}_{t-1}, \mathbf{x}_t; \bm{\theta})$$
- **Representational Equivalence**: An RNN unfolded across $T$ time steps is a deep feedforward network with $T$ layers where all layers share identical parameters.

### 2. Backpropagation Through Time (BPTT)
- **Total Sequence Loss**: Sum of per-step losses:
  $$\mathcal{L} = \sum_{t=1}^T \mathcal{L}_t$$
- **Gradient with Respect to Recurrent Weights $\mathbf{W}_{hh}$**:
  Applying the multivariable chain rule along the unfolded computational DAG:
  $$\frac{\partial \mathcal{L}}{\partial \mathbf{W}_{hh}} = \sum_{t=1}^T \sum_{k=1}^t \frac{\partial \mathcal{L}_t}{\partial \mathbf{h}_t} \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} \frac{\partial^+ \mathbf{h}_k}{\partial \mathbf{W}_{hh}}$$
  where $\frac{\partial^+ \mathbf{h}_k}{\partial \mathbf{W}_{hh}}$ denotes the direct derivative evaluating $\mathbf{h}_{k-1}$ as constant.
- **Temporal Jacobian Chain**:
  $$\frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} = \prod_{j=k+1}^t \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}} = \prod_{j=k+1}^t \operatorname{diag}(\sigma'(\mathbf{a}_j)) \mathbf{W}_{hh}^\top$$

### 3. The Mathematics of Vanishing and Exploding Gradients
- **Eigenvalue Decomposition**: Let $\mathbf{W}_{hh} = \mathbf{Q} \bm{\Lambda} \mathbf{Q}^{-1}$ with eigenvalues $\lambda_1, \dots, \lambda_d$.
- **Temporal Power Scaling**: Over a temporal horizon $\tau = t - k$:
  $$\mathbf{W}_{hh}^\tau = \mathbf{Q} \bm{\Lambda}^\tau \mathbf{Q}^{-1}$$
- **The Two Failure Regimes**:
  1. *Vanishing Gradients ($\lambda_{\max} < 1$ or saturating activations where $\sigma' \to 0$)*:
     The product $\prod \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}}$ decays exponentially as $\mathcal{O}(\lambda_{\max}^\tau) \to 0$. Gradient signals from distant past time steps vanish, leaving the model blind to long-range context (e.g. subject-verb agreement across long subordinate clauses).
  2. *Exploding Gradients ($\lambda_{\max} > 1$)*:
     The product scales exponentially as $\mathcal{O}(\lambda_{\max}^\tau) \to \infty$, leading to floating-point overflows (`NaN`), oscillating weights, and catastrophic optimization collapse.
- **Remediation**:
  - Gradient clipping by global norm: $\mathbf{g} \leftarrow \mathbf{g} \cdot \min\left(1, \frac{v}{\|\mathbf{g}\|_2}\right)$.
  - Structural gating mechanisms (LSTM, GRU) that establish linear identity memory paths.

### 4. Gated Recurrent Architectures
- **The LSTM Principle (Hochreiter & Schmidhuber, 1997)**:
  - Introduces a dedicated internal memory cell $\mathbf{c}_t$ governed by an additive update rule:
    $$\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t$$
  - When the forget gate is saturated at $1$ ($\mathbf{f}_t = \mathbf{1}$) and input gate is closed ($\mathbf{i}_t = \mathbf{0}$):
    $$\frac{\partial \mathbf{c}_t}{\partial \mathbf{c}_{t-1}} = \mathbf{I}$$
  - The Jacobian is the identity matrix! Error signals propagate across arbitrary temporal horizons without exponential vanishing or explosion—the **Constant Error Carousel (CEC)**.
- **The GRU Principle (Cho et al., 2014)**:
  - Eliminates the separate cell state, maintaining only a gated hidden state $\mathbf{h}_t$.
  - Couples the forget and input gates into a single update gate $\mathbf{z}_t$:
    $$\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$$
  - Provides computational efficiency with fewer parameters while maintaining competitive empirical performance on sequence modeling tasks.
