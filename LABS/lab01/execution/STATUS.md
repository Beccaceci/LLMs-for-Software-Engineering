# Laboratory 01 execution

The notebook's existing TODO implementations were reviewed. The previous saved outputs were cleared for a fresh execution as requested. A clean CPU preparation run completed **17 of 50 code cells**, including the matrix timing experiment, the complete 50-epoch linear regression example, and both computational graph/backpropagation examples. No current notebook error outputs remain. Every completed cell's exact source hash matches its saved execution record.

Observed linear-regression parameters were weight 1.9957 and bias 0.9978. The final graph example produced loss 9.0 and derivatives 18.0 and 12.0. These are real outputs from the saved notebook, not reconstructed values.

The other **33 cells** require the CIFAR dataset and/or the full CIFAR-10/CIFAR-100 training sequence. They have not been executed in this fresh run. The full datasets and original epoch counts are retained: 5 epochs for the simple classifier, 5 for scratch ResNet-18, 5 for pretrained ResNet-18, and 1 for the frozen-backbone CIFAR-100 classification head.

## Fixes

- Select MPS on this Apple Silicon machine, with `LAB01_DEVICE=cpu` available for independent preparation.
- Use the lab-local `data/` cache, matching the ongoing original-archive download; `LAB01_DATA_DIR` can override it.
- Use notebook-compatible DataLoader worker count zero.
- Release the channel-statistics cell's 1.23 GB float64 temporary before model training.
- Call `pretrained_model.train()` when fine-tuning that model.
- Keep the frozen CIFAR-100 backbone's BatchNorm running statistics fixed while training its new classification head.
- Repair the two local markdown image paths to the existing `images/` folder.
- Seed PyTorch and limit CPU threads to four for the shared machine.

The existing solution PDF was not rebuilt or edited and does not describe this new execution state.

## Resume

Wait for the parent coordinator's MPS allocation, then run the entire notebook from a clean kernel:

```sh
/private/tmp/llms-lab01-venv/bin/python LABS/lab01/execution/run_notebook.py > LABS/lab01/execution/full.log 2>&1
```

The runner checkpoints actual outputs and source hashes after every cell. It uses the `llms-lab01` kernel. `requirements-lock.txt` and `environment.json` record the tested environment; Graphviz's `dot` is present at `/opt/homebrew/bin/dot`.

For the data-independent CPU preparation run:

```sh
/private/tmp/llms-lab01-venv/bin/python LABS/lab01/execution/run_notebook.py --light --cells 2,4,6,11,12,14,16,18,20,22,24,25,26,28,80,83,84
```

The earlier `light.log` records a coordinator interruption before any dataset download, to prevent a second download into the old `~/data` path. `light-independent.log` and `light-execution.json` contain the successful preparation run.

## Dataset download repair

The official Toronto archive endpoint measured about 80 KB/s on a single connection and supports HTTP range responses. The original cache process was stopped before starting the replacement. `cache_datasets.py` downloads eight disjoint ranges concurrently from the exact torchvision archive URLs, validates response ranges and lengths, assembles them into a separate temporary file, checks torchvision's official MD5, and only then replaces the incomplete archive and extracts it. This changes transport only, not dataset content. `data/` is ignored as generated cache material.

The caching command is:

```sh
/private/tmp/llms-lab01-venv/bin/python LABS/lab01/execution/cache_datasets.py > LABS/lab01/execution/cache.log 2>&1
```

Caching completed successfully. Both original archives passed their official MD5 checks; each dataset contains 50,000 training and 10,000 test examples. The ResNet-18 weight file passed its expected SHA-256 prefix check. `cache-validation.json` records the hashes and sizes. No cache process remains running. The full execution is ready and awaits the coordinator’s MPS go-ahead.
