import re

def parse_router_response(text):
    # Remove punctuation/case variation, then require an exact supported decision.
    normalized = " ".join(re.sub(r"[^a-zA-Z\s]", " ", text).lower().split())
    routes = {"use cases": "Use Cases", "class diagram": "Class Diagram"}
    if normalized not in routes:
        raise ValueError(f"Router produced an unsupported decision: {text!r}")
    return routes[normalized]

fixed_response = parse_router_response(response)
print("Router selection:", fixed_response)
if fixed_response == "Use Cases":
    sys_prompt = (
        "You are a requirements analyst. Extract user-goal use cases grounded only in the "
        "provided requirements. Group concise use cases by actor; avoid inventing features."
    )
    shot_example = [
        {"role": "user", "content": "Customers browse menus and place orders. Drivers update delivery status."},
        {"role": "assistant", "content": "Customers: Browse menus; Place orders.\nDrivers: Update delivery status."},
    ]
    query = f"Extract the actors and their user-goal use cases.\n\nRequirements:\n{requirements_text}"
    messages = [{"role": "system", "content": sys_prompt}, *shot_example,
                {"role": "user", "content": query}]
    prompt_use_cases = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    response_uc = make_a_query(prompt_use_cases, tokenizer, model, device, max_new_tokens=2000)
    print(response_uc)
else:
    sys_prompt = (
        "You are a software designer. Extract only domain class names grounded in the "
        "provided requirements, one per line. Do not list methods, attributes, or imagined classes."
    )
    shot_example = [
        {"role": "user", "content": "Customers place orders containing products. Drivers deliver the orders."},
        {"role": "assistant", "content": "Customer\nOrder\nProduct\nDriver"},
    ]
    query = f"Identify the domain classes for a class diagram.\n\nRequirements:\n{requirements_text}"
    messages = [{"role": "system", "content": sys_prompt}, *shot_example,
                {"role": "user", "content": query}]
    prompt_class_diagram = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    response_cd = make_a_query(prompt_class_diagram, tokenizer, model, device, max_new_tokens=2000)
    print(response_cd)