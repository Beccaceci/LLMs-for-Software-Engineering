import torch
from torchviz import make_dot

# Define tensors with requires_grad=True to track operations
a = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(3.0, requires_grad=True)
c = torch.tensor(4.0, requires_grad=True)

# Define a function involving these tensors
y = (a*b*c+c)*c + b

# Visualize the computational graph
make_dot(y, params={"a": a, "b": b, "c": c})