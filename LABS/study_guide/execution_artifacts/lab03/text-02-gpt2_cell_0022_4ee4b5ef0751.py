# Beam Search (simple version with fixed beam width)

# NOTE: each score is the log-probability of the sequence
# (remember, the sum of log-probabilities is the log-probability of the product)
# (i.e., of the entire sentence)
def beam_search(model, input_ids, max_length, beam_width=3):
    mask = torch.ones_like(input_ids).to(device)
    sequences = [(input_ids.to(device), mask, 0.0)]  # (sequence, mask, score)
    for _ in range(max_length):
        all_candidates = []
        for seq, mask, score in sequences:
            # Compute the logits
            logits = model(input_ids=seq, attention_mask=mask).logits[:, -1, :]

            # Compute the top k tokens and their probabilities
            probs = torch.softmax(logits, dim=-1)
            top_k_probs, top_k_tokens = torch.topk(probs, beam_width, dim=-1) # Get top k tokens

            for i in range(beam_width):
                candidate_seq = torch.cat([seq, top_k_tokens[:, i].unsqueeze(-1)], dim=-1)  # Add token to sequence
                candidate_mask = torch.cat([mask, torch.ones((1, 1), dtype=torch.long, device=device)], dim=-1)
                candidate = (candidate_seq, candidate_mask, score - torch.log(top_k_probs[:, i]).item()) # Update score
                all_candidates.append(candidate) # Add new candidate

        # Select top `beam_width` sequences
        sequences = sorted(all_candidates, key=lambda x: x[2])[:beam_width]

        if sequences[0][0][0, -1].item() == tokenizer.eos_token_id:
            break

    return sequences[0][0]

# Beam Search
output_beam = beam_search(model, input_ids, max_length, beam_width=5)
print(prompt)
print(tokenizer.decode(output_beam[0, input_length:], skip_special_tokens=True))