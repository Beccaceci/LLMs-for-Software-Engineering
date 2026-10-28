# Read every page, not only the first page displayed above.
with pymupdf.open("example2.pdf") as doc:
    text = "\n".join(page.get_text("text") for page in doc)
text_summarization_prompt = (
    "Summarize the following article in five concise bullet points. "
    "Include its main topic, problem, method, findings, and limitations. "
    "Use only facts stated in the article."
)
prompt_str = "{PROMPT}\n\nArticle:\n{BODY}".format(PROMPT=text_summarization_prompt, BODY=text)
r1 = make_a_query(prompt_str, tokenizer, model, device, max_new_tokens=300)
print(r1)