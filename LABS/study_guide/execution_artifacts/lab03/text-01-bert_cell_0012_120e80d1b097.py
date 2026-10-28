sentence1 = "This is a short sentence."

# Tokenize the sentence with padding=True and max_length=10
tokens_single = tokenizer(sentence1, return_tensors="pt", padding="max_length", max_length=10)

# Display tokenized output and input IDs
print("Single Sentence Tokenization:")
print("Tokens:", tokenizer.convert_ids_to_tokens(tokens_single['input_ids'][0]))
print("Input IDs:", tokens_single['input_ids'][0])