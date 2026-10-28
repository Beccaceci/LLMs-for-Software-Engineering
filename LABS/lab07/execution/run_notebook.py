"""Run Lab 07 from a clean kernel and checkpoint actual outputs after every cell."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def prepare_local_kernel() -> None:
    """Point this lab's clean kernel at the interpreter running the script.

    A previous per-user kernelspec referenced an ephemeral /private/tmp venv.
    Keeping a generated kernelspec under this lab avoids changing other labs or
    relying on that temporary path.
    """
    jupyter_root = ROOT / "execution" / "jupyter"
    spec_dir = jupyter_root / "kernels" / "llms-lab07"
    spec_dir.mkdir(parents=True, exist_ok=True)
    spec = {
        "argv": [sys.executable, "-Xfrozen_modules=off", "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Python (Lab 07 local run)",
        "language": "python",
        "metadata": {"debugger": True},
    }
    (spec_dir / "kernel.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    inherited = os.environ.get("JUPYTER_PATH", "")
    os.environ["JUPYTER_PATH"] = os.pathsep.join([str(jupyter_root), *([inherited] if inherited else [])])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", help="Attempt model access and independently run CSV reference preparation")
    args = parser.parse_args()
    path = ROOT / "text-07-stories.ipynb"
    notebook = nbformat.read(path, as_version=4)
    prepare_local_kernel()
    client = NotebookClient(notebook, timeout=None, kernel_name="llms-lab07", allow_errors=args.prepare,
                            resources={"metadata": {"path": str(ROOT)}})
    record = {"started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "python": platform.python_version(), "platform": platform.platform(),
              "mode": "independent preparation" if args.prepare else "clean full execution", "cells": []}
    selected = {0, 6} if args.prepare else None
    with client.setup_kernel():
        for index, cell in enumerate(notebook.cells):
            if cell.cell_type != "code" or not cell.source.strip() or (selected is not None and index not in selected):
                continue
            print(f"Starting cell {index}", flush=True)
            start = time.perf_counter()
            status = "interrupted"
            try:
                client.execute_cell(cell, index)
                status = "error" if any(o.output_type == "error" for o in cell.outputs) else "ok"
            except Exception:
                status = "error"
                raise
            finally:
                record["cells"].append({"index": index, "source_sha256": hashlib.sha256(cell.source.encode()).hexdigest(),
                                        "execution_count": cell.execution_count, "status": status,
                                        "seconds": time.perf_counter() - start})
                nbformat.write(notebook, path)
                (ROOT / "execution" / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
                print(f"Cell {index}: {status}", flush=True)
    return 1 if any(c["status"] != "ok" for c in record["cells"]) else 0

if __name__ == "__main__":
    raise SystemExit(main())
