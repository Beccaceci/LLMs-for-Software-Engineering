# Tokenize the dataset
def tokenize_function(sample):
    tokenized_input = tokenizer(sample['text'], padding="max_length", truncation=True, max_length=256)
    return tokenized_input

train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)