# Adapt the same actual generation/test/static-analysis workflow to the two new tasks.
# Checkpoints are sequentially released by select_engine, never loaded together.
for engine_label, engine_id in [("Llama-3.2-3B-Instruct","meta-llama/Llama-3.2-3B-Instruct"),
                                ("Qwen2.5-Coder-1.5B-Instruct",additional_model_id)]:
    select_engine(engine_id)
    for task_name, task in additional_tasks.items():
        prompt = tokenizer.apply_chat_template([
            {"role":"system","content":sys_prompt},{"role":"user","content":task["prompt"]}],
            tokenize=False,add_generation_prompt=True)
        code = make_a_query(prompt,tokenizer,model,device)
        if code.startswith("```"): code = code.split("\n",1)[1].rsplit("```",1)[0].strip()
        print(engine_label,task_name,code)
        task["sources"][engine_label] = code
        additional_results[task_name] = compare_codes(task["sources"],task["test_file"],task["function_file"],task_name)
print(json.dumps(additional_results,indent=2))
