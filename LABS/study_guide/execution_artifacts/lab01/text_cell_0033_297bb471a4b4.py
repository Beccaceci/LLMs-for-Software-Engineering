# TODO: find the mean value and the standard deviation of the images in the dataset
# Note:
# - The images are available in trainset.data
# - Scale the images to the [0,1] range before proceeding
# - Compute a different mean and standard deviation for each color channel
scaled_data = trainset.data / 255.0
images_mean = tuple(scaled_data.mean(axis=(0, 1, 2)).tolist())
images_std = tuple(scaled_data.std(axis=(0, 1, 2)).tolist())
print(f"Mean: {images_mean}")
print(f"Std: {images_std}")
