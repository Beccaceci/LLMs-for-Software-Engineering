viz_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    # note the padding_mode policy: this implies that the "missing" pixels
    # will be reflected from the border pixels
    # (more info in the documentation => https://pytorch.org/vision/main/generated/torchvision.transforms.RandomCrop.html)
    transforms.RandomCrop(32, padding_mode='reflect', padding=5)
])

im = transforms.ToPILImage()(images[10])
n_transforms = 9

fig, ax = plt.subplots(3,3, figsize=(4,4))
# TODO: Visualize the original image ,then apply different transformations to it
# Note: each time you apply the viz_transform transformation, a random transformation will be applied to the image
ax[0, 0].imshow(im)
ax[0, 0].set_title('Original', fontsize=8)
ax[0, 0].axis('off')

for i in range(1, n_transforms):
    r, c = divmod(i, 3)
    ax[r, c].imshow(viz_transform(im))
    ax[r, c].set_title(f'Aug {i}', fontsize=8)
    ax[r, c].axis('off')
plt.tight_layout()