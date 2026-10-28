# Load pre-trained BERT model (with `output_attentions=True`) and tokenizer
model = BertModel.from_pretrained(model_name, output_attentions=True)
tokenizer = BertTokenizer.from_pretrained(model_name)

sentence = "The dog ate the food because it was hungry"

# Tokenize the sentence
inputs = tokenizer(sentence, return_tensors="pt")

# Get the model outputs
outputs = model(**inputs)

attention = outputs.attentions  # This returns a list of attention matrices