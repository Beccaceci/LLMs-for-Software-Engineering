def train_model(model, dataloader, criterion, optimizer, num_epochs=10):
    """
    Trains the given model on the provided dataset.

    Args:
    - model: The model to be trained.
    - dataloader: A DataLoader object to iterate over the dataset.
    - criterion: The loss function used to compute the training loss.
    - optimizer: The optimizer used to update the model parameters.
    - num_epochs: The number of training epochs.

    Returns:
    - loss_history: A list containing the loss value for each epoch.
    """
    
    # Set the model to training mode
    model.train()
    
    # Initialize an empty list to store the loss history
    loss_history = []
    
    # Loop through the epochs
    for epoch in range(num_epochs):
        total_loss = 0
        
        # Iterate over the batches of the dataloader
        for inputs, target in dataloader:
            # Add a feature dimension to the input data (input_size is assumed to be 1)
            inputs = inputs.unsqueeze(-1)  # Shape: [batch_size, seq_len, input_size]
            
            # Zero the gradients of the optimizer
            optimizer.zero_grad()
            
            # Perform a forward pass through the model and compute the loss
            outputs, _ = model(inputs)
            loss = criterion(outputs.squeeze(), target)
            
            # Perform backpropagation to compute the gradients
            loss.backward()
            
            # Update the model's parameters using the optimizer
            optimizer.step()
            
            # Accumulate the total loss for this batch
            total_loss += loss.item()
        
        # Compute the average loss for the current epoch
        avg_loss = total_loss / len(dataloader)
    
        loss_history.append(avg_loss)
        
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss:.4f}')
    
    plt.plot(loss_history)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Loss During Training')
    plt.show()
    
    return loss_history
