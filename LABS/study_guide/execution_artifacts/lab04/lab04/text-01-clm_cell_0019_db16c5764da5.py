# TODO: Generate Output of the Model Before Fine-Tuning (use `generate` and then `decode` methods of the model and tokenizer) 
output_pretrained = pretrained_model.generate(**inputs, max_new_tokens=100, do_sample=False, pad_token_id=tokenizer.eos_token_id)
generated_pretrained = tokenizer.decode(output_pretrained[0], skip_special_tokens=True)

print("**Before Fine-Tuning (Pre-Trained GPT-2)**:")
print(generated_pretrained)