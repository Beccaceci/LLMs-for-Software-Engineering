import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ARTIFACTS = LAB_DIR / "execution"
ARTIFACTS.mkdir(exist_ok=True)
RUN_ENV = dict(os.environ)
RUN_ENV["PYTHONPATH"] = str(LAB_DIR.parent) + os.pathsep + RUN_ENV.get("PYTHONPATH", "")
RUN_ENV["PYTHONDONTWRITEBYTECODE"] = "1"


def run_command(arguments, tag):
    result = subprocess.run(
        [sys.executable, "-B", *arguments], cwd=LAB_DIR, env=RUN_ENV,
        capture_output=True, text=True, timeout=120,
    )
    (ARTIFACTS / f"{tag}.log").write_text(result.stdout + result.stderr)
    return result


def parse_test_results(xml_path):
    root = ET.parse(xml_path).getroot()
    cases = root.findall(".//testcase")
    if not cases:
        raise RuntimeError(f"No tests collected; see {xml_path}")
    outcomes = {}
    for case in cases:
        key = case.get("classname", "") + "::" + case.get("name", "")
        outcomes[key] = (
            "error" if case.find("error") is not None else
            "failed" if case.find("failure") is not None else
            "skipped" if case.find("skipped") is not None else "passed"
        )
    counts = {state: sum(value == state for value in outcomes.values())
              for state in ("passed", "failed", "error", "skipped")}
    counts["total"] = len(cases)
    counts["pass_rate"] = counts["passed"] / counts["total"]
    counts["outcomes"] = outcomes
    return counts


def run_suite(test_file, tag):
    xml_path = ARTIFACTS / f"{tag}.xml"
    result = run_command([
        "-m", "pytest", str(test_file), "-q", "--tb=short", "--disable-warnings",
        f"--junitxml={xml_path}",
    ], tag)
    if result.returncode not in (0, 1):
        raise RuntimeError(f"pytest infrastructure error: {tag}; see its log")
    counts = parse_test_results(xml_path)
    if counts["error"]:
        raise RuntimeError(f"Collection/setup error in {tag}; see its log")
    return result, counts


result, manual_baseline = run_suite("test_function_01_manual.py", "manual-baseline")
errors, failures, passes = (manual_baseline[key] for key in ("error", "failed", "passed"))
print(f"# Passed: {passes}")
print(f"# Failed: {failures}")
print(f"# Errors: {errors}")
pass_rate = manual_baseline["pass_rate"]
print(f"Pass Rate: {pass_rate:.2%}")
assert pass_rate == 1.0