from transformers import AutoTokenizer

model_name = "google-t5/t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)

# print the type of the tokenizer
print(type(tokenizer))
