# ------------------ Initial setup ---------------------
import gc
import torch
from huggingface_hub import get_token
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

set_seed(42)
torch.set_num_threads(2)
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
print("Using device:", device)

# Read a local saved login or HF_TOKEN; never store a token in the notebook.
hf_token = get_token()
model_id = "meta-llama/Llama-3.2-3B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.float16, low_cpu_mem_usage=True, token=hf_token,
).to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token, clean_up_tokenization_spaces=False)
tokenizer.pad_token = tokenizer.eos_token


def make_a_query(prompt: str, tokenizer, model, device, max_new_tokens: int = 200):
    # Chat-template prompts already contain special tokens; do not add another BOS.
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
    prompt_length = inputs["input_ids"].shape[1]
    eot_id = tokenizer.convert_tokens_to_ids("<|eot_id|>")
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.15,
            top_p=0.9,
            num_beams=1,
            # Stop on Llama's end-of-turn marker and the model's EOS marker.
            eos_token_id=list(dict.fromkeys([eot_id, tokenizer.eos_token_id])),
            pad_token_id=tokenizer.pad_token_id,
        )
    answer = tokenizer.decode(output[0, prompt_length:], skip_special_tokens=True).strip()
    del output, inputs
    gc.collect()
    if getattr(device, "type", str(device)) == "mps":
        torch.mps.empty_cache()
    return answer
