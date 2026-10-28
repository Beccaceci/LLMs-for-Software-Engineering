# Train from the public GPT-2 checkpoint with fixed 1,024-token padding. This
# is a fresh, matched timing run; the earlier medical-domain checkpoint is untouched.
def sync_device():
    if device == "mps":
        torch.mps.synchronize()
    elif device == "cuda":
        torch.cuda.synchronize()

def train_padding_variant(name, mode):
    from transformers import Trainer, TrainingArguments
    output_dir = f"./padding-benchmarks/{name}"
    model = AutoModelForCausalLM.from_pretrained(model_name, attn_implementation="sdpa")
    model.config.use_cache = False
    args = TrainingArguments(
        output_dir=output_dir, overwrite_output_dir=True, max_steps=12,
        per_device_train_batch_size=1, gradient_accumulation_steps=6,
        per_device_eval_batch_size=1, save_strategy="no", logging_dir=f"{output_dir}/logs",
        logging_steps=6, eval_strategy="no", report_to="none",
        seed=42, data_seed=42, dataloader_pin_memory=(device == "cuda"),
    )
    trainer = Trainer(model=model, args=args, train_dataset=train_unpadded,
                      eval_dataset=eval_unpadded, data_collator=CausalPaddingCollator(tokenizer, mode))
    sync_device()
    started = time.perf_counter()
    result = trainer.train()
    sync_device()
    elapsed = time.perf_counter() - started
    record = {"variant": name, "padding": mode, "wall_seconds": elapsed,
              "trainer_metrics": result.metrics, "global_step": trainer.state.global_step,
              "final_epoch": trainer.state.epoch, "device": device, "seed": 42,
              "train_examples": len(train_unpadded), "eval_examples": len(eval_unpadded),
              "max_steps": 12, "evaluation": "disabled for matched short timing run",
              "microbatch": 1, "gradient_accumulation_steps": 6}
    result_path = Path("padding-benchmarks/training-results.json")
    prior = json.loads(result_path.read_text()) if result_path.exists() else []
    prior.append(record)
    result_path.write_text(json.dumps(prior, indent=2, default=str) + "\n")
    del trainer, model
    import gc
    gc.collect()
    if device == "mps": torch.mps.empty_cache()
    if device == "cuda": torch.cuda.empty_cache()
    print(json.dumps(record, indent=2, default=str))
    return record
