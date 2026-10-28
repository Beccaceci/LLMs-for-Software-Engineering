from transformers import BertForNextSentencePrediction
model_nsp = BertForNextSentencePrediction.from_pretrained(model_name)

sentence_a = "Arthur Conan Doyle is my favorite author"
sentence_b = "I read all of his books"

# Tokenize the two sentences 
inputs_nsp = tokenizer(sentence_a, sentence_b, return_tensors="pt")

print("Tokens:", tokenizer.convert_ids_to_tokens(inputs_nsp['input_ids'][0]))

with torch.no_grad():

    # Get the model outputs
    outputs_nsp = model_nsp(**inputs_nsp)
    logits = outputs_nsp.logits
    probs = torch.softmax(logits, dim=-1)

print(f"True: {probs[0,0].item():.6f}, False: {probs[0,1].item():.6f}")
