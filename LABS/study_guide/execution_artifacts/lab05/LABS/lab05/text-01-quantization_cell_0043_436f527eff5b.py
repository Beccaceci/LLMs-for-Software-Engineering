def get_model_size(model):
    """Get the size of the model in MB"""
    torch.save(model.state_dict(), "temp.pth")
    size = os.path.getsize("temp.pth") / 1e6  # size in "MB" (technically, it should be 1024**2, but we approximate to 1e6 to get an easier conversion #params <=> MB)
    os.remove("temp.pth")
    return size

print(f"Model size before quantization {(get_model_size(model)):.2f} MB")