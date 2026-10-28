# Laboratory 08 execution status

The requested code blanks are filled. Execution is **partial**. The existing notebook has a recorded 401 from an earlier environment; local Hugging Face authentication and access to the prescribed checkpoint have since been verified. A clean successful run is pending the shared MPS slot. No replacement model or invented model output is used.

| Code cell index | State | Evidence |
|---|---|---|
| 1 | Passed | Seeded 100 × 5 vectors, actual perturbations, cosine matrix |
| 3 | Passed | TPR 0.44, FPR 0.03888888888888889 at threshold 0.95 |
| 5 | Passed | ROC plot, grid AUC 0.920869, exact ranking AUC 0.920541 |
| 8 | Prior attempt failed; retry queued | Prior environment returned HTTP 401; current environment verifies access at revision `0cb88a4f764b7a12671c53f0838cd831a0843b95` |
| 10 | Blocked | Router generation depends on the model in cell 8 |
| 12 | Blocked | Task generation depends on the router/model |

The ROC outputs above are the explicitly requested synthetic experiment, not measured LLM performance. The grid uses 100 thresholds in [0,1] and adds positive/negative infinity so the curve includes none-positive and all-positive endpoints even when cosine scores are negative. `cell_005.png` is exported from the notebook's actual output and was visually inspected. Nine synthetic helper checks passed, including known confusion matrices, unknown/ambiguous router decisions, and empty-data rejection. All six source cells compile.

Fixed runtime and mathematical issues include confusion-count updates, aligned-matrix indexing, safe rate denominators, the `appy_chat_template` typo, duplicated chat special tokens, model inference mode, and deterministic unattended router input. The router accepts only a supported model-produced decision and raises on unsupported output; it does not infer an answer from the expected route.

`baseline.json` records the pre-edit notebook hash and cell inventory. `execution.json` records observed results and exact source hashes. `requirements-lock.txt` records the isolated Python 3.11 environment. `final-manifest.json` records the saved notebook state.

No Lab 08 model or execution process remains active.

## Resume

After allocation of the shared MPS compute slot:

```sh
/Users/nicolabeccaceci/.venvs/llms-lab08/bin/python LABS/lab08/execution/run_notebook.py
```

The default request asks for use cases. To exercise the other router branch in a separate clean run:

```sh
LAB08_TASK='Generate the class diagram for the hiking platform.' /Users/nicolabeccaceci/.venvs/llms-lab08/bin/python LABS/lab08/execution/run_notebook.py
```

To recreate the environment after `/private/tmp` cleanup, install `requirements-lock.txt` into a Python 3.11 virtual environment and register its IPython kernel as `llms-lab08`. Authentication must remain local; no token belongs in the notebook.


The user has scoped this pass to notebook solutions and execution; lecture review is deferred until the professor provides the recordings.
