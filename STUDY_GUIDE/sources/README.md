# Study Guide Source Materials Architecture

To guarantee completeness, zero omission, and rigorous pedagogical grounding, all source materials are strictly partitioned into a structured hierarchy prior to chapter or laboratory authoring:

```
STUDY_GUIDE/sources/
├── shared/                              # Common materials across all chapters and labs
│   ├── books/                           # Reference textbooks (Raschka, Welch, Xiao & Zhu)
│   ├── papers/                          # Multi-chapter foundational papers (Shannon, Vaswani)
│   └── multimedia/                      # Channel-wide lecture notes & breakdowns
├── lectures/                            # Volume I: Lectures source materials
│   ├── shared/                          # Cross-cutting lecture resources
│   ├── chapter_01/                      # Chapter 01: Introduction to Language Models
│   │   ├── slides/                      # Symlink to SLIDES/01-Language-Models-Intro.pdf
│   │   ├── transcriptions/              # Symlink to TRANSCRIPTIONS/LECTURES/01-...
│   │   ├── papers/                      # Shannon 1948, Kneser-Ney 1995, Bengio 2003
│   │   └── multimedia/                  # Karpathy makemore Part 1, StatQuest
│   ├── chapter_02/                      # Chapter 02: Deep Learning Foundations
│   │   ├── slides/                      # Symlink to SLIDES/02-DL-Intro.pdf
│   │   ├── papers/                      # Cybenko 1989, Hornik 1989, Rosenblatt 1958
│   │   └── multimedia/                  # Karpathy micrograd, 3B1B Neural Networks
│   ├── chapter_03/                      # Chapter 03: Word Representations & Word2Vec
│   │   ├── slides/                      # Symlink to SLIDES/03-WordEmbeddings.pdf
│   │   ├── transcriptions/              # Symlink to TRANSCRIPTIONS/LECTURES/03-04-...
│   │   ├── books/                       # Raschka Chapter 2 summary notes
│   │   ├── papers/                      # Mikolov 2013a/b, Bojanowski 2017, Morin 2005
│   │   └── multimedia/                  # Enkk 2023 embeddings video, Karpathy makemore
│   ├── chapter_04/                      # Chapter 04: Recurrent Neural Networks
│   │   ├── slides/                      # Symlink to SLIDES/04-RNN.pdf
│   │   ├── transcriptions/              # Symlink to TRANSCRIPTIONS/LECTURES/03-04-...
│   │   ├── papers/                      # Hochreiter 1997, Cho 2014, Sutskever 2014
│   │   └── multimedia/                  # Karpathy Unreasonable Effectiveness of RNNs
│   └── chapter_05/ ... chapter_16/      # Scaffolded directories for syllabus modules
└── laboratories/                        # Volume II: Laboratories source materials
    ├── shared/                          # PyTorch environments & autograd cheatsheets
    ├── lab_01/                          # Laboratory 01: PyTorch Foundations
    │   ├── notebooks/                   # Symlink to LABS/lab01/text.ipynb
    │   ├── transcriptions/              # Symlink to TRANSCRIPTIONS/LABORATORIES/Lab01-...
    │   └── references/                  # PyTorch official tensor & autograd documentation
    └── lab_02/ ... lab_10/              # Scaffolded directories for each practical lab
```

## Duplication & File Handling Protocol
1. **Zero-Byte Deduplication via Relative Symlinks**:
   - Course slides (`SLIDES/*.pdf`), lecture audio transcriptions (`TRANSCRIPTIONS/LECTURES/*.md`), and laboratory notebooks (`LABS/labXX/*.ipynb`) are linked using relative symlinks (`ln -sf`).
   - This prevents storage bloat while guaranteeing that any updates to primary slides or transcripts are immediately available in the corresponding chapter's source folder.
2. **Git Tracking & Large Binaries**:
   - As enforced by `.gitignore`, large proprietary or external binaries (`*.pdf`, `*.epub`, `*.mp4`, `*.m4a`) are excluded from Git commits to keep the repository compact, while all Markdown indices (`README.md`, notes, summaries) are tracked.
