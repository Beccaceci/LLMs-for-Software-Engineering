## Lab 04

The fourth lab is divided into two parts:
- CLM: this part uses causal language modeling (CLM) to generate new sequences of tokens. You will use GPT-2 to generate new sequences of tokens. In particular, you will first fine-tune the model on a medical text dataset. Then, you will use the fine-tuned model to generate new sequences of tokens that are (somewhat) coherent with the medical domain.

- LLMs: this part focuses on using various LLMs (Llama 3.2, and Mistral v0.2). You will see how we can use instruction-tuned versions of those models to get coherent answers to various questions. 

The following are the files you will use for this lab:
- CLM exercise ([text](text-01-clm.ipynb)) ([solution](solution-01-clm.ipynb))
- LLMs exercise ([text](text-02-llms.ipynb)) ([solution](solution-02-llms.ipynb))

## Local execution

The completed exercises are saved in `text-01-clm.ipynb` and `text-02-llms.ipynb`; outputs are written into each notebook as cells finish. The execution runner and pinned package versions are in `execution/`.

From this directory, recreate the Python environment and register its Jupyter kernel with:

```sh
uv venv /private/tmp/llms-lab04-venv --python 3.11
uv pip install --python /private/tmp/llms-lab04-venv/bin/python -r execution/requirements-lock.txt
/private/tmp/llms-lab04-venv/bin/python -m ipykernel install --user --name llms-lab04 --display-name 'Python (Lab 04)'
```

The Llama exercises require a local Hugging Face login with approved access to both `meta-llama/Llama-3.2-1B` and `meta-llama/Llama-3.2-1B-Instruct`. Configure that login using `/private/tmp/llms-lab04-venv/bin/hf auth login`. Credentials are read from the local Hugging Face credential store or `HF_TOKEN`; they are never embedded in notebook source.

Run both notebooks from clean kernels with:

```sh
/private/tmp/llms-lab04-venv/bin/python execution/run_notebooks.py
```

To execute the public Mistral exercise independently of gated Llama access:

```sh
/private/tmp/llms-lab04-venv/bin/python execution/run_notebooks.py text-02-llms.ipynb --cells 3,29,32,34,36,37
```

GPT-2 still selects 1,000 training abstracts and 500 evaluation abstracts, uses a 1,024-token context, and is configured for one epoch. The original batch size of six exceeded MPS memory, so training uses one example per microbatch and six accumulation steps, with one example per evaluation batch. Padding labels use `-100`; attended tokens, including genuine EOS tokens, retain their token IDs. The model performs the next-token label shift internally.

Llama is loaded in FP16 as requested. Mistral loads the same official `mistralai/Mistral-7B-Instruct-v0.2` checkpoint with Quanto 4-bit weights on MPS machines with less than 24 GB of memory, and FP16 otherwise. This is recorded in its cell output. Models are released between successive LLM loads.

Execution records contain cell source hashes, timings, execution status, package versions, and checkpoint revisions. The initial GPT-2 memory failure remains in `execution/clm-initial-oom.log`; its corrected run is separate. The authentication failure remains visible until local Llama access is configured and that section can be rerun.
