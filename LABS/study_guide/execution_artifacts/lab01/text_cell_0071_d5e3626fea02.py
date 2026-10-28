# Load the CIFAR-100 dataset
trainset_cifar100 = torchvision.datasets.CIFAR100(root=dataset_dir, train=True, download=True, transform=transform_train)
trainloader_cifar100 = torch.utils.data.DataLoader(trainset_cifar100, batch_size=100, shuffle=True)

testset_cifar100 = torchvision.datasets.CIFAR100(root=dataset_dir, train=False, download=True, transform=transform_test)
testloader_cifar100 = torch.utils.data.DataLoader(testset_cifar100, batch_size=100, shuffle=False)