from transformers import Trainer, TrainingArguments

batch_size = 32
num_train_epochs = 1

learning_rate = 2e-4
weight_decay = 0.01

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    eval_strategy="steps",
    eval_steps=10,
    learning_rate=learning_rate,
    # Accumulate smaller microbatches to retain effective batch size 32.
    per_device_train_batch_size=4,
    gradient_accumulation_steps=batch_size // 4,
    per_device_eval_batch_size=8,
    num_train_epochs=num_train_epochs,
    weight_decay=weight_decay,
    logging_dir='./logs',  # Directory for storing logs
    logging_steps=10,  # Log every 10 steps
    report_to="none",
    seed=42,
    dataloader_pin_memory=torch.cuda.is_available(),
)

# Initialize the Trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics
)