#!/usr/bin/env python3
"""Build Lab05's editable solution source from notebook code and output evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # LABS
GUIDE = ROOT / "study_guide"
CHAPTER = GUIDE / "chapters" / "05_quantization_lora.tex"
WRAPPER = GUIDE / "standalone" / "lab05" / "lab05_solution.tex"
INVENTORY = GUIDE / "coverage" / "lab05.inventory.json"
NB_QUANT = ROOT / "lab05" / "text-01-quantization.ipynb"
NB_LORA = ROOT / "lab05" / "text-02-LoRA.ipynb"

# Purpose precedes the exact source; interpretation follows the saved output.
# Neither part is a repeated label or a cell caption.
NARRATIVE = {
    ("text-01-quantization.ipynb", 3): (
        "We start with a fixed seed and two small tensors: a 3 by 5 weight matrix and a length-five input vector. Setting one coordinate in each to zero makes it possible to observe how the two quantizers treat zero.",
        "These tensors are the common reference for the unquantized product and both quantization schemes. Their small dimensions keep the integer arithmetic inspectable.",
    ),
    ("text-01-quantization.ipynb", 6): (
        "Before changing precision, this product records the reference output of the original matrix and vector. Every later reconstruction is compared with this value.",
        "The floating-point result is the numerical target for the quantized calculations that follow.",
    ),
    ("text-01-quantization.ipynb", 8): (
        "This helper implements symmetric absmax quantization. Its scale maps the largest magnitude to 127, rounding maps values to integer levels, and clamping keeps them in the symmetric range from -127 to 127. The zero-range guard makes an all-zero tensor safe to quantize.",
        "The function returns both integer codes and the scale needed to recover approximate floating-point values.",
    ),
    ("text-01-quantization.ipynb", 10): (
        "Quantization is useful only if the integer representation can be interpreted again. This inverse helper converts the codes to float and multiplies by their saved scale.",
        "The original scale is required downstream; without it the integer codes do not retain the magnitude of the source tensor.",
    ),
    ("text-01-quantization.ipynb", 12): (
        "We now apply the same symmetric scheme independently to the matrix and vector. Independent scales use each operand's available integer range effectively.",
        "The resulting integer tensors and separate scales feed the reconstruction checks and integer dot product.",
    ),
    ("text-01-quantization.ipynb", 13): (
        "This comparison examines the matrix codes, the original weights, and the dequantized approximation. The mean absolute difference condenses coordinate-wise rounding error into one diagnostic.",
        "The reconstructed matrix stays close to the original and preserves the deliberately zero entry. The small nonzero mean error is quantization loss, not a change to the original tensor.",
    ),
    ("text-01-quantization.ipynb", 14): (
        "The same round trip is checked for the input vector, using its own scale. This separates weight error from activation error.",
        "The vector reconstruction also preserves zero; its mean absolute error is reported independently from the matrix's.",
    ),
    ("text-01-quantization.ipynb", 16): (
        "This is the tempting low-precision computation: multiply the quantized matrix and vector while they are still int8. It exposes a hardware arithmetic issue separate from the rounding errors measured above.",
        "The displayed result has wrapped values because the dot products exceed the int8 range. Quantized operands therefore need a wider accumulator even when their storage uses eight bits.",
    ),
    ("text-01-quantization.ipynb", 18): (
        "Inspecting the first matrix row and the vector lets us verify one dot product by hand and compare it with the wrapped result.",
        "The integer operands are individually representable in int8; their products' sum is not. This isolates accumulation overflow as the cause.",
    ),
    ("text-01-quantization.ipynb", 20): (
        "The corrected calculation promotes both operands to int16 before multiplication and accumulation. This is wide enough for these short illustrative rows and prevents int8 wraparound.",
        "The larger integer values are the proper dot products in quantized-code space. Production kernels generally accumulate low-bit products into a wider type as well.",
    ),
    ("text-01-quantization.ipynb", 23): (
        "The integer dot products are converted back to the original output scale by multiplying the matrix and vector scales. This follows from independently scaled operands: each product carries both factors.",
        "The reconstructed output is close to the original floating-point product; the remaining difference is the accumulated effect of quantizing both operands.",
    ),
    ("text-01-quantization.ipynb", 25): (
        "A final scalar error summarizes the effect of absmax quantization on the matrix-vector result, rather than on either input alone.",
        "The measured mean absolute output error is about 0.00675 for this seeded example. It is an observed result for these tensors, not a general error bound.",
    ),
    ("text-01-quantization.ipynb", 27): (
        "The second helper uses an asymmetric min-max mapping. It stretches the observed range to the full int8 interval, stores a zero point, and reverses both operations during dequantization. The constant-range guard avoids division by zero.",
        "Unlike absmax, this mapping can use all 256 codes and need not map real zero to integer zero. The returned scale and zero point are both required to interpret the codes.",
    ),
    ("text-01-quantization.ipynb", 28): (
        "We quantize the same matrix and vector with independent min-max ranges. Reusing the same examples makes the later error comparison meaningful.",
        "Each operand now carries its own scale and zero point; these are needed for both reconstruction and the corrected dot product.",
    ),
    ("text-01-quantization.ipynb", 30): (
        "This check dequantizes the matrix, measures its mean absolute error, and prints the zero point so we can see how real zero is encoded.",
        "The full int8 range is used and the matrix error is small. The nonzero zero point shows that a real zero is represented by an offset code rather than by integer zero.",
    ),
    ("text-01-quantization.ipynb", 32): (
        "As in the symmetric case, the min-max integer dot product uses int16 accumulation. The result is kept in code space until the zero-point offsets are removed.",
        "This cell prepares the raw dot products; interpreting them as real values requires the correction terms in the next computation.",
    ),
    ("text-01-quantization.ipynb", 34): (
        "Expanding the two affine quantization equations gives the corrected product. The row-wise matrix-code sums, vector-code sum, and shared inner dimension account for the cross terms introduced by both zero points.",
        "The resulting expression removes the offsets before dividing by the product of scales. This is why asymmetric quantization cannot simply multiply the raw int8 result by two scales.",
    ),
    ("text-01-quantization.ipynb", 35): (
        "We print the corrected min-max result beside the original output and compute their mean absolute difference. This closes the small numerical comparison.",
        "The result remains close to the floating-point reference. Although this particular error is small, asymmetric mapping trades exact zero representation for tighter use of the available code range.",
    ),
    ("text-01-quantization.ipynb", 39): (
        "The Llama experiment uses a CPU baseline because PyTorch's dynamic int8 Linear quantization is a CPU path. The same CPU device and QNNPACK engine are used for the baseline and quantized timings to keep the comparison aligned.",
        "QNNPACK is the selected quantized operator backend. The widget warning is only a notebook display dependency and is preserved in the diagnostics appendix.",
    ),
    ("text-01-quantization.ipynb", 40): (
        "The gated Llama checkpoint is accessed through the existing local Hugging Face credential store. The code checks access without printing or embedding a token, then clears the temporary variable.",
        "Authentication succeeds in the finalized run, allowing the exact gated checkpoint to load in the next step. An earlier failed attempt is retained as historical diagnostics only.",
    ),
    ("text-01-quantization.ipynb", 42): (
        "This cell loads the public gated Llama 3.2 1B base model in float32 on CPU and loads a left-padding tokenizer. Setting EOS as the pad token lets differently sized prompts share a batch.",
        "The model and tokenizer become the common baseline for parameter-size measurement, generation, and the two quantized alternatives.",
    ),
    ("text-01-quantization.ipynb", 43): (
        "Rather than infer memory from a parameter count, this helper serializes the state dictionary and measures its file size. It establishes the storage baseline before quantization.",
        "The value reports serialized model-state size in decimal megabytes; it is not peak runtime memory, which also includes activations and framework overhead.",
    ),
    ("text-01-quantization.ipynb", 45): (
        "Twenty copies of one short prompt are tokenized together, then the unquantized model greedily generates 30 new tokens. The batch provides a stable workload for the later CPU timing comparison.",
        "The decoded batch preserves each prompt followed by its continuation. The elapsed time is specific to this hardware, batch, and software stack.",
    ),
    ("text-01-quantization.ipynb", 48): (
        "PyTorch replaces Linear layers with dynamically quantized int8 versions while leaving other modules, including embeddings, in their existing representation. The serialized state size is measured again.",
        "The size change reflects only modules supported by this transformation and its metadata. It should not be mistaken for every parameter becoming one byte.",
    ),
    ("text-01-quantization.ipynb", 50): (
        "Displaying the module tree makes the transformation concrete: it shows which Linear layers are now dynamically quantized and which layers retain their original types.",
        "The printed structure is architectural evidence for the selective conversion performed in the previous cell.",
    ),
    ("text-01-quantization.ipynb", 51): (
        "The same 20 prompts are generated with the int8 model using greedy decoding and the same 30-token budget. Comparing strings and elapsed time with the baseline isolates the observed effect of this configuration.",
        "The full decoded output and runtime are preserved. Any speed or text difference is specific to the tested backend and does not establish a general performance or quality guarantee.",
    ),
    ("text-01-quantization.ipynb", 53): (
        "After deleting the float32 and int8 models, this cell loads a fresh 4-bit BitsAndBytes model on CPU. Explicit cleanup avoids holding all large variants together; the same prompt batch is moved to the new model's device.",
        "The output confirms the CPU int4 backend and measures the serialized quantized state. The configuration stores 4-bit weights with float32 computation; weight storage precision and arithmetic precision are distinct.",
    ),
    ("text-01-quantization.ipynb", 54): (
        "The final generation repeats the same greedy prompt batch and token budget with the int4 model, completing the baseline/int8/int4 comparison.",
        "The generated strings and elapsed time are evidence for this run only. Quantization level alone does not predict latency or generation quality independently of the backend and workload.",
    ),
    ("text-02-LoRA.ipynb", 3): (
        "The LoRA exercise begins with PyTorch and BERT imports, a fixed seed, and an MPS availability check. This provides deterministic initialization and records the accelerator environment for the later training comparison.",
        "MPS is available on this host. The notebook's Trainer selects the device during training; the availability message alone does not prove that a particular run used it.",
    ),
    ("text-02-LoRA.ipynb", 4): (
        "This small reporting helper totals trainable and total parameters and expresses the trainable fraction as a percentage. We use it before and after adapter insertion to quantify the parameter savings.",
        "The function produces no printed result until called on a model; it is reused for both the manual and PEFT implementations.",
    ),
    ("text-02-LoRA.ipynb", 7): (
        "We load the uncased BERT encoder with a two-class sequence-classification head and its matching tokenizer. The pretrained encoder supplies language features; the classification head is newly initialized for sentiment labels.",
        "Transformers warns that the classifier weights are random and must be trained for the task. The head's trainability later becomes an important difference between the manual and PEFT runs.",
    ),
    ("text-02-LoRA.ipynb", 8): (
        "Before modifying BERT, the helper establishes the full fine-tuning baseline: every parameter in the encoder and classifier is trainable.",
        "All 109,483,778 parameters are initially trainable. This count is compared with the much smaller adapter-only parameter set.",
    ),
    ("text-02-LoRA.ipynb", 10): (
        "The manual adapter wraps a linear layer with its original operation plus a rank-eight update $(xA)B$. The standard initialization uses Kaiming-uniform A and zero B, so the adapter initially contributes exactly zero while its parameters can learn.",
        "This class preserves the base projection and adds a low-rank trainable path. Its parameter dimensions are input-by-rank and rank-by-output, so the added count is proportional to rank rather than input times output.",
    ),
    ("text-02-LoRA.ipynb", 12): (
        "Each BERT encoder block has six linear projections selected here: query, key, value, attention output, and the two feed-forward transformations. Replacing them applies the same adapter construction throughout the encoder.",
        "The model now contains a base projection plus a low-rank path at each selected site. Layer normalization, embeddings, and the task classifier are not replaced by this loop.",
    ),
    ("text-02-LoRA.ipynb", 14): (
        "To make the experiment parameter-efficient, all model parameters are frozen first. The loop then enables gradients only for each manually inserted A and B matrix.",
        "This policy trains the adapters while leaving the pretrained encoder and the randomly initialized classifier frozen. That frozen classifier is a limitation when comparing accuracy with PEFT, which also trains its task head.",
    ),
    ("text-02-LoRA.ipynb", 16): (
        "The parameter helper now checks whether freezing and replacement produced the expected trainable count. The assertion guards the architecture calculation against a missed or duplicated projection.",
        "The six adapter sites across twelve layers contain 1,327,104 trainable parameters, about 1.20% of the full model. The classifier remains frozen in this manual path.",
    ),
    ("text-02-LoRA.ipynb", 18): (
        "The IMDB dataset is shuffled with seed 42 and reduced to 2,000 training and 1,000 test examples. This small, disjoint sample keeps the demonstration manageable while preserving a reproducible comparison set.",
        "The cached dataset is used in offline mode. The same selected rows feed both adapter implementations.",
    ),
    ("text-02-LoRA.ipynb", 19): (
        "This metric callback converts the Trainer's logits to class predictions and computes accuracy against the reference labels. It is reused for initial evaluation, periodic validation, and final comparison.",
        "The callback returns a single accuracy metric for each evaluation event, keeping the comparison focused on held-out classification accuracy.",
    ),
    ("text-02-LoRA.ipynb", 20): (
        "The tokenizer converts the review text into padded, truncated BERT inputs. Mapping both splits in batches prepares model-ready data once for both training approaches.",
        "The tokenized datasets contain aligned input IDs, attention masks, and labels; later Trainers can reuse them without retokenizing.",
    ),
    ("text-02-LoRA.ipynb", 21): (
        "The Trainer configuration keeps an effective batch of 32 using microbatches of four and eight accumulation steps. It specifies one epoch, the shared learning rate and weight decay, evaluation and logging every ten updates, and disables external reporting.",
        "The same arguments and metric callback are reused for both implementations. This cell creates the training controller but does not yet evaluate or update the model.",
    ),
    ("text-02-LoRA.ipynb", 22): (
        "Before training, we measure the manual adapter model on the held-out split. This establishes the starting accuracy of the frozen random classifier plus untrained adapters.",
        "Initial accuracy is 0.5070, close to chance for two balanced classes. The progress trace is retained in the diagnostics appendix.",
    ),
    ("text-02-LoRA.ipynb", 23): (
        "The manual adapters are trained for one epoch on the seeded 2,000-review subset, with held-out evaluation at regular update intervals. The complete validation table shows how accuracy and loss change during adaptation.",
        "The 62-update run reports the per-checkpoint losses and accuracies in full. Its training time is about 810 seconds on this host; the assigned classifier remains frozen, so interpret this result as the notebook's adapter-only implementation rather than a fully matched classifier fine-tune.",
    ),
    ("text-02-LoRA.ipynb", 24): (
        "After the manual adapter epoch, the same held-out set is evaluated again to quantify its endpoint under the shared metric.",
        "Accuracy rises from 0.5070 to 0.6580. This is an observed result on 1,000 selected reviews and the fixed random classifier, not a general benchmark.",
    ),
    ("text-02-LoRA.ipynb", 27): (
        "Before testing PEFT, the notebook releases the manual Trainer and model, clears cached MPS allocations, resets the seed, and reloads a fresh BERT classifier. This prevents learned weights from leaking into the second approach.",
        "The warning again identifies the newly initialized classification head. Reloading it under the same seed makes the PEFT branch start from a reproducible baseline.",
    ),
    ("text-02-LoRA.ipynb", 29): (
        "PEFT's LoRA configuration uses rank eight, alpha 32, dropout 0.1, and targets the same six encoder Linear projections per layer. Its sequence-classification wrapper also keeps the task head trainable.",
        "The PEFT model now contains low-rank modules at the selected sites. Its trainable count will include the classification head as well as the adapters.",
    ),
    ("text-02-LoRA.ipynb", 30): (
        r"This type inspection confirms that \texttt{get\_peft\_model} returned the sequence-classification PEFT wrapper expected for the task.",
        "The Python type is `PeftModelForSequenceClassification`, so the task-specific classifier is preserved by the wrapper.",
    ),
    ("text-02-LoRA.ipynb", 32): (
        "Printing the first encoder block verifies where PEFT inserted its A and B projections and shows that the original linear layers remain as the adapter base.",
        "The module tree displays adapters on the attention and feed-forward linears. This is the library-managed counterpart to the manual replacements above.",
    ),
    ("text-02-LoRA.ipynb", 34): (
        "The PEFT helper calculates trainable parameters after wrapping. Comparing the result with the manual count reveals whether the task head is included.",
        "PEFT trains 1,328,642 parameters, including 1,538 classifier weights and biases, versus 1,327,104 manual adapter parameters. The accuracy comparison therefore is not perfectly controlled.",
    ),
    ("text-02-LoRA.ipynb", 36): (
        "A second Trainer is constructed with the same tokenized splits, metric callback, and training arguments. Only the model object changes to the PEFT-wrapped classifier.",
        "The comparison is ready to run with the same one-epoch schedule and effective batch size as the manual path.",
    ),
    ("text-02-LoRA.ipynb", 37): (
        "PEFT adapters are trained for one epoch using the shared Trainer configuration. The saved table records validation loss and accuracy at each logged checkpoint.",
        "The 62-update run reports training loss 0.5761 and runtime 814.4 seconds; the full step table is preserved. The task head is trainable here, unlike in the manual branch, so the accuracy difference combines implementation and head-training effects.",
    ),
    ("text-02-LoRA.ipynb", 38): (
        "The final cell evaluates the trained PEFT classifier once more on the held-out reviews so its endpoint can be read alongside the manual result.",
        "Final accuracy is 0.8170 on this selected test subset. The difference from the manual 0.6580 result is suggestive for this run, but the two branches differ in classifier trainability and PEFT dropout.",
    ),
}

DEFERRED_OUTPUTS = {
    ("text-01-quantization.ipynb", 39): {0},
    ("text-02-LoRA.ipynb", 3): {0},
    ("text-02-LoRA.ipynb", 22): {0},
    ("text-02-LoRA.ipynb", 24): {0},
    ("text-02-LoRA.ipynb", 38): {0},
}


def tex_path(path: str) -> str:
    if path.startswith("study_guide/"):
        return "../../" + path[len("study_guide/"):]
    if path.startswith("lab05/"):
        return "../../../" + path
    raise ValueError(f"Unexpected Lab05 artifact path: {path}")


def pipeline(nodes: list[str]) -> str:
    names = "abcdef"
    coords = [(0, 0), (4.5, 0), (9, 0), (9, -1.6), (4.5, -1.6), (0, -1.6)]
    lines = [r"\begin{figure}[htbp]", r"\centering", r"\resizebox{\linewidth}{!}{%",
             r"\begin{tikzpicture}[>=Stealth,stage/.style={draw=steelBlue,fill=skyBlue,rounded corners=2pt,align=center,text width=3.5cm,minimum height=.85cm,font=\small\sffamily}]"]
    for i, (label, (x, y)) in enumerate(zip(nodes, coords)):
        lines.append(rf"\node[stage] ({names[i]}) at ({x}cm,{y}cm) {{{label}}};")
    for i in range(5):
        lines.append(rf"\draw[->,thick,steelBlue] ({names[i]}) -- ({names[i+1]});")
    lines += [r"\end{tikzpicture}%", r"}", r"\caption{The exercise pipeline, from input to checked result.}", r"\end{figure}"]
    return "\n".join(lines)


def source(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else str(value)


def cell_tex(nb_name: str, nb_rel: str, cell_index: int, cell: dict, record: dict) -> str:
    purpose, interpretation = NARRATIVE[(nb_name, cell_index)]
    src = source(cell).rstrip("\n")
    source_hash = record["source_sha256"]
    lines = [r"\smallskip", r"\noindent " + purpose,
             rf"\label{{res:lab05-{('quant' if 'quantization' in nb_name else 'lora')}-{cell_index:04d}}}",
             rf"% coverage-cell: LABS/{nb_rel} cell={cell_index} source_sha256={source_hash}",
             r"\begin{lstlisting}[style=studycode]", src, r"\end{lstlisting}", r"\par\smallskip"]
    outputs = record.get("outputs", [])
    if not outputs:
        lines.append(interpretation)
        return "\n".join(lines)
    deferred = DEFERRED_OUTPUTS.get((nb_name, cell_index), set())
    for output in outputs:
        oi = output["index"]
        export = next(item for item in record["exported_outputs"] if item["index"] == oi)
        artifact = export.get("presentation_artifact", "")
        marker_artifact = artifact or "-"
        lines.append(rf"% coverage-output: LABS/{nb_rel} cell={cell_index} output={oi} source_sha256={source_hash} payload_sha256={output['payload_sha256']} artifact={marker_artifact}")
        lines.append(rf"\label{{out:lab05-{('quant' if 'quantization' in nb_name else 'lora')}-{cell_index:04d}-{oi:02d}}}")
        if oi in deferred:
            lines.append(r"\textit{The complete progress or warning stream is reproduced in Appendix~\ref{app:lab05-diagnostics}.}")
        elif artifact:
            lines.append(rf"\lstinputlisting[style=terminalOutput]{{{tex_path(artifact)}}}")
        else:
            lines.append(r"\textit{This output slot has no printable text representation.}")
    lines.append(interpretation)
    return "\n".join(lines)


def build() -> None:
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = {(c["notebook"], c["cell_index"]): c for c in inv["cells"]}
    notebooks = {
        "text-01-quantization.ipynb": json.loads(NB_QUANT.read_text(encoding="utf-8")),
        "text-02-LoRA.ipynb": json.loads(NB_LORA.read_text(encoding="utf-8")),
    }
    expected = {(Path(r["notebook"]).name, r["cell_index"]) for r in inv["cells"]}
    if expected != set(NARRATIVE):
        missing, extra = expected - set(NARRATIVE), set(NARRATIVE) - expected
        raise ValueError(f"Narrative coverage mismatch; missing={missing}, stale={extra}")

    out: list[str] = [
        r"\section[Quantization]{Quantization: from low-bit arithmetic to Llama inference}",
        r"\label{sec:lab05-quant}",
        r"This exercise first makes low-bit arithmetic visible on a small matrix and vector, where symmetric and asymmetric quantization can be compared directly. It then applies post-training quantization to Llama 3.2 1B, measuring serialized size and a fixed CPU generation workload across float32, PyTorch int8, and BitsAndBytes int4. The toy example isolates rounding, zero points, and accumulation overflow; the model experiment shows how these ideas behave in a real decoder-only network.",
        pipeline(["Float matrix and vector", "Absmax scale and int8 codes", "Wider accumulation", "Min-max scale and zero point", "Corrected dequantized product", "Llama size and generation comparison"]),
        r"\subsection{Absmax quantization and accumulation}",
    ]
    quant = notebooks["text-01-quantization.ipynb"]["cells"]
    for i in (3, 6, 8, 10, 12, 13, 14, 16, 18, 20, 23, 25):
        out.append(cell_tex("text-01-quantization.ipynb", "lab05/text-01-quantization.ipynb", i, quant[i], records[("lab05/text-01-quantization.ipynb", i)]))
    out += [
        r"\subsection{Min-max quantization and the zero-point correction}",
        r"Symmetric absmax mapping dedicates its range around zero, so it cannot use the extra negative int8 endpoint. Min-max mapping instead maps observed extrema to -128 and 127. With zero points $z_W$ and $z_x$, the recovered product must expand $(q_W-z_W)(q_x-z_x)$: subtract $z_x\sum q_W$ and $z_W\sum q_x$, then add $Kz_Wz_x$, where $K$ is the inner dimension. Only after this correction do we divide by both scales.",
    ]
    for i in (27, 28, 30, 32, 34, 35):
        out.append(cell_tex("text-01-quantization.ipynb", "lab05/text-01-quantization.ipynb", i, quant[i], records[("lab05/text-01-quantization.ipynb", i)]))
    out += [
        r"\subsection{Dynamic quantization on a decoder-only model}",
        r"The small arithmetic example uses toy values and cannot show storage or generation behavior at model scale. The next sequence compares a float32 baseline with two post-training representations using the same 20 prompts, greedy decoding, and 30 new tokens. All timed variants use CPU, because the PyTorch dynamic int8 path and the installed BitsAndBytes CPU backend are being compared on a common device.",
    ]
    for i in (39, 40, 42, 43, 45, 48, 50, 51, 53, 54):
        out.append(cell_tex("text-01-quantization.ipynb", "lab05/text-01-quantization.ipynb", i, quant[i], records[("lab05/text-01-quantization.ipynb", i)]))

    out += [
        r"\clearpage",
        r"\section[LoRA]{Low-Rank Adaptation: manual adapters and PEFT}",
        r"\label{sec:lab05-lora}",
        r"The second exercise adapts BERT for binary IMDB sentiment classification without updating all of its weights. The manual implementation adds rank-eight paths to the six Linear transformations in each encoder block, freezes the base model, and trains the adapters on a seeded 2,000-review subset. A second run uses Hugging Face PEFT with the same selected transformations and Trainer configuration. We compare parameter counts and held-out accuracy while keeping visible a key difference: PEFT also trains the newly initialized classification head, whereas the manual path freezes it.",
        pipeline(["Pretrained BERT", "Six target linears per layer", "Freeze base and train low-rank A/B", "Seeded IMDB split", "One-epoch evaluation", "PEFT wrapper and comparison"]),
        r"\subsection{Build and train the manual adapter}",
    ]
    lora = notebooks["text-02-LoRA.ipynb"]["cells"]
    for i in (3, 4, 7, 8, 10, 12, 14, 16, 18, 19, 20, 21, 22, 23, 24):
        out.append(cell_tex("text-02-LoRA.ipynb", "lab05/text-02-LoRA.ipynb", i, lora[i], records[("lab05/text-02-LoRA.ipynb", i)]))
    out += [
        r"\subsection{Apply the same encoder adapters with PEFT}",
        r"The PEFT path starts from a freshly loaded BERT checkpoint after the manual model is released. Its target-module list is derived from the same six encoder linears per layer. The library also keeps the sequence-classification head trainable; this adds 1,538 parameters and means the final accuracy comparison is informative but not perfectly controlled.",
    ]
    for i in (27, 29, 30, 32, 34, 36, 37, 38):
        out.append(cell_tex("text-02-LoRA.ipynb", "lab05/text-02-LoRA.ipynb", i, lora[i], records[("lab05/text-02-LoRA.ipynb", i)]))

    out += [
        r"\clearpage",
        r"\appendix",
        r"\section{Diagnostic output and earlier authentication attempt}",
        r"\label{app:lab05-diagnostics}",
        r"The complete warnings and progress-only streams omitted from the computational narrative are retained here. They remain tied to their source outputs by the coverage manifest and raw payload hashes.",
    ]
    for record in inv["cells"]:
        nb_name = Path(record["notebook"]).name
        key = (nb_name, record["cell_index"])
        for oi in DEFERRED_OUTPUTS.get(key, set()):
            output = next(o for o in record["outputs"] if o["index"] == oi)
            exported = next(o for o in record["exported_outputs"] if o["index"] == oi)
            artifact = exported.get("presentation_artifact", "")
            if artifact:
                out += [rf"\paragraph{{Diagnostic stream from {nb_name}, cell {record['cell_index']}.}}",
                        rf"\lstinputlisting[style=terminalOutput]{{{tex_path(artifact)}}}"]
    out += [
        r"\paragraph{Earlier authentication failure.} The first saved attempt stopped at the notebook's local Hugging Face authentication check. The later execution used the account's existing credential store and successfully loaded the approved checkpoint. No credential value is included here.",
        r"\begin{lstlisting}[style=terminalOutput]",
        r"RuntimeError: Llama 3.2 requires an approved Hugging Face account. Run hf auth login locally or set HF_TOKEN, then rerun.",
        r"\end{lstlisting}",
        r"\section{Execution and reproducibility notes}",
        r"No Lab05 lecture recording was available among the supplied course files. The only additional Whisper item inspected was a computer-vision lecture on object detection and segmentation, so it was excluded as unrelated. The professor's promised Laboratory 05 recording can be incorporated later. Explanations and numerical claims here follow the notebook source and its recorded executions rather than inferred lecture content.",
        r"The quantization arithmetic uses seeded toy tensors. The Llama comparison uses checkpoint revisions and exact package versions recorded in \path{lab05/execution/environment.json}; CPU timing depends on the host, thread scheduling, backend, and model-cache state. Serialized state size is not peak inference memory. The LoRA runs use a seeded 2,000/1,000 IMDB subset, microbatch four, eight-step accumulation, and one epoch. Manual training took about 810 seconds and PEFT about 814 seconds on this host. The manual path freezes the new classification head, while PEFT trains it, so the 0.658 versus 0.817 accuracy results are not an isolated causal comparison of the adapter implementations.",
    ]

    CHAPTER.parent.mkdir(parents=True, exist_ok=True)
    CHAPTER.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    WRAPPER.parent.mkdir(parents=True, exist_ok=True)
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
\hypersetup{colorlinks=true,linkcolor=politoNavy,urlcolor=steelBlue,pdftitle={Laboratory 05 complete solution},pdfauthor={Politecnico di Torino}}
\newcommand{\labSolutionTitle}{Laboratory 05: Quantization and Low-Rank Adaptation}
\newcommand{\labSolutionSubtitle}{Complete notebook-aligned solution}
\titleformat{\section}{\normalfont\sffamily\Large\bfseries\color{politoNavy}}{\thesection}{0.8em}{}
\titleformat{\subsection}{\normalfont\sffamily\large\bfseries\color{steelBlue}}{\thesubsection}{0.8em}{}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\sffamily\color{bodyGray}\nouppercase{\rightmark}}
\fancyhead[R]{\small\sffamily\bfseries\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\small\sffamily\thepage}\renewcommand{\headrulewidth}{0pt}}
\lstdefinestyle{studycode}{language=Python,basicstyle=\fontsize{7.4}{8.8}\ttfamily,keywordstyle=\bfseries\color{politoNavy},commentstyle=\itshape\color{bodyGray},stringstyle=\color{ForestGreen},numbers=left,numberstyle=\tiny\color{bodyGray},numbersep=6pt,tabsize=4,showstringspaces=false,breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true,frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg},literate={█}{{\ensuremath{\blacksquare}}}1 {▎}{{|}}1 {▋}{{|}}1 {—}{{---}}1 {’}{{'}}1}
\lstdefinestyle{terminalOutput}{basicstyle=\fontsize{7.2}{8.5}\ttfamily,breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true,showstringspaces=false,frame=single,rulecolor=\color{codeFrame},backgroundcolor=\color{codeBg},literate={█}{{\ensuremath{\blacksquare}}}1 {▎}{{|}}1 {▋}{{|}}1 {—}{{---}}1 {’}{{'}}1}
\lstset{style=studycode}
\setlist{nosep,leftmargin=1.5em}
\begin{document}
\input{../../frontmatter/solution_titlepage}
\tableofcontents
\clearpage
\input{../../chapters/05_quantization_lora.tex}
\end{document}
"""
    WRAPPER.write_text(wrapper, encoding="utf-8")
    print(f"Wrote {CHAPTER} and {WRAPPER}; {len(expected)} cells mapped")


if __name__ == "__main__":
    build()
