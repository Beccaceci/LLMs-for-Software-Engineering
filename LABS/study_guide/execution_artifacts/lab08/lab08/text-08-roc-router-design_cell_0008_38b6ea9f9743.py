# Reference Llama model; authenticate locally with an approved Hugging Face account.
import os
import torch
from huggingface_hub import get_token
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

set_seed(42)
torch.set_num_threads(4)
device = torch.device("cuda" if torch.cuda.is_available() else
                      "mps" if torch.backends.mps.is_available() else "cpu")
print("Using device:", device)
model_id = "meta-llama/Llama-3.2-3B-Instruct"
model_revision = "0cb88a4f764b7a12671c53f0838cd831a0843b95"
hf_token = get_token()
if hf_token is None:
    raise RuntimeError("Llama 3.2 3B access requires a locally authenticated Hugging Face account.")
model = AutoModelForCausalLM.from_pretrained(
    model_id, revision=model_revision,
    torch_dtype=torch.float16 if device.type != "cpu" else torch.float32,
    low_cpu_mem_usage=True, token=hf_token,
).to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(
    model_id, revision=model_revision, token=hf_token
)
tokenizer.pad_token = tokenizer.eos_token

def make_a_query(prompt, tokenizer, model, device, max_new_tokens=200):
    # The string already contains the chat template's special tokens.
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
    prompt_length = inputs["input_ids"].shape[1]
    with torch.inference_mode():
        output = model.generate(
            **inputs, max_new_tokens=max_new_tokens, do_sample=False,
            eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id,
        )
    return tokenizer.decode(output[0, prompt_length:], skip_special_tokens=True).strip()