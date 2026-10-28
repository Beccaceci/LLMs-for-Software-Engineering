messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

# TODO: Format the messages using the chat template and generate the output text
input_tokens = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
prompt_string = tokenizer.decode(input_tokens, skip_special_tokens=False)

outputs = pipe(prompt_string, max_new_tokens=100, do_sample=False, add_special_tokens=False)

print(outputs[0]["generated_text"])