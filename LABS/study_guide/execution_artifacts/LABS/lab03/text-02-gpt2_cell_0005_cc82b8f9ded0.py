# Set the model to evaluation mode
model.eval()

# Define the input prompt
prompt = "I had called upon my friend, Mr. Sherlock Holmes, one day in the autumn of last year and found him in deep conversation with a very stout, florid-faced, elderly gentleman with fiery red hair."

# Tokenize the input prompt
input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)

# Autoregressively generate tokens (`max_length=200`, `do_sample=True`, `temperature=1.1`)
generated_ids = model.generate(input_ids, max_length=200, do_sample=True, temperature=1.1, pad_token_id=tokenizer.eos_token_id)

# Decode and print the generated text
generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

print("Generated Text:")
print(generated_text)
