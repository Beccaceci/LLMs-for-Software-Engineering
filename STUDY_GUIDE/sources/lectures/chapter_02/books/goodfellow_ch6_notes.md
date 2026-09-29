# Ian Goodfellow, Yoshua Bengio, & Aaron Courville: "Deep Learning" — Chapter 6 Notes

Source: [Deep Learning (MIT Press, 2016)](https://www.deeplearningbook.org/), Chapter 6: *Deep Feedforward Networks*.

## Key Pedagogical Principles & Technical Insights

### 1. The Mandatory Requirement of Non-Linear Activations: Stacking Collapse Proof
- **Core Premise**: Deep feedforward networks are designed to represent complex non-linear functions by composing multiple layers of affine transformations interleaved with non-linear activation functions.
- **The Linear Stacking Collapse**: Suppose we construct an $L$-layer network where every activation function is the identity mapping $f(z) = z$:
  $$\mathbf{h}_1 = \mathbf{W}_1^\top \mathbf{x} + \mathbf{b}_1$$
  $$\mathbf{h}_2 = \mathbf{W}_2^\top \mathbf{h}_1 + \mathbf{b}_2 = \mathbf{W}_2^\top (\mathbf{W}_1^\top \mathbf{x} + \mathbf{b}_1) + \mathbf{b}_2 = (\mathbf{W}_1 \mathbf{W}_2)^\top \mathbf{x} + (\mathbf{W}_2^\top \mathbf{b}_1 + \mathbf{b}_2)$$
  By induction across all $L$ layers:
  $$\hat{\mathbf{y}} = \mathbf{W}_{\text{eff}}^\top \mathbf{x} + \mathbf{b}_{\text{eff}}, \quad \text{where } \mathbf{W}_{\text{eff}} = \prod_{l=1}^L \mathbf{W}_l, \quad \mathbf{b}_{\text{eff}} = \mathbf{b}_L + \sum_{l=1}^{L-1} \left(\prod_{k=l+1}^L \mathbf{W}_k^\top\right) \mathbf{b}_l$$
- **Theoretical Implication**: Any depth of linear layers collapses into a single equivalent affine transformation. The network cannot compute non-linear decision boundaries (such as XOR). Therefore, non-linear activation functions are mathematically mandatory to unlock expressive representational capacity.

### 2. Hidden Unit Dynamics and Pathologies
- **Logistic Sigmoid**: $\sigma(z) = \frac{1}{1 + e^{-z}}$.
  - *Derivative*: $\sigma'(z) = \sigma(z)(1 - \sigma(z))$.
  - *Pathology*: Saturated regimes when $|z| \gg 0$ cause $\sigma'(z) \to 0$. In backpropagation, multiplying by near-zero derivatives causes vanishing gradients in early layers. Furthermore, $\sigma(z) \in (0, 1)$ is strictly positive, introducing zig-zagging gradient dynamics during optimization.
- **Hyperbolic Tangent**: $\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}} = 2\sigma(2z) - 1$.
  - *Derivative*: $\tanh'(z) = 1 - \tanh^2(z)$.
  - *Properties*: Zero-centered range $(-1, +1)$ improves gradient descent conditioning compared to sigmoid, but still suffers from derivative saturation when $|z| > 2$.
- **Rectified Linear Unit (ReLU)**: $\text{ReLU}(z) = \max(0, z)$.
  - *Derivative*: $\frac{d}{dz}\text{ReLU}(z) = \mathbf{1}_{z > 0}$ (with subgradient 0 at $z=0$).
  - *Advantages*: Constant gradient of $1.0$ for all positive activations, completely eliminating derivative saturation in active regimes and accelerating gradient descent convergence.
  - *Dying ReLU Pathology*: If large gradient updates drive weights such that a neuron outputs $z < 0$ across all training inputs, its gradient becomes permanently 0.0, rendering the neuron "dead" and unrecoverable.

### 3. Output Units and Maximum Likelihood Cost Functions
- **The Failure of Mean Squared Error (MSE) for Classification**:
  - When MSE $L(y, \hat{y}) = \frac{1}{2}(y - \hat{y})^2$ is paired with a sigmoid output $\hat{y} = \sigma(z)$:
    $$\frac{\partial L}{\partial z} = (\hat{y} - y) \sigma'(z) = (\hat{y} - y) \sigma(z)(1 - \sigma(z))$$
  - If the model makes a highly confident incorrect prediction (e.g. $y=1, z=-10 \implies \hat{y} \approx 0$), $\sigma'(z) \approx 0$, causing $\frac{\partial L}{\partial z} \to 0$. The gradient vanishes precisely when the prediction error is maximal, freezing parameter updates.
- **Maximum Likelihood & Cross-Entropy**:
  - For Bernoulli likelihood with negative log-likelihood $\mathcal{L}_{\text{BCE}} = -[y \ln \hat{y} + (1 - y) \ln(1 - \hat{y})]$:
    $$\frac{\partial \mathcal{L}_{\text{BCE}}}{\partial z} = \frac{\partial \mathcal{L}}{\partial \hat{y}} \frac{d\hat{y}}{dz} = \left(-\frac{y}{\hat{y}} + \frac{1 - y}{1 - \hat{y}}\right) \sigma(z)(1 - \sigma(z)) = \hat{y} - y$$
  - The saturating derivative $\sigma'(z)$ is canceled analytically by the denominator of the logarithmic loss! The gradient is directly proportional to the linear prediction error $\hat{y} - y$, providing powerful gradient signals regardless of saturation.

### 4. Computational Graphs & Adjoint Backpropagation
- **Forward Mode**: Computes activations topologically from input nodes to scalar loss $\mathcal{L}$.
- **Reverse Mode (Backpropagation)**: Propagates adjoint variables $\delta_i = \frac{\partial \mathcal{L}}{\partial u_i}$ backwards through the directed acyclic graph:
  $$\frac{\partial \mathcal{L}}{\partial u_i} = \sum_{j \in \text{children}(i)} \frac{\partial \mathcal{L}}{\partial u_j} \frac{\partial u_j}{\partial u_i}$$
- **Computational Efficiency**: Evaluates exact gradients with respect to all $W$ network parameters in $\mathcal{O}(W)$ time, matching the asymptotic complexity of a single forward pass.
