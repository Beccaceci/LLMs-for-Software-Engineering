from transformers import BitsAndBytesConfig
import gc

# Release both previous models before loading the next one on this 16 GB Mac.
del model, quantized_model
gc.collect()

# BitsAndBytes 0.50.2 supports the CPU backend on macOS ARM64. Keep all
# three timed experiments on CPU here so their timings are comparable.
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float32,
)
quantized_model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=quantization_config,
    torch_dtype=torch.float32, device_map="cpu", low_cpu_mem_usage=True,
).eval()
inputs = inputs.to(quantized_model.device)
print("4-bit backend: BitsAndBytes (CPU)")
print(f"Model size after quantization: {get_model_size(quantized_model):.2f} MB")