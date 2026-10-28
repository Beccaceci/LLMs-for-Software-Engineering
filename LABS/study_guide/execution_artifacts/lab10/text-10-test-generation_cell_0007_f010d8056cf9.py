def measure_coverage(test_file, tag):
    data_file = ARTIFACTS / f".coverage-{tag}"
    xml_path = ARTIFACTS / f"{tag}-coverage-tests.xml"
    result = run_command([
        "-m", "coverage", "run", f"--data-file={data_file}",
        "--source=lab10.function_01", "-m", "pytest", str(test_file),
        "-q", "--tb=short", f"--junitxml={xml_path}",
    ], f"{tag}-coverage-run")
    if result.returncode not in (0, 1):
        raise RuntimeError(f"Coverage test execution failed: {tag}")
    result2 = run_command([
        "-m", "coverage", "report", f"--data-file={data_file}",
        "--include=*/lab10/function_01.py", "-m",
    ], f"{tag}-coverage-report")
    if result2.returncode != 0:
        raise RuntimeError(result2.stdout + result2.stderr)
    line = next(line for line in result2.stdout.splitlines() if "function_01.py" in line)
    coverage = float(re.search(r"(\d+(?:\.\d+)?)%", line).group(1))
    return result, result2, coverage


result, result2, coverage = measure_coverage("test_function_01_manual.py", "manual")
print(result2.stdout)
print(f"Coverage: {coverage}%")