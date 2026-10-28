"""Execute the gated Llama 3.2 sequence in a clean Lab 04 kernel."""
from run_notebooks import ROOT, execute

indices = {3, 4, 8, 10, 12, 14, 15, 17, 19, 21, 24, 26}
raise SystemExit(0 if execute(ROOT / "text-02-llms.ipynb", indices) else 1)
