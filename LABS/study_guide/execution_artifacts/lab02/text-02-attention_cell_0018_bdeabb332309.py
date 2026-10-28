class AttentionHead(nn.Module):
    def __init__(self, d_model, seq_len, other_positional_encodings_present):
        """
        Initializes the AttentionHead.

        Args:
        - d_model (int): The dimensionality of the input and output features.
        - seq_len (int): The length of the input sequence.
        - other_positional_encodings_present (bool): Whether other positional encodings are being used.
        
        Notes:
        - This class uses the Scaled Dot-Product Attention mechanism to compute attention.
        - It also applies linear transformations to the query, key, and value matrices.
        """
        super(AttentionHead, self).__init__()
        self.d_k = d_model
        self.seq_len = seq_len

        # Define linear layers for query, key, and value
        self.query_layer = nn.Linear(d_model, d_model)
        self.key_layer = nn.Linear(d_model, d_model)
        self.value_layer = nn.Linear(d_model, d_model)

        # Define the scaled dot-product attention mechanism
        self.scaled_dot_attention = ScaledDotProductAttention(self.seq_len, self.d_k, other_positional_encodings_present)

        # Define the final output linear layer
        self.fc_out = nn.Linear(d_model, d_model)

    def forward(self, query, key, value):
        """
        Computes the attention output and weights.

        Args:
        - query: The query matrix (shape: [batch_size, seq_len, d_model]).
        - key: The key matrix (shape: [batch_size, seq_len, d_model]).
        - value: The value matrix (shape: [batch_size, seq_len, d_model]).
        
        Returns:
        - output: The final output after applying attention.
        - attention_weights: The attention weights for each query/key pair.
        """
        
        # Apply the linear transformations to the query, key, and value matrices
        Q = self.query_layer(query)
        K = self.key_layer(key)
        V = self.value_layer(value)

        # Apply the scaled dot-product attention mechanism
        attention_output, attention_weights = self.scaled_dot_attention(Q, K, V)

        # Squeeze the attention output and pass it through the final linear layer
        output = self.fc_out(attention_output)

        return output, attention_weights
