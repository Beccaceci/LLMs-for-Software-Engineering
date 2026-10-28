def compute_average(grades):
    """Trim one minimum and maximum from six valid grades; do not mutate input."""
    from numbers import Real
    import math
    if not isinstance(grades, (list, tuple)) or len(grades) != 6:
        raise ValueError("Exactly six grades are required")
    for grade in grades:
        if isinstance(grade, bool):
            raise ValueError("Boolean values are not grades")
        if not isinstance(grade, Real):
            raise TypeError("Grades must be real numbers")
        if not math.isfinite(grade) or not (18 <= grade <= 30 or grade == 33):
            raise ValueError("Grades must be between 18 and 30, or 33 for laude")
    return sum(sorted(grades)[1:-1]) / 4

from pathlib import Path
import json

print(f"The computed average is: {compute_average([18,25,30,33,22,28]):.2f}")
# Fresh code authored by this Codex agent in this session, not a captured ChatGPT UI response.
# Preserve provenance rather than falsely labeling this as an external GPT run.
codex_result = 'def compute_average(grades):\n    """Return the trimmed mean of six grades, with 33 representing laude."""\n    import math\n    from numbers import Real\n    if not isinstance(grades, (list, tuple)) or len(grades) != 6:\n        raise ValueError("Expected exactly six grades")\n    for value in grades:\n        if isinstance(value, bool):\n            raise ValueError("A boolean is not a grade")\n        if not isinstance(value, Real):\n            raise TypeError("Expected numeric grades")\n        if not math.isfinite(value) or not (18 <= value <= 30 or value == 33):\n            raise ValueError("Invalid grade")\n    return (sum(grades) - min(grades) - max(grades)) / 4\n'
my_codes = {"Codex": codex_result}
code_provenance = {"Codex": "Fresh Codex-generated baseline from this solving session"}
Path("function_01.py").write_text(codex_result)
print(code_provenance)

sys_prompt = "You are a Python programmer. Return only valid Python source, without Markdown fences or explanations."
query = """Implement compute_average(grades). Require exactly six grades; accept real values from 18 to 30 inclusive or 33 for laude. Reject booleans/invalid values with ValueError and nonnumeric values with TypeError. Return the arithmetic mean after removing exactly one minimum and one maximum. Do not mutate the input."""
