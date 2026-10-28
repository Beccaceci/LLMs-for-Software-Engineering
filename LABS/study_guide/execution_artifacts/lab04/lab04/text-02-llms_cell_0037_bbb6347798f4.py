import json

# Function to parse model's answer and verify correctness
def verify_answer(entry):
    try:
        # Extract expected values
        num1, num2 = entry["num_1"], entry["num_2"]
        expected_answer = num1 + num2
        
        # Extract the assistant's response from the list of messages
        assistant_message = next(
            (msg["content"] for msg in entry["model_answer"] if msg["role"] == "assistant"), None
        )
        
        if assistant_message is None:
            raise ValueError("Assistant's message not found in model_answer")
        
        # Parse model's structured answer from JSON
        model_response = json.loads(assistant_message.strip())  # Ensure model_answer is a string
        
        print(f"Expected answer: {num1} + {num2} = {expected_answer}")
        print(f"Model's answer: {model_response['num_1']} + {model_response['num_2']} = {model_response['answer']}")
        
        # Check if the values match
        if (model_response["num_1"] == num1 and 
            model_response["num_2"] == num2 and 
            model_response["answer"] == expected_answer):
            return True
        else:
            return False
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        # Handle cases where parsing fails or keys are missing
        print(f"Error verifying entry: {entry}. Error: {e}")
        return False

# Load answers from the JSON file and verify
try:
    with open("model_answers.json", "r") as f:
        saved_answers = json.load(f)
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Error loading JSON file: {e}")
    saved_answers = []

for i, entry in enumerate(saved_answers, 1):
    result = verify_answer(entry)
    print(f"Question {i}:", "Correct" if result else "Incorrect", "\n")