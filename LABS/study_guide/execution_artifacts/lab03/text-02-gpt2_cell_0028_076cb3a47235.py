# Top-p (Nucleus) Sampling: Sample from the smallest set of tokens whose cumulative probability exceeds p
def top_p_sampling(model, input_ids, max_length, p=0.9):
    output = input_ids.to(device)
    attention_mask = torch.ones_like(output).to(device)
    for _ in range(max_length):
        # Compute the logits
        logits = model(input_ids=output, attention_mask=attention_mask).logits[:, -1, :]

        # Create a mask to filter out tokens with cumulative probability above p
        sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
        sorted_probs = torch.softmax(sorted_logits, dim=-1)
        cumulative_probs = torch.cumsum(sorted_probs, dim=-1) # Cumulative Distribution Function (CDF)
        top_p_mask = cumulative_probs <= p
        top_p_mask[..., 0] = True  # Ensure at least one token is considered

        filtered_logits = sorted_logits.clone()
        filtered_logits[~top_p_mask] = -float('inf')

        # Recompute the probabilities and sample from the updated distribution
        top_p_probs = torch.softmax(filtered_logits, dim=-1)
        sampled_index = torch.multinomial(top_p_probs, num_samples=1)
        next_token = torch.gather(sorted_indices, -1, sampled_index)

        # Update the output and attention mask
        output = torch.cat([output, next_token], dim=-1)
        attention_mask = torch.cat([attention_mask, torch.ones((1, 1), dtype=torch.long, device=device)], dim=-1)

        if next_token.item() == tokenizer.eos_token_id:
            break

    return output

# Top-p (Nucleus) Sampling
output_top_p = top_p_sampling(model, input_ids, max_length, p=0.9)
print(prompt)
print(tokenizer.decode(output_top_p[0, input_length:], skip_special_tokens=True))