import torch
from torchviz import make_dot

# Define the tensors and compute the loss
# Define theta1, theta2, x, and y as tensors, then compute the loss
# Notes:
# - set theta1 = 2.0, theta2 = 3.0, x = 1.0, y = 3.0
# - the loss is defined as (theta1 * theta2 * x - y)^2
# - all the tensors should be specified to require gradients
theta1 = torch.tensor(2.0, requires_grad=True)
theta2 = torch.tensor(3.0, requires_grad=True)
x = torch.tensor(1.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)

loss = (theta1 * theta2 * x - y)**2

# Visualize the computational graph
make_dot(loss, params={'theta1': theta1, 'theta2': theta2, 'x': x, 'y': y})
