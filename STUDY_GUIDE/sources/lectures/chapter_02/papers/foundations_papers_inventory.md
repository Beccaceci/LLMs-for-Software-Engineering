# Chapter 02 Academic Papers Inventory & Mathematical Syntheses

This inventory provides complete mathematical formulations and theoretical bounds for the foundational deep learning literature integrated into Chapter 02.

---

## 1. The Perceptron & Linear Decision Boundaries
- **Citation**: Rosenblatt, F. (1958). *The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain*. Psychological Review, 65(6), 386–408.
- **Key Contributions**:
  - **Single-Layer Perceptron Architecture**:
    $$z = \mathbf{w}^\top \mathbf{x} + b = \sum_{i=1}^d w_i x_i + b$$
    $$y = f(z) = \begin{cases} 1 & \text{if } z \ge 0 \\ 0 & \text{if } z < 0 \end{cases}$$
  - **Perceptron Learning Rule**: For target label $y^* \in \{0, 1\}$:
    $$\mathbf{w} \leftarrow \mathbf{w} + \eta (y^* - y) \mathbf{x}, \quad b \leftarrow b + \eta (y^* - y)$$
  - **Perceptron Convergence Theorem (Novikoff, 1962)**: If training data is linearly separable with margin $\gamma = \min_k \frac{y_k^*(\mathbf{w}^{*\top} \mathbf{x}_k)}{\|\mathbf{w}^*\|_2} > 0$ and bounded radius $\|\mathbf{x}_k\|_2 \le R$, the algorithm converges in at most $k \le \left(\frac{R}{\gamma}\right)^2$ updates.
  - **Linear Inseparability & XOR Failure (Minsky & Papert, 1969)**: Proved that single-layer perceptrons cannot compute non-linearly separable functions like XOR, freezing connectionist research until multi-layer backpropagation emerged.

---

## 2. Generalized Adjoint Error Backpropagation
- **Citation**: Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). *Learning representations by back-propagating errors*. Nature, 323(6088), 533–536.
- **Key Contributions**:
  - Generalizes the delta rule to multi-layer networks via recursive multivariable chain rule application:
    $$\delta_j \equiv \frac{\partial \mathcal{L}}{\partial z_j} = \sigma'(z_j) \sum_{k \in \operatorname{downstream}(j)} w_{kj} \delta_k$$
  - **Weight Gradient**:
    $$\frac{\partial \mathcal{L}}{\partial w_{ji}} = \frac{\partial \mathcal{L}}{\partial z_j} \frac{\partial z_j}{\partial w_{ji}} = \delta_j a_i$$
  - **Vectorized Matrix Calculus Form**:
    $$\mathbf{z} = \mathbf{W}^\top \mathbf{x} + \mathbf{b}, \quad \bm{\delta} = \nabla_{\mathbf{z}} \mathcal{L}$$
    $$\frac{\partial \mathcal{L}}{\partial \mathbf{W}} = \mathbf{x} \bm{\delta}^\top, \quad \frac{\partial \mathcal{L}}{\partial \mathbf{b}} = \bm{\delta}, \quad \frac{\partial \mathcal{L}}{\partial \mathbf{x}} = \mathbf{W} \bm{\delta}$$

---

## 3. The Universal Approximation Theorem (UAT)
- **Citations**:
  - Cybenko, G. (1989). *Approximation by superpositions of a sigmoidal function*. Mathematics of Control, Signals, and Systems, 2(4), 303–314.
  - Hornik, K., Stinchcombe, M., & White, H. (1989). *Multilayer feedforward networks are universal approximators*. Neural Networks, 2(5), 359–366.
- **Key Theorems & Bounds**:
  - **Cybenko's Theorem**: Let $\sigma$ be any continuous sigmoidal function ($\lim_{t \to -\infty} \sigma(t) = 0$ and $\lim_{t \to +\infty} \sigma(t) = 1$). Then finite sums of the form:
    $$G(\mathbf{x}) = \sum_{i=1}^N \alpha_i \sigma(\mathbf{w}_i^\top \mathbf{x} + b_i)$$
    are dense in the Banach space of continuous functions $C(I_n)$ on the $n$-dimensional unit cube $I_n = [0, 1]^n$ under the uniform supremum norm:
    $$\forall g \in C(I_n), \; \forall \epsilon > 0, \; \exists N \in \mathbb{N}, \alpha_i, b_i \in \mathbb{R}, \mathbf{w}_i \in \mathbb{R}^n: \quad \sup_{\mathbf{x} \in I_n} |G(\mathbf{x}) - g(\mathbf{x})| < \epsilon$$
  - **Hornik's Generalization**: Extended density to arbitrary non-constant, bounded continuous activations $\sigma$, establishing that the architecture of feedforward networks—not the specific choice of activation—is fundamentally responsible for universal representation.
  - **The Intuitive Bump-Function Construction**: Combining pairs of oppositely signed sigmoids creates localized gate/box wavelets:
    $$B(x) = \sigma(w(x - a)) - \sigma(w(x - b))$$
    As $w \to \infty$, $B(x)$ approaches an indicator function $\mathbf{1}_{[a, b]}(x)$. In $d$ dimensions, intersecting $d$ such wavelets produces localized $d$-dimensional hypercubes whose linear combinations approximate Riemann integrals over continuous manifolds.

---

## 4. Variance Preservation & Weight Initialization
- **Citation**: Glorot, X., & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. AISTATS 2010, 249–256.
- **Key Contributions**:
  - Investigated gradient vanishing in standard random Gaussian initializations ($W \sim \mathcal{N}(0, 1)$).
  - Derived the variance condition to ensure signal variance remains invariant across layer forward and backward passes:
    $$\text{Forward}: \quad \text{Var}(z^l) = n_{\text{in}} \text{Var}(W) \text{Var}(a^{l-1}) \implies \text{Var}(W) = \frac{1}{n_{\text{in}}}$$
    $$\text{Backward}: \quad \text{Var}(\delta^l) = n_{\text{out}} \text{Var}(W) \text{Var}(\delta^{l+1}) \implies \text{Var}(W) = \frac{1}{n_{\text{out}}}$$
  - **Xavier / Glorot Compromise**:
    $$\text{Var}(W) = \frac{2}{n_{\text{in}} + n_{\text{out}}}$$
    $$W \sim \mathcal{U}\left(-\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}, +\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}\right) \quad \text{or} \quad W \sim \mathcal{N}\left(0, \frac{2}{n_{\text{in}} + n_{\text{out}}}\right)$$

---

## 5. Modern Activation: GELU
- **Citation**: Hendrycks, D., & Gimpel, K. (2016). *Gaussian Error Linear Units (GELUs)*. arXiv:1606.08415.
- **Key Contributions**:
  - Weights input $x$ by its probability of exceeding random standard Gaussian noise $X \sim \mathcal{N}(0, 1)$:
    $$\text{GELU}(x) = x \cdot P(X \le x) = x \Phi(x) = x \cdot \frac{1}{2}\left[1 + \text{erf}\left(\frac{x}{\sqrt{2}}\right)\right]$$
  - Fast Analytic Approximation:
    $$\text{GELU}(x) \approx 0.5x \left(1 + \tanh\left(\sqrt{\frac{2}{\pi}} \left(x + 0.044715 x^3\right)\right)\right)$$
  - Combines deterministic non-linearity with stochastic dropout regularizing behavior, now standard in Transformer LLMs (GPT-2/3/4, BERT).

---

## 6. Adaptive Moment Estimation (Adam)
- **Citation**: Kingma, D. P., & Ba, J. (2014). *Adam: A Method for Stochastic Optimization*. ICLR 2015.
- **Key Contributions**:
  - Maintains exponential moving averages of both past gradients ($m_t$, first raw moment) and squared gradients ($v_t$, second uncentered moment):
    $$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$
  - **Bias Correction**: Initializing $m_0 = \mathbf{0}, v_0 = \mathbf{0}$ biases estimates toward zero in early steps. Corrected via:
    $$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$
  - **Parameter Update Rule**:
    $$\theta_t = \theta_{t-1} - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$
  - Default hyperparameters: $\alpha = 0.001, \beta_1 = 0.9, \beta_2 = 0.999, \epsilon = 10^{-8}$.
