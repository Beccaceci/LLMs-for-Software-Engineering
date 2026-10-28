# Initialize the DataLoader
dataset = TimeSeriesDataset(seq_len=seq_len, num_samples=num_samples)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Instantiate the criterion (MSE loss) and the optimizer (Adam) with a learning rate of 0.0005
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0005)

# Train the model
train_model(model, dataloader, criterion, optimizer, num_epochs=num_epochs)
