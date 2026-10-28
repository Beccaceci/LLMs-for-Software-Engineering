#define three different prompts for extracting users, using the zero-shot, one-shot and few-shot approach. then evaluate the difference in terms of capability to format the output and actual results

# IMPORTANT: wheter you use the chat template or not, remember to add the shots into the correct structure composed by user's query and assistant's response (see previous lab)

query = "Requirements Text:\n" + requirements_text + "\nList the distinct user roles."

shots = [ # This is a list of lists, useful to separate each shot from each other

    # First shot
    [
        {'role': 'user',
          'content': """Requirements Text:
"The application is designed to streamline food delivery operations. Customers can browse menus and place orders. Delivery personnel use the app to view delivery assignments and update order statuses. Restaurant managers can manage their menus and track incoming orders."""},
        {'role': 'assistant', 'content': """1. Customers
2. Delivery Personnel
3. Restaurant Managers"""},
    ],

    # Second shot
    [
      {'role': 'user',
      'content': """Requirements Text:
The platform supports the education sector by providing tools for students, teachers, and administrators. Students can access course materials, submit assignments, and track their progress. Teachers can create content, grade submissions, and communicate with students. Administrators oversee user registrations and system performance."""},
      {'role': 'assistant',
      'content': """1. Students
2. Teachers
3. Administrators"""}
    ],

    # Third shot
    [
        {'role': 'user',
         'content': """Requirements Text:
The system provides real-time updates for commuters, transit operators, and city planners. Commuters can check schedules and delays. Transit operators monitor vehicle statuses and manage timetables. City planners analyze system data to improve routes and infrastructure."""},
        {'role': 'assistant',
         'content': """1. Commuters
2. Transit Operators
3. City Planners"""}
    ]
]


system_prompt = """Extract only the distinct user roles explicitly supported by the supplied requirements.
Return only the role names explicitly stated in the requirements, one per numbered line in the form `1. Role name`.
Do not include a heading, introduction, rationale, examples, actions, or commentary.
Stop immediately after the final role. Do not infer roles absent from the text."""

# Build the message list for each promoting technique

messages_zero_shot = [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}]
prompt_zero_shot = tokenizer.apply_chat_template(messages_zero_shot, tokenize=False, add_generation_prompt=True)

messages_one_shot = [{"role": "system", "content": system_prompt}] + shots[0] + [{"role": "user", "content": query}]
prompt_one_shot = tokenizer.apply_chat_template(messages_one_shot, tokenize=False, add_generation_prompt=True)

messages_few_shots = [{"role": "system", "content": system_prompt}] + [message for shot in shots for message in shot] + [{"role": "user", "content": query}]
prompt_few_shots = tokenizer.apply_chat_template(messages_few_shots, tokenize=False, add_generation_prompt=True)


# Call the LLM function for the three prompts and print the results
roles_extracted_zero_shot = make_a_query(prompt_zero_shot, tokenizer, model, device, max_new_tokens=96)

print("Extracted Roles - zero shot: \n", roles_extracted_zero_shot)

roles_extracted_one_shot = make_a_query(prompt_one_shot, tokenizer, model, device, max_new_tokens=96)

print("Extracted Roles - one shot: \n", roles_extracted_one_shot)


roles_extracted_few_shots = make_a_query(prompt_few_shots, tokenizer, model, device, max_new_tokens=96)

print("Extracted Roles - few shots: \n", roles_extracted_few_shots)