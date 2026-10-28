"""Execute Lab06, preserving each actual output and documenting blocked cells."""
import argparse
import datetime
import hashlib
import json
import platform
import shutil
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "text-06-prompt-engineering-rag.ipynb"


def main(retrieval_only=False):
    notebook = nbformat.read(PATH, as_version=4)
    client = NotebookClient(notebook, timeout=None, kernel_name="llms-lab06",
                            resources={"metadata": {"path": str(ROOT)}})
    started = datetime.datetime.now(datetime.timezone.utc)
    report = {"run_id": started.strftime("full-%Y%m%dT%H%M%SZ"),
              "started_utc": started.isoformat(),
              "python": platform.python_version(), "platform": platform.platform(),
              "mode": "retrieval-only" if retrieval_only else "full", "cells": []}
    history = ROOT / "execution" / "run-history"
    history.mkdir(parents=True, exist_ok=True)
    history_path = history / f"{report['run_id']}.json"
    # Preserve the original gated-repository failure and all prior saved outputs
    # before a clean full run replaces the notebook's current execution state.
    preservation = ROOT / "execution" / "source-preservation"
    preservation.mkdir(parents=True, exist_ok=True)
    if not retrieval_only:
        preserved_nb = preservation / "notebook-before-authenticated-full-run.ipynb"
        preserved_status = preservation / "status-before-authenticated-full-run.json"
        if not preserved_nb.exists():
            shutil.copy2(PATH, preserved_nb)
        current_status = ROOT / "execution" / "status.json"
        if current_status.is_file() and not preserved_status.exists():
            shutil.copy2(current_status, preserved_status)
        # Do not leave stale outputs looking like results of the new clean run.
        for cell in notebook.cells:
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
        nbformat.write(notebook, PATH)
    light_cells = {1, 3, 17, 19, 21}
    failed = False
    with client.setup_kernel():
        for index, cell in enumerate(notebook.cells):
            if cell.cell_type != "code" or not cell.source.strip():
                continue
            record = {"index": index, "source_sha256": hashlib.sha256(cell.source.encode()).hexdigest()}
            if retrieval_only and index not in light_cells:
                record.update(status="blocked", reason="Requires the gated Llama model, which is unavailable without approved credentials.")
            else:
                print(f"Starting cell {index}", flush=True)
                start = time.perf_counter()
                try:
                    client.execute_cell(cell, index)
                    record["status"] = "ok"
                except CellExecutionError as error:
                    failed = True
                    record.update(status="error", error=str(error))
                    print(f"Cell {index} failed: {error.ename}: {error.evalue}", flush=True)
                    if not retrieval_only:
                        report["cells"].append(record)
                        nbformat.write(notebook, PATH)
                        (ROOT / "execution/status.json").write_text(json.dumps(report, indent=2) + "\n")
                        history_path.write_text(json.dumps(report, indent=2) + "\n")
                        raise
                record["seconds"] = time.perf_counter() - start
            report["cells"].append(record)
            nbformat.write(notebook, PATH)
            (ROOT / "execution/status.json").write_text(json.dumps(report, indent=2) + "\n")
            history_path.write_text(json.dumps(report, indent=2) + "\n")
            print(f"Cell {index}: {record['status']}", flush=True)
    return not failed and not retrieval_only


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--retrieval-only", action="store_true")
    args = parser.parse_args()
    raise SystemExit(0 if main(args.retrieval_only) else 1)
