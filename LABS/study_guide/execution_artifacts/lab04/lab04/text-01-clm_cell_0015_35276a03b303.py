# Set Training Parameters
training_args = TrainingArguments(
    output_dir="./gpt2-medical-finetuned",
    overwrite_output_dir=True,
    num_train_epochs=1,
    # Keep the effective batch size at 6 while fitting a 16 GB Mac.
    per_device_train_batch_size=1,
    gradient_accumulation_steps=6,
    per_device_eval_batch_size=1,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=100,
    eval_steps=10,
    eval_strategy="steps",
    report_to="none",
    seed=42,
    dataloader_pin_memory=(device == "cuda"),
)

# TODO: Initialize GPT-2 Model
model = AutoModelForCausalLM.from_pretrained(model_name, attn_implementation="sdpa")
model.config.use_cache = False  # KV caches are only needed for generation.

# TODO: Fine-Tune the Model with the `Trainer` method and pass also the eval_dataset 
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset_eval,
)

import time
training_start = time.perf_counter()
train_result = trainer.train()
fixed_padding_training_seconds = time.perf_counter() - training_start
print(train_result.metrics)
print(f"Fixed-padding training: {fixed_padding_training_seconds:.2f} seconds")

# Save the Fine-Tuned Model
model.config.use_cache = True
model.save_pretrained("./gpt2-medical-finetuned")
tokenizer.save_pretrained("./gpt2-medical-finetuned")