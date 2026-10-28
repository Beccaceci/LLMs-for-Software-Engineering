file_path = LAB_DIR / "function_01.py"


def write_reference(source):
    file_path.write_text(source + "\n")
    # A same-sized mutation made within one timestamp tick can otherwise reuse .pyc.
    for cache in (LAB_DIR / "__pycache__").glob("function_01.*.pyc"):
        cache.unlink()


def evaluate_mutants(test_file, baseline, tag):
    passing_baseline = {key for key, value in baseline["outcomes"].items() if value == "passed"}
    details = []
    try:
        for index, (mutant, description) in enumerate(zip(mutants, mutant_descriptions), 1):
            write_reference(mutant)
            _, counts = run_suite(test_file, f"{tag}-mutant-{index}")
            # An already-failing generated test cannot provide evidence of killing a mutant.
            newly_failing = sorted(key for key, state in counts["outcomes"].items()
                                   if key in passing_baseline and state == "failed")
            killed = bool(newly_failing)
            details.append({"mutant": index, "change": description,
                            "killed": killed, "newly_failing_tests": newly_failing})
            print(f"Mutant {index}: {'killed' if killed else 'survived'} ({description})")
    finally:
        write_reference(original_function)
    return details


manual_mutations = evaluate_mutants("test_function_01_manual.py", manual_baseline, "manual")
killed_mutants = sum(entry["killed"] for entry in manual_mutations)
survived_mutants = len(mutants) - killed_mutants
mutation_score = killed_mutants / len(mutants)
print(f"Killed: {killed_mutants}; survived: {survived_mutants}")
print(f"Mutation score: {mutation_score:.2%}")