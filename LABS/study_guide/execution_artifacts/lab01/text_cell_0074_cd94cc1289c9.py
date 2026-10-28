# Freeze all layers except the classification head
for param in model.parameters():
    param.requires_grad = False

# Unfreeze the classification head
for param in model.fc.parameters():
    param.requires_grad = True