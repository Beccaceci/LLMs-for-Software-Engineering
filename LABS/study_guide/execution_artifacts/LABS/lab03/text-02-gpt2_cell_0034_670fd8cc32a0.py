# Function to generate text using various sampling methods
def generate_text(model, input_ids, max_length, method, **kwargs):

    methods = {
        "greedy": {},
        "beam": {"num_beams": kwargs.get('num_beams', 3), "early_stopping": True},
        "random": {"do_sample": True},
        "top_k": {"do_sample": True, "top_k": kwargs.get('top_k', 50)},
        "top_p": {"do_sample": True, "top_p": kwargs.get('top_p', 0.9)},
        "temperature": {"do_sample": True, "temperature": kwargs.get('temperature', 0.7)}
    }
    return model.generate(input_ids.to(device), max_length=max_length, pad_token_id=tokenizer.eos_token_id, **methods[method])

# Generate text using each sampling method
max_length = 200  # Increased max_length to generate more tokens

# Get the length of the input prompt in tokens
input_length = len(tokenizer.encode(prompt, add_special_tokens=False))

# Greedy Sampling
output_greedy = generate_text(model, inputs['input_ids'], max_length, 'greedy')
print("Greedy Sampling:")
print(tokenizer.decode(output_greedy[0, input_length:], skip_special_tokens=True))


# Beam Search
output_beam = generate_text(model, inputs['input_ids'], max_length, 'beam', num_beams=5)
print("\nBeam Search:")
print(tokenizer.decode(output_beam[0, input_length:], skip_special_tokens=True))

# Random Sampling
output_random = generate_text(model, inputs['input_ids'], max_length, 'random')
print("\nRandom Sampling:")
print(tokenizer.decode(output_random[0, input_length:], skip_special_tokens=True))

# Top-k Sampling
k = 50
output_top_k = generate_text(model, inputs['input_ids'], max_length, 'top_k', top_k=k)
print(f"\nTop-{k} Sampling:")
print(tokenizer.decode(output_top_k[0, input_length:], skip_special_tokens=True))

# Top-p (Nucleus) Sampling
p = 0.9
output_top_p = generate_text(model, inputs['input_ids'], max_length, 'top_p', top_p=p)
print(f"\nTop-{p} (Nucleus) Sampling:")
print(tokenizer.decode(output_top_p[0, input_length:], skip_special_tokens=True))

# Temperature Scaling
temperature = 0.7
output_temperature = generate_text(model, inputs['input_ids'], max_length, 'temperature', temperature=temperature)
print(f"\nTemperature Sampling ({temperature}):")
print(tokenizer.decode(output_temperature[0, input_length:], skip_special_tokens=True))

