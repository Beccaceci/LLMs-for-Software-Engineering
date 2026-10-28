import torch
import torch.nn as nn
from transformers import BertTokenizer, BertForSequenceClassification, set_seed

set_seed(42)
torch.set_num_threads(4)
print("MPS available:", torch.backends.mps.is_available())