sys_prompt = "You are a Python programmer. Return only valid Python source, without Markdown fences or explanations."
query = """Implement compute_average(grades). Require exactly six grades; accept real values from 18 to 30 inclusive or 33 for laude. Reject booleans/invalid values with ValueError and nonnumeric values with TypeError. Return the arithmetic mean after removing exactly one minimum and one maximum. Do not mutate the input."""
prompt = tokenizer.apply_chat_template([
    {"role":"system","content":sys_prompt},
    {"role":"user","content":query},
], tokenize=False, add_generation_prompt=True)
generated_code = make_a_query(prompt, tokenizer, model, device)
# Remove only an enclosing Markdown code fence if the instruction was not followed.
if generated_code.startswith("```"):
    generated_code = generated_code.split("\n",1)[1].rsplit("```",1)[0].strip()
my_codes["Llama-3.2-3B-Instruct"] = generated_code
code_provenance["Llama-3.2-3B-Instruct"] = current_model_id
print(generated_code)
