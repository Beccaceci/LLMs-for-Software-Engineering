"""Check the notebook's mathematical helpers against independent expected cases."""
import ast
import json
from pathlib import Path
import re

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
notebook = json.loads((ROOT / 'text-08-roc-router-design.ipynb').read_text())
namespace = {'np': np, 'cosine_similarity': cosine_similarity, 're': re}
for index in (3, 12):
    tree = ast.parse(''.join(notebook['cells'][index]['source']))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(index), 'exec'), namespace)
compute = namespace['compute_tpr_fpr']
parse = namespace['parse_router_response']
identity = np.eye(2)
assert compute(identity, identity, .9) == (1., 0.)
assert compute(identity, identity, np.inf) == (0., 0.)
assert compute(identity, identity, -np.inf) == (1., 1.)
assert compute(identity, identity[::-1], .9) == (0., 1.)
assert compute([[1., 0.]], [[1., 0.]], .9) == (1., 0.)
try:
    compute([], [], .5)
except ValueError:
    pass
else:
    raise AssertionError('Empty arrays must be rejected')
assert parse(' **Use Cases.** ') == 'Use Cases'
assert parse('"class diagram"') == 'Class Diagram'
try:
    parse('Both Use Cases and Class Diagram')
except ValueError:
    pass
else:
    raise AssertionError('Ambiguous routing must be rejected')
print('Nine synthetic helper checks passed; no generated-model result is simulated.')
