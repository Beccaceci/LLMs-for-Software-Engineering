model_id = "meta-llama/Llama-3.2-1B"
#TODO: load the model and tokenizer 
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32, low_cpu_mem_usage=True).to(device).eval() 
tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side="left")

tokenizer.pad_token = tokenizer.eos_token