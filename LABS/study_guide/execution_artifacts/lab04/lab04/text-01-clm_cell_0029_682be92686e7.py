# Reconcile actual measurements and token-count analysis without assuming
# dynamic padding is faster on this hardware. These are 12-update single runs.
training_runs = json.loads(Path("padding-benchmarks/training-results.json").read_text())
matched = [run for run in training_runs if run.get("max_steps") == 12]
assert {run["variant"] for run in matched} >= {"fixed-padding", "dynamic-padding"}
print(padding_summary.to_string(index=False, formatters={"Padding share": "{:.2f}%".format, "Reduction vs fixed (%)": "{:.2f}%".format}))
print("\nMatched 12-update training measurements (evaluation disabled):")
for run in matched:
    print(f"{run['variant']}: {run['wall_seconds']:.2f} s; steps={run['global_step']}; loss={run['trainer_metrics'].get('train_loss')}")
print("\nTiming is one controlled run per variant on this device; no speedup is assumed.")