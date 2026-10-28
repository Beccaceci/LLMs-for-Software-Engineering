import os
import torch
from huggingface_hub import get_token
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, set_seed

set_seed(42)
torch.set_num_threads(2)
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
print("Using device:", device)


def make_a_query(prompt: str, tokenizer, model, device, max_new_tokens: int = 200):
    """Generate only the continuation, with an explicit local context budget."""
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
    # Keep both the instruction at the start and the final question. Long retrieved
    # documents are explicitly abbreviated to keep beam-search KV memory bounded.
    max_input_tokens = min(4096, model.config.max_position_embeddings - max_new_tokens)
    prompt_length = inputs["input_ids"].shape[1]
    if prompt_length > max_input_tokens:
        print(f"Context shortened from {prompt_length} to {max_input_tokens} tokens for local memory.")
        prefix = max_input_tokens // 4
        for key, value in inputs.items():
            inputs[key] = torch.cat([value[:, :prefix], value[:, -(max_input_tokens-prefix):]], dim=1)
    inputs = inputs.to(device)
    prompt_length = inputs["input_ids"].shape[1]
    with torch.inference_mode():
        output = model.generate(
            **inputs, max_new_tokens=max_new_tokens, repetition_penalty=2.0,
            no_repeat_ngram_size=3, do_sample=False, num_beams=3,
            eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id,
            early_stopping=True,
        )
    return tokenizer.decode(output[0, prompt_length:], skip_special_tokens=True).strip()


# Read credentials from the environment or the locally stored Hugging Face login.
# Never write a token into this notebook.
hf_token = get_token()
model_id = "meta-llama/Llama-3.2-3B-Instruct"
model_revision = "0cb88a4f764b7a12671c53f0838cd831a0843b95"
model = AutoModelForCausalLM.from_pretrained(
    model_id, revision=model_revision, torch_dtype=torch.float16, low_cpu_mem_usage=True, token=hf_token,
).to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(
    model_id, revision=model_revision, token=hf_token, clean_up_tokenization_spaces=False
)
tokenizer.pad_token = tokenizer.eos_token

query = "Tell me the capital of France."
print("Direct generation:")
print(make_a_query(query, tokenizer, model, device))

text_generation_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
outputs = text_generation_pipeline(
    query, max_new_tokens=200, repetition_penalty=2.0, no_repeat_ngram_size=3,
    do_sample=False, num_beams=3, eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.pad_token_id, early_stopping=True,
)
print("Pipeline generation:")
print(outputs[0]["generated_text"])
# These calls are independent: a pipeline does not retain conversation history.