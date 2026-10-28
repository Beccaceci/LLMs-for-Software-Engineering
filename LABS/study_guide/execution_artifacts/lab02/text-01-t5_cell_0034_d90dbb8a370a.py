# Use the tokenizer to tokenize the sentences with padding as a tensor and print the result (use padding=True and return_tensors="pt")
tokens = tokenizer(sentences, padding=True, return_tensors="pt")

print(tokens["input_ids"])
print(tokens["attention_mask"])