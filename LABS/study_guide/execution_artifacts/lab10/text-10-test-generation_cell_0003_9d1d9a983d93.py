import sys
from pathlib import Path
import pytest
import ipytest

# Use the laboratory folder as the notebook working directory.
LAB_DIR = Path.cwd()
assert (LAB_DIR / "function_01.py").is_file(), "Run this notebook from LABS/lab10"
sys.path.insert(0, str(LAB_DIR.parent))

# The manual baseline tests exercise each rule and its strict boundary.
manual_test_source = 'import pytest\nfrom lab10.function_01 import racer_disqualified\n\n@pytest.mark.parametrize("times, penalties, expected", [\n    ([100, 100, 100], [], False),\n    ([150, 150, 150], [], False),\n    ([151, 100, 100], [], True),\n    ([100, 151, 100], [], True),\n    ([100, 100, 151], [], True),\n    ([100, 100, 100], [100], False),\n    ([100, 100, 100], [101], True),\n    ([100, 100, 100], [50, 50], False),\n    ([100, 100, 100], [50, 51], True),\n    ([100, 100, 100], [10] * 5, False),\n    ([100, 100, 100], [10] * 6, True),\n])\ndef test_disqualification_rules(times, penalties, expected):\n    assert racer_disqualified(times, [100, 100, 100], len(penalties), penalties) is expected\n\n@pytest.mark.parametrize("args", [\n    ("100,100,100", [100, 100, 100], 0, []),\n    ([100, 100], [100, 100, 100], 0, []),\n    ([100, 100, 1.5], [100, 100, 100], 0, []),\n    ([100, 100, 100], "100,100,100", 0, []),\n    ([100, 100, 100], [100, 100], 0, []),\n    ([100, 100, 100], [100, 100, "100"], 0, []),\n    ([100, 100, 100], [100, 100, 100], "0", []),\n    ([100, 100, 100], [100, 100, 100], 0, ""),\n    ([100, 100, 100], [100, 100, 100], 1, [1.5]),\n    ([100, 100, 100], [100, 100, 100], 2, [10]),\n])\ndef test_invalid_inputs(args):\n    with pytest.raises(ValueError):\n        racer_disqualified(*args)\n'
(LAB_DIR / "test_function_01_manual.py").write_text(manual_test_source)
exec(compile(manual_test_source, "test_function_01_manual.py", "exec"), globals())
ipytest.autoconfig(raise_on_error=True)

def run_tests():
    return ipytest.run("-vv")

run_tests()