# Few-shot examples contain valid JSON (no trailing comma).
shot_examples = [
    {"role": "user", "content": "Identify the main nouns in this article: The rapid growth of the semiconductor industry has transformed global manufacturing, as companies specializing in advanced chip design and microdevice fabrication struggle to meet soaring technology demands."},
    {"role": "assistant", "content": '[{"name": "semiconductor", "type": "industry", "explanation": "Companies designing and fabricating semiconductor devices"}]'},
    {"role": "user", "content": "Identify the main nouns in this article: The NBA continues to captivate millions of fans worldwide as the premier global stage for professional basketball, driving massive television ratings and international merchandise sales each season."},
    {"role": "assistant", "content": '[{"name": "NBA", "type": "sport league", "explanation": "The National Basketball Association"}]'},
]
entity_system = (
    "Identify the main nouns and named entities in the supplied article. Output only a valid JSON array. "
    'Each item must have the string fields "name", "type", and "explanation".'
)
final_question = {"role": "user", "content": "Identify the main nouns in this article:\n" + text}
messages = [{"role": "system", "content": entity_system}] + shot_examples + [final_question]
prompt_str = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
r7 = make_a_query(prompt_str, tokenizer, model, device, max_new_tokens=500)
print("Few-shot response:", r7)
zero_shot_messages = [{"role": "system", "content": entity_system}, final_question]
zero_shot_prompt = tokenizer.apply_chat_template(zero_shot_messages, tokenize=False, add_generation_prompt=True)
r7_zero_shot = make_a_query(zero_shot_prompt, tokenizer, model, device, max_new_tokens=500)
print("Zero-shot response:", r7_zero_shot)
for label, response in [("few-shot", r7), ("zero-shot", r7_zero_shot)]:
    try:
        entities = json.loads(response)
        assert isinstance(entities, list)
        assert all(set(item) == {"name", "type", "explanation"} and all(isinstance(v, str) for v in item.values()) for item in entities)
        print(label, "valid JSON entity array; entities:", len(entities))
    except (json.JSONDecodeError, AssertionError, TypeError, AttributeError) as error:
        print(label, "invalid entity JSON:", type(error).__name__)