fig, ax = plt.subplots()

ax.imshow(attention[1][0, 1].detach().cpu().numpy(), cmap='viridis', aspect='equal')
ax.set_xticks(np.arange(len(inputs['input_ids'][0])), tokenizer.convert_ids_to_tokens(inputs['input_ids'][0]), rotation=90)
ax.set_yticks(np.arange(len(inputs['input_ids'][0])), tokenizer.convert_ids_to_tokens(inputs['input_ids'][0]));

ax.set_xlabel("Attended token")
ax.set_ylabel("Attending token")