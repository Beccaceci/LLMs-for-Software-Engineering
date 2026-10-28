# Top-k Sampling: Sample from the top k tokens
def top_k_sampling(model, input_ids, max_length, k=50):
    output = input_ids.to(device)
    attention_mask = torch.ones_like(output).to(device)
    for _ in range(max_length):
        # Compute the logits
        logits = model(input_ids=output, attention_mask=attention_mask).logits[:, -1, :]

        # Sample a token from the top k tokens
        top_k_logits, top_k_tokens = torch.topk(logits, k, dim=-1)
        top_k_probs = torch.softmax(top_k_logits, dim=-1)
        sampled_index = torch.multinomial(top_k_probs, num_samples=1)
        next_token = torch.gather(top_k_tokens, -1, sampled_index) # Select the sampled token

        # Update the output and attention mask
        output = torch.cat([output, next_token], dim=-1)
        attention_mask = torch.cat([attention_mask, torch.ones((1, 1), dtype=torch.long, device=device)], dim=-1)

        if next_token.item() == tokenizer.eos_token_id:
            break

    return output

# Top-k Sampling
output_top_k = top_k_sampling(model, input_ids, max_length, k=50)
print(prompt)
print(tokenizer.decode(output_top_k[0, input_length:], skip_special_tokens=True))