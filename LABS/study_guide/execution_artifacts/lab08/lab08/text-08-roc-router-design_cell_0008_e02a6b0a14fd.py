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

def make_a_query(prompt, tokenizer, model, device, max_new_tokens=200,
                 allowed_completions=None):
    # The string already contains the chat template's special tokens.
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
    prompt_length = inputs["input_ids"].shape[1]
    generation_options = {}
    if allowed_completions is not None:
        sequences = [tokenizer.encode(text, add_special_tokens=False)
                     for text in allowed_completions]

        def allow_completion_tokens(batch_id, input_ids):
            generated = input_ids[prompt_length:].tolist()
            matches = [sequence for sequence in sequences
                       if sequence[:len(generated)] == generated]
            if not matches:
                return [tokenizer.eos_token_id]
            next_tokens = {sequence[len(generated)] for sequence in matches
                           if len(sequence) > len(generated)}
            return sorted(next_tokens) if next_tokens else [tokenizer.eos_token_id]

        generation_options["prefix_allowed_tokens_fn"] = allow_completion_tokens
    with torch.inference_mode():
        output = model.generate(
            **inputs, max_new_tokens=max_new_tokens, do_sample=False,
            eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id,
            **generation_options,
        )
    return tokenizer.decode(output[0, prompt_length:], skip_special_tokens=True).strip()
