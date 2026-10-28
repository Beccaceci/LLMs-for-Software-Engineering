# TODO: Tokenize the Dataset using the GPT-2 tokenizer
# Hint: Use the `map` method of the dataset object
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Set padding token to EOS token

def tokenize_function(samples):
    # Tokenize the text column `abstract` in the dataset (set `truncation=True` and `padding="max_length"`)
    # NOTE: You can either use tokenzier as a global variable, or
    # use a closure to capture the tokenizer variable
    return tokenizer(samples["abstract"], truncation=True, padding="max_length", max_length=1024)

# NOTE: you should map the dataset using the tokenize function. 
# (You can optionally consider using the argument `batched=True` for better performance,
# as long as tokenize_function can handle the batch! [note2: the tokenizer can do that!])
tokenized_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=train_dataset.column_names)
tokenized_dataset_eval = eval_dataset.map(tokenize_function, batched=True, remove_columns=eval_dataset.column_names)