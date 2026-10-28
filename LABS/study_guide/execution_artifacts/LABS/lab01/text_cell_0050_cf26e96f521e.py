# Training loop
num_epochs = 5

losses = []

model.train()
for epoch in range(num_epochs):
    running_loss = 0.0
    for inputs, labels in trainloader:
        inputs, labels = inputs.to(device), labels.to(device)

        # TODO: let's implement the training loop for the model
        # Notes:
        # - First, zero the parameter gradients
        optimizer.zero_grad()

        # - Next, get the model's predictions
        outputs = model(inputs)

        # - Compute the loss
        loss = criterion(outputs, labels)

        # - Perform backpropagation (i.e. compute all gradients)
        loss.backward()
        
        # - Finally, update the model's parameters
        optimizer.step()
        losses.append(loss.item())

        running_loss += loss.item()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(trainloader):.4f}")
