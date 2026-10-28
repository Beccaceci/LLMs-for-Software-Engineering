# Laboratory 10 execution

All seven code cells in `text-10-test-generation.ipynb` executed successfully from a clean kernel on 25 October 2026. The notebook contains the observed outputs and no error outputs. Per-cell source hashes, elapsed times, and environment information are recorded in `execution.json` and `environment.json`.

The manual suite has 21 passing cases, 100% statement coverage, and kills all five single-change mutants.

| Test suite | Tests | Passed | Failed | Statement coverage | Mutants killed |
|---|---:|---:|---:|---:|---:|
| Supplied GPT example | 12 | 11 | 1 | 96% | 2/5 |
| Supplied Copilot example | 3 | 3 | 0 | 100% | 5/5 |
| Supplied Qwen example | 20 | 20 | 0 | 100% | 5/5 |
| Fresh Codex-authored suite | 27 | 27 | 0 | 100% | 5/5 |

The supplied GPT example incorrectly expects disqualification for times `[120,140,160]` with winner times `[80,100,110]`; the strict limits are `[120,150,165]`, and none is exceeded. Its incorrect expectation is retained and reported as an experimental result, rather than changing the reference to make it pass. Mutation kills count only new failures among baseline-passing tests, so this existing failure does not inflate the mutation score.

The original `function_01.py` was a leftover mutant ending in `return True`. It is repaired to match the notebook's reference implementation, which returns `disqualified`. The baseline file is preserved as `baseline_function_01.py.txt`. Mutation evaluation restores the reference in a `finally` block, and the notebook runner also restores it after an interruption. Bytecode caches are removed before each mutation to avoid stale imports.

The supplied GPT, Copilot and Qwen test files are byte-for-byte unchanged. Execution copies in `suites/` remove only the Copilot file's unconditional top-level `pytest.main()` call, which otherwise launches nested test discovery during import. The copied test functions are unchanged. Statement coverage is distinct from branch coverage, and a test count represents pytest test items rather than the number of assertions.

## Generation provenance

The GPT, Copilot and Qwen suites are existing repository examples; their original model provenance is not independently verified. This execution evaluates those examples without claiming to regenerate their outputs. The new `test_function_01_codex.py` suite was freshly authored by the Codex agent for this task. No Hugging Face inference or external model API call was performed for Lab 10. `test-provenance.json` records this distinction and source hashes. If a fresh local Hugging Face generation is required in addition to these samples, it remains a separate experiment to schedule after the current shared-model workload.

## Reproduce

The active environment is `/private/tmp/llms-lab10-venv`, with the `llms-lab10` Jupyter kernel. Run from the repository root:

```sh
/private/tmp/llms-lab10-venv/bin/python LABS/lab10/execution/run_notebook.py
```

To recreate it:

```sh
uv venv /private/tmp/llms-lab10-venv --python 3.11
uv pip install --python /private/tmp/llms-lab10-venv/bin/python -r LABS/lab10/execution/requirements-lock.txt
/private/tmp/llms-lab10-venv/bin/python -m ipykernel install --user --name llms-lab10 --display-name 'Python (Lab 10)'
/private/tmp/llms-lab10-venv/bin/python LABS/lab10/execution/run_notebook.py
```

Pytest XML reports, coverage reports, and individual mutation logs are retained under this directory. `comparison.json` records the comparison metrics and exact failing test identifiers. No Lab 10 process remains active after this run.
