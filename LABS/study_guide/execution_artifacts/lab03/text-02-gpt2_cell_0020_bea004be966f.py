# Greedy Sampling: Pick the token with the highest probability
def greedy_sampling(model, input_ids, max_length):
    input_ids = input_ids.to(device)
    for _ in range(max_length):
        # NOTE: There's no need to pass an attention mask, since we are passing a single
        # input sequence and the model will automatically create the mask.
        logits = model(input_ids=input_ids).logits[:, -1, :] # Compute the logits for the last token (1st batch)
        next_token = torch.argmax(logits, dim=1).unsqueeze(1) # Get the most likely next token
        input_ids = torch.hstack([input_ids, next_token]) # Add the token to the output sequence

        if next_token.item() == tokenizer.eos_token_id:
            break

    return input_ids

# Generate and return text using each sampling method
max_length = 100  # Max tokens to generate

# Greedy Sampling
input_length = inputs["input_ids"].shape[-1]
output_greedy = greedy_sampling(model, input_ids, max_length)
print(prompt)
print(tokenizer.decode(output_greedy[0, input_length:], skip_special_tokens=True))