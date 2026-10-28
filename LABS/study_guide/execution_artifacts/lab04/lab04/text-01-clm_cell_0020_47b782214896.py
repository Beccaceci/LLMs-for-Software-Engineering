# TODO: Generate Output of the Model After Fine-Tuning
output_finetuned = finetuned_model.generate(**inputs, max_new_tokens=100, do_sample=False, pad_token_id=tokenizer.eos_token_id)
generated_finetuned = tokenizer.decode(output_finetuned[0], skip_special_tokens=True)

print("**After Fine-Tuning (Fine-Tuned on Medical Dataset)**:")
print(generated_finetuned)