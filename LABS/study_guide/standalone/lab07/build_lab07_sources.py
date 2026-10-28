#!/usr/bin/env python3
"""Build the editable Laboratory 07 solution from notebook execution evidence."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GUIDE = ROOT / "study_guide"
CHAPTER = GUIDE / "chapters" / "07_user_story_generation.tex"
WRAPPER = GUIDE / "standalone" / "lab07" / "lab07_solution.tex"
INVENTORY = GUIDE / "coverage" / "lab07.inventory.json"
NOTEBOOK_PATH = ROOT / "lab07" / "text-07-stories.ipynb"

# These explanations follow the actual computation; code and output are read
# directly from the finalized notebook and hash-addressed export artifacts.
NARRATIVE = {
    0: (
        r"The pipeline begins with a fixed seed, the available compute device, and Llama 3.2 3B Instruct loaded from the locally authenticated Hugging Face account. The helper accepts chat-template prompts, avoids adding a second BOS token, samples at temperature 0.15, and stops at either Llama's end-of-turn or EOS token. After decoding, it frees generated tensors and clears the MPS cache. These shared settings apply to role, function, and purpose generation.",
        r"The output confirms MPS selection and successful model initialization; the loading progress and library warnings are execution diagnostics rather than model answers. Authentication comes from the local Hugging Face credential store, never the notebook. The checkpoint is loaded in FP16. The environment and model revision accompany the run record for reproducibility."
    ),
    2: (
        r"The requirements specification is the shared input for all later stages. Before extracting stories, this cell contrasts a manually serialized system/user conversation with the tokenizer's official chat-template serializer using a small capital-city question. The demo isolates prompt structure from the hiking requirements and shows how an assistant-generation prefix is formed.",
        r"Both paths return exactly \texttt{Paris}. The manual serialization visibly supplies its own system and user headers, while the tokenizer-generated template inserts the model's system metadata (knowledge-cutoff and current date) before the same messages. Both include an assistant-generation prefix; using the official template prevents hand-written header mistakes. Because the prompt text already includes the serialized tokens, \texttt{add\_special\_tokens=False} in the shared helper avoids adding a second beginning token."
    ),
    4: (
        r"This cell creates zero-shot, one-shot, and few-shot role-extraction prompts. The one-shot and few-shot examples are represented as complete alternating user/assistant messages, so each demonstration teaches both the task and the requested list format. The same hiking requirements are then appended as the final user query to each prompt.",
        r"All three prompt conditions returned the same four roles: visitors, local guides, platform managers, and hut workers. The consistency is useful, but the CSV comparison later shows the list misses two reference roles. In this recorded run, adding demonstrations did not change the extracted list; format compliance should not be confused with full coverage."
    ),
    6: (
        r"The evaluation reference is derived from the supplied \texttt{stories.csv}. The helper scans each user-story description for its 'As a ... I want' role phrase, removes duplicates, and sorts the result. Keeping reference preparation in its own cell makes it possible to audit the target set independently of the language model.",
        r"The printed set contains the six distinct role phrases extracted from the CSV. The parenthetical phrase in the first description is retained as part of its role string; the following normalization handles case, whitespace, and a final plural 's', but does not semantically rewrite role names."
    ),
    7: (
        r"This cell parses the few-shot model answer into list items, normalizes the extracted and reference roles, and counts true positives, false positives, and false negatives. Precision is the fraction of extracted roles that match the reference; recall is the fraction of reference roles recovered. The formulas return zero when their denominator is empty, avoiding a division error for empty sets.",
        r"The run reports four true positives, zero false positives, and two false negatives. Precision is 1.0 because every extracted role appears in the CSV reference; recall is 0.667 because two CSV roles were missed. These scores reflect this reference and exact string normalization; they do not establish semantic equivalence or measure zero-shot and one-shot answers, which happen to match in this run."
    ),
    9: (
        r"For each extracted role, this loop asks for concise actions grounded in the complete hiking requirements. A food-delivery example demonstrates the expected numbered-list shape, while the actual query includes the full requirements and names the current role. The parser accepts only an initial, contiguous numbered or bulleted list; it skips a response that begins with NONE or prose, and stops at commentary. Accepted actions become provisional 'As a role, I want to function' tuples.",
        r"The recorded run returns numbered functions for all four extracted roles. The actions are relevant paraphrases of the requirements, not an independently verified or exhaustive inventory. Importantly, no per-role requirement excerpt is constructed despite the original comments describing that as an option; each prompt receives the full requirements."
    ),
    11: (
        r"The final cell demonstrates the 'so that' step for the first generated role/function pair. It separates the existing role and function from the provisional story, then asks the model to infer one purpose using the original requirements and a single worked example. This cell demonstrates purpose generation for one pair rather than completing every tuple in the collection.",
        r"The printed role and function identify the first tuple, and the response demonstrates one 'so that' completion: exploring and discovering suitable hiking routes. The revised in-context example now uses hiking preferences and abilities rather than an unrelated domain. This final cell handles only one pair, so it neither completes all tuples nor validates every earlier function."
    ),
}


def tex_path(path: str) -> str:
    if path.startswith("study_guide/"):
        return "../../" + path.removeprefix("study_guide/")
    if path.startswith("lab07/"):
        return "../../../" + path
    raise ValueError(path)


def build() -> None:
    if not INVENTORY.exists():
        raise SystemExit(f"Run cell_coverage export first: {INVENTORY}")
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    by_index = {cell["cell_index"]: cell for cell in inventory["cells"]}
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    out = [
        r"\section[User-story generation]{User-story generation from requirements}",
        r"\label{sec:lab07-stories}",
        r"This exercise turns a hiking-platform requirements specification into user stories through three linked questions: who uses the system, what each role needs to do, and why that action matters. The same requirements text feeds each extraction stage; a supplied CSV provides a reference set for role-level precision and recall. The process ends by adding a purpose clause to a generated role/function pair. The results are model outputs evaluated against this particular reference, not a proof that the requirements or generated stories are complete.",
        r"\begin{figure}[htbp]\centering\includegraphics[width=\linewidth]{../../../lab07/architecture_diagram.png}\caption{Notebook-provided architecture: requirements feed role extraction, then functions and purposes, producing user stories.}\label{fig:lab07-architecture}\end{figure}",
        r"\subsection{Model setup and prompt serialization}",
    ]
    for index in (0, 2):
        out.append(cell_block(index, notebook["cells"][index], by_index[index]))
    out += [
        r"\subsection{Extracting and evaluating roles}",
        r"The first extraction stage asks the same model to identify the people and stakeholders represented in the hiking-platform requirements. The prompts below differ only in their in-context examples; the CSV reference is prepared separately so the scoring target does not depend on the generated response.",
    ]
    for index in (4, 6, 7):
        out.append(cell_block(index, notebook["cells"][index], by_index[index]))
    out += [
        r"\subsection{From roles to functions and purposes}",
        r"Role names narrow the next prompt to actions that a stakeholder needs from the platform. The notebook converts each extracted action into a provisional role/function story, then asks for the reason behind one such action to complete the familiar 'As a ..., I want ..., so that ...' form.",
    ]
    for index in (9, 11):
        out.append(cell_block(index, notebook["cells"][index], by_index[index]))
    out += [
        r"\begin{quote}\textbf{Reading the result.} The exercise demonstrates a staged requirements-analysis workflow and a simple reference-based metric. Its final purpose-generation cell handles only the first role/function pair, and automatic extraction can omit, duplicate, or paraphrase requirements. A human review is still needed before treating generated stories as accepted requirements.\end{quote}",
        r"\section{Execution and reproducibility notes}",
        r"The matching lecture recording was not available in Whisper or in the supplied course files during this run. Per the task scope, lecture review is deferred until the professor provides the recordings; explanations here are based on the notebook's assignment text, source, provided architecture image, and saved outputs.",
        r"The model is \texttt{meta-llama/Llama-3.2-3B-Instruct}, loaded in FP16 on MPS from the locally authenticated Hugging Face account. Generation uses seeded low-temperature sampling with one beam and task-specific token caps. Samples can vary across framework versions, kernels, and model revisions. The exact dependency versions, model revision, and execution records are listed in the accompanying environment and provenance files.",
    ]
    CHAPTER.parent.mkdir(parents=True, exist_ok=True)
    CHAPTER.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    WRAPPER.write_text(r"""\documentclass[10pt,a4paper,oneside]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{newpxtext}
\usepackage[scaled=0.88]{sourcecodepro}
\usepackage{microtype}
\usepackage[a4paper,top=19mm,bottom=19mm,left=20mm,right=20mm,headheight=16pt,footskip=10mm]{geometry}
\usepackage[dvipsnames,table]{xcolor}
\usepackage{graphicx,amssymb,booktabs,tabularx,array,enumitem,listings,tikz,titlesec,fancyhdr,hyperref}
\definecolor{politoNavy}{RGB}{0,45,98}
\definecolor{steelBlue}{RGB}{35,100,160}
\definecolor{skyBlue}{RGB}{230,240,250}
\definecolor{bodyGray}{RGB}{80,85,90}
\definecolor{codeBg}{RGB}{248,249,251}
\definecolor{codeFrame}{RGB}{220,225,230}
\hypersetup{colorlinks=true,linkcolor=politoNavy,urlcolor=steelBlue,pdftitle={Laboratory 07 complete solution},pdfauthor={Politecnico di Torino}}
\titleformat{\section}{\normalfont\sffamily\Large\bfseries\color{politoNavy}}{\thesection}{0.8em}{}
\titleformat{\subsection}{\normalfont\sffamily\large\bfseries\color{steelBlue}}{\thesubsection}{0.8em}{}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small\sffamily\color{bodyGray}\nouppercase{\rightmark}}\fancyhead[R]{\small\sffamily\bfseries\thepage}\renewcommand{\headrulewidth}{0.4pt}
\lstdefinestyle{studycode}{language=Python,basicstyle=\fontsize{7.4}{8.8}\ttfamily,keywordstyle=\bfseries\color{politoNavy},commentstyle=\itshape\color{bodyGray},stringstyle=\color{ForestGreen},numbers=left,numberstyle=\tiny\color{bodyGray},numbersep=6pt,tabsize=4,showstringspaces=false,breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true,frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg},
literate={█}{{\ensuremath{\blacksquare}}}1 {•}{{\ensuremath{\bullet}}}1 {–}{{--}}1 {—}{{---}}1}
\lstdefinestyle{terminalOutput}{basicstyle=\fontsize{7.2}{8.5}\ttfamily,breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true,showstringspaces=false,frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg},
literate={█}{{\ensuremath{\blacksquare}}}1 {•}{{\ensuremath{\bullet}}}1 {–}{{--}}1 {—}{{---}}1}
\lstset{style=studycode}\setlist{nosep,leftmargin=1.5em}
\newcommand{\labSolutionTitle}{Laboratory 07: User Story Generation}
\newcommand{\labSolutionSubtitle}{Complete notebook-aligned solution}
\begin{document}
\hypersetup{pageanchor=false}
\input{../../frontmatter/solution_titlepage}
\hypersetup{pageanchor=true}
\tableofcontents
\clearpage
\input{../../chapters/07_user_story_generation.tex}
\end{document}
""", encoding="utf-8")
    print(f"Wrote {CHAPTER} and {WRAPPER}")


def cell_block(index: int, cell: dict, record: dict) -> str:
    source = "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
    source_hash = record["source_sha256"]
    purpose, interpretation = NARRATIVE[index]
    lines = [
        r"\medskip\noindent " + purpose,
        rf"% coverage-cell: LABS/lab07/text-07-stories.ipynb cell={index} source_sha256={source_hash}",
        r"\begin{lstlisting}[style=studycode]", source.rstrip("\n"), r"\end{lstlisting}",
        r"\par\smallskip",
    ]
    for output in record.get("exported_outputs", []):
        oi = output["index"]
        artifact = output.get("presentation_artifact", "")
        artifact_marker = artifact if artifact else "-"
        lines += [
            rf"% coverage-output: LABS/lab07/text-07-stories.ipynb cell={index} output={oi} source_sha256={source_hash} payload_sha256={output['payload_sha256']} artifact={artifact_marker}",
            rf"\label{{out:lab07-stories-{index:04d}-{oi:02d}}}",
        ]
        if artifact:
            lines.append(rf"\lstinputlisting[style=terminalOutput]{{{tex_path(artifact)}}}")
        else:
            lines.append(r"\textit{This notebook output has no printable text representation.}")
    if not record.get("outputs"):
        lines.append(interpretation)
    else:
        lines.append(interpretation)
    return "\n".join(lines)


if __name__ == "__main__":
    build()
