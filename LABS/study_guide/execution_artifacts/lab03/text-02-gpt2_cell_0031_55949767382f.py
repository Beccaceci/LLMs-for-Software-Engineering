# Temperature Scaling: Adjust the randomness of predictions by scaling the logits
def temperature_sampling(model, input_ids, max_length, temperature=0.7):
    output = input_ids.to(device)
    attention_mask = torch.ones_like(output).to(device)
    for _ in range(max_length):
        # Compute the logits
        logits = model(input_ids=output, attention_mask=attention_mask).logits[:, -1, :]
        
        # Scale the logits by the temperature parameter and sample from the updated distribution
        scaled_logits = logits / temperature
        probs = torch.softmax(scaled_logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)

        # Update the output and attention mask
        output = torch.cat([output, next_token], dim=-1)
        attention_mask = torch.cat([attention_mask, torch.ones((1, 1), dtype=torch.long, device=device)], dim=-1)

        if next_token.item() == tokenizer.eos_token_id:
            break

    return output

# Temperature Sampling
print(prompt)
print()
print("Temperature 0.25")
output_temperature = temperature_sampling(model, input_ids, max_length, temperature=0.25)
print(tokenizer.decode(output_temperature[0, input_length:], skip_special_tokens=True))
print()
print("Temperature 0.5")
output_temperature = temperature_sampling(model, input_ids, max_length, temperature=0.5)
print(tokenizer.decode(output_temperature[0, input_length:], skip_special_tokens=True))
print()
print("Temperature 0.75")
output_temperature = temperature_sampling(model, input_ids, max_length, temperature=0.75)
print(tokenizer.decode(output_temperature[0, input_length:], skip_special_tokens=True))
print()
print("Temperature 1.1")
output_temperature = temperature_sampling(model, input_ids, max_length, temperature=1.1)
print(tokenizer.decode(output_temperature[0, input_length:], skip_special_tokens=True))
print()
print("Temperature 1.5")
output_temperature = temperature_sampling(model, input_ids, max_length, temperature=1.5)
print(tokenizer.decode(output_temperature[0, input_length:], skip_special_tokens=True))
