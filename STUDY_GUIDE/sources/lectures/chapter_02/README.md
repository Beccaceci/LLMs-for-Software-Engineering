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

## 2. Intuitive Masterclasses & Visual Walkthroughs
- Andrej Karpathy: ["The spelled-out intro to neural networks and backpropagation: building micrograd" (2022)](https://karpathy.github.io/)
  - **Why it matters**: The ultimate mechanistic walkthrough of automatic differentiation and backpropagation.
  - **Key insights**: Implements a scalar-valued reverse-mode autograd engine in ~100 lines of pure Python, builds computational DAGs dynamically, topologically sorts graph nodes, and accumulates adjoint gradients (`out.grad += ...`).
  - **Companion code**: [`micrograd`](https://github.com/karpathy/micrograd) — A tiny scalar-valued autograd engine with a PyTorch-like API.
- 3Blue1Brown (Grant Sanderson): ["Neural Networks Series (Chapters 1–4)" (2017)](https://www.3blue1brown.com/)
  - **Why it matters**: Unsurpassed geometric visualization of high-dimensional optimization surfaces and backpropagation calculus.
  - **Key insights**: Visualizes neural networks as space-warping manifolds, gradient descent as rolling down high-dimensional valleys, and backpropagation as the recursive application of the multivariable chain rule.

## 3. Landmark Seminal Papers (Primary Ground Truth)
- **Origins of Neural Learning & Backpropagation**:
  - Rosenblatt, F. (1958): [The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain](https://doi.org/10.1037/h0042519) — Formulates the single-layer perceptron and linear threshold boundary.
  - Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986): [Learning representations by back-propagating errors](https://doi.org/10.1038/323533a0) — Demonstrates efficient generalized backpropagation through multi-layer hidden representations.
- **Universal Approximation Theorems**:
  - Cybenko, G. (1989): [Approximation by superpositions of a sigmoidal function](https://doi.org/10.1007/BF02551274) — Rigorous proof that a single hidden layer with continuous sigmoidal activations can approximate any continuous function on a compact subset of $\mathbb{R}^n$.
  - Hornik, K., et al. (1989): [Multilayer feedforward networks are universal approximators](https://doi.org/10.1016/0893-6080(89)90020-8) — Generalizes Cybenko to arbitrary non-constant, bounded activation functions.
- **Modern Activations & Optimization Frontiers**:
  - Glorot, X., & Bengio, Y. (2010): [Understanding the difficulty of training deep feedforward neural networks](http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf) — Introduces Xavier/Glorot initialization to stabilize variance across deep linear layers.
  - Kingma, D. P., & Ba, J. (2014): [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — Adaptive moment estimation with first and second moment bias correction.
  - Hendrycks, D., & Gimpel, K. (2016): [Gaussian Error Linear Units (GELUs)](https://arxiv.org/abs/1606.08415) — Introduces smooth non-monotonic stochastic regularized activations adopted by modern LLMs (BERT, GPT).

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
- [`slides/02-DL-Intro.pdf`](slides/02-DL-Intro.pdf): Course lecture slides (symlink to `SLIDES/02-DL-Intro.pdf`).
