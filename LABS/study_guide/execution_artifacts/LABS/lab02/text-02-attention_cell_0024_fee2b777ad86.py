# Define a simple Transformer Model
class Transformer(nn.Module):
    def __init__(self, input_size, d_model, dim_feedforward, num_layers, seq_len, positional_encoding = None, dropout=0.1, max_len=5000):
        super(Transformer, self).__init__()

        self.positional_encoding = positional_encoding

        # Embedding for the time series input
        self.embedding = nn.Linear(input_size, d_model)
        
        # Positional encoding for time series data
        if self.positional_encoding is not None:
            self.pos_encoder = self.positional_encoding(d_model, max_len)
        
        # Transformer encoder layers
        self.encoder_layers = nn.ModuleList(
            [TransformerEncoderBlock(d_model, dim_feedforward, seq_len, False if positional_encoding is None else True, dropout) for _ in range(num_layers)]
        )
        
        # Output layer to predict a single value
        self.fc_out = nn.Linear(d_model, 1)

    def forward(self, x):
        # x shape: [batch_size, seq_len, input_size]
        
        # Embed the input time series data
        x = self.embedding(x)  # Shape: [batch_size, seq_len, d_model]    
        
        # Add positional encoding
        x = self.pos_encoder(x) if self.positional_encoding is not None else x
        
        # List to store attention weights from all layers
        all_attention_weights = []

        # Pass through each Transformer encoder layer
        for layer in self.encoder_layers:
            x, attention_weights = layer(x)
            all_attention_weights.append(attention_weights)

        # Apply final linear layer to get the output
        output = self.fc_out(x[:, -1])  # Take the output of the last time step (sequence regression)
        return output, all_attention_weights  # Return the final output and the attention weights