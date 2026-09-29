# Sources Dossier: Chapter 02 (Deep Learning Foundations for NLP)

This directory houses all required primary and external reference materials for Chapter 02, organized prior to chapter authoring to ensure zero omission and rigorous pedagogical grounding.

## 1. Definitive Graduate Textbooks
- [Deep Learning](https://www.deeplearningbook.org/) (Ian Goodfellow, Yoshua Bengio, Aaron Courville — MIT Press, 2016)
  - **Chapter 6**: Deep Feedforward Networks
  - **Why it matters**: The gold-standard theoretical treatment of multi-layer perceptrons, cost functions, output units, and gradient-based learning.
  - **What it covers**: Linear stacking collapse proofs ($\mathbf{W}_2 \mathbf{W}_1 \mathbf{x} = \mathbf{W}' \mathbf{x}$), hidden units (ReLU, Sigmoid, Tanh), cross-entropy vs. MSE loss surfaces, computational graphs, and the backpropagation adjoint algorithm.
- [Dive into Deep Learning (D2L.ai)](https://d2l.ai/) (Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola)
  - **Chapter 4**: Multilayer Perceptrons
  - **Why it matters**: Pairs mathematical derivations with clean, working PyTorch code from scratch without high-level library abstractions.
  - **What it covers**: Activation function formulas and derivatives, vanishing/exploding gradients in MLPs, numerical stability, and weight initialization strategies.
- [Pattern Recognition and Machine Learning](https://www.microsoft.com/en-us/research/people/cmbishop/prml-book/) (Christopher M. Bishop — Springer, 2006)
  - **Chapter 5**: Neural Networks
  - **Why it matters**: In-depth probabilistic perspective on feedforward network training and maximum likelihood estimation.
  - **What it covers**: Network training as likelihood maximization under Gaussian vs. Bernoulli noise models, Hessian matrices, and regularization.
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) (Dan Jurafsky & James H. Martin — 3rd ed. draft)
  - **Chapter 7**: Neural Networks and Neural Language Models
  - **Why it matters**: Bridges feedforward neural network mechanics with natural language processing pipelines and classification objectives.
  - **What it covers**: Computational graphs, forward inference, cross-entropy loss formulation, and backpropagation for classification.

## 2. Intuitive Masterclasses & Visual Walkthroughs
- Andrej Karpathy: ["The spelled-out intro to neural networks and backpropagation: building micrograd" (2022)](https://karpathy.github.io/)
  - **Why it matters**: The ultimate mechanistic walkthrough of automatic differentiation and backpropagation.
  - **Key insights**: Implements a scalar-valued reverse-mode autograd engine in ~160 lines of pure Python, builds computational DAGs dynamically, topologically sorts graph nodes, and accumulates adjoint gradients (`out.grad += ...`).
  - **Companion code**: [`micrograd` repository](https://github.com/karpathy/micrograd) (`engine.py`: 98 LOC autograd engine, `nn.py`: 62 LOC neural network layers in pure Python).
- 3Blue1Brown (Grant Sanderson): ["Neural Networks Series (Chapters 1–4)" (2017)](https://www.3blue1brown.com/)
  - **Why it matters**: Unsurpassed geometric visualization of high-dimensional optimization surfaces and backpropagation calculus.
  - **Key insights**: Visualizes neural networks as space-warping manifolds, gradient descent as rolling down high-dimensional valleys, and backpropagation as the recursive application of the multivariable chain rule.
- Denny Britz (WildML): ["Speeding up Deep Learning: Implementing a Neural Network from Scratch in Python and NumPy" (2015)](http://www.wildml.com/2015/09/implementing-a-neural-network-from-scratch/)
  - **Why it matters**: Translates scalar autograd intuition into vectorized matrix calculus for dense layers.
  - **Key insights**: Vectorized matrix gradient equations $\frac{\partial \mathcal{L}}{\partial \mathbf{W}} = \mathbf{x} \bm{\delta}^\top$, batch Jacobian transformations, and classification decision boundaries in NumPy (~120 LOC).

## 3. Landmark Seminal Papers (Primary Ground Truth)
- **Origins of Neural Learning & Backpropagation**:
  - Rosenblatt, F. (1958): [The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain](https://doi.org/10.1037/h0042519) — Formulates the single-layer perceptron and linear threshold boundary:
    - Decision hyperplane: $y = f(\mathbf{w}^\top \mathbf{x} + b)$ where $f(z) = \mathbf{1}_{z \ge 0}$
    - Perceptron learning rule: $\mathbf{w} \leftarrow \mathbf{w} + \eta (y^* - y) \mathbf{x}$
    - Linear separability limit: Inability to compute XOR (Minsky & Papert, 1969)
  - Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986): [Learning representations by back-propagating errors](https://doi.org/10.1038/323533a0) — Demonstrates efficient generalized backpropagation through multi-layer hidden representations:
    - Adjoint error recursion: $\delta_j = \frac{\partial \mathcal{L}}{\partial z_j} = \sigma'(z_j) \sum_{k \in \operatorname{downstream}(j)} w_{kj} \delta_k$
    - Weight gradient: $\frac{\partial \mathcal{L}}{\partial w_{ji}} = \delta_j a_i$
    - Vectorized matrix adjoint form: $\frac{\partial \mathcal{L}}{\partial \mathbf{W}} = \mathbf{x} \bm{\delta}^\top, \quad \frac{\partial \mathcal{L}}{\partial \mathbf{x}} = \mathbf{W} \bm{\delta}$
- **Universal Approximation Theorems**:
  - Cybenko, G. (1989): [Approximation by superpositions of a sigmoidal function](https://doi.org/10.1007/BF02551274) — Rigorous proof that a single hidden layer with continuous sigmoidal activations can approximate any continuous function on a compact subset $I_n = [0, 1]^n$:
    - Uniform approximation bound: $\forall \epsilon > 0, \; \sup_{\mathbf{x} \in I_n} \left| \sum_{i=1}^N \alpha_i \sigma(\mathbf{w}_i^\top \mathbf{x} + b_i) - g(\mathbf{x}) \right| < \epsilon$
  - Hornik, K., Stinchcombe, M., & White, H. (1989): [Multilayer feedforward networks are universal approximators](https://doi.org/10.1016/0893-6080(89)90020-8) — Generalizes Cybenko to arbitrary non-constant, bounded continuous activation functions $\sigma$, establishing that multilayer feedforward architectures are universal approximators under the supremum metric.
- **Modern Activations & Optimization Frontiers**:
  - Glorot, X., & Bengio, Y. (2010): [Understanding the difficulty of training deep feedforward neural networks](http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf) — Introduces Xavier/Glorot initialization to preserve activation and gradient variance across deep layers:
    - Variance preservation condition: $\text{Var}(W) = \frac{2}{n_{\text{in}} + n_{\text{out}}}$
    - Uniform sampling range: $W \sim \mathcal{U}\left(-\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}, +\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}\right)$
  - Hendrycks, D., & Gimpel, K. (2016): [Gaussian Error Linear Units (GELUs)](https://arxiv.org/abs/1606.08415) — Introduces smooth non-monotonic stochastic regularized activations adopted by modern LLMs:
    - Definition: $\text{GELU}(x) = x \Phi(x) = x P(X \le x), \quad X \sim \mathcal{N}(0, 1)$
    - Analytic approximation: $\text{GELU}(x) \approx 0.5x \left(1 + \tanh\left(\sqrt{\frac{2}{\pi}} \left(x + 0.044715 x^3\right)\right)\right)$
  - Kingma, D. P., & Ba, J. (2014): [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — Adaptive moment estimation with first and second moment bias correction:
    - First moment: $m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \quad \hat{m}_t = \frac{m_t}{1 - \beta_1^t}$
    - Second moment: $v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$
    - Parameter update: $\theta_t = \theta_{t-1} - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$

## 4. University Video Lectures
- **Stanford CS231n (Deep Learning for Computer Vision)**:
  - Lecture 4: Introduction to Neural Networks & Backpropagation (Justin Johnson / Andrej Karpathy). Rigorous computational graphs, vectorized gradients, and modular layer implementation.
  - Lecture 6: Training Neural Networks I (Serena Yeung). Activation function pathology (saturated sigmoids, dying ReLUs) and weight initialization.
- **MIT 6.S191 (Introduction to Deep Learning)**:
  - Lecture 1: Deep Learning Foundations (Alexander Amini). Perceptrons, activation non-linearities, loss landscapes, and backpropagation flow.

## 5. In This Workspace
You already have detailed materials synthesized in this repository:
- [`STUDY_GUIDE/lectures/chapters/part1_foundations/02_deep_learning_foundations.tex`](../../lectures/chapters/part1_foundations/02_deep_learning_foundations.tex): Chapter 2 of the course study guide, containing:
  - The artificial perceptron and 2D hyperplane decision boundary diagram.
  - Fully connected linear layers with explicit matrix formulations ($\mathbf{y} = \mathbf{W}^\top \mathbf{x} + \mathbf{b}$).
  - Mathematical proof of the linear stacking collapse.
  - Exact PGFPlots curves for Sigmoid, Tanh, ReLU, Leaky ReLU, GELU, and Softmax.
  - Rigorous formulation and intuitive bump-function proof of the Universal Approximation Theorem.
  - Comparative analysis of MSE, BCE, and CCE loss functions.
  - Computational graphs and adjoint backpropagation step-by-step.
- **Empirical Lecture Experiments**:
  - **Single-Point Numerical Backpropagation Worked Example**: Lecture 02 slide 23 works through an exact numerical arithmetic calculation for a single training observation $(x, y)$ with weights $\theta_1, \theta_2$. Traces forward activation propagation, scalar squared error calculation, and the exact chain rule partial derivative steps ($\frac{\partial \mathcal{L}}{\partial \theta_1}, \frac{\partial \mathcal{L}}{\partial \theta_2}$), connecting abstract multivariable calculus directly to numeric parameter updates.
  - **Geometric XOR Linear Inseparability**: Slide 12 illustrates the geometric failure of a single linear hyperplane to separate $(0,0), (1,1)$ (class 0) from $(0,1), (1,0)$ (class 1), proving why multi-layer non-linear stacking is strictly mandatory to fold the coordinate space.
- [`slides/02-DL-Intro.pdf`](slides/02-DL-Intro.pdf): Course lecture slides (symlink to `SLIDES/02-DL-Intro.pdf`).
- [`transcriptions/NOTE_TRANSCRIPTION_UNAVAILABLE.md`](transcriptions/NOTE_TRANSCRIPTION_UNAVAILABLE.md): Documentation note detailing that Lecture 02 was delivered live without a recorded Whisper audio transcript.
