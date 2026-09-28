#!/usr/bin/env python3
"""
Zero-Token Local Lecture Video Transcriber for PoliTO LLM4SE Course.
Extracts audio from .mp4 videos and transcribes using local OpenAI Whisper.
Zero LLM tokens consumed.
Formats output into structured Markdown with timestamps and frontmatter.
Saves to LECTURE_TRANSCRIPTIONS/ with standardized course ordering.
"""

import os
import sys
import re
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

COURSE_MODULE_MAP = {
    1: "01-Language-Models-Intro",
    2: "02-Deep-Learning-Foundations",
    3: "03-Word-Embeddings",
    4: "04-Recurrent-Neural-Networks",
    5: "05-Transformer-Architecture",
    6: "06-Scaling-Laws-Pretraining",
    7: "07-Instruction-Tuning-Alignment",
    8: "08-PEFT-Inference-Optimization",
    9: "09-AI-In-Software-Engineering",
    10: "10-Prompt-Engineering-Chaining",
    11: "11-AI-Agents-MultiAgent",
    12: "12-Automated-Test-Generation-Repair",
    13: "13-Requirements-Engineering-Modeling",
    14: "14-Code-Refactoring-Maintainability",
    15: "15-Evaluation-Metrics-Benchmarks-SE",
    16: "16-Safety-Bias-Ethics-IP"
}

def infer_lecture_number(filename: str) -> int | None:
    """Infer lecture number from filename like 'lecture_05.mp4', '05-transformers.mp4', 'L05.mp4'."""
    patterns = [
        r"(?:lecture|lesson|ch|chapter|lezione|l)?[-_ ]*0*([1-9]|1[0-6])\b",
        r"^0*([1-9]|1[0-6])[-_ ]",
        r"[-_ ]0*([1-9]|1[0-6])\."
    ]
    name = Path(filename).stem.lower()
    for pat in patterns:
        m = re.search(pat, name)
        if m:
            num = int(m.group(1))
            if 1 <= num <= 16:
                return num
    return None

def format_timestamp(seconds: float) -> str:
    """Format seconds into HH:MM:SS string."""
    td = timedelta(seconds=int(seconds))
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def extract_audio(video_path: Path, output_wav: Path) -> bool:
    """Extract 16kHz mono audio from video file using ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(output_wav)
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[ERROR] Failed to extract audio with ffmpeg: {e}", file=sys.stderr)
        return False

DEFAULT_INITIAL_PROMPT = (
    "Word2Vec, word embeddings, vectors, vector space, continuous bag of words, CBOW, Skip-gram, "
    "GloVe, FastText, negative sampling, hierarchical softmax, Huffman tree, out-of-vocabulary, OOV, "
    "subwords, n-grams, recurrent neural networks, RNN, hidden state, backpropagation through time, "
    "BPTT, vanishing gradients, exploding gradients, gradient clipping, LSTM, Long Short-Term Memory, "
    "forget gate, input gate, output gate, cell state, constant error carousel, GRU, Gated Recurrent Unit, "
    "reset gate, update gate, sequence to sequence, seq2seq, encoder-decoder, teacher forcing, "
    "Bahdanau attention, Hochreiter, Schmidhuber, Mikolov, Bengio, Flavio Giobergia, Riccardo Coppola, "
    "Politecnico di Torino"
)

def transcribe_audio(
    audio_path: Path,
    model_name: str = "base.en",
    language: str = "en",
    initial_prompt: str = DEFAULT_INITIAL_PROMPT,
    verbose: bool = True
) -> dict:
    """Transcribe audio using local OpenAI Whisper model (zero LLM tokens)."""
    import whisper
    import torch

    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Loading local Whisper model '{model_name}' on device '{device}' (zero API tokens consumed)...")
    model = whisper.load_model(model_name, device=device)

    print(f"[*] Transcribing audio: {audio_path.name}...")
    options = {
        "task": "transcribe",
        "verbose": verbose,
        "condition_on_previous_text": False,
        "compression_ratio_threshold": 2.4,
        "no_speech_threshold": 0.6,
        "logprob_threshold": -1.0,
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
    }
    if device in ("mps", "cpu"):
        options["fp16"] = False
    if language and not model_name.endswith(".en"):
        options["language"] = language
    if initial_prompt:
        options["initial_prompt"] = initial_prompt

    result = model.transcribe(str(audio_path), **options)
    return result

def save_markdown_transcript(
    result: dict,
    video_path: Path,
    out_dir: Path,
    lecture_num: int | None = None,
    custom_title: str | None = None,
    custom_filename: str | None = None
) -> Path:
    """Save formatted transcript to Markdown with frontmatter and timestamped segments."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # Determine standardized filename
    if custom_filename:
        base_name = Path(custom_filename).stem
    elif lecture_num and lecture_num in COURSE_MODULE_MAP:
        base_name = COURSE_MODULE_MAP[lecture_num]
    elif lecture_num:
        base_name = f"{lecture_num:02d}-{custom_title or video_path.stem}"
    elif custom_title:
        base_name = custom_title
    else:
        base_name = video_path.stem

    # Clean filename
    base_name = re.sub(r"[^\w\-_.]", "-", base_name).strip("-")
    out_file = out_dir / f"{base_name}.md"

    segments = result.get("segments", [])
    full_text = result.get("text", "").strip()
    detected_lang = result.get("language", "en")

    total_duration = segments[-1]["end"] if segments else 0
    duration_str = format_timestamp(total_duration)
    word_count = len(full_text.split())

    topic_title = custom_title or (COURSE_MODULE_MAP.get(lecture_num, base_name) if lecture_num else base_name)
    topic_title_clean = topic_title.replace("-", " ").replace("_", " ")

    lines = [
        "---",
        f"lecture_id: \"{lecture_num:02d}\"" if lecture_num else "lecture_id: null",
        f"topic: \"{topic_title_clean}\"",
        f"source_video: \"{video_path.name}\"",
        f"course: \"Large Language Models for Software Engineering (Politecnico di Torino)\"",
        "instructors:",
        "  - \"Prof. Flavio Giobergia\"",
        "  - \"Prof. Riccardo Coppola\"",
        f"date_transcribed: \"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\"",
        f"detected_language: \"{detected_lang}\"",
        f"total_duration: \"{duration_str}\"",
        f"word_count: {word_count}",
        f"transcription_engine: \"Local OpenAI Whisper (zero LLM tokens consumed)\"",
        "---",
        "",
        f"# Lecture Transcription: {topic_title_clean}",
        "",
        f"> **Source Video**: `{video_path.name}`  ",
        f"> **Duration**: `{duration_str}` | **Word Count**: `{word_count:,}` words | **Language**: `{detected_lang}`  ",
        f"> **Transcription Method**: Offline local Whisper model (100% token-free)",
        "",
        "---",
        "",
        "## Table of Contents & Timeline",
        ""
    ]

    # Generate timeline anchors every ~3-5 minutes or natural pauses
    timeline_entries = []
    chunk_interval = 180.0  # 3 minutes
    last_chunk_time = -chunk_interval

    for seg in segments:
        start_time = seg.get("start", 0)
        if start_time - last_chunk_time >= chunk_interval:
            ts = format_timestamp(start_time)
            snippet = seg.get("text", "").strip()[:60]
            timeline_entries.append(f"- **[{ts}](#{ts.replace(':', '')})**: {snippet}...")
            last_chunk_time = start_time

    lines.extend(timeline_entries if timeline_entries else ["*(Short lecture or single continuous segment)*"])
    lines.extend([
        "",
        "---",
        "",
        "## Timestamped Transcription",
        ""
    ])

    # Add timestamped chunks
    current_chunk = []
    current_chunk_start = 0
    chunk_duration = 120.0  # Group by ~2 minute blocks for readability

    for seg in segments:
        if not current_chunk:
            current_chunk_start = seg.get("start", 0)

        current_chunk.append(seg.get("text", "").strip())

        if seg.get("end", 0) - current_chunk_start >= chunk_duration:
            ts_start = format_timestamp(current_chunk_start)
            ts_end = format_timestamp(seg.get("end", 0))
            chunk_text = " ".join(current_chunk)
            lines.append(f"### <a id=\"{ts_start.replace(':', '')}\"></a>[{ts_start} - {ts_end}]")
            lines.append("")
            lines.append(chunk_text)
            lines.append("")
            current_chunk = []

    if current_chunk:
        ts_start = format_timestamp(current_chunk_start)
        ts_end = format_timestamp(total_duration)
        chunk_text = " ".join(current_chunk)
        lines.append(f"### <a id=\"{ts_start.replace(':', '')}\"></a>[{ts_start} - {ts_end}]")
        lines.append("")
        lines.append(chunk_text)
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Continuous Full Text",
        "",
        full_text,
        ""
    ])

    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file

def main():
    parser = argparse.ArgumentParser(description="Zero-Token Local Whisper Lecture Transcriber for PoliTO LLM4SE")
    parser.add_argument("video_path", type=str, help="Path to input audio/video file (.mp4, .m4a, .wav, etc.)")
    parser.add_argument("--number", "-n", type=int, default=None, help="Lecture number (1-16) to map to syllabus")
    parser.add_argument("--topic", "-t", type=str, default=None, help="Custom topic name")
    parser.add_argument("--filename", "-f", type=str, default=None, help="Custom output filename (e.g. 03-04-Word-Embeddings-And-RNNs.md)")
    parser.add_argument("--model", "-m", type=str, default="base.en", help="Whisper model (tiny, base.en, base, small.en, small, turbo, large)")
    parser.add_argument("--language", "-l", type=str, default="en", help="Audio language (default: en)")
    parser.add_argument("--initial-prompt", "-p", type=str, default=DEFAULT_INITIAL_PROMPT, help="Prompt to guide technical terminology")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Output directory (defaults to TRANSCRIPTIONS/LECTURES if present)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress verbose segment printing during transcription")

    args = parser.parse_args()
    video_path = Path(args.video_path)

    if not video_path.exists():
        print(f"[ERROR] Input file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    lecture_num = args.number or infer_lecture_number(video_path.name)
    if lecture_num:
        print(f"[*] Detected Lecture #{lecture_num}: {COURSE_MODULE_MAP.get(lecture_num, 'Custom')}")
    else:
        print("[!] Could not infer lecture number from filename.")

    if args.output_dir:
        out_dir = Path(args.output_dir)
    elif Path("TRANSCRIPTIONS/LECTURES").exists():
        out_dir = Path("TRANSCRIPTIONS/LECTURES")
    else:
        out_dir = Path("LECTURE_TRANSCRIPTIONS")

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = Path(tmpdir) / "extracted_audio.wav"
        print(f"[*] Extracting 16kHz mono audio from {video_path.name}...")
        if not extract_audio(video_path, wav_path):
            print("[ERROR] Audio extraction failed.", file=sys.stderr)
            sys.exit(1)

        result = transcribe_audio(
            wav_path,
            model_name=args.model,
            language=args.language,
            initial_prompt=args.initial_prompt,
            verbose=not args.quiet
        )
        out_file = save_markdown_transcript(
            result=result,
            video_path=video_path,
            out_dir=out_dir,
            lecture_num=lecture_num,
            custom_title=args.topic,
            custom_filename=args.filename
        )

    print(f"\n[SUCCESS] Lecture transcription completed successfully (0 LLM tokens consumed)!")
    print(f"[+] Output saved to: {out_file.resolve()}")

if __name__ == "__main__":
    main()
