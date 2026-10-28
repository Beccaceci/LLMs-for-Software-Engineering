tic = time.time()

with torch.no_grad():
    #TODO: generate the output from the quantized model
    output = quantized_model.generate(**inputs, max_new_tokens=30, do_sample=False, pad_token_id=tokenizer.eos_token_id)

elapsed_time = time.time() - tic

#TODO: decode the output
output_decoded = tokenizer.batch_decode(output, skip_special_tokens=True)

print("\nquantized model output:", output_decoded)
print("\nTime taken for quantized model:", elapsed_time)