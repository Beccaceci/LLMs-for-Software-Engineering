ds = load_dataset("japhba/pubmed_simple", split="train")
train_dataset = ds.shuffle(seed=42).select(range(1000))
eval_dataset = ds.shuffle(seed=42).select(range(1000, 1500))