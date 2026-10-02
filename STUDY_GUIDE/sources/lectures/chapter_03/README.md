# Sources Dossier: Chapter 03 (Recurrent Neural Networks and Sequence Modeling)

This directory houses all required primary and external reference materials for Chapter 03, organized prior to chapter authoring to ensure zero omission and rigorous pedagogical grounding.

## 1. Definitive Graduate Textbooks
- [Deep Learning](https://www.deeplearningbook.org/) (Ian Goodfellow, Yoshua Bengio, Aaron Courville — MIT Press, 2016)
  - **Chapter 10**: Sequence Modeling: Recurrent and Recursive Nets
  - **Why it matters**: Universally considered the most mathematically complete textbook treatment.
  - **What it covers**: Unfolding computational graphs, Backpropagation Through Time (BPTT), Teacher Forcing, gradient vanishing and exploding proofs, bidirectional RNNs, Encoder-Decoder architectures, and detailed formulations of gated RNNs (LSTMs and GRUs).
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) (Dan Jurafsky & James H. Martin — 3rd ed. draft)
  - **Chapter 9**: Deep Learning Architectures for Sequence Processing: RNNs, LSTMs, and GRUs
  - **Why it matters**: The standard NLP reference. Focuses on sequential language modeling, autoregression, POS-tagging, and classification tasks with clear step-by-step vector walkthroughs.
- [Dive into Deep Learning (D2L.ai)](https://d2l.ai/) (Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola)
  - **Chapter 9** (Recurrent Neural Networks) & **Chapter 10** (Modern Recurrent Neural Networks)
  - **Why it matters**: Bridges mathematical derivations with complete, working PyTorch/NumPy implementations from scratch (without high-level nn.RNN or nn.LSTM abstractions).
  - **What it covers**: Manual implementation of recurrent layers from scratch in PyTorch, gradient clipping by global norm, LSTM gated state updates, and GRU candidate hidden states.

## 2. Intuitive Masterclasses & Visual Walkthroughs
- Christopher Olah (colah's blog): ["Understanding LSTM Networks" (2015)](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
  - **Why it matters**: The undisputed gold standard visual explanation of recurrent cell mechanics.
  - **Key insights**: Dissects the LSTM cell state into an intuitive "conveyor belt" (the Constant Error Carousel) modulated by pointwise multiplications via the forget, input, candidate ($\tilde{C}_t$), and output gates. Also illustrates GRUs.
- Andrej Karpathy: ["The Unreasonable Effectiveness of Recurrent Neural Networks" (2015)](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)
  - **Why it matters**: Demonstrates character-level RNNs, autoregressive sampling, and temperature scaling.
  - **Key insights**: Visualizes individual hidden state neurons operating as interpretable linguistic finite-state machines (e.g., cells that activate specifically inside quotation marks, track indentation depth, or monitor URL structures).
  - **Companion code**: [min-char-rnn.py](https://gist.github.com/karpathy/d4dee566867f8291f086) — A pure 112-line NumPy implementation with explicit manual forward pass and BPTT backpropagation.
- Denny Britz (WildML): ["Recurrent Neural Networks Tutorial" (Parts 1–4)](http://www.wildml.com/2015/09/recurrent-neural-networks-tutorial-part-1-introduction-to-rnns/)
  - **Why it matters**: Walks through the exact matrix calculus behind BPTT step-by-step, deriving $\frac{\partial L_t}{\partial W}$ across all time steps and showing why truncation is necessary.
  - **Key insights**: Derives adjoint backpropagation through time matrices, explains vanishing gradient scaling with sequence length, and shows how to vectorize recurrent batch updates.
  - **Companion code**: [WildML RNN Tutorial Code](https://github.com/dennybritz/rnn-tutorial-rnnlm) — Pure Python/NumPy implementation of an RNN language model with explicit BPTT (~250 LOC).

## 3. Landmark Seminal Papers (Primary Ground Truth)
- **Origins & BPTT Formulation**:
  - Elman, J. L. (1990): [Finding Structure in Time](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=10.1.1.157.9355) — Formulates the Simple Recurrent Network (SRN / Elman RNN):
    - Hidden state recurrence: $\mathbf{h}_t = \sigma_h(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h)$
    - Output projection: $\hat{\mathbf{y}}_t = \text{softmax}(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y)$
  - Werbos, P. J. (1990): [Backpropagation Through Time: What It Does and How to Do It](https://ieeexplore.ieee.org/document/58337) — Formalized gradient computation along the unfolded recurrent graph:
    - Accumulated gradient: $\frac{\partial \mathcal{L}}{\partial \mathbf{W}_{hh}} = \sum_{t=1}^T \sum_{k=1}^t \frac{\partial \mathcal{L}_t}{\partial \mathbf{h}_t} \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} \frac{\partial^+ \mathbf{h}_k}{\partial \mathbf{W}_{hh}}$
- **The Vanishing / Exploding Gradient Proofs**:
  - Bengio, Y., Simard, P., & Frasconi, P. (1994): [Learning Long-Term Dependencies with Gradient Descent is Difficult](https://ieeexplore.ieee.org/document/279181) — The foundational theoretical proof that the spectral radius of the transition matrix causes exponential gradient decay:
    - Decay condition: $\left\| \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_{t-\tau}} \right\| \le \|\mathbf{W}_{hh}^\top\|_2^\tau \cdot \prod_{j=0}^{\tau-1} \|\operatorname{diag}(\sigma'(\mathbf{a}_{t-j}))\|_2 \longrightarrow 0 \quad \text{if } \rho(\mathbf{W}_{hh}) < 1/\gamma$
  - Pascanu, R., Mikolov, T., & Bengio, Y. (2013): [On the Difficulty of Training Recurrent Neural Networks](https://proceedings.mlr.press/v28/pascanu13.html) — Provides the modern Jacobian matrix product proof and introduces gradient clipping by norm:
    - Temporal Jacobian chain: $\frac{\partial \mathcal{L}_t}{\partial \mathbf{h}_j} = \frac{\partial \mathcal{L}_t}{\partial \mathbf{h}_t} \prod_{k=j+1}^t \frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}} = \frac{\partial \mathcal{L}_t}{\partial \mathbf{h}_t} \prod_{k=j+1}^t \operatorname{diag}(1 - \mathbf{h}_k^2) \mathbf{W}_{hh}^\top$
    - Gradient clipping by global norm: $\mathbf{g} \leftarrow \mathbf{g} \cdot \min\left(1, \frac{v}{\|\mathbf{g}\|_2}\right)$
- **Gated Architectures & Sequence-to-Sequence**:
  - Hochreiter, S., & Schmidhuber, J. (1997): [Long Short-Term Memory](https://www.bioinf.jku.at/publications/photocopies/pub-hochreiter-1997.pdf) — Introduces the Constant Error Carousel (CEC), demonstrating how additive memory updates enforce $\frac{\partial \mathbf{C}_t}{\partial \mathbf{C}_{t-1}} = \mathbf{I}$:
    - Cell state: $\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t$
    - Forget gate: $\mathbf{f}_t = \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f)$
    - Input gate: $\mathbf{i}_t = \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i)$
    - Candidate state: $\tilde{\mathbf{c}}_t = \tanh(\mathbf{W}_c [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_c)$
    - Output gate: $\mathbf{o}_t = \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o)$
    - Hidden state: $\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t)$
  - Cho, K., et al. (2014): [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) — Introduces the Gated Recurrent Unit (GRU) and RNN Encoder-Decoder:
    - Reset gate: $\mathbf{r}_t = \sigma(\mathbf{W}_r [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_r)$
    - Update gate: $\mathbf{z}_t = \sigma(\mathbf{W}_z [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_z)$
    - Candidate hidden state: $\tilde{\mathbf{h}}_t = \tanh(\mathbf{W}_h [\mathbf{r}_t \odot \mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_h)$
    - Final hidden state: $\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$
  - Sutskever, I., Vinyals, O., & Le, Q. V. (2014): [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) — Introduces multi-layer LSTM sequence-to-sequence translation:
    - Sequence objective: $\arg\max_\theta \sum_{(X, Y)} \sum_{t=1}^{T'} \log P(y_t \mid \mathbf{v}, y_1, \dots, y_{t-1})$ where $\mathbf{v} = \mathbf{h}_T^{\text{enc}}$
  - Bahdanau, D., Cho, K., & Bengio, Y. (2014): [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) — Solves the fixed-length vector bottleneck of RNN encoders using Additive Soft Attention:
    - Context vector: $\mathbf{c}_i = \sum_{j=1}^{T_x} \alpha_{ij} \mathbf{h}_j$
    - Alignment weights: $\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x} \exp(e_{ik})}$ where $e_{ij} = \mathbf{v}_a^\top \tanh(\mathbf{W}_a \mathbf{s}_{i-1} + \mathbf{U}_a \mathbf{h}_j)$

## 4. University Video Lectures
- **Stanford CS224n (Natural Language Processing with Deep Learning)**:
  - Lecture 6: Language Models and Recurrent Neural Networks (Christopher Manning & Abigail See). Focuses on RNN language models, perplexity, and gradient dynamics.
- **Stanford CS231n (Deep Learning for Computer Vision)**:
  - Lecture 10: Recurrent Neural Networks (Justin Johnson / Andrej Karpathy). Visualizes computational graphs, unrolling in time, and image captioning Seq2Seq architectures.
- **MIT 6.S191 (Introduction to Deep Learning)**:
  - Lecture 2: Recurrent Neural Networks, Transformers, and Attention (Alexander Amini). Visual animations of information flow, hidden state dynamics, and gate operations.

## 5. In This Workspace
You already have detailed materials synthesized in this repository:
- [`STUDY_GUIDE/lectures/chapters/part1_foundations/03_recurrent_neural_networks.tex`](../../lectures/chapters/part1_foundations/03_recurrent_neural_networks.tex): Chapter 3 of the course study guide, containing:
  - The transition from FCNNs to Elman RNNs.
  - The complete BPTT derivation and Jacobian product proof ($\prod_{k=j+1}^t \frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}}$).
  - The Sherlock Holmes character casing training dynamics experiment.
  - Mathematical equations and TikZ diagrams for LSTM gates (CEC) and GRUs.
  - The Seq2Seq information bottleneck that motivated Attention.
- **Empirical Lecture Experiments**:
  - **Sherlock Holmes Casing & Semantic Tracking Experiment**: Slides 19 & 36: Training character-level RNNs on Sherlock Holmes text to compare one-to-one sequence modeling versus encoder-decoder architectures. Shows how character-level models dynamically learn quotation marks, capitalization rules, and indentation depth across training epochs 1 to 1070.
  - **Cat & Mouse Long-Term Dependency Failure**: Slide 25 presents the prompt: *"The mouse was getting chased by the cat through the big house. After a long chase, the cat finally managed to catch the [mouse]"*. Demonstrates that standard Elman RNNs fail to predict *"mouse"* due to vanishing gradients across intervening tokens, outputting grammatically plausible but semantically disconnected completions.
  - **English-to-Italian Translation Length Disparity & Non-Monotonic Alignment**: Slides 31–32 demonstrate why naive recurrent sequence-to-sequence without attention breaks down when target length differs from source length (`[it] [is] [indeed] [sunny] [today]` (5 tokens) $\to$ `[effettivamente] [oggi] [è] [soleggiato]` (4 tokens)), illustrating the fundamental necessity of dynamic encoder-decoder representations.
- [`slides/04-RNN.pdf`](slides/04-RNN.pdf): Course lecture slides (symlink to `SLIDES/04-RNN.pdf`).
- [`transcriptions/03-04-Word-Embeddings-And-RNNs.md`](transcriptions/03-04-Word-Embeddings-And-RNNs.md): Full lecture transcription (symlink to `TRANSCRIPTIONS/LECTURES/03-04-Word-Embeddings-And-RNNs.md`).
