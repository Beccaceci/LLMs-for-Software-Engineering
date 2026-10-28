tokens = tokenizer("Hello, my name is", return_tensors="pt").to(model.device)
batch = model.generate(**tokens, do_sample=True, max_length=50, num_return_sequences=5, pad_token_id=tokenizer.eos_token_id) # (assigning pad_token_id avoids a warning)
tokenizer.batch_decode(batch)