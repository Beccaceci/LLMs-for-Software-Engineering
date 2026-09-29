# Sources Dossier: Chapter 04 (Recurrent Neural Networks and Sequence Modeling)

This directory houses all required primary and external reference materials for Chapter 04, organized prior to chapter authoring to ensure zero omission and rigorous pedagogical grounding.

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

## 2. Intuitive Masterclasses & Visual Walkthroughs
- Christopher Olah (colah's blog): ["Understanding LSTM Networks" (2015)](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
  - **Why it matters**: The undisputed gold standard visual explanation of recurrent cell mechanics.
  - **Key contribution**: Dissects the LSTM cell state into an intuitive "conveyor belt" (the Constant Error Carousel) modulated by pointwise multiplications via the forget, input, candidate ($\tilde{C}_t$), and output gates. Also illustrates GRUs.
- Andrej Karpathy: ["The Unreasonable Effectiveness of Recurrent Neural Networks" (2015)](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)
  - **Why it matters**: Demonstrates character-level RNNs, autoregressive sampling, and temperature scaling.
  - **Key insights**: Visualizes individual hidden state neurons operating as interpretable linguistic finite-state machines (e.g., cells that activate specifically inside quotation marks, track indentation depth, or monitor URL structures).
  - **Companion code**: [min-char-rnn.py](https://gist.github.com/karpathy/d4dee566867f8291f086) — A pure 112-line NumPy implementation with explicit manual forward pass and BPTT backpropagation.
- Denny Britz (WildML): ["Recurrent Neural Networks Tutorial" (Parts 1–4)](http://www.wildml.com/2015/09/recurrent-neural-networks-tutorial-part-1-introduction-to-rnns/)
  - **Why it matters**: Walks through the exact matrix calculus behind BPTT step-by-step, deriving $\frac{\partial L_t}{\partial W}$ across all time steps and showing why truncation is necessary.

## 3. Landmark Seminal Papers (Primary Ground Truth)
- **Origins & BPTT Formulation**:
  - Elman (1990): [Finding Structure in Time](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=10.1.1.157.9355) — Formulates the Simple Recurrent Network (SRN / Elman RNN).
  - Werbos (1990): [Backpropagation Through Time: What It Does and How to Do It](https://ieeexplore.ieee.org/document/58337) — Formalized gradient computation along the unfolded recurrent graph.
- **The Vanishing / Exploding Gradient Proofs**:
  - Bengio, Simard, & Frasconi (1994): [Learning Long-Term Dependencies with Gradient Descent is Difficult](https://ieeexplore.ieee.org/document/279181) — The foundational theoretical proof that the spectral radius of the transition matrix causes gradient decay over temporal horizons.
  - Pascanu, Mikolov, & Bengio (2013): [On the Difficulty of Training Recurrent Neural Networks](https://proceedings.mlr.press/v28/pascanu13.html) — Provides the modern Jacobian matrix product proof ($\prod_{k=t+1}^T \frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}}$) and introduces gradient clipping by norm.
- **Gated Architectures & Sequence-to-Sequence**:
  - Hochreiter & Schmidhuber (1997): [Long Short-Term Memory](https://www.bioinf.jku.at/publications/photocopies/pub-hochreiter-1997.pdf) — Introduces the Constant Error Carousel (CEC), demonstrating how additive memory updates enforce $\frac{\partial \mathbf{C}_t}{\partial \mathbf{C}_{t-1}} = \mathbf{I}$.
  - Cho et al. (2014): [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) — Introduces the Gated Recurrent Unit (GRU) and RNN Encoder-Decoder.
  - Sutskever, Vinyals, & Le (2014): [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) — Introduces multi-layer LSTM sequence-to-sequence translation and the source-reversal trick.
  - Bahdanau, Cho, & Bengio (2014): [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) — Solves the fixed-length vector bottleneck of RNN encoders using Additive Soft Attention, leading directly to the Transformer.

## 4. University Video Lectures
- **Stanford CS224n (Natural Language Processing with Deep Learning)**:
  - Lecture 6: Language Models and Recurrent Neural Networks (Christopher Manning & Abigail See). Focuses on RNN language models, perplexity, and gradient dynamics.
- **Stanford CS231n (Deep Learning for Computer Vision)**:
  - Lecture 10: Recurrent Neural Networks (Justin Johnson / Andrej Karpathy). Visualizes computational graphs, unrolling in time, and image captioning Seq2Seq architectures.
- **MIT 6.S191 (Introduction to Deep Learning)**:
  - Recurrent Neural Networks and Transformers (Alexander Amini). Visual animations of information flow and gate operations.

## 5. In This Workspace
You already have detailed materials synthesized in this repository:
- [`STUDY_GUIDE/lectures/chapters/part1_foundations/04_recurrent_neural_networks.tex`](../../lectures/chapters/part1_foundations/04_recurrent_neural_networks.tex): Chapter 4 of the course study guide, containing:
  - The transition from FCNNs to Elman RNNs.
  - The complete BPTT derivation and Jacobian product proof ($\prod_{k=j+1}^t \frac{\partial \mathbf{h}_k}{\partial \mathbf{h}_{k-1}}$).
  - The Sherlock Holmes character casing training dynamics experiment.
  - Mathematical equations and TikZ diagrams for LSTM gates (CEC) and GRUs.
  - The Seq2Seq information bottleneck that motivated Attention.
- [`slides/04-RNN.pdf`](slides/04-RNN.pdf): Course lecture slides (symlink to `SLIDES/04-RNN.pdf`).
- [`transcriptions/03-04-Word-Embeddings-And-RNNs.md`](transcriptions/03-04-Word-Embeddings-And-RNNs.md): Full lecture transcription (symlink to `TRANSCRIPTIONS/LECTURES/03-04-Word-Embeddings-And-RNNs.md`).
