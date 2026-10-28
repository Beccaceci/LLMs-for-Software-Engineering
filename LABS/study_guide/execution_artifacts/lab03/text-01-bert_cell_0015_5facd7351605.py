sentence2 = "But now it is a little longer."

# Tokenize the two sentences with padding and max_length of 20
# (You can pass a pair of sentences to the tokenizer as the first and
# second argument, they will be treateed as a pair of sentences separated by [SEP])
tokens_pair = tokenizer(sentence1, sentence2, return_tensors="pt", padding="max_length", max_length=20, truncation=True)

# Display tokenized output and input IDs
print("\nTwo Sentences Tokenization:")
print("Tokens:", tokenizer.convert_ids_to_tokens(tokens_pair['input_ids'][0]))
print("Input IDs:", tokens_pair['input_ids'][0])