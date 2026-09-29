# Chapter 01 Academic Papers Inventory & Mathematical Syntheses

This inventory provides complete mathematical formulations and theoretical bounds for the seminal literature integrated into Chapter 01.

---

## 1. Information Theory & Entropy Bounds
- **Citation**: Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal, 27(3), 379–423.
- **Key Contributions**:
  - **Self-Information**: Measures the surprise of observing an event $x$ with probability $P(x)$:
    $$I(x) = -\log_2 P(x)$$
  - **Information Entropy**: The expected self-information over alphabet $\mathcal{X}$:
    $$H(X) = -\sum_{x \in \mathcal{X}} P(x) \log_2 P(x)$$
  - **Joint & Conditional Entropy**:
    $$H(X, Y) = -\sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} P(x, y) \log_2 P(x, y) = H(X) + H(Y \mid X)$$
    $$H(Y \mid X) = -\sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} P(x, y) \log_2 P(y \mid x)$$
  - **Cross-Entropy & Kullback-Leibler Divergence**:
    $$H(P, Q) = -\sum_{x \in \mathcal{X}} P(x) \log_2 Q(x) = H(P) + D_{\text{KL}}(P \parallel Q)$$
    $$D_{\text{KL}}(P \parallel Q) = \sum_{x \in \mathcal{X}} P(x) \log_2 \frac{P(x)}{Q(x)} \ge 0 \quad (\text{Gibbs' Inequality})$$
  - **Entropy Rate of Natural Language**: $\mathcal{H}(L) = \lim_{n \to \infty} \frac{1}{n} H(w_1, \dots, w_n) = \lim_{n \to \infty} H(w_n \mid w_1, \dots, w_{n-1})$.

---

## 2. Good-Turing Frequency Estimation
- **Citation**: Good, I. J. (1953). *The population frequencies of species and the estimation of population parameters*. Biometrika, 40(3-4), 237–264.
- **Key Contributions**:
  - **Re-estimating Frequencies**: Let $N_r = |\{w : c(w) = r\}|$ be the number of distinct $n$-grams that occurred exactly $r$ times in a sample of size $N = \sum_{r=1}^\infty r N_r$.
  - **Adjusted Count Formula**:
    $$r^* = (r + 1) \frac{N_{r+1}}{N_r}$$
  - **Adjusted Probability**:
    $$P_{\text{GT}}(r) = \frac{r^*}{N} = \frac{(r + 1) N_{r+1}}{N \cdot N_r}$$
  - **Total Probability of Unseen Events ($r=0$)**:
    $$P_{\text{GT}}(0) = \frac{0^*}{N} = \frac{1 \cdot N_1}{N \cdot N_0} \implies \text{Total unseen mass } P_{\text{total}}(0) = N_0 \cdot P_{\text{GT}}(0) = \frac{N_1}{N}$$
  - Probability mass assigned to all unseen $n$-grams equals the proportion of singletons ($N_1$) observed in the training corpus.

---

## 3. The Katz Back-off Model
- **Citation**: Katz, S. M. (1987). *Estimation of probabilities from sparse data for the language model component of a speech recognizer*. IEEE Transactions on Acoustics, Speech, and Signal Processing, 35(3), 400–401.
- **Key Contributions**:
  - Distributes the discounted mass of observed $n$-grams strictly to lower-order backoff distributions rather than uniform distributions:
    $$P_{\text{bo}}(w_i \mid w_{i-n+1}^{i-1}) = \begin{cases} d_r \frac{c(w_{i-n+1}^i)}{c(w_{i-n+1}^{i-1})} & \text{if } r = c(w_{i-n+1}^i) > 0 \\ \alpha(w_{i-n+1}^{i-1}) P_{\text{bo}}(w_i \mid w_{i-n+2}^{i-1}) & \text{if } r = 0 \end{cases}$$
  - **Turing Discount Coefficient**:
    $$d_r = \frac{\frac{r^*}{r} - \frac{(k+1) N_{k+1}}{N_1}}{1 - \frac{(k+1) N_{k+1}}{N_1}} \quad \text{for } 1 \le r \le k \quad (k \approx 5)$$
  - **Normalization Backoff Weight $\alpha$**:
    $$\alpha(w_{i-n+1}^{i-1}) = \frac{1 - \sum_{w: c(w_{i-n+1}^{i-1}, w) > 0} P_{\text{bo}}(w \mid w_{i-n+1}^{i-1})}{1 - \sum_{w: c(w_{i-n+1}^{i-1}, w) > 0} P_{\text{bo}}(w \mid w_{i-n+2}^{i-1})}$$

---

## 4. Interpolated Kneser-Ney Smoothing
- **Citation**: Kneser, R., & Ney, H. (1995). *Improved backing-off for m-gram language modeling*. IEEE ICASSP 1995, 181–184.
- **Key Contributions**:
  - Introduces **Absolute Discounting** with fixed parameter $d \in (0, 1)$ ($d \approx \frac{N_1}{N_1 + 2N_2}$) combined with **Continuation Probabilities**:
    $$P_{\text{KN}}(w_i \mid w_{i-1}) = \frac{\max(c(w_{i-1}, w_i) - d, 0)}{c(w_{i-1})} + \lambda(w_{i-1}) P_{\text{cont}}(w_i)$$
  - **Continuation Probability**: Replaces unigram frequency $c(w_i) / N$ with the number of unique histories that precede $w_i$:
    $$P_{\text{cont}}(w_i) = \frac{|\{w_{i-1} : c(w_{i-1}, w_i) > 0\}|}{\sum_w |\{w_{i-1} : c(w_{i-1}, w) > 0\}|}$$
    *Pedagogical Example*: "San Francisco" occurs frequently, making $c(\text{Francisco})$ high. But "Francisco" almost exclusively follows "San". In an unseen context like "I want to eat ...", $P_{\text{cont}}(\text{Francisco})$ is extremely low, whereas $P_{\text{cont}}(\text{apple})$ is high because "apple" follows many distinct verbs/adjectives.
  - **Interpolation Normalizer**:
    $$\lambda(w_{i-1}) = \frac{d}{c(w_{i-1})} |\{w : c(w_{i-1}, w) > 0\}|$$

---

## 5. Modified Kneser-Ney Smoothing Benchmark
- **Citation**: Chen, S. F., & Goodman, J. (1996/1999). *An Empirical Study of Smoothing Techniques for Language Modeling*. Computer Speech & Language, 13(4), 359–394.
- **Key Contributions**:
  - Replaces the single discount $d$ with three distinct discounts based on observed counts: $d_1$ for $c=1$, $d_2$ for $c=2$, and $d_3$ for $c \ge 3$:
    $$d_r = r - (r + 1) \frac{N_{r+1}}{N_r} \cdot \frac{N_1}{N_1 + 2N_2}$$
  - Established Modified Kneser-Ney as the undisputed highest-performing non-neural smoothing method across extensive speech and translation benchmarks.

---

## 6. The Neural Probabilistic Language Model (NPLM)
- **Citation**: Bengio, Y., Ducharme, R., Vincent, P., & Jauvin, C. (2003). *A Neural Probabilistic Language Model*. Journal of Machine Learning Research, 3, 1137–1155.
- **Key Contributions**:
  - Bridges the discrete statistical $n$-gram paradigm to continuous distributed representations:
    1. Maps each word $w \in \mathcal{V}$ to a continuous distributed feature vector $\mathbf{C}(w) \in \mathbb{R}^d$ ($d \ll |\mathcal{V}|$).
    2. Concatenates context vectors: $\mathbf{x} = [\mathbf{C}(w_{t-1})^\top, \dots, \mathbf{C}(w_{t-n+1})^\top]^\top \in \mathbb{R}^{(n-1)d}$.
    3. Feeds $\mathbf{x}$ to a hidden layer with $\tanh$ non-linearity and direct skip connection to output logits:
       $$\mathbf{y} = \mathbf{b} + \mathbf{W}\mathbf{x} + \mathbf{U} \tanh(\mathbf{d} + \mathbf{H}\mathbf{x})$$
    4. Computes next-token conditional probability via softmax:
       $$P(w_t = i \mid w_{t-n+1}^{t-1}) = \frac{\exp(y_i)}{\sum_{j=1}^{|\mathcal{V}|} \exp(y_j)}$$
  - Defeats the curse of dimensionality: semantically similar words occupy nearby vector coordinates in $\mathbb{R}^d$, enabling automatic generalization to unseen sequences.
