"""Run the completed Lab 10 notebook and checkpoint observed output after each cell."""
import datetime
import hashlib
import json
import platform
from pathlib import Path
import time
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'text-10-test-generation.ipynb'
notebook = nbformat.read(path, as_version=4)
client = NotebookClient(notebook, timeout=600, kernel_name='llms-lab10',
                        resources={'metadata': {'path': str(ROOT)}})
records = []
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
    with client.setup_kernel():
        for index, cell in enumerate(notebook.cells):
            if cell.cell_type != 'code' or not cell.source.strip():
                continue
            print(f'Starting cell {index}', flush=True)
            begin = time.perf_counter()
            status = 'success'
            try:
                client.execute_cell(cell, index)
            except BaseException:
                status = 'error'
                raise
            finally:
                records.append({'cell_index': index, 'source_sha256': hashlib.sha256(cell.source.encode()).hexdigest(),
                                'seconds': time.perf_counter() - begin, 'status': status})
                nbformat.write(notebook, path)
                (ROOT / 'execution' / 'execution.json').write_text(json.dumps({
                    'started_utc': started, 'python': platform.python_version(), 'platform': platform.platform(),
                    'backend': 'CPU (pytest, coverage, mutation analysis)', 'cells': records,
                }, indent=2) + '\n')
                print(f'Cell {index}: {status}, {records[-1]["seconds"]:.2f}s', flush=True)
finally:
    # A notebook interrupt during mutation analysis must not leave a mutant on disk.
    namespace = {}
    import ast
    tree = ast.parse(notebook.cells[1].source)
    reference = next(ast.literal_eval(node.value) for node in tree.body
                     if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'original_function' for t in node.targets))
    (ROOT / 'function_01.py').write_text(reference + '\n')
