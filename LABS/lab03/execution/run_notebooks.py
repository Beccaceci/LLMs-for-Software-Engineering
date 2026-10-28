"""Run Lab 03 notebooks cell by cell with exact source hashes and saved outputs."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import platform
import time

import nbformat
import psutil
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]

def execute(path):
    notebook = nbformat.read(path, as_version=4)
    notebook.metadata.kernelspec = {"name":"llms-lab03","display_name":"Python (Lab 03)","language":"python"}
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.execution_count = None
            cell.outputs = []
    client = NotebookClient(notebook, timeout=None, kernel_name="llms-lab03",
        extra_arguments=["--InteractiveShell.cache_size=0"],
        resources={"metadata":{"path":str(ROOT)}})
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records = []
    (ROOT/"execution"/(path.name+".run-start.json")).write_text(json.dumps({"started_utc":started,"notebook":path.name},indent=2)+"\n")
    with client.setup_kernel():
        for i, cell in enumerate(notebook.cells):
            if cell.cell_type != "code" or not cell.source.strip():
                continue
            print(f"{path.name}: starting cell {i}",flush=True)
            begin=time.perf_counter();status="ok"
            try:
                client.execute_cell(cell,i)
            except BaseException:
                status="error"
                raise
            finally:
                pid=client.km.provisioner.pid
                rss=psutil.Process(pid).memory_info().rss if pid else None
                records.append({"cell_index":i,"execution_count":cell.get("execution_count"),"source_sha256":hashlib.sha256(cell.source.encode()).hexdigest(),"seconds":time.perf_counter()-begin,"kernel_rss_bytes":rss,"status":status})
                nbformat.write(notebook,path)
                (ROOT/"execution"/(path.stem+".execution.json")).write_text(json.dumps({"started_utc":started,"python":platform.python_version(),"platform":platform.platform(),"cells":records},indent=2)+"\n")
                print(f"{path.name}: cell {i}: {status} ({records[-1]['seconds']:.1f}s)",flush=True)
    return records

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("notebooks",nargs="*",default=["text-01-bert.ipynb","text-02-gpt2.ipynb"])
    args=parser.parse_args()
    for name in args.notebooks:
        execute(ROOT/name)
