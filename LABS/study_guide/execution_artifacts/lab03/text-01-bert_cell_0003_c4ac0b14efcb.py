from transformers import BertModel, BertTokenizer
import torch
import matplotlib.pyplot as plt

model_name = "bert-base-uncased"

# Load pre-trained BERT model
model = BertModel.from_pretrained(model_name)

print(model)