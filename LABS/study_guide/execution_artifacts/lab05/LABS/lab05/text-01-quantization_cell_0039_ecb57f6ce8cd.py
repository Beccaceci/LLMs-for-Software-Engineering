import torch
import os
import time 
from transformers import AutoTokenizer, AutoModelForCausalLM

torch.set_num_threads(4)
# PyTorch dynamic quantization is a CPU backend. Keep the FP32 baseline
# on CPU as well so its timing is comparable to the int8 result.
device = torch.device("cpu")
if "qnnpack" in torch.backends.quantized.supported_engines:
    torch.backends.quantized.engine = "qnnpack"
print("Quantization engine:", torch.backends.quantized.engine)