#!/usr/bin/env python3
"""Generate Lab09's complete standalone chapter and coverage manifest."""
from __future__ import annotations
import hashlib, json, re, shutil
from pathlib import Path
import nbformat

LABS=Path(__file__).resolve().parents[3]
GUIDE=LABS/'study_guide'
NB_PATH=LABS/'lab09/text-09-code-generation.ipynb'
INV_PATH=GUIDE/'coverage/lab09.inventory.json'
CHAPTER=GUIDE/'chapters/09_code_generation.tex'
WRAPPER=GUIDE/'standalone/lab09/lab09_solution.tex'

N={
1:("We start with an executable reference for the grade requirement: exactly six finite real values, each from 18 through 30 or equal to 33 for laude; one minimum and one maximum are removed, and the input must remain unchanged. The function checks types and values before sorting, so malformed input cannot silently become a plausible average. A fresh Codex-authored baseline is stored with its provenance; it is not presented as a ChatGPT response.","The sample `[18, 25, 30, 33, 22, 28]` produces 26.25 after removing 18 and 33 and averaging the remaining four grades. The accompanying provenance dictionary identifies the generated source as a new Codex baseline from this session."),
3:("The next cell expresses the contract as black-box pytest tests. Parametrized cases cover ordinary and laude values, tied minima or maxima, fractional grades, invalid list lengths and bounds, NaN/infinity, booleans, and nonnumeric types. It also verifies that valid lists are not mutated. These tests establish the reference oracle before generated implementations are compared.","This cell defines the test cases but does not execute them; the following cell runs them against the reference function."),
5:("The notebook runs the tests in a fresh ipytest module and stops immediately if the reference fails. That guard prevents subsequent model comparisons from measuring a faulty oracle. The run also calls out a disagreement in one unchanged supplied test: its 1% tolerance accepts an expectation of 27.75 for a case whose exact trimmed average is 28.0.","All 22 notebook-authored reference tests pass. The supplied test is preserved rather than edited; a strict exact-value assertion checks the 28.0 result independently."),
7:("With a passing reference, this cell prepares the pinned local inference workflow. It chooses MPS when available, seeds generation, and keeps only one model resident at a time, explicitly clearing accelerator memory before switching. The requested Hugging Face model ID is `meta-llama/Llama-3.2-3B-Instruct`; despite the original notebook wording, it is Llama 3.2, not CodeLlama. The helper returns only generated continuation text, while `apply_chat_template` will serialize system and user messages for the model.","The clean execution selected MPS and loaded both checkpoint shards. The widget progress warning is environmental display noise; the weights loaded successfully. The notebook does not pin a repository commit, so the PDF records the model ID and runtime environment without inventing a revision."),
8:("Now the grade requirements are framed as a system instruction and a user task, then serialized with the model's official chat template and an assistant-generation prefix. Greedy decoding requests at most 768 new tokens. The code removes only an enclosing Markdown fence if one appears and stores the actual result and model ID for downstream test execution.","The recorded Llama completion is printed in full in the output block. The generation configuration also emits warnings because temperature and top-p are set while `do_sample=False`; those sampling controls are inert under greedy decoding. The generated function is tested next without rewriting or repairing it."),
10:("To evaluate generated code, this helper runs pytest in a temporary directory with a fresh import path, writes JUnit XML, and parses individual test outcomes instead of relying on fragile summary-text parsing. It saves stdout and the report under `execution/evaluations/`, then returns passed, failed, error, skipped, and functional-correctness values. This isolates each candidate from stale bytecode and earlier models' files.","The separately authored Codex baseline passes 14 of 14 supplied tests, yielding functional correctness 1.0. The tokenizers-after-fork messages come from subprocess evaluation and do not alter the tests."),
12:("The Llama source is now passed through that same evaluator against the same preserved grade tests. The cell stores the observed functional-correctness fraction for the later comparison; it does not infer success from the source looking plausible.","Llama passes 9 of 14 grade tests and fails 5, so the measured functional correctness is 9/14 = 0.6429. The nonzero pytest exit is retained as a real model result, not hidden by the later metrics."),
14:("This cell combines static and dynamic evaluation. Radon measures cyclomatic complexity, maintainability index, lines of code, and comments; pytest measures behavior on the shared suite. Each actual source is written to a provenance-named file before analysis. Only sources present in `my_codes` are compared, avoiding a fabricated GPT or ChatGPT result.","For grades, Codex records CC 9, MI 58.00, 14 LOC, and 0 comments, with 14/14 tests passing. Llama records CC 7, MI 89.72, 38 LOC, and 6 comments, with 9/14 passing. A higher maintainability score in this single run does not compensate for failures or establish an overall quality ranking."),
16:("The metrics are plotted on separate axes because they use different scales: complexity, maintainability, lines, comments, and test pass fraction are not directly commensurate quantities. The plot gives a compact view of the two observed grade implementations; it is a visualization of this run, not a statistical comparison across repeated samples.","The saved figure reproduces the cell's five metric panels. The coverage inventory also retains the notebook's original figure payload, and the rendered version is included at readable resolution."),
18:("The second exercise adds the explicitly requested Qwen comparison while keeping the original Llama result and Codex baseline. `select_engine` releases Llama before loading `Qwen/Qwen2.5-Coder-1.5B-Instruct`; the same task prompt, greedy decoding helper, and grading test suite are reused. The additional model is a supplementary local comparison and does not replace the prescribed Llama run.","Qwen passes 8/14 grade tests (0.5714). Static metrics are CC 7, MI 62.31, 14 LOC, and 0 comments; Llama is 9/14 and Codex is 14/14. The full generated Qwen code, warnings, JSON metrics, and recorded model provenance appear in the output. These scores describe this prompt, test set, checkpoints, and single run only."),
20:("The third exercise introduces two more requirements: a group railway fee and a track-dependent maximum time. This cell creates a fresh Codex implementation and focused black-box tests for each task, writes the source and test files, and validates the local baselines before generating any further model candidates. The fee rule gives a discount only when a group has at least two passengers and an adult; the bike rule has exact speed boundaries for track types A and B and a fixed multiplier for C.","The two Codex baselines pass their observed suites: 13/13 railway cases and 19/19 bike cases. The source strings and test files become the comparison state consumed by the final cell."),
21:("Finally, the workflow loops over Llama and Qwen sequentially and over both new tasks. Each candidate is generated from the matching task prompt, saved as the observed source, and evaluated with the same test and Radon pipeline. The loop prints candidate code and a JSON result object for every engine-task pair; it never loads both checkpoints together.","For railway, Llama passes 8/13 tests (0.6154); Qwen's generated source yields one collection/runtime error before any tests run, so its 0.0 metric is not equivalent to a tested 0% pass rate. For bike, Llama passes 11/19 (0.5789) and Qwen 17/19 (0.8947). The Codex baselines remain 13/13 and 19/19. The complete generated implementations and all recorded result fields follow the cell. This comparison demonstrates variation across tasks and tests; it does not establish general model capability."),
}


def latex_inline(text: str) -> str:
    def render(match):
        value=match.group(1).replace("\\", r"\textbackslash{}").replace("_", r"\_").replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
        return r"\texttt{"+value+"}"
    return re.sub(r"`([^`]+)`", render, text)


def clean_output(path: Path) -> str:
    text=path.read_text(errors='replace')
    text=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text)
    return text.replace('\r','\n').replace('█','#').rstrip()


def main():
    nb=nbformat.read(NB_PATH,as_version=4)
    inv=json.loads(INV_PATH.read_text())
    by={c['cell_index']:c for c in inv['cells']}
    parts=[r"\section[Grade generation]{Exercise 1: generating and evaluating the grade function}",r"\label{sec:lab09-grades}",
      "The first exercise turns a precise grade rule into an executable reference, checks it at boundaries, and measures two observed generated implementations against the same test suite. The process moves from specification and tests to inference, evaluation, static analysis, and a compact metric plot.",
      r"\begin{figure}[htbp]\centering\resizebox{\linewidth}{!}{\begin{tikzpicture}[>=Stealth,stage/.style={draw=steelBlue,fill=skyBlue,rounded corners,align=center,text width=3.0cm,minimum height=.85cm,font=\small\sffamily}]\node[stage](a){Grade requirement};\node[stage,right=7mm of a](b){Reference code\\and tests};\node[stage,right=7mm of b](c){Llama generation};\node[stage,right=7mm of c](d){pytest and\\Radon metrics};\node[stage,right=7mm of d](e){Metric figure};\draw[->,thick,steelBlue](a)--(b);\draw[->,thick,steelBlue](b)--(c);\draw[->,thick,steelBlue](c)--(d);\draw[->,thick,steelBlue](d)--(e);\end{tikzpicture}}\caption{The grade solution is evaluated against a fixed contract and test suite.}\end{figure}",
      r"\medskip\noindent The input is six grades and an explicit validity rule; the desired result is a trimmed mean and predictable exceptions. A useful comparison must therefore check both valid numerical results and rejection behavior, then interpret test outcomes alongside static metrics."]
    for i in [1,3,5,7,8,10,12,14,16,18,20,21]:
      if i==18:
        parts += [r"\clearpage",r"\section[Multiple agents]{Exercise 2: comparing additional code-generation agents}",r"\label{sec:lab09-agents}","The second exercise keeps the same grade requirement and test oracle while adding the public Qwen 2.5 Coder model. This isolates the comparison to the generated implementation and measured outcome for this task; no external ChatGPT response is claimed."]
      if i==20:
        parts += [r"\clearpage",r"\section[Additional functions]{Exercise 3: extending the comparison to railway and bike tasks}",r"\label{sec:lab09-additional}","The final exercise changes the specification to two different branching problems. A railway discount depends on group composition and size, while the bike task maps speed bands and track types to a maximum time. The same source-generation, test-execution, and static-analysis pipeline is reused so the comparison includes actual observed code and outcomes for each task.",
        r"\begin{figure}[htbp]\centering\resizebox{\linewidth}{!}{\begin{tikzpicture}[>=Stealth,stage/.style={draw=steelBlue,fill=skyBlue,rounded corners,align=center,text width=3.2cm,minimum height=.85cm,font=\small\sffamily}]\node[stage](a){Railway and bike\\requirements};\node[stage,right=9mm of a](b){Codex reference\\and focused tests};\node[stage,right=9mm of b](c){Llama and Qwen\\generation};\node[stage,right=9mm of c](d){Fresh pytest and\\Radon evaluation};\draw[->,thick,steelBlue](a)--(b);\draw[->,thick,steelBlue](b)--(c);\draw[->,thick,steelBlue](c)--(d);\end{tikzpicture}}\caption{The additional tasks reuse the same validated comparison pipeline.}\end{figure}"]
      cell=nb.cells[i]
      entry=by[i]; sha=hashlib.sha256(cell.source.encode()).hexdigest(); before,after=N[i]
      parts.append(r"\medskip\noindent "+latex_inline(before))
      parts.append(f"% coverage-cell: LABS/lab09/text-09-code-generation.ipynb cell={i} source_sha256={sha}")
      parts.append(r"\begin{lstlisting}[style=studycode]"+"\n"+cell.source.rstrip()+"\n"+r"\end{lstlisting}")
      outs=entry.get('exported_outputs',[])
      if outs:
        aggregate=f"study_guide/execution_artifacts/lab09/lab09-cell-{i:04d}-outputs.txt"
        parts.append(r"\label{out:lab09-cell-%04d}"%i)
        displays=[]
        for o in outs:
          raw=o.get('raw_payload_artifacts',[])
          if raw:
            payload=clean_output(LABS/raw[0]['path'])
          else:
            payload=clean_output(LABS/o['presentation_artifact'])
          displays.append(f"--- notebook output {o['index']} ---\n"+payload)
          parts.append(f"% coverage-output: LABS/lab09/text-09-code-generation.ipynb cell={i} output={o['index']} source_sha256={sha} payload_sha256={o['payload_sha256']} artifact={aggregate}")
        agg_path=LABS/aggregate
        agg_path.write_text("\n\n".join(displays)+"\n")
        agg_hash=hashlib.sha256(agg_path.read_bytes()).hexdigest()
        for o in entry.get('exported_outputs',[]):
          o['presentation_artifact']=aggregate
          o['presentation_sha256']=agg_hash
        parts.append(r"\lstinputlisting[style=terminalOutput]{../../execution_artifacts/lab09/"+Path(aggregate).name+"}")
        if i==16:
          fig="../../figures/lab09/grade_code_metrics.png"
          destination=GUIDE/"figures/lab09/grade_code_metrics.png"
          destination.parent.mkdir(parents=True,exist_ok=True)
          shutil.copy2(LABS/"study_guide/execution_artifacts/lab09/text-09-code-generation_cell_0016_ebaf2737dae2_output_0.png",destination)
          parts.append("% exported notebook image: text-09-code-generation_cell_0016_ebaf2737dae2_output_0.png")
          parts.append(r"\begin{figure}[htbp]\centering\includegraphics[width=0.93\linewidth]{"+fig+r"}\caption{Recorded grade-code comparison: complexity, maintainability, size, comments, and functional correctness.}\end{figure}")
      parts.append(latex_inline(after))
    parts += [r"\subsection{What these comparisons do and do not show}","The reference and fresh Codex baseline pass the observed grade, railway, and bike tests. Llama and Qwen results vary by task, and one Qwen railway run raises a test-collection error rather than producing a measured set of passes and failures. Static metrics such as lines of code and cyclomatic complexity describe the source's structure; they do not guarantee that it follows the requirements. Each pass fraction is tied to a specific finite suite, prompt, checkpoint ID, and local run.","The Lab 09 lecture recording was not provided for this notebook-only pass. This solution makes no lecture-derived claims; its explanations and results come from the assignment notebook, local model execution, and saved test artifacts."]
    CHAPTER.parent.mkdir(parents=True,exist_ok=True)
    CHAPTER.write_text("\n\n".join(parts)+"\n")
    INV_PATH.write_text(json.dumps(inv,indent=2)+"\n")
    wrapper=r"""\documentclass[10pt,a4paper,oneside]{article}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage{newpxtext}\usepackage[scaled=0.88]{sourcecodepro}\usepackage{microtype}\usepackage[a4paper,top=19mm,bottom=19mm,left=20mm,right=20mm,headheight=16pt,footskip=10mm]{geometry}\usepackage[dvipsnames,table]{xcolor}\usepackage{amssymb,graphicx,booktabs,tabularx,array,enumitem,listings,tikz,titlesec,fancyhdr,hyperref}\usetikzlibrary{arrows.meta,positioning}\definecolor{politoNavy}{RGB}{0,45,98}\definecolor{steelBlue}{RGB}{35,100,160}\definecolor{skyBlue}{RGB}{230,240,250}\definecolor{bodyGray}{RGB}{80,85,90}\definecolor{codeBg}{RGB}{248,249,251}\definecolor{codeFrame}{RGB}{220,225,230}\hypersetup{colorlinks=true,linkcolor=politoNavy,urlcolor=steelBlue,pdftitle={Laboratory 09 solution: LLM code generation}}\titleformat{\section}{\normalfont\sffamily\Large\bfseries\color{politoNavy}}{\thesection}{.8em}{}\titleformat{\subsection}{\normalfont\sffamily\large\bfseries\color{steelBlue}}{\thesubsection}{.8em}{}\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small\sffamily\color{bodyGray}\nouppercase{\rightmark}}\fancyhead[R]{\small\sffamily\bfseries\thepage}\renewcommand{\headrulewidth}{.4pt}\lstdefinestyle{studycode}{language=Python,basicstyle=\fontsize{7.2}{8.6}\ttfamily,keywordstyle=\bfseries\color{politoNavy},commentstyle=\itshape\color{bodyGray},stringstyle=\color{ForestGreen},numbers=left,numberstyle=\tiny\color{bodyGray},numbersep=5pt,tabsize=4,showstringspaces=false,breaklines=true,columns=fullflexible,keepspaces=true,frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg}}\lstdefinestyle{terminalOutput}{basicstyle=\fontsize{6.8}{8.1}\ttfamily,breaklines=true,columns=fullflexible,keepspaces=true,frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg}}\newcommand{\labSolutionTitle}{Laboratory 09: LLM-Based Code Generation and Evaluation}\newcommand{\labSolutionSubtitle}{Complete notebook-aligned solution}\begin{document}\input{../../frontmatter/solution_titlepage}\tableofcontents\clearpage\input{../../chapters/09_code_generation.tex}\end{document}
"""
    WRAPPER.write_text(wrapper)

if __name__=='__main__': main()
