new_system_prompt = (
    "You are a researcher writing a concise scientific brief. Summarize the supplied article's "
    "research problem, approach, findings, and limitations. Be faithful to the article, "
    "distinguish evidence from speculation, and do not invent facts."
)
prompt_str = "{PROMPT}\n\nArticle:\n{BODY}".format(PROMPT=text_summarization_prompt, BODY=text)
messages = [{"role": "system", "content": new_system_prompt}, {"role": "user", "content": prompt_str}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
r3 = make_a_query(prompt, tokenizer, model, device, max_new_tokens=300)
print(r3)