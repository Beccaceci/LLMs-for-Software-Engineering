class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        
        # Create a matrix of shape (max_len, d_model) to hold the positional encodings
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        # Compute sine and cosine positional encodings
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)  # Apply sine to even indices in the encoding
        pe[:, 1::2] = torch.cos(position * div_term)  # Apply cosine to odd indices in the encoding
        
        pe = pe.unsqueeze(0).transpose(0, 1)  # Reshape for batch compatibility
        self.register_buffer('pe', pe)  # Register pe as a buffer so it doesn't get updated during backpropagation

    def forward(self, x):
        # Add positional encoding to the input
        return x + self.pe[:x.size(0), :].repeat(1,x.shape[1],1)