quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
).to('cpu')

# Model size after quantization
print(f"Model size after quantization {(get_model_size(quantized_model)):.2f} MB")