# Zero-Token Lecture Video Transcription Protocol

This protocol defines the step-by-step procedure for converting professor lecture `.mp4` video recordings into structured, timestamped Markdown transcriptions **without consuming any LLM tokens**, relying entirely on local OpenAI Whisper and `ffmpeg`.

---

## 1. Why Zero-Token Local Transcription?

University lectures in the PoliTO MSc course are typically 1.5 to 3 hours long (~20,000 to 45,000 words). Sending long audio or video to cloud LLM APIs would consume hundreds of thousands of tokens, hit rate limits, and incur unnecessary costs.
By leveraging local Whisper on macOS with Apple Silicon GPU acceleration (PyTorch `mps`), transcription runs:
- **100% Offline & Private**
- **0 LLM Tokens Consumed**
- **High Accuracy** using Whisper's `turbo`, `medium`, or `large` models.

---

## 2. File Format Decision: Why `.md` (Markdown) is Chosen Over `.txt`

Markdown (`.md`) is strictly superior to raw `.txt` for lecture transcriptions:

1. **Structured Frontmatter**: Stores standardized metadata (lecture number, course module, source video name, duration, date, instructors).
2. **Timestamped Jump Anchors**: Groups speech into digestible 2-minute blocks with clickable anchor tags (e.g., `### [00:14:20 - 00:16:30]`), enabling instant verification against the original video.
3. **Table of Contents & Timeline**: Highlights thematic transitions across the 2-hour recording.
4. **Dual Presentation**: Includes both the timestamped breakdown for auditing and a continuous prose section at the bottom for fluid reading.

---

## 3. Standardized Naming Convention & Directory

All transcriptions are automatically saved in:
```
/Users/nicolabeccaceci/Desktop/LLMs/LECTURE_TRANSCRIPTIONS/
```

Files are named following the course syllabus order:
```
LECTURE_TRANSCRIPTIONS/
├── 01-Language-Models-Intro.md
├── 02-Deep-Learning-Foundations.md
├── 03-Word-Embeddings.md
├── 04-Recurrent-Neural-Networks.md
├── 05-Transformer-Architecture.md
├── 06-Scaling-Laws-Pretraining.md
├── 07-Instruction-Tuning-Alignment.md
├── 08-PEFT-Inference-Optimization.md
├── 09-AI-In-Software-Engineering.md
├── 10-Prompt-Engineering-Chaining.md
├── 11-AI-Agents-MultiAgent.md
├── 12-Automated-Test-Generation-Repair.md
├── 13-Requirements-Engineering-Modeling.md
├── 14-Code-Refactoring-Maintainability.md
├── 15-Evaluation-Metrics-Benchmarks-SE.md
└── 16-Safety-Bias-Ethics-IP.md
```

If a custom title is used, the format preserves the zero-padded index: `XX-<Topic-Name>.md`.

---

## 4. Execution Workflow

When an `.mp4` file is provided:

### Automated Command:
Run the provided transcriber utility:
```bash
python3 scripts/transcribe_lecture.py /path/to/lecture_video.mp4
```

### Options & Flags:
- `--number / -n <1-16>`: Explicitly assign course lecture number (auto-inferred if in filename like `lecture_05.mp4`).
- `--model / -m <turbo|medium|small|base>`: Choose Whisper model (default: `turbo`, optimized for speed and accuracy).
- `--language / -l <en|it>`: Audio language (default: `en` for PoliTO LLM4SE).
- `--output-dir / -o <dir>`: Custom destination folder (default: `LECTURE_TRANSCRIPTIONS`).

### Internal Pipeline:
1. `ffmpeg` extracts high-clarity 16kHz mono audio (`.wav`) into a temporary file.
2. Local Whisper processes the audio in native chunks on Apple Silicon MPS/CPU.
3. The Markdown document is assembled with YAML frontmatter, timeline anchors, and continuous text.
4. Output is written to `LECTURE_TRANSCRIPTIONS/XX-<Topic>.md`.

---

## 5. Handoff to Study Guide Integration

Once `LECTURE_TRANSCRIPTIONS/XX-<Topic>.md` is generated, the agent immediately initiates Step 1 & Step 2 of the study guide skill:
1. **Audit & Concept Extraction**: Read the transcription and map all definitions, slide references, algorithms, and questions asked by students.
2. **Pre-Ingestion External Research**: Query ArXiv, Karpathy, 3B1B, Enkk, and Lex Fridman to prepare deep explanations.
3. **Drafting & LaTeX Compilation**: Integrate into the corresponding chapter/section following the selected integration mode.
