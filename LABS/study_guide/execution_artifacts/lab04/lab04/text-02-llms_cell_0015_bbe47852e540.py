
messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "What is 2 + 2?"},
]

# Format the messages using the chat template
formatted_messages = chat_template.format(
    system_message=messages[0]["content"],
    user_message=messages[1]["content"]
)


print(formatted_messages)