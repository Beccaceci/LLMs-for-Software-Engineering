# Laboratory 02 execution status

Both notebooks were executed from clean Python 3.11 CPU kernels on 26 October 2026. All 66 nonempty code cells completed with no error outputs: the T5 notebook ran 51/51 cells, and the attention notebook ran 15/15 cells. The per-cell execution records contain cell index, exact source SHA-256, execution count, duration, and peak kernel memory observation.

The current notebook source hashes match the executed cells. The clean run used the cached `google-t5/t5-base` checkpoint and retained the notebook's datasets, training schedules, and evaluation steps.

During this work, the attention notebook's relative-position bias was registered as a trainable parameter, its sinusoidal encoding was corrected to index sequence positions for batch-first inputs, and the CPU square-root scale was made device-safe. The original Lab 02 PDF predates these notebook fixes and was not rebuilt because this task concerns solving and executing the notebooks.

Reproduce from the repository root with:

```sh
/private/tmp/llms-lab02-venv/bin/python LABS/lab02/execution/run_notebooks.py
```
