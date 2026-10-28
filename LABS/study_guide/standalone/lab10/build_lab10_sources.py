#!/usr/bin/env python3
"""Build a notebook-aligned solution with hidden cell/output coverage markers."""
import hashlib, json, re
from pathlib import Path
import nbformat
LABS=Path(__file__).resolve().parents[3]; GUIDE=LABS/'study_guide'
NB_PATH=LABS/'lab10/text-10-test-generation.ipynb'
CHAPTER=GUIDE/'chapters/10_test_generation.tex'; WRAPPER=GUIDE/'standalone/lab10/lab10_solution.tex'
INV=GUIDE/'coverage/lab10.inventory.json'
N={
1:("We start from the known reference implementation of \\texttt{racer\\_disqualified}. Its contract combines strict thresholds for event times and penalties with type and shape validation. The source is embedded as a string so later cells can restore it after each mutation. This gives the experiment a stable oracle: tests are judged against the stated rules rather than against a candidate test author's assumptions.","This setup creates the reference source used by the isolated test runner and mutation generator. It prints no output; subsequent cells write it into a temporary test environment."),
3:("The first suite is designed around the function's decision boundaries: values below, equal to, and above each limit, plus malformed argument shapes and types. The test runner launches pytest in an isolated directory and parses JUnit XML, so outcomes remain structured even as the code file changes.","All 21 manually authored tests pass on the reference. This establishes a consistent baseline, but passing tests alone do not show whether every important statement or behavior is covered."),
5:("Pass rate is computed from JUnit results: it measures whether examples agree with known-correct code. This is the reverse direction from functional correctness, where candidate code is checked against trusted tests. Structured outcomes also identify which test failed instead of relying on pytest's display text.","The manual suite reports 21 passed, zero failed or errored, and a 100% pass rate. This validates the examples against the reference but does not establish sensitivity to defects."),
7:("The next measurement runs the suite under statement coverage. The helper reads the coverage report for \\texttt{function\\_01.py}, separating executed statements from unrelated test-runner code. Coverage can show that a line ran, but not whether both outcomes of a condition were checked.","The manual tests execute all 24 statements, for 100% statement coverage. This is useful but not sufficient evidence of strong tests: execution does not guarantee that assertions would detect an incorrect result."),
9:("Mutation testing supplies that stronger probe by introducing five plausible one-expression defects. Each mutation is compiled before use, and only one condition or return value changes at a time. The following cell installs them individually and checks whether the suite distinguishes each altered implementation from the reference.","Five single-change mutants are ready. No mutant has been evaluated yet; this cell only creates the variants."),
11:("For each mutation, the runner removes stale bytecode, installs the changed function, and reruns the same suite. A mutant is killed only if a test that passed on the reference now fails; an already failing test cannot count as evidence. A `finally` block restores the known implementation even if an evaluation raises an error.","The manual suite kills all five mutants, giving a 100% mutation score for this finite mutation set. The score strengthens the coverage result while remaining limited to these five chosen defects."),
13:("The final comparison repeats these measurements for the saved GPT, Copilot, and Qwen test examples and for a newly authored Codex suite. Existing examples are evaluated as supplied; their historical model provenance is not independently verified. The Copilot execution copy removes only an unconditional nested pytest launch, leaving test functions unchanged. This notebook performs no external model generation.","The results preserve an important failure: GPT expects `[120, 140, 160]` to be disqualified against winners `[80, 100, 110]`, although the strict 1.5× limits are `[120, 150, 165]` and none is exceeded. GPT passes 11/12 tests, covers 96% of statements, and kills 2/5 mutants. Copilot passes 3/3 and kills 5/5; Qwen passes 20/20 and kills 5/5; the fresh Codex suite passes 27/27 and kills 5/5. Statement coverage differs from branch coverage, and mutation kills count only newly failing tests. These observations compare the particular saved suites, not the general capabilities of their named systems."),
}

def main():
 nb=nbformat.read(NB_PATH,as_version=4); inv=json.loads(INV.read_text()); by={c['cell_index']:c for c in inv['cells']}
 p=[r"\section[LLM test generation]{Exercise: evaluating test suites generated with LLMs}",r"\label{sec:lab10-test-generation}","This exercise starts with correct code and evaluates whether test suites detect violations of its rules. A hand-written baseline leads to pass-rate and statement-coverage measures, then to mutation testing and a comparison of saved generated suites.",r"\begin{figure}[htbp]\centering\begin{tikzpicture}[>=Stealth,stage/.style={draw=steelBlue,fill=skyBlue,rounded corners,align=center,text width=3cm,minimum height=.9cm,font=\small\sffamily}]\node[stage](a){Reference function\\and requirements};\node[stage,right=8mm of a](b){Manual and\\saved test suites};\node[stage,right=8mm of b](c){Pass rate and\\statement coverage};\node[stage,right=8mm of c](d){Single-change\\mutations};\draw[->,thick,steelBlue](a)--(b);\draw[->,thick,steelBlue](b)--(c);\draw[->,thick,steelBlue](c)--(d);\end{tikzpicture}\caption{Each suite is compared with a fixed reference and controlled defects.}\end{figure}",r"\medskip\noindent Pass rate asks whether examples agree with the reference; coverage asks which statements ran; mutation testing asks whether tests reject selected faulty variants. Together they provide distinct evidence about a suite's quality."]
 for cell_index,c in enumerate(nb.cells):
  if c.cell_type!='code' or not c.source.strip(): continue
  i=cell_index; entry=by[i]; sha=hashlib.sha256(c.source.encode()).hexdigest(); lead,interp=N[i]
  p += [r"\medskip\noindent "+lead,f"% coverage-cell: LABS/lab10/text-10-test-generation.ipynb cell={i} source_sha256={sha}",r"\begin{lstlisting}[style=studycode]"+"\n"+c.source.rstrip()+"\n"+r"\end{lstlisting}"]
  outs=entry.get('exported_outputs',[])
  if outs:
   p.append(r'\label{out:lab10-cell-%04d}' % i)
   displays=[]
   for o in outs:
    art='study_guide/execution_artifacts/lab10/lab10-cell-%04d-outputs.txt' % i; oi=o['index']
    p.append(f"% coverage-output: LABS/lab10/text-10-test-generation.ipynb cell={i} output={oi} source_sha256={sha} payload_sha256={o['payload_sha256']} artifact={art}")
    raw_path=o.get('raw_payload_artifacts',[{}])[0].get('path',art)
    text=(LABS/raw_path).read_text(errors='replace')
    text=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', text)
    displays.append(f"--- notebook output {oi} ---\n"+text.rstrip())
   out=GUIDE/'execution_artifacts/lab10'/f'lab10-cell-{i:04d}-outputs.txt'; out.write_text("\n\n".join(displays)+"\n")
   import hashlib as _hashlib
   aggregate_rel='study_guide/execution_artifacts/lab10/'+out.name
   aggregate_sha=_hashlib.sha256(out.read_bytes()).hexdigest()
   for exported_output in entry.get('exported_outputs', []):
    exported_output['presentation_artifact']=aggregate_rel
    exported_output['presentation_sha256']=aggregate_sha
   INV.write_text(json.dumps(inv, indent=2)+'\n')
   p.append(r"\lstinputlisting[style=terminalOutput]{../../execution_artifacts/lab10/"+out.name+"}")
  p.append(interp)
 p += [r"\subsection{Interpreting the comparison}","The strict inequalities make the threshold boundaries central: equality is accepted, and only a value above the limit disqualifies. The GPT example's failed expectation is therefore retained as an observed test defect. The results support only a narrow conclusion about these suites and five selected mutants, not a general ranking of model providers. No Lab 10 lecture recording was supplied, so the explanations here follow the notebook and execution evidence only."]
 CHAPTER.parent.mkdir(parents=True,exist_ok=True); CHAPTER.write_text("\n\n".join(p)+"\n")
 WRAPPER.write_text(r"""\documentclass[10pt,a4paper,oneside]{article}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage{newpxtext}\usepackage[scaled=0.88]{sourcecodepro}\usepackage{microtype}\usepackage[a4paper,top=19mm,bottom=19mm,left=20mm,right=20mm,headheight=16pt,footskip=10mm]{geometry}\usepackage[dvipsnames,table]{xcolor}\usepackage{amssymb,graphicx,booktabs,tabularx,array,enumitem,listings,tikz,titlesec,fancyhdr,hyperref}\usetikzlibrary{arrows.meta,positioning}\definecolor{politoNavy}{RGB}{0,45,98}\definecolor{steelBlue}{RGB}{35,100,160}\definecolor{skyBlue}{RGB}{230,240,250}\definecolor{bodyGray}{RGB}{80,85,90}\definecolor{codeBg}{RGB}{248,249,251}\definecolor{codeFrame}{RGB}{220,225,230}\hypersetup{colorlinks=true,linkcolor=politoNavy,urlcolor=steelBlue,pdftitle={Laboratory 10 solution: test generation}}\titleformat{\section}{\normalfont\sffamily\Large\bfseries\color{politoNavy}}{\thesection}{.8em}{}\titleformat{\subsection}{\normalfont\sffamily\large\bfseries\color{steelBlue}}{\thesubsection}{.8em}{}\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small\sffamily\color{bodyGray}\nouppercase{\rightmark}}\fancyhead[R]{\small\sffamily\bfseries\thepage}\renewcommand{\headrulewidth}{.4pt}\lstdefinestyle{studycode}{language=Python,basicstyle=\fontsize{7.4}{8.8}\ttfamily,keywordstyle=\bfseries\color{politoNavy},commentstyle=\itshape\color{bodyGray},stringstyle=\color{ForestGreen},numbers=left,numberstyle=\tiny\color{bodyGray},numbersep=6pt,tabsize=4,showstringspaces=false,breaklines=true,columns=fullflexible,keepspaces=true,frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg}}\lstdefinestyle{terminalOutput}{basicstyle=\fontsize{7.2}{8.5}\ttfamily,breaklines=true,columns=fullflexible,keepspaces=true,frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg}}\newcommand{\labSolutionTitle}{Laboratory 10: LLM-Based Test Generation}\newcommand{\labSolutionSubtitle}{Complete notebook-aligned solution}\begin{document}\input{../../frontmatter/solution_titlepage}\tableofcontents\clearpage\input{../../chapters/10_test_generation.tex}\end{document}
""")
if __name__=='__main__': main()
