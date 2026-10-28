import ipytest
ipytest.autoconfig()
# A clean notebook test module, independent of test files used for model comparison.
reference_exit_code = ipytest.run("-vv")
if int(reference_exit_code) != 0:
    raise RuntimeError("Reference tests failed; fix the reference before comparing generated code")
print("All notebook reference boundary/validation tests passed.")
print("Supplied test_valid_grades_with_30laude expects 27.75 with 1% tolerance; exact answer is 28.0.")
print("The supplied test file is preserved; strict tests above check the exact result.")
