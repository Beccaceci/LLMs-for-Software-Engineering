import random 

vocabulary = tokenizer.get_vocab()

# print 10 random words from the vocabulary
reverse_vocab = {v: k for k, v in vocabulary.items()}

vocab_keys = list(vocabulary.keys())
print(random.sample(vocab_keys, 10))