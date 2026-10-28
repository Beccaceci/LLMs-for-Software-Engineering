# Use the model to generate a translation of the input sentence
out_tokens = model.generate(**tokens)
tokenizer.batch_decode(out_tokens)
