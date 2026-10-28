# Load a pre-trained model (ResNet18)
pretrained_model = models.resnet18(weights='DEFAULT')

# The model has a fully connected layer at the end (called `fc`) that needs to be replaced with a new one of the appropriate size
pretrained_model.fc = nn.Linear(pretrained_model.fc.in_features, 10)

# To get the number of input features for the new layer, you can access the in_features attribute of the original fc layer
pretrained_model = pretrained_model.to(device) # move the model (all layers, even new ones) to the device
