#!/usr/bin/env python3
"""Export Lab08 notebook evidence and build its editable standalone chapter."""
from __future__ import annotations

import json
import sys
from pathlib import Path

LABS = Path(__file__).resolve().parents[3]
GUIDE = LABS / "study_guide"
SKILL_SCRIPTS = LABS / ".agents/skills/laboratory-study-guide-integrator/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
import cell_coverage  # noqa: E402

NOTEBOOK = LABS / "lab08/text-08-roc-router-design.ipynb"
ARTIFACTS = GUIDE / "execution_artifacts/lab08"
INVENTORY = GUIDE / "coverage/lab08.inventory.json"
COVERAGE = GUIDE / "coverage/lab08.json"
CHAPTER = GUIDE / "chapters/08_roc_router_design.tex"

NARRATIVE = {
    1: (
        "The first computation builds a reproducible toy retrieval problem: each of 100 expected vectors has five coordinates, and its paired actual vector is perturbed coordinate by coordinate. The row index is therefore a known positive match; all other expected/actual pairs are negative. Cosine similarity turns every pair into a score, which is the ranking signal evaluated by the following threshold cells.",
        "The printed matrix is a 100 by 100 score matrix, abbreviated by NumPy with an ellipsis. Its diagonal contains the intended matches, while off-diagonal values are candidate mismatches. A high cosine score indicates directional similarity only; the synthetic index alignment supplies the ground truth in this exercise.",
    ),
    3: (
        "With scores available, this helper converts a threshold into a binary decision for each of the 10,000 pairs. The known diagonal is positive and every off-diagonal pair is negative. It counts the four confusion-matrix outcomes, then normalizes true positives by all positives and false positives by all negatives. The equal-shape and nonempty checks prevent a silently invalid comparison.",
        "At threshold 0.95, TPR is 0.44: 44 of 100 planted matches pass. FPR is about 0.03889: 385 of 9,900 mismatches also pass. This single operating point motivates sweeping thresholds for the ROC curve.",
    ),
    5: (
        "The next cell repeatedly calls the same classifier while lowering the score threshold. Positive and negative infinity explicitly represent classifying no pairs or all pairs as positive, even though cosine scores may be negative. The plotted curve traces the sensitivity/false-alarm tradeoff; its diagonal is the random-ranking reference. The exact ranking AUC is also computed so the discretized threshold-grid approximation can be checked.",
        "The curve lies well above the random diagonal for this seeded synthetic task. The threshold-grid area is 0.920869 and the exact pair-ranking AUC is 0.920541; their small difference comes from finite threshold sampling. These are properties of this constructed vector data, not measured language-model quality.",
    ),
    8: (
        "The second exercise begins by selecting the available accelerator, fixing the generation seed, and loading the pinned Llama 3.2 3B Instruct checkpoint and tokenizer. Local Hugging Face authentication grants access without embedding a credential in the notebook. The helper accepts an already serialized chat prompt, disables extra token insertion, performs greedy continuation under inference mode, and slices off the prompt tokens so callers receive only newly generated text.",
        "The printed device confirms that this run selected MPS. The tokenizer and checkpoint remain in memory for the routing and task-generation cells. Model-loading progress and the notebook-widget warning are transcribed in the diagnostics appendix.",
    ),
    10: (
        r"This cell supplies a long hiking-platform requirements document and asks the model to classify a separate user request into one of two exact labels. Applying the tokenizer's official chat template serializes system and user roles, then adds the assistant-generation prefix. The helper constrains each generated token to one of the two tokenized candidate labels, preventing free-form text from escaping the router's interface. A short generation budget is appropriate because the router needs only a label, not a design artifact. The raw decision is saved as \texttt{response} for strict validation in the next cell.",
        "The user instruction and raw model response are shown verbatim. The decision determines which specialized prompt branch runs next; the parser rejects unsupported or explanatory output rather than quietly guessing a route.",
    ),
    12: (
        "The final code cell normalizes case and punctuation, then accepts only the two declared route labels. Each branch builds an independent task prompt with a small format example and sends the complete hiking requirements to the same model. The use-case branch asks for actor-grouped user goals; the class branch asks for grounded domain-class names. Both decode at most 2,000 new tokens, and only the branch selected by the router executes.",
        r"The parser accepts the exact model-produced label \texttt{Use Cases}, selects that branch, and the model returns actor-grouped user-goal actions. The list is grounded in the supplied text but still needs review for completeness and invented behavior; successful routing and a plausible artifact do not establish a reliable general classifier or requirements analyst. The separate ChatGPT comparison requested in the notebook is not represented as a result because no independent ChatGPT generation was recorded. A fair comparison would use the same requirements, user request, output limits, and rubric, then compare route accuracy, requirement coverage, unsupported additions, and format validity over multiple cases.",
    ),
}


def src(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else str(value)


def tex_path(path: str) -> str:
    if path.startswith("study_guide/"):
        return "../../" + path[len("study_guide/"):]
    if path.startswith("lab08/"):
        return "../../../" + path
    raise ValueError(f"Unexpected Lab08 artifact path: {path}")


def pipeline(nodes: list[str]) -> str:
    coords = [(0, 0), (4.5, 0), (9, 0), (9, -1.6), (4.5, -1.6), (0, -1.6)]
    lines = [r"\begin{figure}[htbp]", r"\centering", r"\resizebox{\linewidth}{!}{%",
             r"\begin{tikzpicture}[>=Stealth,stage/.style={draw=steelBlue,fill=skyBlue,rounded corners=2pt,align=center,text width=3.5cm,minimum height=.85cm,font=\small\sffamily}]"]
    for i, (label, (x, y)) in enumerate(zip(nodes, coords)):
        lines.append(rf"\node[stage] ({'abcdef'[i]}) at ({x}cm,{y}cm) {{{label}}};")
    for i in range(5):
        lines.append(rf"\draw[->,thick,steelBlue] ({'abcdef'[i]}) -- ({'abcdef'[i+1]});")
    lines.extend([r"\end{tikzpicture}%", r"}", r"\caption{The computation pipeline from inputs to checked results.}", r"\end{figure}"])
    return "\n".join(lines)


def build() -> None:
    inventory = cell_coverage.export([NOTEBOOK], LABS, ARTIFACTS)
    if inventory.get("input_errors"):
        raise RuntimeError(inventory["input_errors"])
    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    INVENTORY.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    records = {item["cell_index"]: item for item in inventory["cells"]}
    diagnostics = []
    body = [
        r"\section[Threshold evaluation]{Threshold evaluation with a receiver operating characteristic curve}",
        r"\label{sec:lab08-roc}",
        "This exercise turns similarity scores into a threshold-based retrieval evaluation. A seeded synthetic dataset provides known positive matches, allowing the notebook to count true and false decisions and inspect their tradeoff across thresholds. The example teaches how to calculate and interpret ROC/AUC; it does not measure the quality of a language model.",
        pipeline(["Seed paired five-dimensional vectors", "Compute all cosine pair scores", "Threshold the known matches", "Sweep thresholds and plot ROC", "Compare approximate and exact AUC", "Discuss alignment and limitations"]),
        r"\subsection{Constructing scores and evaluating a threshold}",
    ]
    for index in (1, 3, 5):
        record = records[index]
        source_hash = record["source_sha256"]
        purpose, interpretation = NARRATIVE[index]
        body += [purpose,
                 rf"% coverage-cell: LABS/{record['notebook']} cell={index} source_sha256={source_hash}",
                 r"\phantomsection", rf"\label{{res:lab08-cell-{index:04d}}}",
                 r"\begin{lstlisting}[style=studycode]", src(notebook["cells"][index]).rstrip("\n"), r"\end{lstlisting}"]
        for output in record["outputs"]:
            exp = record["exported_outputs"][output["index"]]
            artifact = exp.get("presentation_artifact", "")
            body.append(rf"% coverage-output: LABS/{record['notebook']} cell={index} output={output['index']} source_sha256={source_hash} payload_sha256={output['payload_sha256']} artifact={artifact or '-'}")
            body.append(r"\phantomsection" + rf"\label{{out:lab08-cell-{index:04d}-{output['index']:02d}}}")
            if (index == 8 and output["index"] in {0, 2, 3, 4, 5, 6}) or (index in {10, 12} and output["index"] == 1):
                diagnostics.append((index, output["index"], exp))
                continue
            if artifact:
                body.append(rf"\lstinputlisting[style=terminalOutput]{{{tex_path(artifact)}}}")
            for figure in exp.get("figures", []):
                body.append(rf"\begin{{center}}\includegraphics[width=.82\linewidth]{{{tex_path(figure)}}}\end{{center}}")
        body.append(interpretation)
    body += [
        "Increasing vector dimension does not automatically improve retrieval: for independent random coordinates, unrelated cosine scores concentrate as dimension grows, while the paired-signal distribution depends on how perturbation scales with dimension. Increasing the perturbation generally weakens the planted pairing, but its effect should be measured with labeled examples rather than assumed from a single score. If row alignment is unknown, index equality is not ground truth; an independently labeled match set or trusted identifiers are required before reporting TPR, FPR, or AUC. Cosine similarity by itself cannot establish correctness.",
        r"\clearpage",
        r"\section[LLM router]{A two-stage LLM router for software design tasks}",
        r"\label{sec:lab08-router}",
        "The second exercise separates intent classification from artifact generation. A first Llama call selects a supported route, and a second call uses a task-specific prompt to propose use cases or class names from the hiking-platform requirements. This division makes the routing decision inspectable and gives each task a narrower output contract.",
        pipeline(["Select device and load pinned model", "Serialize user request as chat", "Classify into an exact route", "Validate the route label", "Generate the selected design artifact", "Evaluate coverage and grounding"]),
        r"\subsection{Model setup and continuation helper}",
    ]
    for index in (8, 10, 12):
        record = records[index]
        source_hash = record["source_sha256"]
        purpose, interpretation = NARRATIVE[index]
        body += [purpose,
                 rf"% coverage-cell: LABS/{record['notebook']} cell={index} source_sha256={source_hash}",
                 r"\phantomsection", rf"\label{{res:lab08-cell-{index:04d}}}",
                 r"\begin{lstlisting}[style=studycode]", src(notebook["cells"][index]).rstrip("\n"), r"\end{lstlisting}"]
        for output in record["outputs"]:
            exp = record["exported_outputs"][output["index"]]
            artifact = exp.get("presentation_artifact", "")
            body.append(rf"% coverage-output: LABS/{record['notebook']} cell={index} output={output['index']} source_sha256={source_hash} payload_sha256={output['payload_sha256']} artifact={artifact or '-'}")
            body.append(r"\phantomsection" + rf"\label{{out:lab08-cell-{index:04d}-{output['index']:02d}}}")
            if (index == 8 and output["index"] in {0, 2, 3, 4, 5, 6}) or (index in {10, 12} and output["index"] == 1):
                diagnostics.append((index, output["index"], exp))
                continue
            if artifact:
                body.append(rf"\lstinputlisting[style=terminalOutput]{{{tex_path(artifact)}}}")
            for figure in exp.get("figures", []):
                body.append(rf"\begin{{center}}\includegraphics[width=.82\linewidth]{{{tex_path(figure)}}}\end{{center}}")
        body.append(interpretation)
    body += [
        r"\subsection{Reading the router as an evaluated component}",
        r"Chat serialization and instruction tuning solve different problems. The chat template inserts model-specific boundary and role tokens around messages and ends with an assistant-generation prefix; instruction tuning teaches the model how to respond to those serialized instructions. Adding special tokens a second time can change the prompt, so the helper tokenizes the already-rendered template with \texttt{add\_special\_tokens=False}. It then returns only the continuation by slicing at the original prompt length. Greedy decoding (\texttt{do\_sample=False}) makes this run repeatable for fixed weights and input; sampling instead draws from a probability distribution and can produce different continuations.",
        r"The router uses \texttt{max\_new\_tokens=8}, a cap on newly generated text. \texttt{max\_length} would instead cap prompt plus continuation, making the available answer length depend on the prompt size. The task generation uses a 2,000-new-token budget because it must produce an artifact. The strict parser rejects unsupported output, which prevents an invalid response from silently selecting an arbitrary branch.",
        "The separate ChatGPT comparison requested in the notebook is not represented as a result because no independent ChatGPT generation was recorded. A fair comparison would use the same requirements, user request, output limits, and rubric, then compare route accuracy, requirement coverage, unsupported additions, and format validity over multiple cases.",
        r"\appendix",
        r"\section{Execution diagnostics}",
        "The selected outputs in this appendix preserve initialization progress and warnings that are not needed to understand the successful result. Their source cell and output index remain identified so the raw execution record can be matched to the notebook.",
    ]
    for index, output_index, exp in diagnostics:
        artifact = exp.get("presentation_artifact", "")
        if not artifact:
            continue
        body.append(rf"\subsection*{{Cell {index}, diagnostic output {output_index} (source: \hyperref[out:lab08-cell-{index:04d}-{output_index:02d}]{{notebook output}})}}")
        body.append(rf"\lstinputlisting[style=terminalOutput]{{{tex_path(artifact)}}}")
    CHAPTER.parent.mkdir(parents=True, exist_ok=True)
    CHAPTER.write_text("\n\n".join(body) + "\n", encoding="utf-8")
    entries = []
    for record in inventory["cells"]:
        i = record["cell_index"]
        exp_outputs = record.get("exported_outputs", [])
        entries.append({
            "key": record["key"], "source_sha256": record["source_sha256"],
            "exercise_chapter": "Threshold evaluation" if i in (1, 3, 5) else "A two-stage LLM router",
            "exercise_name": "Threshold evaluation with a receiver operating characteristic curve" if i in (1, 3, 5) else "A two-stage LLM router for software design tasks",
            "section": "Score construction and ROC analysis" if i in (1, 3, 5) else "Llama model setup and task routing",
            "source_artifact": record.get("exported_source"),
            "execution_evidence": "execution_count" if record.get("execution_count") is not None else "",
            "execution_note": "" if record.get("execution_count") is not None else "",
            "output_anchor": f"res:lab08-cell-{i:04d}" if record.get("output_substantive") else "",
            "output_disposition": "attached_and_interpreted" if record.get("output_substantive") else "state_change_or_no_display_explained",
            "output_types": [output["type"] for output in record.get("outputs", [])],
            "figures": [figure for item in exp_outputs for figure in item.get("figures", [])],
            "outputs": [{"index": output["index"], "source_sha256": record["source_sha256"],
                         "payload_sha256": output["payload_sha256"],
                         "presentation_artifact": exp_outputs[output["index"]].get("presentation_artifact", "")}
                        for output in record.get("outputs", [])],
            "artifacts": [],
        })
    COVERAGE.write_text(json.dumps({"schema_version": 1, "cells": entries}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
