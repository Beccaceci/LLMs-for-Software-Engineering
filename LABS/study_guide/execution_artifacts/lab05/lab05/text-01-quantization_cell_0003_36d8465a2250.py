import torch

torch.random.manual_seed(0)

n_rows = 3
n_cols = 5

# TODO: Create two random tensors, W (of shape n_rows, n_cols) and x (of shape n_cols)
W = torch.randn(n_rows, n_cols)
x = torch.randn(n_cols)

W[0,0] = 0
x[0] = 0