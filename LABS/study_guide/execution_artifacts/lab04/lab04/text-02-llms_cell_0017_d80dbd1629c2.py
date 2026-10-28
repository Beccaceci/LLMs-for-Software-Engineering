# Generate the output text 
outputs = pipe(
    formatted_messages,
    max_new_tokens=256,
    do_sample=True,
)

print(outputs[0]["generated_text"])