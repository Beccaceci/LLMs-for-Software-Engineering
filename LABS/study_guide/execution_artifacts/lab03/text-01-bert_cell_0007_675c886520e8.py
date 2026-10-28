# Load pre-trained tokenizer
tokenizer = BertTokenizer.from_pretrained(model_name)

sentence = "hello, this is a sentence!"

# Tokenize the sentence 
tokens = tokenizer.tokenize(sentence)
print("Tokens:", tokens)

# Convert tokens to IDs
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print("Token IDs:", token_ids)