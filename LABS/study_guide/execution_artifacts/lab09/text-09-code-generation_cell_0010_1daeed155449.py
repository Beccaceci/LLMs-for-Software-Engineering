import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_test_results(result_string):
    def count(pattern):
        match = re.search(pattern, result_string)
        return int(match.group(1)) if match else 0
    return count(r"(\d+)\s+errors?"), count(r"(\d+)\s+failed"), count(r"(\d+)\s+passed")

def evaluate_code(code, test_file="test_cases_01.py", function_file="function_01.py", name="generated"):
    # Each subprocess gets a fresh import directory; no model can inherit the prior code's bytecode.
    evidence = Path("execution") / "evaluations" / re.sub(r"[^A-Za-z0-9_.-]", "_", name)
    evidence.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="lab09-tests-") as temporary:
        run_dir = Path(temporary)
        (run_dir/function_file).write_text(code)
        shutil.copy2(test_file, run_dir/Path(test_file).name)
        result = subprocess.run([sys.executable,"-m","pytest",Path(test_file).name,
            "-q","--disable-warnings","--tb=short","--color=no","--junitxml=report.xml"],
            cwd=run_dir, capture_output=True, text=True, timeout=60)
        (evidence/"stdout.txt").write_text(result.stdout+result.stderr)
        report = run_dir/"report.xml"
        if not report.exists(): raise RuntimeError("pytest produced no test report: "+result.stderr)
        shutil.copy2(report,evidence/"junit.xml")
        cases = ET.parse(report).getroot().findall(".//testcase")
        failures = sum(case.find("failure") is not None for case in cases)
        errors = sum(case.find("error") is not None for case in cases)
        skipped = sum(case.find("skipped") is not None for case in cases)
        passes = len(cases)-failures-errors-skipped
        total = passes+failures+errors
        if total == 0: raise RuntimeError("No tests ran")
        metrics = {"Passed":passes,"Failed":failures,"Errors":errors,"Skipped":skipped,
            "FunctionalCorrectness":passes/total,"pytest_exit_code":result.returncode,
            "SourceSHA256":hashlib.sha256(code.encode()).hexdigest()}
        (evidence/"metrics.json").write_text(json.dumps(metrics,indent=2))
        print(name,metrics)
        return metrics

codex_metrics = evaluate_code(my_codes["Codex"],name="Codex_grades")
codex_functional_correctness = codex_metrics["FunctionalCorrectness"]
