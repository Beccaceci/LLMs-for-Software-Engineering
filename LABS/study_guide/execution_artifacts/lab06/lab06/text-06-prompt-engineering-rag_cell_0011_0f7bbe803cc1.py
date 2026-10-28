# Prompt chaining: the first answer becomes context for a second question.
prompt_str = "State the main topic of this article in one sentence.\n\nArticle:\n" + text
messages = [{"role": "system", "content": new_system_prompt}, {"role": "user", "content": prompt_str}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
r4 = make_a_query(prompt, tokenizer, model, device)
print("Topic:", r4)
prompt_str2 = (
    f"The article was described as follows: {r4}\n"
    "What problem does this work address, and how? Answer using the article below.\n\nArticle:\n" + text
)
messages = [{"role": "system", "content": new_system_prompt}, {"role": "user", "content": prompt_str2}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
r5 = make_a_query(prompt, tokenizer, model, device)
print("Problem addressed:", r5)