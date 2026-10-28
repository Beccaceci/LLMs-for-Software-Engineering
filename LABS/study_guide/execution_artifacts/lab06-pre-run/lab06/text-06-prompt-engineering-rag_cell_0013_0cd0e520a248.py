import json
json_prompt_addition = (
    'Output only valid JSON with the keys "topic" and "explanation". '
    'Both values must be strings; the explanation must contain fewer than ten words. '
    'Example: {"topic": "machine learning", "explanation": "Methods that learn patterns from data"}.'
)
prompt_str = "Identify the main topic of this article.\n\nArticle:\n" + text
messages = [
    {"role": "system", "content": new_system_prompt + "\n" + json_prompt_addition},
    {"role": "user", "content": prompt_str},
]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
r6 = make_a_query(prompt, tokenizer, model, device)
print(r6)
# A format instruction does not guarantee valid JSON: verify the actual generation.
try:
    parsed_json = json.loads(r6)
    assert set(parsed_json) == {"topic", "explanation"}
    assert all(isinstance(value, str) for value in parsed_json.values())
    assert len(parsed_json["explanation"].split()) < 10
    print("JSON syntax, keys, types, and explanation length: valid")
except (json.JSONDecodeError, AssertionError, TypeError) as error:
    print("The generated response did not satisfy the requested JSON schema:", type(error).__name__)