# Chapter 06: A Brief History of Large Language Models, Pre-training Paradigms, and Scaling Laws
## Autonomous 5-Part Knowledge Retrieval & Triangulation Dossier

This dossier establishes the authoritative foundation for Chapter 06 of the Master's Study Guide in *Large Language Models for Software Engineering* (Politecnico di Torino), taught by Prof. Flavio Giobergia and Prof. Riccardo Coppola.

---

## 1. Definitive Graduate Textbooks

### 1.1 Jurafsky & Martin (3rd ed. draft, 2024) — *Speech and Language Processing*
- **Chapters**:
  - Chapter 10: *Large Language Models and Autoregressive Decoding* (Sections 10.1--10.6)
  - Chapter 11: *Prompting, In-Context Learning, and Instruction Tuning* (Sections 11.1--11.4)
- **Official URL**: [https://web.stanford.edu/~jurafsky/slp3/](https://web.stanford.edu/~jurafsky/slp3/)
- **Why It Matters**: Provides standard formalisms for causal language modeling (CLM), negative log-likelihood cross-entropy objectives, greedy vs. stochastic sampling strategies, subword vocabulary tokenization dynamics, and prompt formatting for in-context learning.
- **What It Covers**:
  - Unrolled causal language model objective: $\mathcal{L}_{\text{CLM}}(\theta) = -\frac{1}{T} \sum_{t=1}^T \log P_\theta(w_t \mid w_{<t})$.
  - Mathematical formalization of zero-shot, one-shot, and few-shot conditioning: $P(y \mid x, \mathcal{D}_{\text{demo}})$.
  - Analysis of pre-training corpora scale and the shift from task-specific fine-tuning heads to universal text-to-text generation.

### 1.2 Simon J.D. Prince (2023) — *Understanding Deep Learning* (MIT Press)
- **Chapters**:
  - Chapter 12: *Language Models* (Sections 12.1--12.8)
  - Chapter 13: *Scaling, Pre-training, and Fine-Tuning* (Sections 13.1--13.5)
- **Official URL**: [https://udlbook.github.io/udlbook/](https://udlbook.github.io/udlbook/)
- **Why It Matters**: Delivers a mathematically rigorous, first-principles derivation of empirical scaling laws, parameter counts, FLOP compute estimation, and the analytical derivation of the Chinchilla compute-optimal frontier.
- **What It Covers**:
  - Floating-point operation (FLOP) count for standard Transformer forward-backward passes: $C \approx 6 N D$.
  - Constrained optimization of power-law loss models under compute budget constraints.
  - Architectural balance between embedding dimension $d_{\text{model}}$, layer count $L$, and attention heads $h$.

### 1.3 Zhang, Lipton, Li, & Smola (2023) — *Dive into Deep Learning (D2L.ai)*
- **Chapters**:
  - Chapter 11: *Attention Mechanisms and Transformers*
  - Chapter 15: *Natural Language Processing: Pretraining*
- **Official URL**: [https://d2l.ai/](https://d2l.ai/)
- **Why It Matters**: Detailed tensor algebra, attention masking implementations, causal masking matrices, and loss backpropagation mechanics.
- **What It Covers**:
  - Pre-training vs. fine-tuning computational graphs.
  - Practical considerations in large-scale dataset filtering and batch sampling.

---

## 2. Intuitive Masterclasses & Visual Walkthroughs

### 2.1 Andrej Karpathy (2023) — *Let's build GPT: from scratch, in code, spelled out*
- **Official URL**: [https://www.youtube.com/watch?v=kCc8FmEb1nY](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- **Why It Matters**: Unpacks the minimal causal decoder architecture, demonstrating why masked multi-head attention operates autoregressively without encoder or cross-attention layers.
- **Key Insights**:
  - The causal mask $\mathbf{M}_{\text{causal}}$ ensures token $t$ only computes dot-products with keys $k \le t$.
  - Weight sharing between token embeddings and the final unembedding projection layer.
  - The simplicity of next-token prediction: scaling simple objectives with large compute and data generates complex emergent behavior.

### 2.2 Andrej Karpathy (2023) — *State of GPT* (Microsoft Build 2023)
- **Official URL**: [https://www.youtube.com/watch?v=bZQun8Y4L2A](https://www.youtube.com/watch?v=bZQun8Y4L2A)
- **Why It Matters**: Maps the modern 4-stage pipeline of LLM training: (1) Pre-training (base models, compute-heavy), (2) Supervised Fine-Tuning (SFT / instruction tuning), (3) Reward Modeling (RM), and (4) Reinforcement Learning from Human Feedback (RLHF / PPO / DPO).
- **Key Insights**:
  - Base models are token-prediction engines, not assistants; prompting strategies (shots) orient them toward downstream tasks.
  - Compute allocation: $\approx 99\%$ of total training compute is spent on pre-training.

### 2.3 Lilian Weng (2023) — *Large Language Model Pre-training & Inference Optimization*
- **Official URLs**:
  - [https://lilianweng.github.io/posts/2023-01-10-inference-optimization/](https://lilianweng.github.io/posts/2023-01-10-inference-optimization/)
  - [https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- **Why It Matters**: Comprehensive analytical summaries of scaling law papers, compute budgets, and memory bottlenecks.

---

## 3. Landmark Seminal Research Papers

### 3.1 Foundations of the GPT Family (Decoder-Only Pre-training)
1. **GPT-1**: Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018). *Improving Language Understanding by Generative Pre-Training*. OpenAI Technical Report.
   - *Architecture*: 12 layers, 12 heads, $d_{\text{model}} = 768$, 117M parameters, 512 context length, BPE with 40,000 merges.
   - *Training*: BooksCorpus (7,000 unpublished books, $\approx 5\text{ GB}$ of text).
   - *Methodology*: Semi-supervised learning: unsupervised pre-training via next-token prediction followed by supervised fine-tuning on task-specific classification heads.
2. **GPT-2**: Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). *Language Models are Unsupervised Multitask Learners*. OpenAI Blog, 1(8), 9.
   - *Architecture*: Up to 48 layers, 1.5B parameters, 1024 context length, BPE with 50,257 tokens, pre-layer normalization (Pre-LN).
   - *Training*: WebText ($\approx 40\text{ GB}$, 45M outbound links from Reddit posts with $\ge 3$ upvotes).
   - *Core Breakthrough*: **Zero fine-tuning**. Unsupervised multitask learning: conditioned on prompt text, the model demonstrates emergent zero-shot capabilities across translation, summarization, and question answering.
3. **GPT-3**: Brown, T., Mann, B., Ryder, N., Subbiah, M., et al. (2020). *Language Models are Few-Shot Learners*. NeurIPS 2020. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165).
   - *Architecture*: 96 layers, 96 heads, $d_{\text{model}} = 12{,}288$, 175B parameters, 2048 context length, alternating dense and locally banded sparse attention.
   - *Dataset Mixture*: Filtered Common Crawl (410B tokens, 570GB filtered from 45TB), WebText2 (19B tokens), Books1 (12B tokens), Books2 (55B tokens), Wikipedia (3B tokens), total 300B training tokens.
   - *Core Breakthrough*: **In-Context Learning (ICL)**. Parity with or superiority over fine-tuned state-of-the-art models without any gradient updates ($\nabla_\theta = \mathbf{0}$) using zero-shot, one-shot, and few-shot prompts.

### 3.2 Empirical Scaling Laws and the Compute-Optimal Correction
1. **Kaplan Scaling Laws**: Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., et al. (2020). *Scaling Laws for Neural Language Models*. [arXiv:2001.08361](https://arxiv.org/abs/2001.08361).
   - *Empirical Formulations*:
     $$L(N) = \left(\frac{N_c}{N}\right)^{\alpha_N}, \quad L(D) = \left(\frac{D_c}{D}\right)^{\alpha_D}, \quad L(C) = \left(\frac{C_c}{C}\right)^{\alpha_C}$$
   - *Compute Allocation Conclusion*: Given compute budget $C$, scale parameters heavily while scaling dataset size slowly:
     $$N \propto C^{0.73}, \quad D \propto C^{0.27}$$
   - *Historical Impact*: Triggered an industry race toward oversized models (Gopher 280B, Megatron-Turing 530B, PaLM 540B) trained on fixed token budgets ($\approx 300\text{B}$ tokens).
2. **Chinchilla Compute-Optimal Correction**: Hoffmann, J., Borgeaud, S., Mensch, A., Sifre, L., et al. (DeepMind, March 2022). *Training Compute-Optimal Large Language Models*. [arXiv:2203.15556](https://arxiv.org/abs/2203.15556).
   - *Central Claim*: Previous models were **severely oversized and undertrained**.
   - *Compute Formulation*: $C \approx 6 N D$. Under optimal learning rate schedules, parameters and tokens should scale in **equal proportion**:
     $$N_{\text{opt}} \propto \sqrt{C}, \quad D_{\text{opt}} \propto \sqrt{C}$$
   - *Three Analytical Approaches*:
     - **Approach 1 (Empirical Minima)**: Evaluate learning curves of fixed-size models across varying compute budgets, finding parameter size that minimizes loss for each FLOP tier.
     - **Approach 2 (IsoFLOP Profiles)**: Fix compute budget $C$ and train varying parameter sizes $N$, fitting a quadratic parabola on $L(N)$ to locate vertex minimum $\operatorname{argmin}_N L(N)$.
     - **Approach 3 (Parametric 2D Loss Fitting)**: Fit the joint surface $L(N, D) = E + \frac{A}{N^\alpha} + \frac{B}{D^\beta}$ using L-BFGS, yielding $\alpha \approx 0.34, \beta \approx 0.28$, resulting in $a = \frac{\beta}{\alpha+\beta} \approx 0.45, b = \frac{\alpha}{\alpha+\beta} \approx 0.55$.
   - *Chinchilla 70B Demonstration*: Trained on the exact compute budget of Gopher 280B ($5.76 \times 10^{23}$ FLOPs), Chinchilla has $1/4$ the parameters (70B vs 280B) but $4\times$ the tokens (1.4T vs 300B), uniformly outperforming Gopher, GPT-3, Jurassic-1, and MT-NLG.

### 3.3 The Race to Scale (Oversized Pre-Chinchilla Models)
1. **Jurassic-1**: Lieber, O., Sharir, O., Lenz, B., & Shoham, Y. (AI21 Labs, 2021). 178B parameters, 250K vocabulary.
2. **Gopher**: Rae, J. W., Borgeaud, S., Cai, T., et al. (DeepMind, Dec 2021). *Scaling Language Models: Methods, Analysis & Insights from Training Gopher*. 280B parameters, 300B tokens, 120-page comprehensive evaluation.
3. **Megatron-Turing NLG**: Smith, S., Patwary, M., Norick, B., et al. (Microsoft & NVIDIA, 2021). 530B parameters, 270B tokens.
4. **PaLM**: Chowdhery, A., Narang, S., Devlin, J., et al. (Google, 2022). *PaLM: Scaling Language Modeling with Pathways*. 540B parameters, Pathways TPU v4 architecture.

### 3.4 The Open-Weights Revolution and Modern Post-Chinchilla Architectures
1. **LLaMA Series (Meta AI)**:
   - Touvron, H., et al. (Feb 2023). *LLaMA: Open and Efficient Foundation Language Models*. [arXiv:2302.13971](https://arxiv.org/abs/2302.13971). 7B, 13B, 33B, 65B; trained intentionally beyond the Chinchilla optimal point (1T--1.4T tokens) to optimize downstream inference latency. Architectural enhancements: RMSNorm, SwiGLU activations, Rotary Position Embeddings (RoPE).
   - Touvron, H., et al. (Jul 2023). *Llama 2: Open Foundation and Fine-Tuned Chat Models*. 7B, 13B, 70B; 2T tokens, Grouped-Query Attention (GQA).
   - Dubey, A., et al. (Meta AI, 2024). *The Llama 3 Herd of Models*. 8B, 70B, 405B; 15T tokens, 128K context window, 405B dense flagship model.
2. **Mistral AI**:
   - Jiang, A. Q., et al. (2023). *Mistral 7B*. Sliding Window Attention (SWA), GQA, outperforming Llama 2 13B.
3. **Falcon**:
   - Almazrouei, E., et al. (TII, 2023). *The Falcon Series of Language Models*. Multiquery attention, RefinedWeb dataset.

---

## 4. Top University Video Lectures

1. **Stanford CS224n (Prof. Christopher Manning & John Hewitt)**:
   - Lecture 8: *Transformers and Pre-training*
   - Lecture 9: *Large Language Models, Scaling Laws, and In-Context Learning*
2. **MIT 6.S191 (Prof. Alexander Amini)**:
   - Lecture 2: *Recurrent Neural Networks and Transformers*
   - Lecture 7: *Foundation Models and Generative AI*
3. **Stanford CS25 (Transformers United)**:
   - Seminar on *Scaling Laws and Chinchilla Compute Optimality*

---

## 5. In This Workspace

- **Slide Deck**: `SLIDES/06-LLM-History.pdf` (26 slides, Prof. Flavio Giobergia).
  - Slides 1--5: GPT-1 architecture, unsupervised pre-training, supervised fine-tuning.
  - Slides 6--7: GPT-2 architecture, WebText, zero fine-tuning, emergent multitask execution.
  - Slides 8--9: Kaplan et al. (2020) scaling laws, power laws, parameter-heavy compute allocation.
  - Slides 10--13: GPT-3 (175B), In-Context Learning (zero, one, few-shot), dataset mixtures.
  - Slides 14--15: The race to larger models (Jurassic-1, Gopher 280B, MT-NLG 530B, PaLM 540B).
  - Slides 16--22: Chinchilla paper breakdown, oversized/undertrained critique, 3 approaches to compute optimality, $N \propto \sqrt{C}, D \propto \sqrt{C}$.
  - Slides 23--26: Shift back to smaller models trained on more tokens, open-weights ecosystem (LLaMA 1/2/3, Mistral, Falcon, GLM).
- **Lecture Video**: `~/Downloads/Portale della Didattica - Pagina del Corso.mp4` (Duration: 01:19:11).
- **Target Transcript**: `STUDY_GUIDE/TRANSCRIPTIONS/LECTURES/06-LLM-History-II.md`.
- **Target LaTeX Chapter**: `STUDY_GUIDE/lectures/chapters/part1_foundations/06_scaling_laws_pretraining.tex`.
- **Integration Architecture**:
  - Modular hybrid architecture:
    - *Part 1 (Interpolated)*: Fully reconstructed with academic rigor from slides 1--13, seminal papers (GPT-1/2/3, Kaplan), and textbooks. Structured with clean modularity so that when the recording for Part 1 is provided, it can be seamlessly refined.
    - *Part 2 (Spoken Lecture Ground Truth)*: Ingested line-by-line from the transcription of `06-LLM-History-II.md`, capturing Prof. Giobergia's exact pacing, insights, analogies, and student Q&A.
