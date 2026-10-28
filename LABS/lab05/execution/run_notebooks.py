"""Execute Lab 05 from a clean kernel and checkpoint real outputs after each cell."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import time

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]

def execute(path, stop_before=None, indices=None):
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(notebook, timeout=None, kernel_name="llms-lab05",
                            resources={"metadata": {"path": str(ROOT)}})
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records = []
    status = "partial: selected cells" if indices is not None else "complete"
    try:
        with client.setup_kernel():
            for i, cell in enumerate(notebook.cells):
                if indices is not None and i not in indices:
                    continue
                if stop_before is not None and i >= stop_before:
                    status = "partial: heavy execution pending"
                    break
                if cell.cell_type != "code" or not cell.source.strip():
                    continue
                print(f"{path.name}: starting cell {i}", flush=True)
                begin = time.perf_counter()
                cell_status = "ok"
                try:
                    client.execute_cell(cell, i)
                except BaseException:
                    cell_status = "error"
                    status = "error"
                    raise
                finally:
                    records.append({"cell_index": i, "source_sha256": hashlib.sha256(cell.source.encode()).hexdigest(),
                                    "seconds": time.perf_counter() - begin, "status": cell_status})
                    nbformat.write(notebook, path)
                    (ROOT / "execution" / f"{path.stem}.execution.json").write_text(json.dumps({
                        "started_utc": started, "status": status, "cells": records,
                    }, indent=2) + "\n")
                    print(f"{path.name}: cell {i}: {cell_status} ({records[-1]['seconds']:.1f}s)", flush=True)
    except Exception as exc:
        print(f"{path.name}: STOPPED: {type(exc).__name__}: {exc}", flush=True)
        return False
    finally:
        manifest = ROOT / "execution" / f"{path.stem}.execution.json"
        if manifest.exists():
            data = json.loads(manifest.read_text())
            data["status"] = status
            manifest.write_text(json.dumps(data, indent=2) + "\n")
    return status == "complete"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("notebooks", nargs="*", default=["text-01-quantization.ipynb", "text-02-LoRA.ipynb"])
    parser.add_argument("--stop-before", type=int)
    parser.add_argument("--offline", action="store_true", help="Use the already cached models and datasets")
    parser.add_argument("--cells", help="Comma-separated independent cell indices")
    args = parser.parse_args()
    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["HF_DATASETS_OFFLINE"] = "1"
    indices = set(map(int, args.cells.split(","))) if args.cells else None
    results = [execute(ROOT / name, args.stop_before, indices) for name in args.notebooks]
    raise SystemExit(0 if all(results) else 1)
