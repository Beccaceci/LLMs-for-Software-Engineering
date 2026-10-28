device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"The device is set to: {device}")