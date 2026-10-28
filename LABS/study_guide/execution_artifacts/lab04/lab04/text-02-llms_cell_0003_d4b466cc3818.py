from huggingface_hub import login, get_token
import os
import gc

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, set_seed

set_seed(42)
torch.set_num_threads(4)
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Inference backend: {device}")

def release_model():
    # Release the previous pipeline before loading the next multi-billion parameter model.
    globals().pop("pipe", None)
    globals().pop("model", None)
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    elif torch.backends.mps.is_available():
        torch.mps.empty_cache()