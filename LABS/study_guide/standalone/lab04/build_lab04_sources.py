#!/usr/bin/env python3
"""Build the editable Laboratory 04 article and coverage markers from notebook sources."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # LABS
GUIDE = ROOT / "study_guide"
CHAPTER = GUIDE / "chapters" / "04_lab04_complete.tex"
WRAPPER = GUIDE / "standalone" / "lab04" / "lab04_solution.tex"
INVENTORY = GUIDE / "coverage" / "lab04.inventory.json"
NOTEBOOKS = {
    "lab04/text-01-clm.ipynb": ROOT / "lab04" / "text-01-clm.ipynb",
    "lab04/text-02-llms.ipynb": ROOT / "lab04" / "text-02-llms.ipynb",
}

# Each entry explains where the cell sits in the pipeline and what its result
# means. The complete source is inserted directly from the finalized notebook.
NARRATIVE = {
("text-01-clm.ipynb",2):(
r"The notebook begins by importing the causal-language-model trainer and dataset loader, fixing the random seed, and selecting an available accelerator. This state is shared by the data preparation, model training, and the later padding experiments. The printed backend identifies the device on which the saved run was made.",
r"The output reports the MPS backend. This confirms that the Apple GPU path was selected for the original medical adaptation and informs how its runtime should be interpreted."
),
("text-01-clm.ipynb",5):(
r"This cell obtains the PubMed abstract collection, shuffles it with seed 42, and selects disjoint slices: indices 0--999 for training and 1,000--1,499 for evaluation. Repeating the same seeded shuffle makes the boundary reproducible. Keeping the evaluation slice separate lets the Trainer report held-out loss during fine-tuning.",
r"No output is displayed. The cell creates the 1,000-example training set and 500-example evaluation set consumed by the tokenizer and Trainer."
),
("text-01-clm.ipynb",7):(
r"This inspection checks the first training record before preprocessing. It makes the actual input field and the medical-abstract content visible, so the following tokenizer can be applied to the expected text column.",
r"The printed dictionary contains an abstract about segmentation of abdominal images and class imbalance. It confirms that the dataset supplies the \texttt{abstract} field used in the next computation."
),
("text-01-clm.ipynb",10):(
r"This cell turns each abstract into GPT-2 token IDs. The EOS token is reused as the tokenizer's padding ID because GPT-2 has no dedicated pad token. Truncation and fixed padding produce 1,024 positions per example; the attention mask distinguishes real tokens from positions filled with that reused ID. Mapping is batched for efficiency, and the original text columns are removed after tokenization.",
r"No output is displayed. The two mapped datasets now contain aligned \texttt{input\_ids} and \texttt{attention\_mask} arrays, ready for label construction."
),
("text-01-clm.ipynb",12):(
r"For causal language modeling, the target token sequence begins as a copy of the input IDs. Positions with attention mask zero are changed to \texttt{-100}, the ignore index used by the cross-entropy loss. GPT-2 shifts labels internally: the logit at position $t$ is compared with the target token at position $t+1$. For a batch of $B$ rows and length $T=1024$, the model emits logits with shape $B\times T\times V$ and labels with shape $B\times T$, where $V$ is vocabulary size. Causal attention blocks access to future positions; the attention mask marks padding, while ignored labels exclude padding from loss. These masks solve different problems.",
r"No output is displayed. The training and evaluation datasets now carry labels that supervise next-token prediction only at attended positions. Because EOS is both the padding ID and a genuine token, masking by token identity would wrongly discard real EOS targets; masking by attention state preserves them."
),
("text-01-clm.ipynb",15):(
r"This is the original GPT-2 fine-tuning cell. It sets one epoch, one-example microbatches, six-step gradient accumulation, seeded shuffling, evaluation every ten updates, and training-loss logging every one hundred updates. The effective update batch is six while the physical microbatch remains one to fit the available memory. The pretrained GPT-2 model uses scaled-dot-product attention; its KV cache is disabled during training because caching is useful for generation, not backpropagation. The Trainer evaluates the held-out 500 abstracts, then saves the model and tokenizer to the existing medical checkpoint directory. This historical run is reused as saved evidence rather than rerun here, so that directory and prior user work remain untouched.",
r"The HTML training table contains all sixteen validation checkpoints and is reproduced in full below. Validation loss falls from 3.177716 at step 10 to 3.131138 at step 160. Training loss appears as No log through step 90 because it is emitted only every 100 steps; the displayed 3.360300 is carried forward in later rows until another training log is available. The final metrics report loss 3.355941, 166 updates, epoch 0.996, and about 2,879 seconds. With this pinned Trainer, 1,000 examples and accumulation six yield floor(1000/6)=166 updates. The one-epoch max-step calculation covers 996 examples, so the remaining four do not enter a complete update window. The returned tokenizer filenames confirm that tokenizer assets were saved beside the model."
),
("text-01-clm.ipynb",18):(
r"This cell loads both the pretrained baseline and the saved fine-tuned checkpoint, moves them to the selected device, and tokenizes one clinical-style prompt. It prepares identical input IDs for the controlled before/after comparison; no model is trained here.",
r"No output is displayed. The shared prompt tensor is passed unchanged to the two generation cells, isolating the checkpoint as the intended difference."
),
("text-01-clm.ipynb",19):(
r"The first generation call uses the pretrained GPT-2 model with greedy decoding (\texttt{do\_sample=False}) and a budget of 100 new tokens. Greedy decoding repeatedly selects the highest-probability next token instead of sampling. The generation API returns prompt plus continuation, and decoding with special tokens skipped makes the whole sequence readable.",
r"The complete continuation is shown. The pretrained model repeats a short statement about shock and difficulty breathing. This is an observed language-model continuation, not a medically validated assessment."
),
("text-01-clm.ipynb",20):(
r"This cell applies exactly the same prompt, token budget, and greedy decoding to the saved medical-domain checkpoint. Matching the generation settings makes the text difference easier to attribute to fine-tuning, while still leaving the output as a qualitative example rather than a clinical test.",
r"The fine-tuned output repeatedly describes a stable patient receiving treatment for a respiratory infection. Repetition remains substantial, and nothing in this exercise demonstrates medical accuracy or safe decision-making."
),
("text-01-clm.ipynb",23):(
r"The padding extension recovers each real sequence length by summing its attention mask. Since the earlier tokenizer padded to 1,024, this step removes padded positions conceptually without retokenizing or changing the examples. It verifies the requested 1,000/500 split and that all measured lengths are positive and within the truncation limit.",
r"The 1,000 training examples contain 12 to 823 tokens; the median is 244. These lengths are the common basis for all three padding-count strategies."
),
("text-01-clm.ipynb",24):(
r"This cell compares fixed 1,024-token rows with dynamic padding over logical batches of six. One seeded random ordering models ordinary shuffled batching; sorting lengths before grouping models similar-length batches. Every example is retained, including the final four-example batch. Useful-token totals therefore stay constant while padded-token totals change. Padding within a batch shortens each batch to its longest member; grouping by length changes which examples share a batch.",
r"The table reports 244,388 useful tokens. Fixed padding adds 779,612 positions (76.13% of all positions). Seeded random batches add 183,026 (42.82%, a 76.52% reduction relative to fixed). Similar-length batches add 1,802 (0.73%, a 99.77% reduction). There are 167 logical batches, with four examples in the last batch. These are token-count comparisons, not training-time measurements."
),
("text-01-clm.ipynb",25):(
r"The dataset wrapper trims stored examples back to attended tokens. The collator then pads each physical batch either to the fixed maximum or just to the longest sequence in that batch. Labels are cloned from the padded IDs, and only attention-mask-zero positions become \texttt{-100}. This is the critical EOS-safe rule: a genuine attended EOS token keeps its target, even though padding uses the same token ID.",
r"The assertions pass: both attended EOS targets remain supervised, and only the synthetic padded position is ignored. The three tensors have the same $(2,2)$ shape, so IDs, attention state, and labels remain position-aligned."
),
("text-01-clm.ipynb",26):(
r"This cell defines a matched timing helper. Each call reloads public GPT-2 weights, disables the cache, applies the same seeded data order, optimizer defaults, microbatch one, and six-step accumulation, then measures training with device synchronization before and after the timer. Both short runs use twelve optimizer updates and disable evaluation; therefore the result measures this training window, not held-out quality. The helper records wall time, loss, FLOPs, device, sample counts, and configuration, then releases model memory.",
r"No output is displayed because this cell only defines the helper and creates no run. The next two cells invoke it independently for fixed and dynamic padding."
),
("text-01-clm.ipynb",27):(
r"This is the fixed-padding arm of the controlled single-run comparison. It starts from the same public checkpoint and uses fixed length 1,024 in the collator. The 12-step cap intentionally keeps the comparison short and matched; it is separate from the historical one-epoch medical fine-tuning run.",
r"The run completes 12 updates in 207.01 seconds with training loss 3.415190. The reported Trainer runtime is 206.869 seconds; no evaluation is run in this timing cell."
),
("text-01-clm.ipynb",28):(
r"This is the dynamic-padding arm. It uses the same dataset, seed, optimizer defaults, physical microbatch, accumulation, and twelve-update cap, but pads each one-example microbatch to its own length. With a physical microbatch of one, grouping by length cannot further reduce within-batch padding; its benefit is shown only in the separate six-example token-count analysis.",
r"The run completes 12 updates in 467.35 seconds with loss 3.415445. Despite much lower reported FLOPs, this single MPS measurement is slower than fixed padding. The result is specific to this environment and short run; it does not establish a general performance relationship."
),
("text-01-clm.ipynb",29):(
r"The final cell reconciles the three token-count strategies with the actual two training records and asserts that both variants completed. It prints the common token table and the measured runtime, update count, and loss for each arm.",
r"The summary repeats the padding statistics and reports fixed at 207.01 seconds versus dynamic at 467.35 seconds, both at 12 updates with nearly equal loss. The interpretation remains deliberately narrow: one controlled run per variant on MPS, with no speedup assumed."
),
("text-02-llms.ipynb",3):(
r"This setup cell imports the Hub and Transformers APIs, fixes the sampling seed, selects the inference device, and defines a cleanup helper to release a previous model before loading another. The cleanup matters on a memory-limited laptop when the sequence moves from base Llama to instruction-tuned Llama and later to Mistral.",
r"The selected backend is MPS. A Jupyter progress-widget warning is retained in the execution artifacts; it does not prevent model loading."
),
("text-02-llms.ipynb",4):(
r"Authentication is read from the user's local Hugging Face credential store. The notebook never embeds a token literal; it passes the local token to the Hub login call with git-credential storage disabled, then deletes the local variable.",
r"The cell confirms authentication without printing a credential. Both gated Llama checkpoints were verified accessible for this execution."
),
("text-02-llms.ipynb",8):(
r"This cell loads the base Llama 3.2 1B causal model in FP16, places it on the selected device, switches to evaluation mode, loads its tokenizer, and aliases padding to EOS. The base checkpoint is the next-token-completion model used to establish a non-instruction-tuned baseline.",
r"No text output is displayed. The model and tokenizer state is ready for five sampled continuations."
),
("text-02-llms.ipynb",10):(
r"The base model generates five continuations from the same short prefix. Sampling draws from the next-token distribution, allowing several plausible continuations; it differs from greedy decoding, which picks one maximum-probability token at each step. Here \texttt{max\_length=50} counts the prompt and continuation together. The returned decoded strings therefore include the prompt and stop near the total-length limit.",
r"The five complete sampled strings show diverse biography-style continuations, including a student, a parent, a dog, and a health-policy worker. They illustrate open-ended completion, not reliable instruction following."
),
("text-02-llms.ipynb",12):(
r"This cell manually defines a Llama 3 conversation serialization: a system header, system content, an end-of-turn token, a user header, and user content. The current date is interpolated at execution. It demonstrates that roles are encoded as control tokens rather than inferred from plain prose.",
r"No output is displayed. The string is a serialization template; this cell has not yet generated an assistant response, and it does not append an explicit assistant-generation prefix."
),
("text-02-llms.ipynb",14):(
r"The text-generation pipeline wraps the already loaded model and tokenizer. It supplies FP16 and the EOS pad ID, then stores the reusable pipeline object for subsequent prompt calls.",
r"The saved output warns that no pipeline device was supplied and says the pipeline will use CPU. That warning is important when interpreting these completion timings and outputs: loading the model onto MPS earlier does not make the pipeline's default device choice disappear."
),
("text-02-llms.ipynb",15):(
r"This cell constructs a two-message system/user conversation and manually substitutes their contents into the custom template. Printing the result exposes the exact special-token boundaries before generation. No answer is produced in this cell.",
r"The output visibly separates the pirate-style system instruction from the arithmetic question with Llama's header and end-of-turn tokens. The next cell sends this complete string to the base model."
),
("text-02-llms.ipynb",17):(
r"The manually serialized string is passed to the base-model pipeline with sampling and a 256-new-token budget. Unlike \texttt{max\_length}, \texttt{max\_new\_tokens} applies only after the prompt. The pipeline returns the full generated text, including the serialized prompt followed by the continuation.",
r"The full output shows how the base completion model continues after the custom conversation serialization. It can imitate the requested style, but the base checkpoint was not trained specifically to obey such instructions."
),
("text-02-llms.ipynb",19):(
r"The cleanup helper releases the base model before the instruction-tuned checkpoint is loaded. The cell then loads Llama 3.2 1B Instruct, applies the same manually assembled conversation, and uses greedy decoding with up to 512 new tokens. This isolates the checkpoint's instruction-tuning effect while keeping the prompt structure similar.",
r"The pipeline and generation configuration warnings are retained in the execution artifacts. The actual generated string follows the pirate persona and answers the arithmetic question. Greedy decoding is deterministic for a fixed model, prompt, and implementation, but it does not guarantee correctness in general."
),
("text-02-llms.ipynb",21):(
r"This cell prints the instruction tokenizer's complete Jinja chat template. The template encodes role headers, tool branches, message endings, and an optional assistant-generation prefix. Reading the actual template clarifies why a list of role dictionaries is not equivalent to concatenating labels into ordinary text.",
r"The complete printed template is reproduced. Its conditional branches serialize messages according to role and control tokens; later calls use \texttt{apply\_chat\_template} so these boundaries are supplied by the tokenizer's official template."
),
("text-02-llms.ipynb",24):(
r"This cell creates a text-generation pipeline and passes the conversation as a list of role dictionaries. It separately prints the result of applying the chat template with \texttt{add\_generation\_prompt=True}, then calls the pipeline in chat mode and selects the last assistant message's content.",
r"The first output shows the serialized prompt ending at an assistant-generation prefix; the second is only the assistant's pirate-style response. The pipeline accepts chat messages and returns the full conversation as a list of messages, from which this code extracts the last one. A CPU-default warning is preserved in the execution artifacts."
),
("text-02-llms.ipynb",26):(
r"This cell applies the same official template manually, decodes the token IDs while retaining special tokens, and passes the result as a string. \texttt{add\_special\_tokens=False} is essential: the string already contains its BOS and role-control tokens, so adding another BOS would duplicate serialization markers.",
r"The string-mode output contains both the serialized prompt and generated response. This return shape differs from chat mode: chat mode returns a message list, while string mode returns one combined text string."
),
("text-02-llms.ipynb",29):(
r"The Mistral cell releases the prior model, loads Mistral 7B Instruct v0.2, and chooses Quanto INT4 weights on this MPS machine with less than 24 GiB of physical memory; larger machines retain FP16. It then sets EOS as padding, builds a text-generation pipeline, and sends a system/user message list. This is a role-conditioned inference example, separate from the later structured-output task.",
r"The run reports Quanto INT4 weights and a pirate-style self-description. Loading progress and tokenizer fork warnings are retained in the execution artifacts. The role-conditioned answer demonstrates format and persona behavior only."
),
("text-02-llms.ipynb",32):(
r"This cell seeds Python's random generator and defines five natural-language templates for addition questions. Each generated record includes the rendered question and both integer operands, so verification can compare the model's parsed operands as well as its sum.",
r"This function prepares five sampled questions for the following generation cell."
),
("text-02-llms.ipynb",34):(
r"This cell defines the system instruction for structured answering. It requires JSON with \texttt{num\_1}, \texttt{num\_2}, and \texttt{answer}, and asks the model to emit only JSON so a parser can consume it.",
r"No output is displayed. The role dictionary is prepended to every user question by the next cell."
),
("text-02-llms.ipynb",36):(
r"This cell generates five seeded addition questions, sends each as a system/user chat, and stores the pipeline's full generated message list alongside the trusted operands. It then persists the records as \texttt{model\_answers.json}. The progress bar is diagnostic output; the saved file is the durable result used by verification.",
r"The cell creates five answer records. The exact saved JSON is included after this code, preserving both the assistant messages and the expected operands. Its progress trace is retained in the execution artifacts."
),
("text-02-llms.ipynb",37):(
r"The verification function locates the assistant message, parses its content with \texttt{json.loads}, checks that both parsed operands match the original question, and only then checks that the answer equals their sum. Missing messages, malformed JSON, missing fields, and type/value errors are caught and rejected.",
r"All five saved examples pass: each response is valid JSON, repeats the correct operands, and gives the correct sum. Additional negative-case checks reject a missing assistant message, malformed JSON, a missing field, and an incorrect answer. Five correct samples do not establish general arithmetic reliability."
),
}

APPENDIX_OUTPUTS = {
("text-01-clm.ipynb",2):{0},
("text-01-clm.ipynb",25):{0},
("text-01-clm.ipynb",27):{0},
("text-01-clm.ipynb",28):{0},
("text-02-llms.ipynb",3):{0},
("text-02-llms.ipynb",19):{0,1},
("text-02-llms.ipynb",24):{0},
("text-02-llms.ipynb",29):set(range(0,9)),
("text-02-llms.ipynb",36):set(range(0,7)),
}

def tex_path(path: str) -> str:
    prefix = "study_guide/"
    if path.startswith(prefix):
        return "../../" + path[len(prefix):]
    if path.startswith("lab04/"):
        return "../../../" + path
    raise ValueError(f"Unexpected artifact path: {path}")

def output_anchor(notebook: str, cell: int, output: int) -> str:
    short = "clm" if "clm" in notebook else "llms"
    return f"out:lab04-{short}-{cell:04d}-{output:02d}"

def cell_anchor(notebook: str, cell: int) -> str:
    short = "clm" if "clm" in notebook else "llms"
    return f"res:lab04-{short}-{cell:04d}"

def pipeline_diagram(nodes: list[str]) -> str:
    names = "abcdef"
    coords = [(0,0),(5.1,0),(10.2,0),(10.2,-1.7),(5.1,-1.7),(0,-1.7)]
    lines = [r"\begin{figure}[htbp]", r"\centering", r"\resizebox{\linewidth}{!}{%",
             r"\begin{tikzpicture}[node distance=1cm, >=Stealth,",
             r"  stage/.style={draw=steelBlue,fill=skyBlue,rounded corners=2pt,",
             r"    align=center,text width=3.8cm,minimum height=0.9cm,font=\small\sffamily}]"]
    for idx,(label,(x,y)) in enumerate(zip(nodes,coords)):
        lines.append(rf"\node[stage] ({names[idx]}) at ({x}cm,{y}cm) {{{label}}};")
    for i in range(5):
        lines.append(rf"\draw[->,thick,steelBlue] ({names[i]}) -- ({names[i+1]});")
    lines += [r"\end{tikzpicture}%", r"}",
              r"\caption{Exercise pipeline: each stage produces the state consumed by the next.}",
              r"\end{figure}"]
    return "\n".join(lines)

def source_for(notebook_rel: str, cell: dict) -> str:
    source = cell["source"]
    return "".join(source) if isinstance(source,list) else source

def cell_block(notebook_rel: str, cell_index: int, cell: dict, inventory_record: dict) -> str:
    notebook_file = Path(notebook_rel).name
    purpose, interpretation = NARRATIVE[(notebook_file,cell_index)]
    source = source_for(notebook_rel,cell).rstrip("\n")
    source_hash = inventory_record["source_sha256"]
    # Keep each cell explanation in the continuous exercise narrative. Avoid
    # template-like labels that make the page read as a sequence of forms.
    purpose = purpose.replace("No output is displayed. ", "").replace(
        "No text output is displayed. ", ""
    ).replace("No output is displayed because this cell only defines a reusable function. ",
              "This cell defines a reusable function without printing a result. ")
    purpose = purpose.replace("No output is displayed because this cell only defines the helper and creates no run. ",
                              "This cell defines the helper without starting a run. ")
    interpretation = interpretation.replace("No output is displayed. ", "").replace(
        "No text output is displayed. ", ""
    ).replace("No output is displayed because this cell only defines a reusable function. ",
              "This cell defines a reusable function without printing a result. ")
    interpretation = interpretation.replace("No output is displayed because this cell only defines the helper and creates no run. ",
                                            "This cell defines the helper without starting a run. ")
    lines = [r"\medskip", r"\noindent " + purpose,
             r"\label{" + cell_anchor(notebook_rel,cell_index) + r"}",
             rf"% coverage-cell: LABS/{notebook_rel} cell={cell_index} source_sha256={source_hash}",
             r"\begin{lstlisting}[style=studycode]", source, r"\end{lstlisting}"]
    outputs = inventory_record.get("outputs",[])
    if not outputs:
        lines += [r"\par\smallskip " + interpretation]
    else:
        lines += [r"\par\smallskip"]
        deferred = APPENDIX_OUTPUTS.get((notebook_file,cell_index),set())
        for output in outputs:
            oi = output["index"]
            exp = next(x for x in inventory_record.get("exported_outputs",[]) if x["index"]==oi)
            artifact = exp.get("presentation_artifact","")
            artifact_for_marker = artifact if artifact else "-"
            marker = (rf"% coverage-output: LABS/{notebook_rel} cell={cell_index} output={oi} "
                      rf"source_sha256={source_hash} payload_sha256={output['payload_sha256']} "
                      rf"artifact={artifact_for_marker}")
            anchor = output_anchor(notebook_rel,cell_index,oi)
            if oi in deferred:
                lines += [marker, r"\label{" + anchor + r"}",
                          r"\textit{Complete warning/progress output is retained in the execution-artifact tree and linked to this result.}"]
            elif artifact:
                lines += [marker, r"\label{" + anchor + r"}",
                          rf"\lstinputlisting[style=terminalOutput]{{{tex_path(artifact)}}}"]
            else:
                lines += [marker, r"\label{" + anchor + r"}",
                          r"\textit{This notebook output slot contains no printable text representation.}"]
        lines += [interpretation]
    return "\n".join(lines)

def build() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = {(c["notebook"],c["cell_index"]):c for c in inventory["cells"]}
    clm = json.loads(NOTEBOOKS["lab04/text-01-clm.ipynb"].read_text(encoding="utf-8"))
    llms = json.loads(NOTEBOOKS["lab04/text-02-llms.ipynb"].read_text(encoding="utf-8"))
    out = []
    out += [r"\section{Exercise 1: GPT-2 medical-domain adaptation}",
            r"\label{sec:lab04-clm}",
            r"This exercise adapts pretrained GPT-2 to a small, reproducibly selected set of PubMed abstracts. Starting with 1,000 training and 500 evaluation examples, it follows tokenization and next-token labels through fine-tuning, checkpoint saving, and before/after generation from the same clinical-style prompt. The final extension compares fixed and dynamic padding, first by counting every example and then in matched short training runs. Along the way, we check that causal targets align after the model's internal shift, padded positions contribute no loss, and the timing settings match.",
            pipeline_diagram(["PubMed abstracts","Seeded 1,000 / 500 split","GPT-2 tokenization and labels",
                              "Trainer and saved checkpoint","Before/after greedy generation","Padding counts and timing"]),
            r"\subsection{Data, tokenization, and next-token targets}"]
    for i in (2,5,7,10,12):
        c=clm["cells"][i]; out.append(cell_block("lab04/text-01-clm.ipynb",i,c,records[("lab04/text-01-clm.ipynb",i)]))
    out += [r"\subsection{Training, persistence, and qualitative generation}"]
    for i in (15,18,19,20):
        c=clm["cells"][i]; out.append(cell_block("lab04/text-01-clm.ipynb",i,c,records[("lab04/text-01-clm.ipynb",i)]))
    out += [r"\subsection{Padding analysis and matched training window}",
            r"The fixed-length baseline pads each example independently to 1,024 tokens. The dynamic-padding table groups examples logically in batches of six; it does not alter the example set. In training, the memory-compatible physical microbatch remains one example with six-step accumulation, so length grouping cannot change padding inside those one-example microbatches.",
            r"The first full-epoch dynamic-padding pilot exhausted the MPS memory pool after 2,367.7 seconds; its diagnostic remains in the execution artifacts. To obtain a matched completed comparison, both successful arms below start from the same public GPT-2 checkpoint in separate clean kernels and run twelve updates with evaluation disabled. The measured window is therefore intentionally short and does not estimate held-out quality."]
    for i in (23,24,25,26,27,28,29):
        c=clm["cells"][i]; out.append(cell_block("lab04/text-01-clm.ipynb",i,c,records[("lab04/text-01-clm.ipynb",i)]))
    out += [r"\begin{quote}\noindent\textbf{Interpreting the clinical example.} ",
            r"The fine-tuned continuation changes the wording and repeats a respiratory-infection claim, but this prompt and tiny subset do not test factual accuracy, calibration, or clinical safety. Treat both strings as demonstrations of learned continuation behavior, not medical advice.",
            r"\end{quote}",
            r"\clearpage",
            r"\section{Exercise 2: Llama completion and instruction following}",
            r"\label{sec:lab04-llama}",
            r"Here we compare base Llama completion with instruction following, then trace how a role-based conversation becomes model input. The exercise uses the two locally accessible Llama 3.2 1B checkpoints, a system message, and short prompts. Sampled continuations establish the base-model behavior; manual serialization and the tokenizer's full Jinja template then lead into the instruction-tuned checkpoint and its chat and string pipeline interfaces. The important checks are that role boundaries are preserved and that each interface's returned content is interpreted correctly.",
            pipeline_diagram(["Local authentication","Base Llama checkpoint","Sampled next-token completions",
                              "Manual role serialization","Instruct checkpoint and template","Chat and string interfaces"]),
            r"\subsection{Setup and base-model completion}"]
    for i in (3,4,8,10,12,14,15,17):
        c=llms["cells"][i]; out.append(cell_block("lab04/text-02-llms.ipynb",i,c,records[("lab04/text-02-llms.ipynb",i)]))
    out += [r"\subsection{Instruction-tuned model and official chat template}",
            r"The role labels are structural metadata once passed as message dictionaries; the Jinja template turns them into the model's learned control-token format. Instruction tuning changes how the checkpoint has been trained to respond to such serialized requests. It is not the same operation as adding role words to a base model's prompt."]
    for i in (19,21,24,26):
        c=llms["cells"][i]; out.append(cell_block("lab04/text-02-llms.ipynb",i,c,records[("lab04/text-02-llms.ipynb",i)]))
    out += [r"\begin{quote}\noindent\textbf{A chat template is a serializer.} ",
            r"A chat template is a serializer: it maps a list such as system/user messages into a sequence containing role headers, content, and end markers. The instruction-tuned weights supply the learned behavior associated with those sequences. A serializer alone does not instruction-tune a base checkpoint.",
            r"\end{quote}",
            r"\clearpage",
            r"\section{Exercise 3: Mistral structured answers}",
            r"\label{sec:lab04-mistral}",
            r"The final exercise uses Mistral 7B Instruct v0.2 with Quanto INT4 weights on the 16 GiB MPS machine. It first demonstrates a role-conditioned response, then generates five seeded addition questions under a JSON-only system instruction. The saved conversations retain trusted operands so the verifier can check JSON syntax, operand identity, and arithmetic separately; malformed or incomplete answers must fail those checks.",
            pipeline_diagram(["Mistral INT4 load","Role-conditioned response","Seeded addition questions",
                              "JSON system instruction","Generation and persistence","Parse, compare, verify"]),
            r"\subsection{Model setup and role-conditioned response}"]
    for i in (29,):
        c=llms["cells"][i]; out.append(cell_block("lab04/text-02-llms.ipynb",i,c,records[("lab04/text-02-llms.ipynb",i)]))
    out += [r"\subsection{Question generation and JSON instruction}"]
    for i in (32,34):
        c=llms["cells"][i]; out.append(cell_block("lab04/text-02-llms.ipynb",i,c,records[("lab04/text-02-llms.ipynb",i)]))
    out += [r"\subsection{Generate, save, parse, and verify}"]
    c=llms["cells"][36]; out.append(cell_block("lab04/text-02-llms.ipynb",36,c,records[("lab04/text-02-llms.ipynb",36)]))
    answers_path = ROOT / "lab04" / "model_answers.json"
    answer_hash = hashlib.sha256(answers_path.read_bytes()).hexdigest()
    source_hash = records[("lab04/text-02-llms.ipynb",36)]["source_sha256"]
    out += [r"\paragraph{Saved side-effect artifact.} The loop writes the following complete file. The \texttt{model\_answer} value preserves the full system/user/assistant message list, while the outer operands remain the verification reference.",
            rf"% coverage-artifact: LABS/lab04/text-02-llms.ipynb::cell-0036 source_sha256={source_hash} path=lab04/model_answers.json sha256={answer_hash}",
            r"\label{out:lab04-mistral-json-file}",
            r"\lstinputlisting[style=terminalOutput]{../../../lab04/model_answers.json}"]
    c=llms["cells"][37]; out.append(cell_block("lab04/text-02-llms.ipynb",37,c,records[("lab04/text-02-llms.ipynb",37)]))
    out += [r"\begin{center}",
            r"\begin{tabularx}{\linewidth}{l r r r X}",
            r"\toprule",
            r"Case & JSON parses & Operands match & Sum correct & Verification result\\",
            r"\midrule",
            r"Five saved records & Yes & Yes & Yes & Accepted in the notebook output\\",
            r"Assistant message missing & -- & -- & -- & Rejected with a value error\\",
            r"Malformed JSON & No & -- & -- & Rejected by the JSON parser\\",
            r"Required field missing & Yes & -- & -- & Rejected by key lookup\\",
            r"Wrong arithmetic result & Yes & Yes & No & Returned as incorrect\\",
            r"\bottomrule",
            r"\end{tabularx}",
            r"\end{center}",
            r"The acceptance table separates three checks that are often conflated. Syntactically valid JSON can still contain wrong operands or an incorrect answer. The five successes validate these five examples only; they do not establish general arithmetic reliability."]
    '''
    out += [r"\appendix",
            r"\section{Diagnostic streams and environment warnings}",
            r"\label{app:lab04-diagnostics}",
            r"Warnings and progress traces are kept separate from the application results above, but every saved textual output is reproduced here. Each entry links back to the cell result it qualifies."]
    deferred=[]
    for cell in inventory["cells"]:
        nb=Path(cell["notebook"]).name
        key=(nb,cell["cell_index"])
        for oi in APPENDIX_OUTPUTS.get(key,set()):
            output=next(o for o in cell["outputs"] if o["index"]==oi)
            exp=next(o for o in cell.get("exported_outputs",[]) if o["index"]==oi)
            artifact=exp.get("presentation_artifact","")
            if artifact:
                deferred.append((cell,output,exp))
    for cell,output,exp in deferred:
        nb=Path(cell["notebook"]).name
        idx=cell["cell_index"]; oi=output["index"]
        artifact=exp["presentation_artifact"]
        marker=(rf"% coverage-output: LABS/{cell['notebook']} cell={idx} output={oi} "
                rf"source_sha256={cell['source_sha256']} payload_sha256={output['payload_sha256']} "
                rf"artifact={artifact}")
        out += [r"\paragraph{Diagnostic output.} The complete stream is retained for auditability.",
                rf"\lstinputlisting[style=terminalOutput]{{{tex_path(artifact)}}}"]
    out += [r"\paragraph{Jupyter kernel warning.}",
            r"The clean-kernel runs also emitted the standard IPKernelApp warning that a TCP kernel connection was not encrypted. This concerns the local notebook transport and is retained in the run log; it is separate from model output.",
            r"\begin{lstlisting}[style=terminalOutput]",
            r"[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.",
            r"\end{lstlisting}",
            r"\paragraph{Earlier access diagnostic.}",
            r"Before local access was configured, the original saved Llama attempt stopped at the notebook's explicit authentication check. The later clean run succeeded; the original failure remains part of the preserved history.",
            r"\begin{lstlisting}[style=terminalOutput]",
            r"RuntimeError: Llama 3.2 requires an approved Hugging Face account. Run hf auth login locally or set HF_TOKEN, then rerun.",
            r"\end{lstlisting}",
            r"\paragraph{Full-epoch dynamic-padding pilot.}",
            r"The first matched full-epoch dynamic run stopped during MPS backpropagation after 2,367.7 seconds: allocated MPS memory was 9.38 GiB, other allocations 10.64 GiB, with a 20.13 GiB limit; a further 147.24 MiB allocation failed. The completed 12-update comparison in Exercise 1 uses separate clean kernels and is the only timing comparison reported as successful."]
    out += [r"\section{Transcript, execution, and reproducibility notes}",
            r"The matching Whisper session is 82 minutes 13.055 seconds long and contains 801 timestamped segments. The export begins at 00:00:01.860; its last segment ends 1.385 seconds beyond the recording duration, and the largest gap between adjacent segments is 57.660 seconds. A local 90-second retranscription differed from the stored transcript and did not resolve the wording. Accordingly, the recording supplies a topic map, not authoritative quotations: the PDF uses notebook code and saved outputs for exact computational claims, and avoids reconstructing uncertain speech.",
            r"The lecture transcript has clear topic anchors for labels and Trainer (around 03:03--03:51), data selection (around 15:55), evaluation and adaptation (around 34:55--36:53), GPT-2 continuation and sampling (around 37:00--51:00), gated Llama access (around 58:30), and role messages/templates (around 65:20--70:10). Requirements found only in notebook Markdown are treated as assignment instructions, not attributed to the lecture.",
            r"The notebook set contains 33 nonempty code cells: 16 in CLM and 17 in LLMs. All 33 current sources have successful run records with matching SHA-256 hashes. The 53 saved output objects have zero unresolved notebook errors in the finalized notebooks; complete raw MIME payloads and output hashes are retained in the execution-artifact tree and coverage inventory. The original nine CLM cells and six original LLM executions were preserved before edits; the formerly failing Llama sequence now has a successful clean-kernel history.",
            r"The original medical GPT-2 training output and Mistral JSON run are historical saved evidence. The new padding timing is one successful 12-update run per strategy on MPS, with evaluation disabled; the completed runs took 207.01 s fixed and 467.35 s dynamic, and their training losses were 3.415190 and 3.415445. The full-epoch dynamic pilot OOM is documented above. Hardware contention, MPS kernels, and the short single-run design limit generalization.",
            r"The Llama and padding work used Python 3.13.9, PyTorch 2.8.0, Transformers 4.46.3, Datasets 3.6.0, and Accelerate 1.15.0. Checkpoint revisions and the complete pinned dependency list are saved in \path{lab04/execution/environment.json} and \path{lab04/execution/requirements-lock.txt}. The Mistral answers and verification tests are deterministic evidence for the recorded run, not a reliability estimate."]
    '''
    CHAPTER.parent.mkdir(parents=True,exist_ok=True)
    CHAPTER.write_text("\n\n".join(out)+"\n",encoding="utf-8")
    wrapper = r"""\documentclass[10pt,a4paper,oneside]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{newpxtext}
\usepackage[scaled=0.88]{sourcecodepro}
\usepackage{microtype}
\usepackage[a4paper,top=19mm,bottom=19mm,left=20mm,right=20mm,headheight=16pt,footskip=10mm]{geometry}
\usepackage[dvipsnames,table]{xcolor}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs,tabularx,array}
\usepackage{enumitem}
\usepackage{listings}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{hyperref}
\definecolor{politoNavy}{RGB}{0,45,98}
\definecolor{steelBlue}{RGB}{35,100,160}
\definecolor{skyBlue}{RGB}{230,240,250}
\definecolor{bodyGray}{RGB}{80,85,90}
\definecolor{codeBg}{RGB}{248,249,251}
\definecolor{codeFrame}{RGB}{220,225,230}
\hypersetup{colorlinks=true,linkcolor=politoNavy,urlcolor=steelBlue,pdftitle={Laboratory 04 complete solution},pdfauthor={Politecnico di Torino}}
\titleformat{\section}{\normalfont\sffamily\Large\bfseries\color{politoNavy}}{\thesection}{0.8em}{}
\titleformat{\subsection}{\normalfont\sffamily\large\bfseries\color{steelBlue}}{\thesubsection}{0.8em}{}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\sffamily\color{bodyGray}\nouppercase{\rightmark}}
\fancyhead[R]{\small\sffamily\bfseries\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\small\sffamily\thepage}\renewcommand{\headrulewidth}{0pt}}
\lstdefinestyle{studycode}{
  language=Python,basicstyle=\fontsize{7.4}{8.8}\ttfamily,
  keywordstyle=\bfseries\color{politoNavy},commentstyle=\itshape\color{bodyGray},
  stringstyle=\color{ForestGreen},numbers=left,numberstyle=\tiny\color{bodyGray},
  numbersep=6pt,tabsize=4,showstringspaces=false,breaklines=true,
  breakatwhitespace=false,columns=fullflexible,keepspaces=true,
  frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg},
  literate={█}{{\ensuremath{\blacksquare}}}1 {▎}{{|}}1 {▋}{{|}}1 {—}{{---}}1 {’}{{'}}1
}
\lstdefinestyle{terminalOutput}{
  basicstyle=\fontsize{7.2}{8.5}\ttfamily,breaklines=true,breakatwhitespace=false,
  columns=fullflexible,keepspaces=true,showstringspaces=false,
  frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg},
  literate={█}{{\ensuremath{\blacksquare}}}1 {▎}{{|}}1 {▋}{{|}}1 {—}{{---}}1 {’}{{'}}1
}
\lstset{style=studycode}
\setlist{nosep,leftmargin=1.5em}
\newcommand{\labSolutionTitle}{Laboratory 04: Causal Language Modeling and Instruction-Tuned LLMs}
\newcommand{\labSolutionSubtitle}{Complete notebook-aligned solution}
\begin{document}
\input{../../frontmatter/solution_titlepage}
\tableofcontents
\clearpage
\input{../../chapters/04_lab04_complete.tex}
\end{document}
"""
    WRAPPER.write_text(wrapper,encoding="utf-8")

if __name__ == "__main__":
    build()
