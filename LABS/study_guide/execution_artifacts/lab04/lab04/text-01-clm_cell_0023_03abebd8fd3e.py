# The saved dataset already contains 1,024 positions per row. Recover each
# unpadded prefix using its attention mask; an attended EOS remains content.
import json
import math
import random
import time
from pathlib import Path
import pandas as pd
from torch.utils.data import Dataset

train_lengths = [int(sum(row["attention_mask"])) for row in tokenized_dataset]
eval_lengths = [int(sum(row["attention_mask"])) for row in tokenized_dataset_eval]
assert len(train_lengths) == 1000 and len(eval_lengths) == 500
assert all(0 < length <= 1024 for length in train_lengths + eval_lengths)
print(f"Training examples: {len(train_lengths)}; evaluation examples: {len(eval_lengths)}")
print(f"Training token lengths: min={min(train_lengths)}, median={int(pd.Series(train_lengths).median())}, max={max(train_lengths)}")
