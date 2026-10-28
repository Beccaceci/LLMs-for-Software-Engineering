from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

model_name = 'gpt2'  

# Load GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
model.to(device)

model