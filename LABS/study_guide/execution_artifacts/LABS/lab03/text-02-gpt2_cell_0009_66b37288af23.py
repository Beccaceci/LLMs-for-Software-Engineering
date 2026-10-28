model_name = 'gpt2'
model = GPT2Model.from_pretrained(model_name, output_attentions=True)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Input prompt
prompt = "I love Italian food, my favorite dish is"

# Tokenize the input prompt
inputs = tokenizer(prompt, return_tensors='pt')

with torch.no_grad():
    # Generate the model output and retrieve attention weights
    outputs = model(**inputs)
    attentions = outputs.attentions

# Visualize the attention weights from the last layer
attention_matrix = attentions[-1][0][10].cpu().numpy()  # Last layer, tenth head

# Get the tokens for the input prompt
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

# Plot the attention matrix (last layer, first head) with words as labels
plt.figure(figsize=(10, 8))
sns.heatmap(attention_matrix, xticklabels=tokens, yticklabels=tokens, cmap='viridis')
plt.title('Self-Attention Matrix (Last Layer, Tenth Head)')
plt.xlabel('Token')
plt.ylabel('Token')
plt.show()
