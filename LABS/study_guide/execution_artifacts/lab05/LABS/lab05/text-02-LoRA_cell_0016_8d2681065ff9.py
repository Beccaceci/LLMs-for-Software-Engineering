print_trainable_parameters(model)
assert sum(p.numel() for p in model.parameters() if p.requires_grad) == 1_327_104