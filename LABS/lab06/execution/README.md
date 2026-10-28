# Laboratory 06 execution record

The notebook has 12 nonempty code cells and covers prompt engineering, PDF ingestion, BERT-CLS retrieval, and RAG versus direct answers. The authenticated clean run completed cells 1–21; final RAG cell 23 failed with MPS out of memory during Llama attention. The complete failed execution is preserved in `run-history/cell23-mps-oom-attempt.json` and the full-run status/history, including the original source hash and traceback.

The original attempt to load `meta-llama/Llama-3.2-3B-Instruct` returned a gated-repository 401 before local authentication was configured. Access is now verified at revision `0cb88a4f764b7a12671c53f0838cd831a0843b95`; no credential is stored in the notebook or this directory.

A lower-memory retry is prepared: RAG prompts are capped at 1,024 tokens, decoding uses one beam and at most 96 new tokens, and each generation releases MPS workspace allocations. `retry_cell23.py` starts a clean kernel and runs only cell dependencies (model setup, corpus extraction, BERT embeddings, retrieval, and RAG) while preserving successful outputs for all other cells. Do not load the model until the parent task explicitly releases the serialized MPS slot. Then run:

```sh
/Users/nicolabeccaceci/.venvs/llms-lab06/bin/python LABS/lab06/execution/retry_cell23.py
```

The pinned environment is `/Users/nicolabeccaceci/.venvs/llms-lab06` (Python 3.13.9, PyTorch 2.8.0, Transformers 4.46.3, PyMuPDF 2.0, scikit-learn 1.9.1). The `llms-lab06` Jupyter kernel points to this environment. Each attempt is stored separately under `execution/run-history/`; the OOM diagnostic will remain available after a successful retry.

No matching Lab06 lecture recording or transcript is currently available. See `transcript-validation.md`; explanations will rely on notebook instructions and supplied papers until the professor provides the recording.
