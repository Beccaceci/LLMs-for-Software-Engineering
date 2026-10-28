# Define a more complex neural network model
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        # Define the linear layers for the model: each layer requires specifying the number of input and output features

        # - The first layer takes as input a flattened image (32x32x3) and should produce 512 features
        #   (i.e., it encodes the image into a 512-dimensional space)
        self.fc1 = nn.Linear(32 * 32 * 3, 512)

        # - The second layer should produce 256 features
        self.fc2 = nn.Linear(512, 256)

        # - The output layer should produce 10 features (these will be the logits)    
        self.fc3 = nn.Linear(256, 10)

    def forward(self, x):
        # Implement the forward pass

        # - first step: flatten the input (preserve the batch size, flatten the rest)
        x = x.view(x.size(0), -1)

        # - apply the first linear layer with ReLU activation
        x = F.relu(self.fc1(x))

        # - apply the second linear layer with ReLU activation
        x = F.relu(self.fc2(x))

        # - apply the output layer (no activation needed for the output layer)
        x = self.fc3(x)

        return x