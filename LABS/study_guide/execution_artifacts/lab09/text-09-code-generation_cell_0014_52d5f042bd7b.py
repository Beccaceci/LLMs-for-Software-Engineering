import radon.complexity as radon_complexity
import radon.metrics as radon_metrics
import radon.raw as radon_raw

def analyze_code_with_radon(file_path):
    code = Path(file_path).read_text()
    functions = radon_complexity.cc_visit(code)
    raw = radon_raw.analyze(code)
    return {"CC":max((block.complexity for block in functions),default=0),
        "MI":radon_metrics.mi_visit(code,multi=False),"LOC":raw.loc,
        "Comments":raw.comments}

def compare_codes(codes, test_file="test_cases_01.py", function_file="function_01.py", suffix="grades"):
    results = {}
    for name, code in codes.items():
        # Export each exact observed source, then measure the same source.
        source_path = Path("execution")/"sources"/(re.sub(r"[^A-Za-z0-9_.-]","_",name)+"_"+suffix+".py")
        source_path.parent.mkdir(parents=True,exist_ok=True)
        source_path.write_text(code)
        static = analyze_code_with_radon(source_path)
        dynamic = evaluate_code(code,test_file,function_file,name+"_"+suffix)
        results[name] = {**static,**dynamic}
    return results

overall_results = compare_codes(my_codes)
print(json.dumps(overall_results,indent=2))
print("Only actually generated sources are included:",code_provenance)
