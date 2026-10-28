# show a mask token 
mask_token = tokenizer.mask_token 
mask_token_id = tokenizer.convert_tokens_to_ids(mask_token)

# Encode a text
text = "I do not know how the sentence will [MASK]."

# Tokenize the text
tokens = tokenizer.tokenize(text)

# Convert tokens to IDs
token_ids = tokenizer.convert_tokens_to_ids(tokens)

# Print each token and its ID
for token, token_id in zip(tokens, token_ids):
    print(f"Token: {token}, ID: {token_id}")