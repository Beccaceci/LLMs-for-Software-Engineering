# Tokenize the two sentences 
sentence_c = "However, it's raining today"
inputs_nsp_false = tokenizer(sentence_a, sentence_c, return_tensors="pt")

print("Tokens:", tokenizer.convert_ids_to_tokens(inputs_nsp_false['input_ids'][0]))

with torch.no_grad():

    # Get the model outputs
    outputs_nsp = model_nsp(**inputs_nsp_false)
    logits = outputs_nsp.logits
    probs = torch.softmax(logits, dim=-1)

print(f"True: {probs[0,0].item():.6f}, False: {probs[0,1].item():.6f}")
