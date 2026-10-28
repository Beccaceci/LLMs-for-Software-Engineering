# Build correctly masked causal-LM batches. Padding uses EOS as its token ID,
# so the attention mask—not token identity—decides which labels become -100.
class UnpaddedTokenDataset(Dataset):
    def __init__(self, encoded):
        self.rows = []
        for row in encoded:
            length = int(sum(row["attention_mask"]))
            self.rows.append({"input_ids": row["input_ids"][:length], "attention_mask": row["attention_mask"][:length]})
    def __len__(self):
        return len(self.rows)
    def __getitem__(self, index):
        return self.rows[index]

class CausalPaddingCollator:
    def __init__(self, tokenizer, mode):
        self.tokenizer, self.mode = tokenizer, mode
    def __call__(self, features):
        batch = self.tokenizer.pad(
            [{"input_ids": f["input_ids"], "attention_mask": f["attention_mask"]} for f in features],
            padding="max_length" if self.mode == "fixed" else True,
            max_length=MAX_LENGTH if self.mode == "fixed" else None,
            return_tensors="pt",
        )
        labels = batch["input_ids"].clone()
        labels[batch["attention_mask"] == 0] = -100
        batch["labels"] = labels
        return batch

train_unpadded = UnpaddedTokenDataset(tokenized_dataset)
eval_unpadded = UnpaddedTokenDataset(tokenized_dataset_eval)
collator_check = CausalPaddingCollator(tokenizer, "dynamic")([
    {"input_ids": [tokenizer.eos_token_id, 17], "attention_mask": [1, 1]},
    {"input_ids": [tokenizer.eos_token_id], "attention_mask": [1]},
])
assert collator_check["labels"][0, 0].item() == tokenizer.eos_token_id
assert collator_check["labels"][1, 0].item() == tokenizer.eos_token_id
assert collator_check["labels"][1, 1].item() == -100
print("Collator check passed: attended EOS targets remain; only padded labels are ignored.")
print("Example batch tensor shapes:", {key: tuple(value.shape) for key, value in collator_check.items()})
