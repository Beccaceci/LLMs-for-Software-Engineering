"""Check parsing/metrics using explicitly synthetic cases, never model results."""
import ast
import hashlib
import json
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
notebook = json.loads((ROOT / "text-07-stories.ipynb").read_text())
scope = {}
for index in (6, 9):
    tree = ast.parse("".join(notebook["cells"][index]["source"]))
    selected = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    exec(compile(ast.Module(body=selected, type_ignores=[]), f"lab07-cell-{index}-helpers", "exec"), scope)

extract = scope["extract_unique_roles"]
roles = extract(str(ROOT / "stories.csv"))
assert roles and "visitor" in roles and "local guide" in roles and "hut worker" in roles
assert len(roles) == len(set(roles))
assert scope["extract_list_items"]("1. Visitors\n2. **Local guides**\n3. Hut workers") == ["Visitors", "Local guides", "Hut workers"]
assert scope["extract_list_items"]("01 Visitors\n02 Platform Manager(s)\nNote: additional explanation") == ["Visitors", "Platform Manager"]
assert scope["extract_list_items"]("A paragraph containing a user role but no list.") == []
assert scope["normalize_roles"](["Local Guides", "localguide", "Visitors"]) == {"localguide", "visitor"}
assert scope["role_metrics"](["visitor", "hiker"], ["visitors", "manager"]) == (1, 1, 1, 0.5, 0.5)
assert scope["role_metrics"]([], []) == (0, 0, 0, 0.0, 0.0)
assert scope["extract_functions"]("1. Browse hikes.\n2. Start a hike.\n") == ["Browse hikes", "Start a hike"]
assert scope["extract_functions"]("NONE\nHowever, implied functions include browsing and planning.") == []
assert scope["extract_functions"]("A paragraph with invented claims\n1. Invented action") == []
assert scope["extract_functions"]("1. Browse hikes.\nAn explanation follows.\n2. Invented action") == ["Browse hikes"]
assert scope["create_user_stories"]("visitor", ["browse hikes"]) == [("visitor", "As a visitor, I want to browse hikes")]
record = {
    "kind": "helper validation with explicitly synthetic cases; not model-generated results",
    "status": "passed", "checks": 13,
    "reference_roles_from_csv": roles,
    "checked_cell_source_sha256": {str(i): hashlib.sha256("".join(notebook["cells"][i]["source"]).encode()).hexdigest() for i in (6, 9)},
}
(ROOT / "execution" / "helper-checks.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
