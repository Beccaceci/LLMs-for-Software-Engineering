from transformers import Trainer, TrainingArguments

batch_size = 32
num_train_epochs = 2

learning_rate = 2e-5
weight_decay = 0.01

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    eval_strategy="steps",
    eval_steps=10,
    learning_rate=learning_rate,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=num_train_epochs,
    weight_decay=weight_decay,
    logging_steps=10,  # 
)

# Initialize the Trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics
)