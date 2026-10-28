current_roles = actual_roles
user_stories = list()

#this function will be used to extract the functions from the answer provided by the llm agent

def extract_functions(text: str):
    """Accept only an initial, contiguous numbered/bulleted list of functions."""
    functions = []
    started = False
    for line in text.splitlines():
        line = line.strip()
        if not line:
            if started:
                break
            continue
        if line.upper() == "NONE":
            return []
        match = re.match(r"^(?:\d+[.)]|[-*•])\s+(.+?)\s*$", line)
        if not match:
            if started:
                break
            return []
        started = True
        item = match.group(1).strip().rstrip(".")
        if item:
            functions.append(item)
    return list(dict.fromkeys(functions))



#this function can be used to format a user story in the expected format. it returns a list of tuples (user, story)

def create_user_stories(role: str, functions: list[str]):
    """
    Generate user stories in the standard format.
    """
    user_stories = [(role, f"As a {role}, I want to {function}") for function in functions]
    return user_stories


for role in current_roles:

    #1. Loop over the list of roles and extract the piece of text from requirements related to that role
    print("\n\nExtracting stories for role", role)


    #define a prompt to extract functions for a given user
    #the prompt will be composed of the following fields:
    # - context: usage persona of the Lllama agent and instructions
    # - examples: examples of requirements text, role and user
    # - task: description of the task to perform. here you have to provide the current role
    # - answer field: placeholder from which the response will start

    #a tentative example can be the following one (you can generate many of them for instance by using another LLM agent, e.g. ChatGPT)
    example_text = [
        {
            'role': 'user',
            'content': """**Requirements Text**:
The application is designed to streamline food delivery operations. Customers can browse menus and place orders. Delivery personnel use the app to view delivery assignments and update order statuses. Restaurant managers can manage their menus and track incoming orders.

Role: Delivery personnel
List the functions for this role."""
        },

        {
            'role': 'assistant',
            'content': """1. View delivery assignments.
2. Update order status."""
        }
    ]

    system_prompt = (
        "Extract only actions explicitly supported by the requirements for the requested role. "
        "Return 1 to 8 numbered lines, each formatted `1. Verb phrase` and no more than eight words. "
        "Use no heading, explanation, prose, claims, or action not stated in the requirements. "
        "Stop after the final list item. If no action is stated for that role, return exactly `NONE`."
    )

    query = f"Requirements Text:\n{requirements_text}\n\nRole: {role}\nList the functions for this role."

    messages = [{"role": "system", "content": system_prompt}] + example_text + [{"role": "user", "content": query}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


    #now ask the agent and get the response
    response = make_a_query(prompt, tokenizer, model, device, max_new_tokens=128)  # Memory-safe cap for a concise numbered action list

    print(response)

    functions = extract_functions(response)

    tmp_user_stories = create_user_stories(role, functions)
    if not functions:
        if response.strip().upper() == "NONE":
            print("No explicit supported functions were returned for this role.")
            continue
        raise ValueError(f"The model returned no numbered functions for {role}: {response}")
    user_stories.extend(tmp_user_stories)