class LoRA(nn.Module):
    def __init__(self, original_layer, rank=8):
        super(LoRA, self).__init__()
        self.original_layer = original_layer
        self.rank = rank
        self.in_features = original_layer.in_features
        self.out_features = original_layer.out_features

        # Initialize the Low-rank matrices A and B
        self.A = nn.Parameter(torch.zeros(self.in_features, rank))
        self.B = nn.Parameter(torch.randn(size=(rank, self.out_features)))

    def forward(self, x):
        # The output is the original layer output plus the low-rank adaptation

        # LoRA output
        lora_output = (x @ self.A) @ self.B

        # layer output, which combines the original output with the LoRA one 
        return self.original_layer(x) + lora_output