"""Re-execute RAG cell 23 and its notebook dependencies in a clean kernel."""
import datetime
import hashlib
import json
import platform
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "text-06-prompt-engineering-rag.ipynb"
# Notebook cell indices: setup/model, PDF corpus, BERT abstracts, retrieval, RAG.
DEPENDENCY_INDICES = (1, 17, 19, 21, 23)


def main():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    previous = json.loads((ROOT / "execution" / "status.json").read_text())
    failed_run_id = previous.get("run_id")
    run_id = datetime.datetime.now(datetime.timezone.utc).strftime("retry-cell23-%Y%m%dT%H%M%SZ")
    report = {
        "run_id": run_id,
        "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "mode": "clean-kernel-cell23-dependency-retry",
        "supersedes_failed_run": failed_run_id,
        "selected_cell_indices": list(DEPENDENCY_INDICES),
        "cells": [],
    }
    history = ROOT / "execution" / "run-history"
    history.mkdir(parents=True, exist_ok=True)
    history_path = history / f"{run_id}.json"
    selected = {index: notebook.cells[index] for index in DEPENDENCY_INDICES}
    for index, cell in selected.items():
        if cell.cell_type != "code":
            raise ValueError(f"Expected code cell at notebook index {index}")
        cell.outputs = []
        cell.execution_count = None
    client = NotebookClient(
        notebook,
        timeout=None,
        kernel_name="llms-lab06",
        resources={"metadata": {"path": str(ROOT)}},
    )
    try:
        with client.setup_kernel():
            for index in DEPENDENCY_INDICES:
                cell = notebook.cells[index]
                record = {
                    "index": index,
                    "source_sha256": hashlib.sha256(cell.source.encode()).hexdigest(),
                }
                print(f"Starting retry dependency cell {index}", flush=True)
                started = time.perf_counter()
                try:
                    client.execute_cell(cell, index)
                except CellExecutionError as error:
                    record.update(
                        status="error",
                        error_name=error.ename,
                        error_value=error.evalue,
                        seconds=time.perf_counter() - started,
                    )
                    report["cells"].append(record)
                    nbformat.write(notebook, NOTEBOOK)
                    history_path.write_text(json.dumps(report, indent=2) + "\n")
                    raise
                record.update(status="ok", seconds=time.perf_counter() - started)
                report["cells"].append(record)
                # Save incrementally so an interrupted retry still preserves actual outputs.
                nbformat.write(notebook, NOTEBOOK)
                history_path.write_text(json.dumps(report, indent=2) + "\n")
                print(f"Cell {index}: ok", flush=True)
        report["status"] = "success"
    except Exception:
        report["status"] = "failed"
        raise
    finally:
        report["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        history_path.write_text(json.dumps(report, indent=2) + "\n")
        # Keep original full-run diagnostics untouched; publish a clearly named retry report.
        (ROOT / "execution" / "cell23-retry-status.json").write_text(json.dumps(report, indent=2) + "\n")
    # Merge successful selected-cell evidence into the full-run status while retaining the
    # failed run separately under run-history and in the notebook's older output artifacts.
    if report.get("status") == "success":
        merged = json.loads(json.dumps(previous))
        merged["run_id"] = run_id
        merged["mode"] = "full-with-cell23-retry"
        merged["supersedes_failed_run"] = failed_run_id
        replacements = {r["index"]: r for r in report["cells"]}
        merged["cells"] = [replacements.get(r.get("index"), r) for r in merged.get("cells", [])]
        for index in DEPENDENCY_INDICES:
            if index not in {r.get("index") for r in merged["cells"]}:
                merged["cells"].append(replacements[index])
        (ROOT / "execution" / "status.json").write_text(json.dumps(merged, indent=2) + "\n")
    return 0 if report.get("status") == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
