fig, ax = plt.subplots(12, 12, figsize=(10, 10))

for i in range(12):
    for j in range(12):
        ax[i, j].imshow(attention[i][0, j].detach().cpu().numpy(), cmap='viridis', aspect='auto')
        ax[i, j].axis('off')