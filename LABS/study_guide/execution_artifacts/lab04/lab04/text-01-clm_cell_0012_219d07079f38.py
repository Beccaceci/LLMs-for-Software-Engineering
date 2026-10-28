# TODO: Add labels to the dataset
def add_labels(samples):
    # NOTE: The labels, in causal modeling, should be the same as the input_ids
    samples["labels"] = [
        [token if attended else -100 for token, attended in zip(ids, mask)]
        for ids, mask in zip(samples["input_ids"], samples["attention_mask"])
    ]  # Ignore padding in the loss; GPT-2 shifts labels internally.
    return samples

tokenized_dataset = tokenized_dataset.map(add_labels, batched=True)
tokenized_dataset_eval = tokenized_dataset_eval.map(add_labels, batched=True)