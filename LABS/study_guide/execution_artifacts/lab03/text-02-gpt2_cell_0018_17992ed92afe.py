# Load pre-trained GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
model.to(device)

# Set the pad token to eos token
tokenizer.pad_token = tokenizer.eos_token

# Set the model to evaluation mode
model.eval()

# Input prompt
prompt = "I had called upon my friend, Mr. Sherlock Holmes, one day in the autumn of last year and found him in deep conversation with a very stout, florid-faced, elderly gentleman with fiery red hair."

# Tokenize the input prompt
inputs = tokenizer(prompt, return_tensors='pt').to(device)
input_ids = inputs['input_ids']