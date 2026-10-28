# Define a basic Transformer Encoder block
class TransformerEncoderBlock(nn.Module):
    def __init__(self, d_model, dim_feedforward, seq_len, other_positional_encodings_present, dropout=0.1):
        '''
        Initializes a basic Transformer Encoder block.

        Args:
        - d_model (int): The dimensionality of the input and output features.
        - dim_feedforward (int): The dimensionality of the feedforward network.
        - seq_len (int): The length of the input sequence.
        - other_positional_encodings_present (bool): Whether other positional encodings are being used.
        - dropout (float): The dropout probability.

        Notes:
        - This class uses the AttentionHead defined above.
        '''
        super(TransformerEncoderBlock, self).__init__()
        self.attention = AttentionHead(d_model, seq_len, other_positional_encodings_present)
        self.norm1 = nn.LayerNorm(d_model)

        # Define the second layer normalization
        self.norm2 = nn.LayerNorm(d_model)

        # Feed-forward network
        self.ffn = nn.Sequential(
            nn.Linear(d_model, dim_feedforward),
            nn.ReLU(),
            nn.Linear(dim_feedforward, d_model)
        )

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        '''
        Passes the input through the Transformer Encoder block.

        Args:
        - x: The input tensor (shape: [batch_size, seq_len, d_model]).

        Returns:
        - output: The output tensor (shape: [batch_size, seq_len, d_model]).
        - attention_weights: The attention weights for each query/key pair.
        '''

        # Attention head
        attention_output, attention_weights = self.attention(x, x, x)
        x = self.norm1(x + self.dropout(attention_output))

        # Pass the output through the feed-forward network
        ffn_output = self.ffn(x)

        # Apply the second layer normalization with the residual connection
        output = self.norm2(x + self.dropout(ffn_output))

        return output, attention_weights