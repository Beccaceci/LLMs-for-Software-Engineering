# Demonstrate purpose extraction for one (role, story) pair, as requested.
if not user_stories:
    raise ValueError("No user stories were generated in the previous step.")
user_story1 = user_stories[0]
role, initial_story = user_story1
prefix = f"As a {role}, I want to "
function = initial_story[len(prefix):] if initial_story.startswith(prefix) else initial_story
print("Role:", role)
print("Function:", function)

system_prompt = (
    "You are a requirements analyst. Use the requirements and the given role and function "
    "to infer the supported purpose. Return exactly one complete story in the format "
    "'As a <role>, I want to <function>, so that <purpose>.' Do not invent capabilities "
    "or add an explanation."
)
shot_examples = [
    {"role": "user", "content": "Requirements: Visitors filter hiking trails by difficulty, length, or starting point to select a suitable route.\nRole: visitor\nFunction: filter hiking trails by difficulty"},
    {"role": "assistant", "content": "As a visitor, I want to filter hiking trails by difficulty, so that I can choose a route suited to my abilities."},
]
query = f"Requirements:\n{requirements_text}\n\nRole: {role}\nFunction: {function}"
messages = [{"role": "system", "content": system_prompt}] + shot_examples + [{"role": "user", "content": query}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
response = make_a_query(prompt, tokenizer, model, device, max_new_tokens=128)  # One concise user-story purpose clause
print(response)