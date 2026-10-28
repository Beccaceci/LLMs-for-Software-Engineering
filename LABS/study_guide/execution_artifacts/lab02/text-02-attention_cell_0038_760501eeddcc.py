import matplotlib.pyplot as plt
import numpy as np
import torch

# Visualize the Attention Weights
def visualize_attention(model, dataset):
    model.eval()
    for i in range(len(dataset)):
        inputs, target = dataset[i]
        if target != 0: 
            # Reshape the input for the Transformer: [batch_size, seq_len, input_size]
            inputs = inputs.unsqueeze(0).unsqueeze(2)
            outputs, attention_weights = model(inputs)
            break

    # Plot the input time series (after undoing the batch and input dimension)
    plt.plot(inputs.permute(1, 0, 2).squeeze().numpy(), label="Input Series")

    # The attention weights are returned from all layers, so let's use the attention from the last layer
    attention_weights = attention_weights[-1][0].detach().numpy()  # [batch_size, num_heads, seq_len, seq_len]

    # Normalize attention weights for better visibility
    normalized_attention_weights = (attention_weights - np.min(attention_weights)) / (np.max(attention_weights) - np.min(attention_weights))
    
    
    # Plot the normalized attention weights
    plt.plot(normalized_attention_weights.mean(axis=0), label="Normalized Attention Weights", linestyle='--')
    plt.scatter(seq_len, target, color='r', label='True Target')
    plt.scatter(seq_len, outputs[-1].item(), color='g', label='Predicted Target')
    plt.title(f"Example of a prediction:\nTrue Target: {target.item():.2f}, Predicted: {outputs[-1].item():.2f}")
    plt.legend(loc='upper left')
    plt.show()



visualize_attention(model, dataset)