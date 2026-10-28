transform_train_example = transforms.Compose([
    transforms.RandomHorizontalFlip(),  # Randomly flip the image horizontally for the data augmentation
    transforms.RandomCrop(32, padding_mode='reflect', padding=5),  # Randomly crop the image for the data augmentation
    transforms.ToTensor(),  # Convert the image to a tensor
    transforms.Normalize(images_mean, images_std)  # Normalize the tensor
])