import torch
import torch.nn as nn

# Define the Scaled Dot-Product Attention Mechanism
class ScaledDotProductAttention(nn.Module):
    def __init__(self, seq_len, d_k, other_positional_encodings_present):
        super(ScaledDotProductAttention, self).__init__()

        self.d_k = d_k
        self.seq_len = seq_len
        self.other_positional_encodings_present = other_positional_encodings_present

        self.rel_layer = torch.randn(1, self.seq_len, self.seq_len, requires_grad=True) # Create a learnable relative positional encoding

    def forward(self, query, key, value):
        # Compute the attention scores: (Q * K^T) / sqrt(d_k)
        scores = torch.matmul(query, key.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.d_k, dtype=torch.float32)) # Scaled Dot-Product
        
        # Add relative positional encodings if no other positional encodings are present: scores + rel_layer
        if not self.other_positional_encodings_present:
            scores = scores + self.rel_layer
        
        # Compute the attention weights: softmax(scores + rel_layer)
        attention_weights = torch.softmax(scores, dim=-1)
        
        # Compute the output: output = attention_weights * V
        output = torch.matmul(attention_weights, value)
        
        return output, attention_weights