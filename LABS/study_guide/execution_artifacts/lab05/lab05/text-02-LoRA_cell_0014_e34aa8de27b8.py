# Freeze all parameters except the LoRA parameters

# Freeze all parameters
for param in model.parameters():
    param.requires_grad = False 
    
# Unfreeze only LoRA parameters
for layer in model.modules():
    if isinstance(layer, LoRA):
        layer.A.requires_grad = True
        layer.B.requires_grad = True