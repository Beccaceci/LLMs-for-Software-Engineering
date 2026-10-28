# Use the model to generate the next token
output = model(**tokens, decoder_input_ids=decoder_input_ids)
output.logits.shape