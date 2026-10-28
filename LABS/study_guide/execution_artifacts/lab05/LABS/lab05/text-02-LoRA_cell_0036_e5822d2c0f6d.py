from transformers import Trainer, TrainingArguments

# Initialize the Trainer object
trainer = Trainer(
    model=peft_model,
    args=training_args, # we will recycle the same training arguments as before!
    train_dataset=train_dataset, # also datasets, 
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics # and compute_metrics
)