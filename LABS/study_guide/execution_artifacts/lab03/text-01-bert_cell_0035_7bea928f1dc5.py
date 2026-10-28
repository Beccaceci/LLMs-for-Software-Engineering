# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'

# Load pre-trained BERT model for masked language modeling
model_mlm = BertForMaskedLM.from_pretrained(model_name)

print(model_mlm.cls)
