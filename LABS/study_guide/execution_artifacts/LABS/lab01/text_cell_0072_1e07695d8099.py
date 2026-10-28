# Modify the classification head for CIFAR-100 (100 classes)

model = pretrained_model
model.fc = nn.Linear(model.fc.in_features, 100)
model = model.to(device)