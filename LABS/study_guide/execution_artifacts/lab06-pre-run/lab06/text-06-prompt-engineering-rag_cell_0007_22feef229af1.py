system_prompt = """You are a helpful, respectful and honest assistant.
Always answer as helpfully as possible, while being safe. Your answers should not include any harmful,
unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses
are socially unbiased and positive in nature. If a question does not make any sense, or is not factually
coherent, explain why instead of answering something not correct. If you don't know the answer to a question,
please don't share false information."""
prompt_str = "{PROMPT}\n\nArticle:\n{BODY}".format(PROMPT=text_summarization_prompt, BODY=text)
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt_str},
]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
r2 = make_a_query(prompt, tokenizer, model, device, max_new_tokens=300)
print(r2)
print("Compare with the unformatted prompt above: bullet structure, factual coverage, and unsupported claims.")