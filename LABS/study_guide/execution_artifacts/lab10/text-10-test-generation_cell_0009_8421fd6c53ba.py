# Each mutant changes exactly one expression in the reference implementation.
def mutate_once(old, new):
    assert original_function.count(old) == 1
    mutated = original_function.replace(old, new, 1)
    compile(mutated, "function_01.py", "exec")
    return mutated

mutant1 = mutate_once("if penalty > 100:", "if penalty < 100:")
mutant2 = mutate_once("tot_penalties > 100", "tot_penalties >= 100")
mutant3 = mutate_once("n_penalties > 5", "n_penalties >= 5")
mutant4 = mutate_once("times[i] > max_time", "times[i] >= max_time")
mutant5 = mutate_once("return disqualified", "return True")
mutants = [mutant1, mutant2, mutant3, mutant4, mutant5]
mutant_descriptions = [
    "reverse individual penalty comparison", "include total penalty boundary",
    "include penalty-count boundary", "include time boundary", "always disqualify",
]
print(f"Prepared {len(mutants)} single-change mutants.")