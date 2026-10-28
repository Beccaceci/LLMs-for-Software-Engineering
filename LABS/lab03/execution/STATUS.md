# Laboratory 03 execution handoff

The notebooks are source-complete. The execution environment and per-cell runner are ready at `/private/tmp/llms-lab03-venv` (`llms-lab03` kernel); exact dependencies are recorded in `requirements-lock.txt`, and original notebook/code/output states are preserved in `baseline.json` and the adjacent `*.baseline` files.

## Current execution evidence

`text-02-gpt2.ipynb` was started from a clean kernel on CPU to prepare cells that do not need the shared MPS slot. Cells 3, 5, 8, 9, 12, 13, 17, and 18 completed without errors; the remaining manual autoregressive generation cells were stopped before completion because they were too slow on CPU. Their outputs are not marked complete. The notebook records those eight successful outputs and source hashes in `text-02-gpt2.execution.json`.

`text-01-bert.ipynb` has no new execution from this task. Its previous saved outputs had no recorded errors, but it needs a fresh clean run for final verification. No Lab 03 execution process is active.

## Fixes made

The six manual GPT-2 sampling helpers now run without gradient tracking, avoiding unnecessary graph and memory growth during inference. Nucleus sampling now includes the first token that crosses the cumulative probability threshold. `LAB03_DEVICE` provides an optional CPU override for preflight; without it, the notebook selects CUDA, then MPS, then CPU.

## Resume

After the shared MPS slot is free, execute both notebooks sequentially from the repository root:

```sh
/private/tmp/llms-lab03-venv/bin/python LABS/lab03/execution/run_notebooks.py text-01-bert.ipynb text-02-gpt2.ipynb
```

The runner starts a clean kernel for each notebook, saves actual cell output after every completed cell, and records the source hash, duration, and kernel memory. BERT's existing two-epoch, 2,000-example training settings are unchanged.
