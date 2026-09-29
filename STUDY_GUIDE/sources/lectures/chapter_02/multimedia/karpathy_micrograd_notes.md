# Multimedia Reference Notes: Chapter 02 (Andrej Karpathy, 3Blue1Brown, Denny Britz)

This document synthesizes key pedagogical takeaways, code architectures, and visual intuition from educational multimedia integrated into Chapter 02.

---

## 1. Andrej Karpathy: "The Spelled-Out Intro to Neural Networks and Backpropagation" (micrograd)
- **Source Video**: *The spelled-out intro to neural networks and backpropagation: building micrograd* (2022).
- **Companion Code**: [`micrograd`](https://github.com/karpathy/micrograd) (`engine.py`: 98 LOC autograd engine, `nn.py`: 62 LOC neural network layers in pure Python).
- **Core Insights & Mechanics**:
  1. *The `Value` Data Structure*:
     - Encapsulates scalar data `self.data` alongside its accumulating adjoint gradient `self.grad`.
     - Maintains references to previous operand nodes in `self._prev` (children of the computational graph) and the operation that created the node `self._op`.
  2. *Reverse-Mode Automatic Differentiation via Closures*:
     - For multiplication $z = x \cdot y$:
       $$\frac{\partial \mathcal{L}}{\partial x} = \frac{\partial \mathcal{L}}{\partial z} \cdot y, \quad \frac{\partial \mathcal{L}}{\partial y} = \frac{\partial \mathcal{L}}{\partial z} \cdot x$$
     - Implemented in `_backward()` lambda:
       ```python
       def _backward():
           self.grad += other.data * out.grad
           other.grad += self.data * out.grad
       out._backward = _backward
       ```
     - Accumulating with `+=` correctly handles variables with multiple fan-outs (multivariable chain rule sum over paths).
  3. *Topological DAG Sorting*:
     - Gradients must propagate strictly in reverse topological order.
     - A depth-first search (DFS) builds an ordered list of nodes ensuring every child node completes its `.backward()` pass before its parents are invoked.
  4. *Neuron, Layer, and MLP Scaffolding*:
     - Shows that an artificial neuron is simply a dot product of inputs and learnable weights plus bias, followed by a non-linearity like $\tanh$ or $\text{ReLU}$.

---

## 2. 3Blue1Brown (Grant Sanderson): Neural Networks Series (Chapters 1–4)
- **Source Videos**: *But what is a neural network?*, *Gradient descent, how neural networks learn*, *What is backpropagation really doing?*, *Backpropagation calculus* (2017).
- **Core Insights**:
  1. *Geometric Space-Warping*:
     - Visualizes layers as sequential coordinate transformations folding and stretching high-dimensional space so that non-linearly separable classes become linearly separable.
  2. *The Optimization Landscape*:
     - Casts parameter optimization as finding the global minimum on a cost surface with millions of dimensions.
     - Demonstrates why local gradient descent is effective and why saddle points and plateaus dominate high dimensions rather than local minima.
  3. *Intuitive Backpropagation Calculus*:
     - Explains the chain rule visually as a cascade of gear ratios: how much a small nudge in a synaptic weight $\Delta w$ alters the pre-activation $\Delta z$, which alters the activation $\Delta a$, which alters the cost $\Delta C$.

---

## 3. Denny Britz (WildML): Implementing a Neural Network from Scratch in Python and NumPy
- **Source Tutorial**: *Speeding up Deep Learning: Implementing a Neural Network from Scratch in Python and NumPy* (2015).
- **Core Insights**:
  1. *Transition from Scalar to Vectorized Autograd*:
     - Scalar autograd (like `micrograd`) is vital for pedagogical comprehension, but production deep learning relies on vectorized matrix operations.
  2. *Batch Vectorized Matrix Gradients*:
     - For input batch $\mathbf{X} \in \mathbb{R}^{B \times d_{\text{in}}}$, weights $\mathbf{W}_1 \in \mathbb{R}^{d_{\text{in}} \times d_h}$, and error adjoints $\bm{\delta}_1 \in \mathbb{R}^{B \times d_h}$:
       $$\frac{\partial \mathcal{L}}{\partial \mathbf{W}_1} = \mathbf{X}^\top \bm{\delta}_1 \in \mathbb{R}^{d_{\text{in}} \times d_h}$$
       $$\frac{\partial \mathcal{L}}{\partial \mathbf{b}_1} = \sum_{i=1}^B \bm{\delta}_{1, i} \in \mathbb{R}^{1 \times d_h}$$
       $$\bm{\delta}_1 = (\bm{\delta}_2 \mathbf{W}_2^\top) \odot \sigma'(\mathbf{Z}_1)$$
  3. *NumPy Acceleration*:
     - Demonstrates a complete 2-layer classifier in ~120 lines of NumPy running 100x faster than pure Python scalar loops, cleanly classifying the non-linear two-moons benchmark dataset.
