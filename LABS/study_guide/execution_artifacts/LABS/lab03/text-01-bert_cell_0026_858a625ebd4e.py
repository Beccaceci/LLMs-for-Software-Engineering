fig, ax = plt.subplots()

ax.set_aspect('equal')
cbar = ax.imshow(cosine_sim[:128, :128], cmap='viridis', vmin=-1, vmax=1)
ax.set_xlabel('Vector 1')
ax.set_ylabel('Vector 2')
# add colorbar
fig.colorbar(cbar, ax=ax)