# Count attended and padded positions for each policy using exactly the same
# training examples. The final group is retained even when it has fewer than 6.
BATCH_SIZE = 6
MAX_LENGTH = 1024

def padded_positions(lengths, batches):
    return sum(len(batch) * max(batch) - sum(batch) for batch in batches)

def grouped_lengths(lengths):
    return [lengths[i:i + BATCH_SIZE] for i in range(0, len(lengths), BATCH_SIZE)]

fixed_padding = len(train_lengths) * MAX_LENGTH - sum(train_lengths)
random_order = list(train_lengths)
random.Random(42).shuffle(random_order)
random_padding = padded_positions(train_lengths, grouped_lengths(random_order))
sorted_order = sorted(train_lengths)
similar_padding = padded_positions(train_lengths, grouped_lengths(sorted_order))
useful_tokens = sum(train_lengths)
rows = []
for name, padding in [("Fixed length 1,024", fixed_padding), ("Dynamic, seeded random batches", random_padding), ("Dynamic, similar-length batches", similar_padding)]:
    total = useful_tokens + padding
    rows.append({"Strategy": name, "Useful tokens": useful_tokens, "Padded tokens": padding, "Padding share": 100 * padding / total, "Reduction vs fixed (%)": 100 * (fixed_padding - padding) / fixed_padding})
padding_summary = pd.DataFrame(rows)
print(padding_summary.to_string(index=False, formatters={"Padding share": "{:.2f}%".format, "Reduction vs fixed (%)": "{:.2f}%".format}))
print(f"Logical batches: {math.ceil(len(train_lengths) / BATCH_SIZE)} (last batch size {len(train_lengths) % BATCH_SIZE or BATCH_SIZE})")
Path("padding-benchmarks").mkdir(exist_ok=True)
padding_summary.to_json("padding-benchmarks/token-counts.json", orient="records", indent=2)
