# Chapter 03 Academic Papers Inventory & Mathematical Syntheses

This inventory provides complete mathematical formulations and theoretical context for the seminal literature integrated into Chapter 03.

---

## 1. Word2Vec: Efficient Continuous Space Estimation
- **Citation**: Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013a). *Efficient Estimation of Word Representations in Vector Space*. arXiv preprint arXiv:1301.3781.
- **Key Contribution**: Stripped away the hidden non-linear layer from Bengio et al.'s neural probabilistic language model, creating two log-bilinear architectures capable of scaling to billions of tokens:
  - **CBOW (Continuous Bag-of-Words)**: Predicts the center target word from context tokens:
    $$\mathbf{h} = \frac{1}{2C} \sum_{-C \le j \le C, j \ne 0} \mathbf{v}_{w_{t+j}} = \frac{1}{2C} \mathbf{W}_{\text{in}}^\top \sum \mathbf{e}_c$$
  - **Skip-Gram**: Predicts context tokens within window $C$ from the center word:
    $$\mathcal{L}_{\text{SG}} = -\sum_{t=1}^T \sum_{-C \le j \le C, j \ne 0} \log P(w_{t+j} \mid w_t)$$
- **The Bottleneck**: Full Softmax denominator $\sum_{k=1}^V \exp(\mathbf{u}_k^\top \mathbf{v}_w)$ requires $\mathcal{O}(V)$ operations per prediction.

---

## 2. Distributed Representations and Negative Sampling (SGNS)
- **Citation**: Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., & Dean, J. (2013b). *Distributed Representations of Words and Phrases and their Compositionality*. NeurIPS 2013.
- **Key Contribution**:
  - Replaces full Softmax with **Skip-Gram Negative Sampling (SGNS)**, transforming multi-class prediction into $1+K$ binary logistic regressions:
    $$\mathcal{L}_{\text{SGNS}}(\mathbf{v}_w, \mathbf{u}_c, \{\mathbf{u}_{w_{n,k}}\}_{k=1}^K) = \log \sigma(\mathbf{u}_c^\top \mathbf{v}_w) + \sum_{k=1}^K \log \sigma(-\mathbf{u}_{w_{n,k}}^\top \mathbf{v}_w)$$
  - **Analytical Gradients**:
    $$\frac{\partial \mathcal{L}}{\partial \mathbf{u}_c} = (1 - \sigma(\mathbf{u}_c^\top \mathbf{v}_w)) \mathbf{v}_w = \sigma(-\mathbf{u}_c^\top \mathbf{v}_w) \mathbf{v}_w$$
    $$\frac{\partial \mathcal{L}}{\partial \mathbf{u}_{w_{n,k}}} = -\sigma(\mathbf{u}_{w_{n,k}}^\top \mathbf{v}_w) \mathbf{v}_w$$
    $$\frac{\partial \mathcal{L}}{\partial \mathbf{v}_w} = \sigma(-\mathbf{u}_c^\top \mathbf{v}_w) \mathbf{u}_c - \sum_{k=1}^K \sigma(\mathbf{u}_{w_{n,k}}^\top \mathbf{v}_w) \mathbf{u}_{w_{n,k}}$$
  - **The 3/4 Unigram Exponent**: Samples negative noise words from $P_n(w) \propto U(w)^{0.75}$, increasing the sampling frequency of rare words relative to frequent stop words.

---

## 3. FastText: Enriching Word Vectors with Subword Character n-grams
- **Citation**: Bojanowski, P., Grave, E., Joulin, A., & Mikolov, T. (2017). *Enriching Word Vectors with Subword Information*. Transactions of the Association for Computational Linguistics, 5, 135–146.
- **Key Contribution**:
  - Solves the Out-of-Vocabulary (OOV) disaster and morphological blindness of Word2Vec.
  - Decomposes words into character $n$-grams enclosed in boundary symbols $\langle, \rangle$ (e.g. for $n=3$, $\texttt{"where"} \to \langle\text{wh}, \text{whe}, \text{her}, \text{ere}, \text{re}\rangle$ plus the special full token $\langle\text{where}\rangle$).
  - Word representation is the sum of subword vectors:
    $$\mathbf{v}_w = \sum_{g \in \mathcal{G}_w} \mathbf{z}_g$$
  - Enables synthesizing valid representations for unseen words or misspellings at test time by summing known character $n$-grams.

---

## 4. Hierarchical Softmax
- **Citation**: Morin, F., & Bengio, Y. (2005). *Hierarchical Probabilistic Neural Network Language Model*. AISTATS.
- **Key Contribution**: Decomposes the vocabulary into a binary Huffman tree where vocabulary words are leaves. The probability of reaching a leaf is the product of sigmoid branch probabilities along the path from the root, reducing complexity from $\mathcal{O}(V)$ to $\mathcal{O}(\log_2 V)$.
