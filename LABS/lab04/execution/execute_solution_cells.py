"""Execute one matched Lab 04 padding variant in an isolated clean kernel."""
import sys
from run_notebooks import ROOT, execute

variant = sys.argv[1] if len(sys.argv) > 1 else "fixed"
base = {2, 5, 10, 12, 23, 24, 25, 26}
if variant == "fixed":
    indices = base | {27}
elif variant == "dynamic":
    indices = base | {28, 29}
else:
    raise SystemExit("usage: execute_solution_cells.py [fixed|dynamic]")
raise SystemExit(0 if execute(ROOT / "text-01-clm.ipynb", indices) else 1)
