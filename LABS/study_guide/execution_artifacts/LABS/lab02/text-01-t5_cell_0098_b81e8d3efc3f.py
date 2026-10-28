fig, ax = plt.subplots(figsize=(4,4))
ax.imshow(output.cross_attentions[0][0, :, 0].detach().numpy())
input_tokens = tokenizer.tokenize(input_sentence) + [ "</s>" ]
ax.set_xticks(range(len(input_tokens)), input_tokens, rotation=90);