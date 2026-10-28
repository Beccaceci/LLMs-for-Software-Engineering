# Laboratory 05 execution handoff

Status: **complete**. The two finalized notebooks have been executed end-to-end, and the standalone solution PDF and editable LaTeX sources are available.

- `text-01-quantization.ipynb`: 28 nonempty code cells completed from a clean kernel. Local Hugging Face authentication succeeded. The float32 baseline, PyTorch dynamic int8, and BitsAndBytes CPU int4 paths all executed on the same prompt batch.
- `text-02-LoRA.ipynb`: all 23 nonempty code cells completed. Manual and PEFT training/evaluation outputs are saved.
- `lab05_solution.pdf`: compiled, extracted, rendered page-by-page, and visually checked. Coverage validator passes; all 51 source cells and 33 output slots are mapped.

## Main measured results

The serialized Llama state size was 4,943.31 MB (float32), 2,288.87 MB (dynamic int8), and 1,598.46 MB (BitsAndBytes int4). The corresponding CPU generation timings were 8.565 s, 11.584 s, and 16.536 s for the same 20 prompts and 30 new greedy tokens. This run shows reduced serialized storage, not a speedup. QNNPACK emitted a retained warning that its current int8 backend ignores `reduce_range`.

The manual LoRA run took 810.0 s for 62 updates and reached 0.6580 validation accuracy, up from 0.5070. PEFT took 814.4 s for 62 updates, with training loss 0.5761 and validation accuracy 0.8170. PEFT trains the classification head while the manual implementation freezes it, so the observed accuracy difference is not an isolated comparison of adapter implementations.

## Provenance and validation

`text-01-quantization.execution.json` and `text-02-LoRA.execution.json` record successful runs and per-cell source hashes that match the current notebooks. `quantization-complete.log` is the new clean-run trace. `quantization.log` preserves the earlier authentication failure as historical diagnostic evidence. Raw notebook output MIME payloads and presentation artifacts are stored under `study_guide/execution_artifacts/lab05/`; inventory and PDF destinations are recorded under `study_guide/coverage/`.

The 15 coverage tests pass, and `cell_coverage.py validate` reports success for all 51 cells. The PDF contains 20 pages; extracted text has no HTML-object placeholder or runtime traceback. Every rendered page was inspected in a full-document contact sheet, with dense pages reviewed at full resolution.

No matching Lab05 lecture recording/transcript was supplied. The unrelated Whisper lecture about object detection and segmentation was excluded. Lecture review can be added when the professor's promised recording becomes available. See `lecture-source-status.md` for the source search note and `validation-report.md` for the concise final validation summary.
