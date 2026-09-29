# Chapter 04 Academic Papers Inventory & Mathematical Syntheses

This inventory provides complete mathematical formulations and theoretical bounds for the foundational sequence modeling literature integrated into Chapter 04.

---

## 1. Simple Recurrent Networks (SRN / Elman RNN)
- **Citation**: Elman, J. L. (1990). *Finding Structure in Time*. Cognitive Science, 14(2), 179–211.
- **Key Contributions**:
  - Introduces internal recurrent feedback by routing the hidden state from the previous time step back into the hidden layer alongside the current input:
    $$\mathbf{h}_t = \sigma_h(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h)$$
    $$\hat{\mathbf{y}}_t = \text{softmax}(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y)$$
  - Demonstrates that the hidden vector $\mathbf{h}_t \in \mathbb{R}^{d_h}$ acts as an internal state space that dynamically preserves temporal context, capable of learning rudimentary grammars and lexical categories without manual feature engineering.

---

## 2. Backpropagation Through Time (BPTT)
- **Citation**: Werbos, P. J. (1990). *Backpropagation Through Time: What It Does and How to Do It*. Proceedings of the IEEE, 78(10), 1550–1560.
- **Key Contributions**:
  - Unfolds the recurrent network into a directed acyclic graph across $T$ discrete time steps.
  - Derives exact parameter gradients by accumulating partial adjoint errors backwards across the temporal sequence:
    $$\frac{\partial \mathcal{L}}{\partial \mathbf{W}_{hh}} = \sum_{t=1}^T \sum_{k=1}^t \frac{\partial \mathcal{L}_t}{\partial \mathbf{h}_t} \left(\prod_{j=k+1}^t \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}}\right) \frac{\partial^+ \mathbf{h}_k}{\partial \mathbf{W}_{hh}}$$

---

## 3. Theoretical Foundations of the Vanishing Gradient Problem
- **Citations**:
  - Bengio, Y., Simard, P., & Frasconi, P. (1994). *Learning Long-Term Dependencies with Gradient Descent is Difficult*. IEEE Transactions on Neural Networks, 5(2), 157–166.
  - Pascanu, R., Mikolov, T., & Bengio, Y. (2013). *On the Difficulty of Training Recurrent Neural Networks*. ICML 2013, 1310–1318.
- **Key Theorems & Bounds**:
  - **Temporal Jacobian Product**:
    $$\frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_t} = \frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_T} \prod_{k=t+1}^T \frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}} = \frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_T} \prod_{k=t+1}^T \operatorname{diag}(\sigma'(\mathbf{a}_k)) \mathbf{W}_{hh}^\top$$
  - **Upper Bound on Gradient Norm**:
    $$\left\| \frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_t} \right\|_2 \le \left\| \frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_T} \right\|_2 \prod_{k=t+1}^T \|\operatorname{diag}(\sigma'(\mathbf{a}_k))\|_2 \|\mathbf{W}_{hh}^\top\|_2 \le \left\| \frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_T} \right\|_2 (\gamma \lambda_{\max})^{T-t}$$
    where $\gamma = \sup_z |\sigma'(z)|$ (for $\tanh$, $\gamma = 1$; for sigmoid, $\gamma = 0.25$).
  - **Sufficient Condition for Vanishing Gradients**: If the spectral radius $\rho(\mathbf{W}_{hh}) < 1/\gamma$, then $\|\frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_t}\|_2 \to 0$ exponentially as $T - t \to \infty$.
  - **Gradient Clipping by Norm (Pascanu et al., 2013)**: To eliminate exploding gradients:
    $$\mathbf{g} \leftarrow \begin{cases} \mathbf{g} & \text{if } \|\mathbf{g}\|_2 \le v \\ \frac{v}{\|\mathbf{g}\|_2} \mathbf{g} & \text{if } \|\mathbf{g}\|_2 > v \end{cases}$$

---

## 4. Long Short-Term Memory (LSTM) & Constant Error Carousel
- **Citation**: Hochreiter, S., & Schmidhuber, J. (1997). *Long Short-Term Memory*. Neural Computation, 9(8), 1735–1780.
- **Key Contributions**:
  - Eliminates gradient decay by establishing an additive memory highway (the Constant Error Carousel, CEC):
    $$\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t$$
  - **Complete Gating Equations**:
    $$\mathbf{f}_t = \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f) \quad \text{(Forget Gate)}$$
    $$\mathbf{i}_t = \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i) \quad \text{(Input Gate)}$$
    $$\tilde{\mathbf{c}}_t = \tanh(\mathbf{W}_c [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_c) \quad \text{(Candidate State)}$$
    $$\mathbf{o}_t = \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o) \quad \text{(Output Gate)}$$
    $$\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t) \quad \text{(Exposed Hidden State)}$$
  - **Derivative of the Cell State**:
    $$\frac{\partial \mathbf{c}_t}{\partial \mathbf{c}_{t-1}} = \operatorname{diag}(\mathbf{f}_t)$$
    If the forget gate is near $1.0$, error signals flow across hundreds of time steps without attenuation.

---

## 5. Gated Recurrent Unit (GRU)
- **Citation**: Cho, K., et al. (2014). *Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation*. EMNLP 2014, 1724–1734.
- **Key Contributions**:
  - Simplifies the LSTM architecture by removing the separate cell state $\mathbf{c}_t$ and coupling forget and input gates:
    $$\mathbf{r}_t = \sigma(\mathbf{W}_r [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_r) \quad \text{(Reset Gate)}$$
    $$\mathbf{z}_t = \sigma(\mathbf{W}_z [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_z) \quad \text{(Update Gate)}$$
    $$\tilde{\mathbf{h}}_t = \tanh(\mathbf{W} [\mathbf{r}_t \odot \mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}) \quad \text{(Candidate Hidden State)}$$
    $$\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t \quad \text{(Final Hidden State)}$$

---

## 6. Sequence to Sequence & The Attention Revolution
- **Citations**:
  - Sutskever, I., Vinyals, O., & Le, Q. V. (2014). *Sequence to Sequence Learning with Neural Networks*. NeurIPS 2014.
  - Bahdanau, D., Cho, K., & Bengio, Y. (2014). *Neural Machine Translation by Jointly Learning to Align and Translate*. ICLR 2015.
- **Key Contributions**:
  - **Seq2Seq Objective**: Maximizes conditional sequence probability:
    $$\mathcal{L} = \sum_{(X, Y)} \sum_{t=1}^{T'} \log P(y_t \mid \mathbf{v}, y_1, \dots, y_{t-1})$$
    where context vector $\mathbf{v} = \mathbf{h}_T^{\text{enc}}$ acts as a single fixed-length bottleneck vector.
  - **Additive Soft Attention (Bahdanau et al., 2014)**:
    Replaces the static bottleneck vector with a dynamic context vector $\mathbf{c}_i$ recomputed for each decoding step $i$:
    $$\mathbf{c}_i = \sum_{j=1}^{T_x} \alpha_{ij} \mathbf{h}_j$$
    $$\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x} \exp(e_{ik})}$$
    $$e_{ij} = \mathbf{v}_a^\top \tanh(\mathbf{W}_a \mathbf{s}_{i-1} + \mathbf{U}_a \mathbf{h}_j)$$
    where $\mathbf{s}_{i-1}$ is the decoder state, $\mathbf{h}_j$ is the $j$-th encoder state, and $\alpha_{ij}$ represents the alignment weight (soft attention).
