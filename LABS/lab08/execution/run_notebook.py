"""Run Lab 08 from a clean kernel and checkpoint observed outputs after each cell."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import platform
from pathlib import Path
import time

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'text-08-roc-router-design.ipynb'

def run(light=False):
    n = nbformat.read(NOTEBOOK, as_version=4)
    client = NotebookClient(n, timeout=None, kernel_name='llms-lab08',
                            resources={'metadata': {'path': str(ROOT)}})
    rows = []
    started = datetime.now(timezone.utc).isoformat()
    succeeded = True
    with client.setup_kernel():
        for index, cell in enumerate(n.cells):
            if cell.cell_type != 'code' or not cell.source.strip():
                continue
            if light and index > 8:
                rows.append({'cell_index': index, 'status': 'blocked',
                             'reason': 'Requires the gated Llama model from cell 8'})
                continue
            print(f'Starting cell {index}', flush=True)
            begin = time.perf_counter()
            status = 'ok'
            try:
                client.execute_cell(cell, index)
            except Exception as exc:
                status = 'error'
                succeeded = False
                print(f'{type(exc).__name__}: {exc}', flush=True)
            rows.append({'cell_index': index, 'status': status,
                         'source_sha256': hashlib.sha256(cell.source.encode()).hexdigest(),
                         'seconds': time.perf_counter() - begin,
                         'execution_count': cell.get('execution_count'),
                         'output_types': [o.output_type for o in cell.get('outputs', [])]})
            nbformat.write(n, NOTEBOOK)
            for output in cell.get('outputs', []):
                png = output.get('data', {}).get('image/png')
                if png:
                    (ROOT / 'execution' / f'cell_{index:03d}.png').write_bytes(base64.b64decode(png))
            (ROOT / 'execution' / 'execution.json').write_text(json.dumps({
                'started_utc': started, 'python': platform.python_version(),
                'platform': platform.platform(), 'light_run': light, 'cells': rows,
            }, indent=2) + '\n')
            print(f'Cell {index}: {status} ({rows[-1]["seconds"]:.2f}s)', flush=True)
            if status == 'error' and not light:
                break
    # Include dependency-blocked rows added after the last executed cell.
    (ROOT / 'execution' / 'execution.json').write_text(json.dumps({
        'started_utc': started, 'python': platform.python_version(),
        'platform': platform.platform(), 'light_run': light, 'cells': rows,
    }, indent=2) + '\n')
    return succeeded

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--light', action='store_true', help='Run ROC and model-access attempt, skip router generation')
    args = parser.parse_args()
    raise SystemExit(0 if run(args.light) else 1)
