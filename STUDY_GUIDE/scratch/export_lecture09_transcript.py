import sqlite3
from datetime import datetime
from pathlib import Path

db_path = '/Users/nicolabeccaceci/Library/Containers/com.goodsnooze.MacWhisper/Data/Library/Application Support/MacWhisper/Database/main.sqlite'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get session
cur.execute("""
    SELECT id, originalFilename, playbackDuration, fullText 
    FROM session 
    WHERE originalFilename = 'efficient fine-tuning and inference'
""")
res = cur.fetchone()
if not res:
    print("Session not found!")
    exit(1)

s_id, orig_fn, duration, full_text = res

# Get lines
cur.execute("""
    SELECT start, end, text 
    FROM transcriptline 
    WHERE sessionID = ? 
    ORDER BY start ASC
""", (s_id,))
lines = cur.fetchall()

def format_ts(ms):
    total_sec = int(ms / 1000)
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    seconds = total_sec % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

out_path = Path("STUDY_GUIDE/transcriptions/LECTURES/09-PEFT-Efficient-FineTuning-Inference.md")

dur_str = format_ts(duration * 1000)
words = len(full_text.split())

md_lines = [
    "---",
    "lecture_id: null",
    "topic: \"09 PEFT Efficient Fine-Tuning and Inference\"",
    f"source_video: \"{orig_fn}.mp4\"",
    "course: \"Large Language Models for Software Engineering (Politecnico di Torino)\"",
    "instructors:",
    "  - \"Prof. Flavio Giobergia\"",
    "  - \"Prof. Riccardo Coppola\"",
    f"date_transcribed: \"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\"",
    "detected_language: \"en\"",
    f"total_duration: \"{dur_str}\"",
    f"word_count: {words}",
    "transcription_engine: \"Local MacWhisper (zero LLM tokens consumed)\"",
    "---",
    "",
    f"# Lecture Transcription: 09 PEFT, Efficient Fine-Tuning and Inference",
    "",
    f"> **Source Video**: `{orig_fn}.mp4`  ",
    f"> **Duration**: `{dur_str}` | **Word Count**: `{words:,}` words | **Language**: `en`  ",
    "> **Transcription Method**: Offline local Whisper model (100% token-free)",
    "",
    "---",
    "",
    "## Table of Contents & Timeline",
    ""
]

# Create TOC entries every ~3 minutes
step_ms = 180 * 1000
next_target = 0
for start, end, text in lines:
    if start >= next_target:
        ts = format_ts(start)
        anchor = ts.replace(":", "")
        snippet = text[:55] + "..." if len(text) > 55 else text
        md_lines.append(f"- **[{ts}](#{anchor})**: {snippet}")
        next_target = start + step_ms

md_lines.extend(["", "---", "", "## Full Verbatim Transcription", ""])

# Group lines into paragraph blocks
curr_block = []
block_start = 0

for i, (start, end, text) in enumerate(lines):
    if not curr_block:
        block_start = start
    curr_block.append(text)
    
    # New paragraph every ~30 seconds or ~60 words
    if end - block_start >= 30000 or len(" ".join(curr_block).split()) >= 60:
        ts = format_ts(block_start)
        anchor = ts.replace(":", "")
        md_lines.append(f"### <a id=\"{anchor}\"></a>[{ts}]")
        md_lines.append("")
        md_lines.append(" ".join(curr_block))
        md_lines.append("")
        curr_block = []

if curr_block:
    ts = format_ts(block_start)
    anchor = ts.replace(":", "")
    md_lines.append(f"### <a id=\"{anchor}\"></a>[{ts}]")
    md_lines.append("")
    md_lines.append(" ".join(curr_block))
    md_lines.append("")

out_path.write_text("\n".join(md_lines), encoding="utf-8")
print(f"Wrote {len(md_lines)} lines to {out_path} ({words} words)")
