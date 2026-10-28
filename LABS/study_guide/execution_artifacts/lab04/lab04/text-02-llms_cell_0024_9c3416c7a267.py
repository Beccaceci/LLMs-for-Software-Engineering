# TODO: Create the pipeline with the model and tokenizer
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, pad_token_id=tokenizer.eos_token_id)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]
input_tokens = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
print(tokenizer.decode(input_tokens))

# Generate in pipeline chat mode; it applies the same chat template internally.
outputs = pipe(messages, max_new_tokens=100, do_sample=False)

# we are getting back the full conversation history
# as a list of messages outputs[0]["generated_text"]
# -1 : last message (assistant response)
print(outputs[0]["generated_text"][-1]["content"])