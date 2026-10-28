# Define the model ID
release_model()

model_id = "mistralai/Mistral-7B-Instruct-v0.2"

# TODO: Load the model and the tokenizer 
# The 7B FP16 weights alone take about 14.5 GB. On this 16 GB Mac,
# load the same checkpoint with 4-bit weights; retain FP16 on larger machines.
from transformers import QuantoConfig
import psutil
use_int4 = device == "mps" and psutil.virtual_memory().total < 24 * 1024**3
load_options = {"quantization_config": QuantoConfig(weights="int4")} if use_int4 else {}
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.float16, device_map=device,
    low_cpu_mem_usage=True, **load_options,
).eval()
print("Mistral weights:", "int4 (Quanto)" if use_int4 else "float16")

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# TODO: Initialize the pipeline for text generation
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, pad_token_id=tokenizer.eos_token_id)

# Define the message prompts for the conversation
messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"}
]

# TODO: Generate the response
outputs = pipe(messages, max_new_tokens=100, pad_token_id=tokenizer.eos_token_id)

# Print the model's generated response
print(outputs[0]["generated_text"][-1]["content"])