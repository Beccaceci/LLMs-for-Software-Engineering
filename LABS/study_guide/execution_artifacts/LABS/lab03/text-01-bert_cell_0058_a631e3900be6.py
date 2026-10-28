# Load the pre-trained BERT model (with `num_labels=2`) and tokenizer
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
tokenizer = BertTokenizer.from_pretrained(model_name)

# set the device to GPU if available and move the model to the device
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)

print(model.classifier)
