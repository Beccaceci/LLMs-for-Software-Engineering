import random
random.seed(42)

def generate_random_math_questions(num_samples=5):
    """
    Generate random math questions with two numbers for a given number of samples.

    Args:
        num_samples (int): The number of math questions to generate.
    
    Returns:
        List of tuples: A list of tuples containing the math question and the two numbers (question, num1, num2).
    """

    # Define templates for math questions with two numbers
    templates = [
        "What is the sum of {} and {}?",
        "Can you add {} and {}?",
        "Calculate the sum of {} and {} for me.",
        "How much is {} plus {}?",
        "Please add {} and {}."
    ]
    
    questions = []
    for _ in range(num_samples):
        # TODO: Randomly select a template and generate two random numbers
        template = random.choice(templates)
        num1 = random.randint(1, 1000)
        num2 = random.randint(1, 1000)
        question = template.format(num1, num2)
        questions.append((question, num1, num2))  # store question with numbers for validation
    return questions