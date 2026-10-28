"""Build the Lab06 standalone article from finalized notebook code/output evidence."""
import json
import re
from pathlib import Path

LABS = Path(__file__).resolve().parents[2]
GUIDE = LABS / "study_guide"
NOTEBOOK_PATH = LABS / "lab06" / "text-06-prompt-engineering-rag.ipynb"
INVENTORY = GUIDE / "coverage" / "lab06.inventory.json"
CHAPTER = GUIDE / "chapters" / "06_lab06_prompt_engineering_rag.tex"

# prose is deliberately written as transitions: no per-cell heading/template paragraphs.
OPENINGS = {
    1: "The first exercise builds a local prompt-engineering workflow around Llama 3.2 3B Instruct. It begins by loading one pinned checkpoint and defining a reusable decoder, then uses an AC Milan article as a common input for plain prompting, role prompts, prompt chaining, and structured output. The diagram shows how each prompt experiment consumes the model and article state established here.",
    3: "Before testing prompts, the notebook obtains a short, familiar article from a local PDF. This makes the content inspectable and gives later summaries a fixed source, so changes in the answer can be related to the prompt rather than a changing document.",
    5: "The same article is now summarized without a role-based chat wrapper. Reading every page avoids silently omitting content, while a specific instruction asks for the topic, problem, method, findings, and limitations. Because this source is an encyclopedia-style football article rather than research, the request also tests whether the model distinguishes absent information from evidence.",
    7: "The next pass packages the instruction as a system message and the article as a user message. `apply_chat_template` serializes these roles into the checkpoint's expected control-token format and appends an assistant-generation prefix. The subsequent answer can be compared with the plain prompt to see what role separation changes, while checking whether it introduces unsupported detail.",
    9: "A more specific persona asks for a concise scientific brief and explicitly separates evidence from speculation. This is still prompt engineering, not a model update: the same weights are used, and only the system-message wording changes.",
    11: "Prompt chaining feeds one generated description into a second question. The first call compresses the article to a sentence; the second call receives that description alongside the full article and asks what problem the work addresses. In this case the article is not a scientific study, so the chain also reveals how a model can turn an ill-fitting requested frame into an invented research narrative.",
    13: "A formatting instruction requests a two-field JSON object with a short explanation. The code then parses the actual text and checks its exact key set, string values, and word limit. Generating JSON is not the same as verifying JSON: this guard makes invalid schema output visible instead of treating it as structured data.",
    15: "Two role-based examples demonstrate entity extraction before the article is supplied. The notebook runs both this few-shot prompt and a zero-shot control, then parses each response and verifies that every element contains the required string fields. The comparison shows whether examples improve the structure in this particular run; it cannot establish general reliability.",
    17: "The second exercise shifts from one prompt document to a ten-paper retrieval corpus. All pages of each numbered PDF are extracted into a dictionary keyed by document ID. The displayed snippets and character counts help verify that the intended files were read before retrieval is built on top of them.",
    19: "Each extracted paper contributes an abstract, located by its heading and cut off before the introduction or keywords. The notebook encodes these ten abstracts with the pretrained uncased BERT encoder and keeps the first-token hidden vector as a compact document representation. The result has shape `[10, 768]`: ten papers by 768 hidden features. This is an inexpensive baseline embedding, not a task-trained retrieval model.",
    21: "The query follows the same BERT path and is compared with the document vectors using cosine similarity. A stable descending sort returns the three closest abstracts, after which the corresponding full paper text is retrieved. The score ranking and a short text prefix make both the embedding decision and the context handed to generation inspectable.",
    23: "The final computation forms a grounded answer prompt from the retrieved papers and compares it with a direct answer that receives only the question. The system message asks for source filenames, restricts answers to the supplied evidence, and treats document text as data. To fit the local MPS memory budget after the first full-context attempt exhausted memory, the finalized run keeps the start and question-bearing tail of a 1,024-token prompt, generates at most 96 tokens with one beam, and clears the MPS workspace between independent responses. This makes the comparison executable on the available machine, but aggressive context shortening and weak abstract retrieval constrain what the result can demonstrate.",
}

INTERPRETATIONS = {
    1: "The output identifies MPS as the selected backend and prints two independent answers to the capital-of-France prompt. The direct helper returns only the continuation, whereas the text-generation pipeline returns the prompt together with its continuation. The warnings about sampling-only `temperature`/`top_p` settings are inert under greedy decoding, and the backend warning records the pipeline's device configuration; neither warning changes the observed answer. This cell establishes the model, tokenizer, reusable generation function, and initial demonstration used by every later prompt.",
    3: "The printed passage is the text actually extracted from the first page of `example2.pdf`. Its AC Milan content becomes the shared article input for the next experiments, making it possible to inspect whether later answers remain faithful to a known source.",
    5: "The model returns a topical summary, but it still fills requested research categories with confident prose despite the article lacking a study design. The answer also misspells the former president's surname. The result is useful as a baseline and demonstrates why a requested output outline does not ensure that each requested category applies.",
    7: "The role-structured response is more visibly organized, yet it falsely changes the founding year from 1899 to 1889 and invents limitations and analysis that the article does not state. Role serialization can make instructions clearer; it does not guarantee factual fidelity.",
    9: "The persona produces a more concise five-part brief, but it still frames descriptive history as research and asserts an unsupported financial position. The comparison isolates the effect of wording while also showing that a more scholarly tone is not evidence of greater accuracy.",
    11: "The first answer describes the source topic; the second then treats that description as a scientific problem statement and invents a study/approach. The dependency between answers is explicit, but chaining can amplify an earlier framing error instead of correcting it. The supplied source should remain the authority.",
    13: "The generated text uses keys `.topic` and `.explanation`, not the required `topic` and `explanation`; the schema assertion therefore fails. The code reports this as an assertion failure rather than accepting syntactically valid but incompatible data. This distinguishes JSON syntax from schema correctness.",
    15: "The few-shot generation is malformed JSON and departs from the example schema by using `description`, empty or null values, arrays in fields, and an invalid nested object. The zero-shot answer is wrapped in Markdown fences and uses `_explanation`/`_explanations`, so it too fails parsing. The validators correctly reject both. Two failed samples are evidence about these generated strings, not a statistical comparison of prompting strategies.",
    17: "Ten nonempty documents are extracted, with titles and first-page snippets visible in the result. The character counts verify the scale of each retrieved source and identify the ten-paper corpus used next. Extraction success confirms text availability, not that all layouts, equations, tables, or references were semantically parsed correctly.",
    19: "The printed abstracts provide the actual text encoded for retrieval, and the final assertion confirms exactly ten 768-dimensional vectors. CLS pooling is simple and reproducible, but general-purpose BERT's first-token representation is not guaranteed to rank systems papers by their answer relevance. This limitation matters when reading the next top-three result.",
    21: "The query vector is `[1, 768]`, and cosine similarity ranks papers 9, 2, and 0 at approximately 0.8042, 0.7916, and 0.7647. The combined retrieved text contains 128,145 characters; only its first 1,000 characters are printed. The target question names DynamoLLM, which is described in paper 5, but paper 5 is absent from the retrieved set. Thus the ranking is a concrete baseline result and a retrieval failure for this query, not proof that the answer context is relevant.",
    23: "For the DynamoLLM question, cosine retrieval again returns papers 9, 2, and 0, missing the likely target paper 5. The RAG answer then cites a nonexistent paper 8 and refers to paper 40, while the direct answer speculates about dynamically allocating resources without evidence. For the workload-aware scheduling question, retrieval returns papers 2, 9, and 0; the RAG answer mentions paper 2 but also invents a source marker `[40]`, and the direct answer asserts general background without citations. The printed strings are visibly malformed and unsupported in places. RAG only helps when retrieval selects relevant evidence and the model uses it faithfully; these two comparisons do not show that either condition held. The earlier long-context, three-beam attempt failed during MPS attention and remains documented in the appendix.",
}


MAIN_OUTPUTS = {(1, 1), (1, 7), (1, 10), (1, 12), (23, 0), (23, 3), (23, 5)} | {(index, output) for index, count in {3: 1, 5: 1, 7: 1, 9: 1, 11: 2, 13: 1, 15: 2, 17: 1, 19: 2, 21: 1}.items() for output in range(count)}

def render_prose(s):
    def inline(match):
        value = match.group(1).replace("\\_", "_").replace("_", r"\_\allowbreak{}")
        return r"\texttt{" + value + "}"
    return re.sub(r"`([^`]+)`", inline, s)

def esc_title(s):
    return s.replace('&', r'\&')


def main():
    nb = json.loads(NOTEBOOK_PATH.read_text())
    inv = json.loads(INVENTORY.read_text())
    by_index = {x['cell_index']: x for x in inv['cells']}
    chunks = []
    chunks.append(r"\section[Prompt engineering with Llama]{Exercise 1: Prompt engineering with Llama 3.2}" + "\n")
    chunks.append(r"\label{sec:lab06-prompt}" + "\n\n" + "This exercise holds a pinned instruction-tuned model and a local article constant while changing how the request is framed. It moves from direct completion through role prompts, a chained prompt, and machine-checked structured responses." + "\n\n")
    chunks.append(r"\begin{figure}[htbp]\centering\resizebox{\linewidth}{!}{%" + "\n")
    chunks.append(r"\begin{tikzpicture}[node distance=1cm,>=Stealth,stage/.style={draw=steelBlue,fill=skyBlue,rounded corners=2pt,align=center,text width=3.4cm,minimum height=.85cm,font=\small\sffamily}]" + "\n")
    nodes=[("a","Pinned Llama\ncheckpoint"),("b","Article from\nexample2.pdf"),("c","Plain and role\nprompts"),("d","Prompt chain and\nJSON schemas")]
    for idx,(key,label) in enumerate(nodes): chunks.append(rf"\node[stage] ({key}) at ({idx*4.1}cm,0) {{{label}}};"+"\n")
    for a,b in zip("abcd","bcd"): chunks.append(rf"\draw[->,thick,steelBlue] ({a}) -- ({b});"+"\n")
    chunks.append(r"\end{tikzpicture}}\caption{The first exercise changes the prompt while holding the model and article fixed.}\end{figure}"+"\n\n")
    for idx in [1,3,5,7,9,11,13,15]:
        chunks.append(r"\medskip\noindent "+render_prose(OPENINGS[idx])+"\n\n")
        rec=by_index[idx]
        sha=rec['source_sha256']
        chunks.append(rf"\label{{res:lab06-cell-{idx+1:04d}}}"+"\n")
        chunks.append(rf"% coverage-cell: LABS/lab06/text-06-prompt-engineering-rag.ipynb cell={idx} source_sha256={sha}"+"\n")
        code=''.join(nb['cells'][idx]['source']).rstrip('\n')
        chunks.append("\\begin{lstlisting}[style=studycode]\n"+code+"\n\\end{lstlisting}\n\\par\\smallskip\n")
        for out in rec['exported_outputs']:
            oi=out['index']; art=out.get('presentation_artifact', '')
            chunks.append(rf"% coverage-output: LABS/lab06/text-06-prompt-engineering-rag.ipynb cell={idx} output={oi} source_sha256={sha} payload_sha256={out['payload_sha256']} artifact={art or '-'}"+"\n")
            if art and (idx, oi) in MAIN_OUTPUTS:
                chunks.append(rf"\label{{out:lab06-cell-{idx+1:04d}-{oi:02d}}}"+"\n")
                chunks.append(rf"\lstinputlisting[style=terminalOutput]{{../../{art.removeprefix('study_guide/')}}}"+"\n")
            elif art:
                pass
        if idx in (1, 23):
            chunks.append(r"\textit{Model-loading, progress, and generation warnings are collected in Appendix~\ref{app:lab06-diagnostics}.}\par"+"\n")
        chunks.append(render_prose(INTERPRETATIONS[idx])+"\n\n")
    chunks.append(r"\clearpage\section[RAG retrieval and grounding]{Exercise 2: Retrieval-augmented generation}"+"\n")
    chunks.append(r"\label{sec:lab06-rag}"+"\n\n"+"This exercise retrieves evidence from a ten-paper corpus and asks an instruction-tuned model to answer with and without that evidence. It starts with PDF text, builds abstract embeddings, ranks full papers, and compares the resulting responses."+"\n\n")
    chunks.append(r"\begin{figure}[htbp]\centering\resizebox{\linewidth}{!}{%"+"\n")
    chunks.append(r"\begin{tikzpicture}[node distance=1cm,>=Stealth,stage/.style={draw=steelBlue,fill=skyBlue,rounded corners=2pt,align=center,text width=3cm,minimum height=.85cm,font=\small\sffamily}]"+"\n")
    nodes=[("a","Ten research\nPDFs"),("b","Extracted\nabstracts"),("c","BERT CLS\nembeddings"),("d","Cosine top-3\nretrieval"),("e","Short-context\nLlama answer")]
    for idx,(key,label) in enumerate(nodes): chunks.append(rf"\node[stage] ({key}) at ({idx*3.6}cm,0) {{{label}}};"+"\n")
    for a,b in zip("abcde","bcde"): chunks.append(rf"\draw[->,thick,steelBlue] ({a}) -- ({b});"+"\n")
    chunks.append(r"\end{tikzpicture}}\caption{Abstract embeddings select full-text documents that are passed into a bounded generation prompt.}\end{figure}"+"\n\n")
    for idx in [17,19,21,23]:
        chunks.append(r"\medskip\noindent "+render_prose(OPENINGS[idx])+"\n\n")
        rec=by_index[idx]; sha=rec['source_sha256']
        chunks.append(rf"\label{{res:lab06-cell-{idx+1:04d}}}"+"\n")
        chunks.append(rf"% coverage-cell: LABS/lab06/text-06-prompt-engineering-rag.ipynb cell={idx} source_sha256={sha}"+"\n")
        code=''.join(nb['cells'][idx]['source']).rstrip('\n')
        chunks.append("\\begin{lstlisting}[style=studycode]\n"+code+"\n\\end{lstlisting}\n\\par\\smallskip\n")
        for out in rec['exported_outputs']:
            oi=out['index']; art=out.get('presentation_artifact', '')
            chunks.append(rf"% coverage-output: LABS/lab06/text-06-prompt-engineering-rag.ipynb cell={idx} output={oi} source_sha256={sha} payload_sha256={out['payload_sha256']} artifact={art or '-'}"+"\n")
            if art and (idx, oi) in MAIN_OUTPUTS:
                chunks.append(rf"\label{{out:lab06-cell-{idx+1:04d}-{oi:02d}}}"+"\n")
                chunks.append(rf"\lstinputlisting[style=terminalOutput]{{../../{art.removeprefix('study_guide/')}}}"+"\n")
            elif art:
                pass
        if idx in (1, 23):
            chunks.append(r"\textit{Model-loading, progress, and generation warnings are collected in Appendix~\ref{app:lab06-diagnostics}.}\par"+"\n")
        chunks.append(render_prose(INTERPRETATIONS[idx])+"\n\n")
    chunks.append(r"\clearpage\appendix\section[Execution and transcript notes]{Execution, limitations, and deferred lecture review}\label{app:lab06-diagnostics}"+"\n")
    chunks.append("The matching Lab06 lecture recording was not present in the available Whisper application or course media when this solution was prepared. The professor is expected to provide it later, so this document makes no lecture-derived claims. The two exercises and their explanations are based on the supplied notebook assignments, finalized code, and saved paper PDFs.\n\n")
    chunks.append("The first full authenticated execution completed the prompt-generation and retrieval cells, but the final 4,096-token, three-beam RAG call exceeded the available MPS allocation. Its preserved trace is included below as a diagnostic; it is not a successful exercise result. The finalized retry uses a 1,024-token context budget, greedy one-beam decoding, a 96-token continuation cap, and explicit MPS cache cleanup.\n\n")
    chunks.append(r"The earlier attempt used up to 4,096 prompt tokens, three beams, and 300 continuation tokens. It failed in MPS scaled dot-product attention after consuming most of the device allocation. The full saved traceback is reproduced as a separate diagnostic artifact; it is not a generated answer."+"\n\n")
    chunks.append(r"\lstinputlisting[style=terminalOutput]{../../../lab06/execution/cell23-mps-oom-diagnostic.txt}"+"\n")
    chunks.append(r"\subsection*{Model-loading and generation warnings}"+"\n")
    chunks.append(r"Warnings and progress output are retained verbatim below for audit. In particular, Transformers reported generation-config values \texttt{temperature} and \texttt{top\_p} that are ignored when \texttt{do\_sample=False}; inference therefore used deterministic beam search or greedy decoding according to the listed beam count."+"\n")
    for index in [1,23]:
        rec=by_index[index]
        for out in rec['exported_outputs']:
            if out.get('presentation_artifact') and (index, out['index']) not in MAIN_OUTPUTS:
                art=out['presentation_artifact'].removeprefix('study_guide/')
                chunks.append(rf"\lstinputlisting[style=diagnosticOutput]{{../../{art}}}"+"\n")
    CHAPTER.parent.mkdir(parents=True, exist_ok=True)
    CHAPTER.write_text(''.join(chunks))

if __name__=='__main__': main()
