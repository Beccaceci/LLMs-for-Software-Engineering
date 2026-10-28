# Random Sampling: Randomly sample a token from the distribution
def random_sampling(model, input_ids, max_length):
    output = input_ids.to(device)
    attention_mask = torch.ones_like(output).to(device)
    for _ in range(max_length):
        # Compute the logits
        logits = model(input_ids=output, attention_mask=attention_mask).logits[:, -1, :]

        # Sample a token from the probability distribution
        probs = torch.softmax(logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)

        # Update the output and attention mask
        output = torch.cat([output, next_token], dim=-1)
        attention_mask = torch.cat([attention_mask, torch.ones((1, 1), dtype=torch.long, device=device)], dim=-1)

        if next_token.item() == tokenizer.eos_token_id:
            break

    return output

# Random Sampling
output_random = random_sampling(model, input_ids, max_length)
print(prompt)
print(tokenizer.decode(output_random[0, input_length:], skip_special_tokens=True))