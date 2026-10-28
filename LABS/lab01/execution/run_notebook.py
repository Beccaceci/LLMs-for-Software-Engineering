"""Execute the Lab 01 notebook cell by cell and save evidence as it completes."""
import datetime
import argparse
import hashlib
import json
from pathlib import Path
import platform
import os
import time

import nbformat
import psutil
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--light', action='store_true', help='CPU cells through the MLP plus independent graph examples')
parser.add_argument('--cells', help='Comma-separated code cell indices')
args = parser.parse_args()
if args.light:
    os.environ['LAB01_DEVICE'] = 'cpu'
indices = set(map(int, args.cells.split(','))) if args.cells else None
path = ROOT / 'text.ipynb'
nb = nbformat.read(path, as_version=4)
nb.metadata.kernelspec = {'name':'llms-lab01','display_name':'Python (Lab 01)','language':'python'}
client = NotebookClient(nb, timeout=None, kernel_name='llms-lab01', extra_arguments=['--InteractiveShell.cache_size=0'], resources={'metadata': {'path':str(ROOT)}})
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
records = []
with client.setup_kernel():
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != 'code' or not cell.source.strip():
            continue
        if args.light and i > 55 and i not in {80, 83, 84}:
            continue
        if indices is not None and i not in indices:
            continue
        print(f'Starting cell {i}', flush=True)
        t0 = time.perf_counter(); status = 'ok'
        try:
            client.execute_cell(cell, i)
        except BaseException:
            status = 'error'
            raise
        finally:
            pid = client.km.provisioner.pid
            rss = psutil.Process(pid).memory_info().rss if pid else None
            records.append({'cell_index':i,'execution_count':cell.get('execution_count'),'source_sha256':hashlib.sha256(cell.source.encode()).hexdigest(),'seconds':time.perf_counter()-t0,'kernel_rss_bytes':rss,'status':status})
            nbformat.write(nb,path)
            record_name = 'light-execution.json' if args.light else 'execution.json'
            (ROOT/'execution'/record_name).write_text(json.dumps({'started_utc':started,'python':platform.python_version(),'platform':platform.platform(),'device':os.getenv('LAB01_DEVICE', 'MPS when available'),'cells':records},indent=2)+'\n')
            print(f'Cell {i}: {status}, {records[-1]["seconds"]:.2f}s',flush=True)
