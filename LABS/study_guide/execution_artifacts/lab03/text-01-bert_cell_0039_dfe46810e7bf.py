top_k = 5
mask = (inputs['input_ids'] == tokenizer.mask_token_id) 
top_k_tokens = torch.argsort(predictions[mask], descending=True)[0, :top_k] # 0 => only take first mask

for token_id, token, logit in zip(top_k_tokens, tokenizer.convert_ids_to_tokens(top_k_tokens), predictions[mask][0, top_k_tokens]):
    print(f"{token} ({token_id}) - logit: {logit:.4f}")