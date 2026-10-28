"""Run both Laboratory 02 notebooks in clean, independent CPU kernels."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import time

import nbformat
from nbclient import NotebookClient
import psutil

ROOT = Path(__file__).resolve().parents[1]

def execute(path):
    notebook = nbformat.read(path, as_version=4)
    notebook.metadata.kernelspec = {"name": "llms-lab02", "display_name": "Python (Lab 02)", "language": "python"}
    client = NotebookClient(notebook, timeout=None, kernel_name="llms-lab02", extra_arguments=["--InteractiveShell.cache_size=0"], resources={"metadata": {"path": str(ROOT)}})
    records = []
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with client.setup_kernel():
        for i, cell in enumerate(notebook.cells):
            if cell.cell_type != "code" or not cell.source.strip():
                continue
            print(f"{path.name}: starting cell {i}", flush=True)
            begin = time.perf_counter()
            status = "ok"
            try:
                client.execute_cell(cell, i)
            except BaseException:
                status = "error"
                raise
            finally:
                rss = psutil.Process(client.km.provisioner.pid).memory_info().rss
                records.append({"cell_index": i, "source_sha256": hashlib.sha256(cell.source.encode()).hexdigest(), "execution_count": cell.get("execution_count"), "seconds": time.perf_counter() - begin, "kernel_rss_bytes": rss, "status": status})
                nbformat.write(notebook, path)
                (ROOT / "execution" / f"{path.stem}.execution.json").write_text(json.dumps({"started_utc": started, "python": platform.python_version(), "platform": platform.platform(), "backend": "CPU", "offline_cache": True, "ipython_output_cache": False, "cells": records}, indent=2) + "\n")
                print(f"{path.name}: cell {i}: {status} ({records[-1]['seconds']:.1f}s, RSS {rss / 1024**3:.2f} GiB)", flush=True)
    return notebook

if __name__ == "__main__":
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    for name in ["text-01-t5.ipynb", "text-02-attention.ipynb"]:
        execute(ROOT / name)
