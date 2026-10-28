model_id = "meta-llama/Llama-3.2-1B"

# TODO: Load the model with `torch.float16` precision and the tokenizer 
# (You can specify the precision with `torch_dtype=torch.float16`)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, low_cpu_mem_usage=True).to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(model_id)

tokenizer.pad_token = tokenizer.eos_token