"""Execute Lab 04 from clean kernels, checkpointing actual cell outputs."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
import uuid

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]

# Prefer kernels installed inside the active Lab 04 environment over stale
# user-level kernelspecs from earlier temporary runs.
_environment_jupyter = str(Path(sys.prefix) / "share" / "jupyter")
_existing_jupyter_path = os.environ.get("JUPYTER_PATH", "")
os.environ["JUPYTER_PATH"] = os.pathsep.join(
    path for path in (_environment_jupyter, _existing_jupyter_path) if path
)

def execute(path, indices=None):
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(notebook, timeout=None, kernel_name="llms-lab04",
                            resources={"metadata": {"path": str(ROOT)}})
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records = []
    run_id = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex[:8]
    try:
        with client.setup_kernel():
            for i, cell in enumerate(notebook.cells):
                if indices is not None and i not in indices:
                    continue
                if cell.cell_type != "code" or not cell.source.strip():
                    continue
                print(f"{path.name}: starting cell {i}", flush=True)
                begin = time.perf_counter()
                status = "ok"
                try:
                    client.execute_cell(cell, i)
                except Exception:
                    status = "error"
                    raise
                finally:
                    records.append({"cell_index": i, "source_sha256": hashlib.sha256(cell.source.encode()).hexdigest(),
                                    "seconds": time.perf_counter() - begin, "status": status})
                    nbformat.write(notebook, path)
                    run_record = {
                        "run_id": run_id, "notebook": path.name,
                        "started_utc": started, "python": platform.python_version(),
                        "platform": platform.platform(), "cells": records,
                    }
                    serialized = json.dumps(run_record, indent=2) + "\n"
                    history = ROOT / "execution" / "run-history" / path.stem
                    history.mkdir(parents=True, exist_ok=True)
                    (history / f"{run_id}.json").write_text(serialized)
                    # Keep the established filename as the latest-run pointer;
                    # immutable per-run records above preserve earlier evidence.
                    (ROOT / "execution" / f"{path.stem}.execution.json").write_text(serialized)
                    print(f"{path.name}: cell {i}: {status} ({records[-1]['seconds']:.1f}s)", flush=True)
    except Exception as exc:
        print(f"{path.name}: STOPPED: {type(exc).__name__}: {exc}", flush=True)
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("notebooks", nargs="*", default=["text-01-clm.ipynb", "text-02-llms.ipynb"])
    parser.add_argument("--cells", help="Comma-separated cell indices for independent sections")
    args = parser.parse_args()
    indices = set(map(int, args.cells.split(","))) if args.cells else None
    results = [execute(ROOT / name, indices) for name in args.notebooks]
    raise SystemExit(0 if all(results) else 1)
