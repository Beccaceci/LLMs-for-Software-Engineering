import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

release_model()

model_id = "meta-llama/Llama-3.2-1B-Instruct"

# Load the model with `torch.float16` precision and the tokenizer 
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, low_cpu_mem_usage=True).to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Set the pad token to the end of the sequence token
tokenizer.pad_token = tokenizer.eos_token

# Create the pipeline with the model and tokenizer
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    pad_token_id=tokenizer.eos_token_id
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "What is 2 + 2?"},
]

# Format the messages using the chat template and generate the output text
formatted_messages = chat_template.format(
    system_message=messages[0]["content"],
    user_message=messages[1]["content"]
)
outputs = pipe(formatted_messages, max_new_tokens=512, do_sample=False)

print(outputs[0]["generated_text"])