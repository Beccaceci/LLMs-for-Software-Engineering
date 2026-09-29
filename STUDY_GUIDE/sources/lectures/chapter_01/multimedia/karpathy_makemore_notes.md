# Multimedia Reference Notes: Chapter 01 (Andrej Karpathy, 3Blue1Brown, StatQuest)

This document synthesizes key pedagogical takeaways, code architectures, and visual intuition from educational multimedia integrated into Chapter 01.

---

## 1. Andrej Karpathy: "Neural Networks: Zero to Hero" — makemore Part 1
- **Source Video**: *Building makemore Part 1: Dataloading, Bigram Language Model, Sampling, Loss, and Backprop* (2022).
- **Companion Code**: [`makemore.py`](https://github.com/karpathy/makemore) (~200 LOC in pure PyTorch).
- **Core Insights & Mechanics**:
  1. *The Bigram Count Matrix*:
     - Vocabulary constructed over characters `.` (start/end token) plus 26 lowercase English letters: $|\mathcal{V}| = 27$.
     - Counts collected in integer tensor `N = torch.zeros((27, 27), dtype=torch.int32)`.
     - Demonstrates that training a classical bigram language model is simply incrementing table entries: `N[ch1, ch2] += 1`.
  2. *Normalization & Laplace Pseudo-Counts*:
     - Adding pseudo-counts to prevent $-\log(0) = \infty$: `P = (N + 1).float() / (N + 1).sum(1, keepdim=True)`.
     - Each row becomes a categorical probability distribution summing to 1.0.
  3. *Autoregressive Sampling Loop*:
     - Uses `torch.multinomial(P[ix], num_samples=1, replacement=True, generator=g).item()` to sample next character iteratively until reaching the `.` boundary.
  4. *Negative Log-Likelihood (NLL) Loss*:
     $$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^N \log P(w_i \mid w_{i-1})$$
     Karpathy explains that minimizing NLL is identical to maximizing the likelihood of the training data.
  5. *The Neural Network Formulation of the Same Model*:
     - Replaces table lookup with a single linear layer: inputs are one-hot vectors $\mathbf{x} \in \mathbb{R}^{27}$, weights are $\mathbf{W} \in \mathbb{R}^{27 \times 27}$.
     - Logits computed as `logits = xenc @ W`, converted to probabilities via `counts = logits.exp()`, `probs = counts / counts.sum(1, keepdims=True)`.
     - Proves that when trained with gradient descent and Cross-Entropy loss, the weights $\mathbf{W}$ converge to the log-probabilities of the frequency table `N`.

---

## 2. 3Blue1Brown (Grant Sanderson): Information Theory and Entropy
- **Source Video**: *Information Theory and Entropy* (2020).
- **Core Insights**:
  1. *Self-Information as Surprise*:
     $$I(x) = -\log_2 P(x) = \log_2 \frac{1}{P(x)}$$
     A highly probable event ($P \to 1$) yields zero information ($I \to 0$), whereas a rare event ($P \to 0$) conveys enormous information ($I \to \infty$). Logarithm ensures additivity for independent events: $I(x, y) = I(x) + I(y)$.
  2. *Shannon Entropy as Expected Surprise*:
     $$H(X) = \mathbb{E}[I(X)] = -\sum_{x} P(x) \log_2 P(x)$$
     Entropy represents the theoretical minimum average number of bits required to encode messages produced by source $X$.
  3. *Cross-Entropy & Kullback-Leibler Divergence*:
     $$H(P, Q) = -\sum_x P(x) \log_2 Q(x) = H(P) + D_{\text{KL}}(P \parallel Q)$$
     Cross-entropy is the expected code length when messages distributed according to true distribution $P$ are encoded using an optimized codebook based on estimated distribution $Q$. The excess code length is the KL divergence $D_{\text{KL}}(P \parallel Q) \ge 0$.

---

## 3. StatQuest with Josh Starmer: Cross-Entropy and Maximum Likelihood
- **Source Video**: *Cross-Entropy and Maximum Likelihood* (2021).
- **Core Insights**:
  1. *Arithmetic Mechanics of Cross-Entropy*:
     - Evaluates true target $y \in \{0, 1\}$ against predicted probability $\hat{y}$:
       $$\text{CE} = -[y \log(\hat{y}) + (1 - y) \log(1 - \hat{y})]$$
  2. *Equivalence to Likelihood Maximization*:
     - Likelihood under Bernoulli distribution: $L = \hat{y}^y (1 - \hat{y})^{1-y}$.
     - Taking log: $\ln L = y \ln \hat{y} + (1 - y) \ln(1 - \hat{y})$.
     - Multiplying by $-1$ yields Negative Log-Likelihood, which is exactly the binary cross-entropy loss function.
  3. *Loss Asymptotics*:
     - When $\hat{y} \to y$, loss approaches 0.
     - When a model confidently predicts $\hat{y} \to 0$ for a true label $y = 1$, loss approaches $+\infty$, penalizing overconfident incorrect predictions heavily.
