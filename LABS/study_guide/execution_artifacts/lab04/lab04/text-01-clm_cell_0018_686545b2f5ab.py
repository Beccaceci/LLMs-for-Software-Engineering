from transformers import AutoModelForCausalLM, AutoTokenizer

# TODO: Load the pre-trained and fine-tuned GPT-2 models
pretrained_model = AutoModelForCausalLM.from_pretrained(model_name).to(device).eval()
finetuned_model = AutoModelForCausalLM.from_pretrained("./gpt2-medical-finetuned").to(device).eval()

# TODO: Tokenize the prompt
tokenizer = AutoTokenizer.from_pretrained("./gpt2-medical-finetuned")
tokenizer.pad_token = tokenizer.eos_token

prompt = "The patient presents with chest pain and shortness of breath."

inputs = tokenizer(prompt, return_tensors="pt").to(device)
input_ids = inputs['input_ids']