class LoRA(nn.Module):
    def __init__(self, original_layer, rank=8):
        super(LoRA, self).__init__()
        self.original_layer = original_layer
        self.rank = rank
        self.in_features = original_layer.in_features
        self.out_features = original_layer.out_features

        # Match the standard LoRA initialization: A uses Kaiming uniform, B starts at zero.
        # Transposing A for initialization gives Kaiming's fan-in the input dimension.
        self.A = nn.Parameter(torch.empty(self.in_features, rank))
        nn.init.kaiming_uniform_(self.A.T, a=5 ** 0.5)
        self.B = nn.Parameter(torch.zeros(rank, self.out_features))

    def forward(self, x):
        # The output is the original layer output plus the low-rank adaptation

        # LoRA output
        lora_output = (x @ self.A) @ self.B

        # layer output, which combines the original output with the LoRA one 
        return self.original_layer(x) + lora_output