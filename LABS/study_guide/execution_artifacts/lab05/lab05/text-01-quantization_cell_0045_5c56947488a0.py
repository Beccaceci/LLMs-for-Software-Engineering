text = "The secret of life is"
# Notice we use a batch of 20 sentences -- we will get better results
# on quantized models when processing a batch of inputs
text = [text]*20

#TODO: encode the text using the tokenizer
inputs = tokenizer(text, return_tensors="pt", padding=True).to(device)

tic = time.time()

with torch.no_grad():
    #TODO: generate the output from the model
    baseline_output = model.generate(**inputs, max_new_tokens=30, do_sample=False, pad_token_id=tokenizer.eos_token_id)

elapsed_time = time.time() - tic

#TODO: decode the output
baseline_decoded = tokenizer.batch_decode(baseline_output, skip_special_tokens=True)

print("Baseline model output:", baseline_decoded)
print("\nTime taken for baseline model:", elapsed_time)