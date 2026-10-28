# Pass in the tokenizer.batch_decode the output of the model to get the translation of the input sentence
tokenizer.batch_decode(output.logits.argmax(dim=-1))