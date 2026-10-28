import json
from tqdm import tqdm

# Generate questions and answers, then save to JSON
questions = generate_random_math_questions(num_samples=5)
answers = []

# Generate structured answers for each question
for question, num1, num2 in tqdm(questions):
    # TODO: Define the message prompts
    formatted_messages = [role_instruction, {"role": "user", "content": question}]
    
    # TODO: Generate the response
    outputs = pipe(formatted_messages, max_new_tokens=100, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    
    # Extract the model's JSON output
    structured_answer = outputs[0]["generated_text"]

    answers.append({
        "question": question,
        "num_1": num1,
        "num_2": num2,
        "model_answer": structured_answer
    })

# Save answers to a JSON file
with open("model_answers.json", "w") as f:
    json.dump(answers, f, indent=2)