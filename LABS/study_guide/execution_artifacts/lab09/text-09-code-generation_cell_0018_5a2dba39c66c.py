# A separate additional-engine comparison, not a replacement for the specified Llama model.
# Run this when a heavy-compute slot is available; it downloads the named public checkpoint.
additional_model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
select_engine(additional_model_id)
additional_prompt = tokenizer.apply_chat_template([
    {"role":"system","content":sys_prompt},{"role":"user","content":query},
], tokenize=False, add_generation_prompt=True)
qwen_chat = make_a_query(additional_prompt,tokenizer,model,device)
if qwen_chat.startswith("```"):
    qwen_chat = qwen_chat.split("\n",1)[1].rsplit("```",1)[0].strip()
my_codes["Qwen2.5-Coder-1.5B-Instruct"] = qwen_chat
code_provenance["Qwen2.5-Coder-1.5B-Instruct"] = additional_model_id
print(qwen_chat)
overall_results = compare_codes(my_codes)
print(json.dumps(overall_results,indent=2))
