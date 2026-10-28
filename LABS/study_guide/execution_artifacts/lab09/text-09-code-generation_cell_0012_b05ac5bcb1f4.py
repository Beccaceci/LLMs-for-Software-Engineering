llama_label = "Llama-3.2-3B-Instruct"
llama_metrics = evaluate_code(my_codes[llama_label],name="Llama_grades")
llama_functional_correctness = llama_metrics["FunctionalCorrectness"]
