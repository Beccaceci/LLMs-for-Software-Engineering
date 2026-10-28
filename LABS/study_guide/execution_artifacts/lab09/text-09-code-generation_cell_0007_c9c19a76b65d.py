import gc
import torch
from huggingface_hub import get_token
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

set_seed(42)
torch.set_num_threads(2)
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print("Using device:", device)
model = tokenizer = None
current_model_id = None

def select_engine(model_id):
    """Hold one model at a time so comparisons fit the local memory budget."""
    global model, tokenizer, current_model_id
    if current_model_id == model_id and model is not None:
        return
    model = tokenizer = None
    current_model_id = None
    gc.collect()
    if device == "mps": torch.mps.empty_cache()
    if device == "cuda": torch.cuda.empty_cache()
    dtype = torch.float16 if device != "cpu" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_id, torch_dtype=dtype, low_cpu_mem_usage=True,
        token=get_token(),
    ).to(device).eval()
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=get_token())
    tokenizer.pad_token = tokenizer.eos_token
    current_model_id = model_id

def make_a_query(prompt, tokenizer, model, device, max_new_tokens=768):
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
    with torch.inference_mode():
        output = model.generate(**inputs, max_new_tokens=max_new_tokens,
            do_sample=False, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

# The supplied checkpoint is Llama 3.2, despite the original heading saying CodeLlama.
model_id = "meta-llama/Llama-3.2-3B-Instruct"
select_engine(model_id)
