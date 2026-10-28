import ast
import datetime
import hashlib
import json

# Fresh generation by the Codex agent handling this lab; no external API is called.
codex_test_source = '"""Fresh Codex-authored tests generated for this laboratory execution."""\nimport pytest\nfrom lab10.function_01 import racer_disqualified\n\n@pytest.mark.parametrize("event", range(3))\n@pytest.mark.parametrize("offset, expected", [(-1, False), (0, False), (1, True)])\ndef test_time_limit_for_each_event(event, offset, expected):\n    winner = [100, 200, 300]\n    times = winner.copy()\n    times[event] = int(1.5 * winner[event]) + offset\n    assert racer_disqualified(times, winner, 0, []) is expected\n\n@pytest.mark.parametrize("penalties, expected", [\n    ([], False), ([99], False), ([100], False), ([101], True),\n    ([50, 50], False), ([50, 51], True), ([1] * 5, False), ([1] * 6, True),\n])\ndef test_penalty_limits(penalties, expected):\n    assert racer_disqualified([10, 20, 30], [10, 20, 30], len(penalties), penalties) is expected\n\n@pytest.mark.parametrize("position, invalid", [\n    (0, (10, 20, 30)), (0, [10, 20]), (0, [10, 20, "30"]),\n    (1, None), (1, [10, 20]), (1, [10, 20, 30.5]),\n    (2, "0"), (3, ()), (3, ["10"]), (3, [10]),\n])\ndef test_reference_input_contract(position, invalid):\n    args = [[10, 20, 30], [10, 20, 30], 0, []]\n    args[position] = invalid\n    with pytest.raises(ValueError):\n        racer_disqualified(*args)\n'
(LAB_DIR / "test_function_01_codex.py").write_text(codex_test_source)

# Evaluate the supplied examples alongside the new, explicitly labeled suite.
test_files = [
    "test_function_01_gpt.py", "test_function_01_copilot.py",
    "test_function_01_qwen.py", "test_function_01_codex.py",
]
suite_dir = ARTIFACTS / "suites"
suite_dir.mkdir(exist_ok=True)
comparison = {}
provenance = []

for test_file in test_files:
    source_path = LAB_DIR / test_file
    test_source = source_path.read_text()
    tree = ast.parse(test_source)
    runner_calls = [node for node in tree.body if isinstance(node, ast.Expr)
                    and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Attribute)
                    and isinstance(node.value.func.value, ast.Name)
                    and node.value.func.value.id == "pytest"
                    and node.value.func.attr == "main"]
    # Remove only side-effectful top-level test-runner invocations in execution copies.
    lines = test_source.splitlines(keepends=True)
    for node in reversed(runner_calls):
        del lines[node.lineno - 1:node.end_lineno]
    execution_path = suite_dir / test_file
    execution_path.write_text("".join(lines))
    provenance.append({
        "file": test_file,
        "origin": "fresh Codex generation" if "codex" in test_file else "supplied repository example",
        "source_sha256": hashlib.sha256(test_source.encode()).hexdigest(),
        "removed_top_level_pytest_main_calls": len(runner_calls),
    })

    print("\nDoing:", test_file)
    write_reference(original_function)
    tag = source_path.stem
    _, baseline = run_suite(execution_path, tag + "-baseline")
    number_of_tests = baseline["total"]
    pass_rate = baseline["pass_rate"]
    print(f"Number of tests: {number_of_tests}")
    print(f"Pass Rate: {pass_rate:.2%} ({baseline['failed']} failed)")
    if baseline["failed"]:
        print("Failing reference tests:", [key for key, state in baseline["outcomes"].items() if state == "failed"])
    _, coverage_report, coverage = measure_coverage(execution_path, tag)
    print(f"Coverage: {coverage}%")
    mutation_details = evaluate_mutants(execution_path, baseline, tag)
    killed_mutants = sum(entry["killed"] for entry in mutation_details)
    survived_mutants = len(mutants) - killed_mutants
    mutation_score = killed_mutants / len(mutants)
    print(f"Mutation score: {mutation_score:.2%}")
    comparison[test_file] = {
        "tests": number_of_tests, "passed": baseline["passed"], "failed": baseline["failed"],
        "pass_rate": pass_rate, "statement_coverage_percent": coverage,
        "killed_mutants": killed_mutants, "survived_mutants": survived_mutants,
        "mutation_score": mutation_score, "mutants": mutation_details,
    }

write_reference(original_function)
(ARTIFACTS / "comparison.json").write_text(json.dumps(comparison, indent=2) + "\n")
(ARTIFACTS / "test-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
print("\nOriginal function restored:", file_path.read_text() == original_function + "\n")