input_size = 1  # Number of input features
seq_len = 40 # Length of the time series sequence

d_model = 64  # Embedding dimension
dim_feedforward = 256  # Feedforward network dimension
num_layers = 3  # Number of Transformer encoder layers

model = Transformer(input_size, d_model, dim_feedforward, num_layers, seq_len)