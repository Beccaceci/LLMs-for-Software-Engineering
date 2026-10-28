"""Summarize saved execution evidence without changing laboratory notebooks."""
import ast
import hashlib
import json
from pathlib import Path


def inspect(path):
    raw = path.read_bytes()
    notebook = json.loads(raw)
    code = []
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if cell["cell_type"] != "code" or not source.strip():
            continue
        try:
            tree = ast.parse(source)
            ellipsis = any(
                isinstance(node, (ast.Assign, ast.AnnAssign, ast.Return, ast.Expr))
                and isinstance(node.value, ast.Constant) and node.value.value is Ellipsis
                for node in ast.walk(tree)
            )  # Preserve legitimate tensor indexing such as x[..., 0].
        except SyntaxError:
            # IPython magics are not ordinary Python syntax.
            ellipsis = None
        code.append({
            "index": index,
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "execution_count": cell.get("execution_count"),
            "output_count": len(cell.get("outputs", [])),
            "ellipsis_placeholder": ellipsis,
            "errors": [{"name": output.get("ename"), "message": output.get("evalue")}
                       for output in cell.get("outputs", [])
                       if output["output_type"] == "error"],
        })
    pending = [cell["index"] for cell in code if cell["execution_count"] is None]
    errors = [cell["index"] for cell in code if cell["errors"]]
    placeholders = [cell["index"] for cell in code if cell["ellipsis_placeholder"]]
    return {
        "path": str(path.relative_to(ROOT)),
        "notebook_sha256": hashlib.sha256(raw).hexdigest(),
        "code_cell_count": len(code),
        "executed_cell_count": len(code) - len(pending),
        "unexecuted_cells": pending,
        "error_cells": errors,
        "ellipsis_cells": placeholders,
        "saved_execution_complete": not (pending or errors or placeholders),
        "cells": code,
    }


ROOT = Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    reports = [inspect(path) for path in sorted(ROOT.glob("lab[0-9][0-9]/*.ipynb"))]
    target = ROOT / "execution" / "notebook-status.json"
    target.write_text(json.dumps(reports, indent=2) + "\n")
    for report in reports:
        print(f"{report['path']}: {report['executed_cell_count']}/{report['code_cell_count']} "
              f"executed, errors={report['error_cells']}, ellipses={report['ellipsis_cells']}")
