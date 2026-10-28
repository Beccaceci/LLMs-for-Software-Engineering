# re-prepare encoder tokens and decoder tokens
# input_sentence = "translate from english to german: hello how are you?"
input_sentence = "translate english to german: hello how are you?"

# Use the tokenizer to tokenize the input sentence as a tensor
tokens = tokenizer(input_sentence, return_tensors="pt")

# Create the token for the decoder input (start with the <pad> token -> tokenizer.pad_token_id)
decoder_input_ids = torch.tensor([[ tokenizer.pad_token_id ]])

# Use the model to generate the output putting the decoder_input_ids as the first token (decoder_input_ids=decoder_input_ids)
output = model(**tokens, decoder_input_ids=decoder_input_ids)
print(output.keys())