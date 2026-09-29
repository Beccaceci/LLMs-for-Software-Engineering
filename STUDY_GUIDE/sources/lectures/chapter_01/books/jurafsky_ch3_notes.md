# Dan Jurafsky & James H. Martin: "Speech and Language Processing" (3rd ed. draft) — Chapter 3 Notes

Source: [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/), Chapter 3: *N-gram Language Models*.

## Key Pedagogical Principles & Technical Insights

### 1. The Probabilistic Sequence Modeling Task
- **Core Objective**: Compute the joint probability of an arbitrary sequence of $N$ words $W = (w_1, w_2, \dots, w_N)$, or predict the conditional probability distribution over the vocabulary for the next word $w_k$ given preceding history $w_{1:k-1}$.
- **Chain Rule of Probability**: Decomposes the joint sequence probability into a product of conditional autoregressive probabilities with zero loss of generality:
  $$P(w_1, w_2, \dots, w_N) = \prod_{k=1}^N P(w_k \mid w_1, w_2, \dots, w_{k-1})$$
- **The Combinatorial Explosion**: As sequence length $N$ grows, the conditioning history $w_{1:k-1}$ creates an intractable state space. For a vocabulary size $|\mathcal{V}| = 10^5$, estimating $P(w_k \mid w_{1:k-1})$ naively requires enumerating $|\mathcal{V}|^k$ possible histories.

### 2. The Markov Property and N-gram Approximations
- **Markov Assumption**: The probability of the incoming word depends only on the immediately preceding $n-1$ words rather than the entire arbitrary history:
  $$P(w_k \mid w_1, \dots, w_{k-1}) \approx P(w_k \mid w_{k-n+1}^{k-1})$$
- **Unigram ($n=1$)**: Complete context independence: $P(w_1, \dots, w_N) \approx \prod_{k=1}^N P(w_k)$.
- **Bigram ($n=2$)**: First-order Markov chain: $P(w_1, \dots, w_N) \approx \prod_{k=1}^N P(w_k \mid w_{k-1})$.
- **Trigram ($n=3$)**: Second-order Markov chain: $P(w_1, \dots, w_N) \approx \prod_{k=1}^N P(w_k \mid w_{k-2}, w_{k-1})$.
- **Maximum Likelihood Estimation (MLE)**: Estimated directly via empirical corpus frequency counts:
  $$P_{\text{MLE}}(w_i \mid w_{i-n+1}^{i-1}) = \frac{c(w_{i-n+1}^i)}{c(w_{i-n+1}^{i-1})} = \frac{c(w_{i-n+1}^{i-1}, w_i)}{\sum_{w \in \mathcal{V}} c(w_{i-n+1}^{i-1}, w)}$$

### 3. The Sparsity Crisis & Zero-Frequency Probability Collapse
- **Extreme Sparsity**: The vocabulary space $|\mathcal{V}|$ grows linearly, but the $n$-gram parameter space grows exponentially as $|\mathcal{V}|^n$. Natural language exhibits long-tail Zipfian behavior: the vast majority of valid linguistic combinations never appear even in multi-gigabyte corpora.
- **Probability Collapse**: If a single test sequence transition $(w_{i-1}, w_i)$ has count $c(w_{i-1}, w_i) = 0$:
  $$P_{\text{MLE}}(w_i \mid w_{i-1}) = 0 \implies P(W) = \prod_{k=1}^N P(w_k \mid w_{k-1}) = 0$$
- **Perplexity Explosion**: When evaluated under perplexity $\text{PPL}(W) = P(W)^{-1/N}$, a single zero count causes division by zero: $\text{PPL}(W) \to \infty$.

### 4. Smoothing Formulations
- **Laplace Add-1 Smoothing**: Reallocates probability mass uniformly by adding a pseudo-count of 1 to every vocabulary entry:
  $$P_{\text{Laplace}}(w_i \mid w_{i-1}) = \frac{c(w_{i-1}, w_i) + 1}{c(w_{i-1}) + |\mathcal{V}|}$$
  *Pathology*: Shifts far too much probability mass to unseen events when $|\mathcal{V}|$ is large (e.g. $|\mathcal{V}| = 10^5$), degrading frequent $n$-gram performance.
- **Add-$k$ (Lidstone) Smoothing**: Reduces the pseudo-count to fractional $k \in (0, 1)$:
  $$P_{\text{Lidstone}}(w_i \mid w_{i-1}) = \frac{c(w_{i-1}, w_i) + k}{c(w_{i-1}) + k|\mathcal{V}|}$$
- **Good-Turing Frequency Estimation**: Re-estimates counts based on the frequency of frequencies $N_r = |\{w : c(w) = r\}|$:
  $$r^* = (r + 1) \frac{N_{r+1}}{N_r}, \quad P_{\text{GT}}(0) = \frac{N_1}{N}$$
- **Interpolated Kneser-Ney Smoothing**: Replaces lower-order unigram frequency with continuation probability $P_{\text{cont}}(w_i)$ (how likely word $w_i$ is to complete an arbitrary unseen preceding context):
  $$P_{\text{KN}}(w_i \mid w_{i-1}) = \frac{\max(c(w_{i-1}, w_i) - d, 0)}{c(w_{i-1})} + \lambda(w_{i-1}) P_{\text{cont}}(w_i)$$
  $$P_{\text{cont}}(w_i) = \frac{|\{w' : c(w', w_i) > 0\}|}{\sum_w |\{w' : c(w', w) > 0\}|}, \quad \lambda(w_{i-1}) = \frac{d}{c(w_{i-1})} |\{w : c(w_{i-1}, w) > 0\}|$$

### 5. Intrinsic Evaluation: Cross-Entropy and Perplexity
- **Empirical Cross-Entropy**: Average negative log-probability per token on test corpus $W = (w_1, \dots, w_N)$:
  $$H(W) = -\frac{1}{N} \log_2 P(w_1, \dots, w_N) = -\frac{1}{N} \sum_{i=1}^N \log_2 P(w_i \mid w_1^{i-1})$$
- **Perplexity ($\text{PPL}$)**: The geometric mean branching factor:
  $$\text{PPL}(W) = 2^{H(W)} = P(w_1, \dots, w_N)^{-1/N} = \sqrt[N]{\prod_{i=1}^N \frac{1}{P(w_i \mid w_1^{i-1})}}$$
- **Pedagogical Meaning**: A language model with $\text{PPL} = k$ is, on average, as uncertain about the next token as if it were choosing uniformly at random among $k$ equally likely candidate words.
