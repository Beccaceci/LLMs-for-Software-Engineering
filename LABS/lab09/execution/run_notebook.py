"""Run Lab09 from a fresh kernel and save only actual outputs after every cell."""
import argparse
import datetime
import hashlib
import json
import platform
import time
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'text-09-code-generation.ipynb'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--light', action='store_true', help='Attempt auth, run independent CPU sections only')
    parser.add_argument('--cells', help='Comma-separated indices for a documented independent section')
    args = parser.parse_args()
    selected = set(map(int, args.cells.split(','))) if args.cells else ({1,3,5,7,10,14,16,20} if args.light else None)
    notebook = nbformat.read(PATH,as_version=4)
    client = NotebookClient(notebook,timeout=None,kernel_name='llms-lab09',
        resources={'metadata':{'path':str(ROOT)}})
    record = {'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python':platform.python_version(),'platform':platform.platform(),'mode':'light' if args.light else 'selected' if selected else 'full','cells':[]}
    run_id = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')
    failed = False
    with client.setup_kernel():
        for index,cell in enumerate(notebook.cells):
            if cell.cell_type != 'code' or not cell.source.strip() or selected is not None and index not in selected:
                continue
            print('Starting cell',index,flush=True)
            started = time.perf_counter()
            status = 'ok'
            try:
                client.execute_cell(cell,index)
            except Exception as exc:
                failed=True;status='error'
                print(type(exc).__name__,str(exc)[-1800:],flush=True)
                if not (args.light and index == 7):
                    raise
            finally:
                record['cells'].append({'index':index,'status':status,'seconds':time.perf_counter()-started,
                    'source_sha256':hashlib.sha256(cell.source.encode()).hexdigest()})
                nbformat.write(notebook,PATH)
                (ROOT/'execution/status.json').write_text(json.dumps(record,indent=2)+'\n')
                (ROOT/'execution'/f'run-{run_id}.json').write_text(json.dumps(record,indent=2)+'\n')
            print('Finished cell',index,status,round(time.perf_counter()-started,2),'seconds',flush=True)
    return 1 if failed else 0

if __name__ == '__main__':raise SystemExit(main())
