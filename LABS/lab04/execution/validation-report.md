# Laboratory 04 solution validation

- PDF: `lab04/lab04_solution.pdf` — compiled successfully; 27 A4 pages.
- Notebook alignment: 33 current code cells (16 CLM, 17 LLM); all source hashes match notebook cells and coverage manifest entries.
- Saved output coverage: 53 output objects; output payload hashes and exported presentation/raw artifacts reconciled by the coverage validator. Rich HTML training output was extracted as its full 16-row table.
- Execution: all 33 finalized notebook cells have successful evidence; both gated Llama checkpoints were accessed locally and the Llama sequence completed. No notebook error outputs remain.
- Tests: targeted coverage suite passed (14 tests).
- Padding analysis: 244,388 useful tokens across 1,000 examples; fixed, seeded random dynamic, and similar-length batches use the same examples including the final partial batch. Label masking preserves attended EOS targets.
- Timing: one matched 12-update run per variant on MPS; fixed-padding 207.01 s (loss 3.41519), dynamic-padding 467.35 s (loss 3.41545). These short single runs are descriptive only. The earlier full-epoch dynamic attempt hit MPS out-of-memory and is retained in the diagnostic appendix.
- Mistral: all five saved examples parse as JSON with correct operands and arithmetic; negative validation cases cover missing assistant, malformed JSON, missing field, and wrong answer.
- Transcript: Whisper Lab04 recording, 82:13.055; 801 timestamped segments. The last segment timestamp exceeds duration by 1.385 s; largest internal gap is 57.660 s. Unclear passages were not reconstructed.
- Editorial layout update: removed label-led Goal, Inputs, Expected result, Success criterion, Pipeline position, and Recorded output paragraphs; exercise openings and cell explanations now read as continuous prose. The contents are separated from Exercise 1, and each major exercise begins on a new page.
- Visual QA: every page rendered to PNG and checked in a 27-page contact sheet, with detailed inspection of code-heavy and diagnostic pages. No clipping or unreadable blocks found.
- Reproducibility limits: historical GPT-2 and Mistral runs are preserved evidence; dynamic padding timing is a controlled single-run comparison; no medical accuracy or general JSON reliability claim is made.
