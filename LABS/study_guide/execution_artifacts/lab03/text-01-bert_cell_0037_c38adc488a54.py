sentence = "I want to eat a [MASK]."

# Tokenize the sentence
inputs = tokenizer(sentence, return_tensors="pt")
print(inputs["input_ids"])

with torch.no_grad():
    
    # Get the model outputs 
    outputs = model_mlm(**inputs)
    predictions = outputs.logits

print(predictions.shape)
