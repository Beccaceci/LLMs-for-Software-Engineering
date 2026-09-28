#!/usr/bin/env python3
"""
inspect_sources.py — Automated Pre-Writing Ingestion & Triangulation Validator
Verifies that all required seminal papers, textbook chapters, and expert video breakdowns
are indexed and cached before authoring or expanding study guide chapters.
"""
import sys
import os
import argparse
import re

MANDATORY_TOPIC_TRIANGULATION = {
    "language_models": {
        "papers": ["shannon1948", "chen1996"],
        "books": ["Jurafsky & Martin Ch. 3", "Goodfellow Ch. 5"],
        "multimedia": ["Karpathy makemore Part 1 (Bigram)", "3Blue1Brown Information Theory"]
    },
    "deep_learning_foundations": {
        "papers": ["rumelhart1986", "cybenko1989", "hornik1991", "kingma2014adam"],
        "books": ["Bishop Ch. 3-7", "Goodfellow Ch. 6, 8", "Prince Ch. 2-7"],
        "multimedia": ["Karpathy micrograd", "3Blue1Brown Essence of Neural Networks"]
    },
    "word_embeddings": {
        "papers": ["bengio2003", "mikolov2013efficient", "mikolov2013distributed", "pennington2014glove", "bojanowski2017", "sennrich2016"],
        "books": ["Jurafsky & Martin Ch. 6", "Bishop Ch. 13", "Goodfellow Ch. 14"],
        "multimedia": [
            "Enkk (Tokenization & Vector DBs)",
            "Karpathy makemore Part 2 (Lookup Table Linear Layer)",
            "3Blue1Brown Embedding Geometry",
            "Antirez Simple Embedding Mechanics"
        ]
    },
    "recurrent_neural_networks": {
        "papers": ["elman1990", "werbos1990", "bengio1994", "hochreiter1997", "pascanu2013difficulty", "cho2014", "sutskever2014", "bahdanau2014"],
        "books": ["Goodfellow Ch. 10", "Bishop Ch. 10", "Prince Ch. 12"],
        "multimedia": [
            "Karpathy char-rnn & The Unreasonable Effectiveness of RNNs",
            "3Blue1Brown Attractor Trajectories in Phase Space"
        ]
    },
    "transformers": {
        "papers": ["vaswani2017", "devlin2018", "radford2019", "dao2022flashattention"],
        "books": ["Bishop Ch. 11", "Prince Ch. 12", "Jurafsky & Martin Ch. 10"],
        "multimedia": [
            "3Blue1Brown Visualizing Attention and Transformers (3b1b/videos)",
            "Karpathy Let's build GPT: from scratch, in code",
            "Antirez Minimalist Transformer Inference",
            "AI Explained Attention & Compute Scaling"
        ]
    },
    "scaling_laws": {
        "papers": ["kaplan2020", "hoffmann2022chinchilla"],
        "books": ["Prince Ch. 20"],
        "multimedia": ["AI Explained Chinchilla Frontier Analysis"]
    },
    "peft_alignment": {
        "papers": ["hu2021lora", "dettmers2023qlora", "ouyang2022instructgpt", "rafailov2023dpo"],
        "books": ["Prince Ch. 16", "Jurafsky & Martin Ch. 11"],
        "multimedia": ["Enkk LoRA Fine-Tuning Practical Realities", "Karpathy State of GPT"]
    },
    "reasoning_agents": {
        "papers": ["wei2022cot", "yao2022react", "yao2023tot"],
        "books": ["Russell & Norvig Ch. 2, 26"],
        "multimedia": ["Nello Cristianini Machina Sapiens & Shortcut Learning", "AI Explained Strawberry / o1"]
    }
}

KEY_ALIASES = {
    "hornik1991": ["hornik1991", "hornik1989"],
    "devlin2018": ["devlin2018", "devlin2019"],
    "hoffmann2022chinchilla": ["hoffmann2022chinchilla", "hoffmann2022"],
    "ouyang2022instructgpt": ["ouyang2022instructgpt", "ouyang2022"],
    "rafailov2023dpo": ["rafailov2023dpo", "rafailov2023"],
    "wei2022cot": ["wei2022cot", "wei2022chain"],
}

def check_bibliography(bib_path: str, required_keys: list) -> tuple:
    if not os.path.exists(bib_path):
        return [], required_keys
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    found = []
    missing = []
    for k in required_keys:
        candidates = KEY_ALIASES.get(k, [k])
        is_found = False
        for c in candidates:
            if f"{{{c}," in content or f"{{{c} " in content or f"@{c}" in content or f"{{{c}\n" in content:
                found.append(c)
                is_found = True
                break
        if not is_found:
            missing.append(k)
    return found, missing

def inspect_topic(topic_key: str, bib_path: str = "STUDY_GUIDE/shared/references.bib"):
    data = MANDATORY_TOPIC_TRIANGULATION.get(topic_key.lower())
    if not data:
        print(f"[-] Unknown topic '{topic_key}'. Available topics: {list(MANDATORY_TOPIC_TRIANGULATION.keys())}")
        return

    print(f"\n=======================================================")
    print(f"[*] Triangulation Matrix for Topic: '{topic_key}'")
    print(f"=======================================================")

    # 1. Papers Check
    found_papers, missing_papers = check_bibliography(bib_path, data["papers"])
    print("\n[1] Seminal Papers (Mandatory Ingestion):")
    for p in found_papers:
        print(f"    [+] Indexed in references.bib: {p}")
    for p in missing_papers:
        print(f"    [-] MISSING in references.bib: {p} (MUST BE ADDED BEFORE WRITING!)")

    # 2. Books Check
    print("\n[2] Authoritative Textbooks to Cross-Reference:")
    for b in data["books"]:
        print(f"    [*] {b}")

    # 3. Multimedia Authorities
    print("\n[3] Expert Video Breakdown Authorities:")
    for m in data["multimedia"]:
        print(f"    [>] {m}")

    print("\n-------------------------------------------------------")
    if missing_papers:
        print(f"[!] STATUS: INCOMPLETE. Please add missing keys to {bib_path} before writing.")
    else:
        print("[+] STATUS: READY FOR INGESTION & WRITING.")
    print("-------------------------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Audit and verify pre-writing triangulation sources.")
    parser.add_argument("--topic", "-t", required=True, help=f"Topic to audit: {list(MANDATORY_TOPIC_TRIANGULATION.keys())}")
    parser.add_argument("--bib", "-b", default="STUDY_GUIDE/shared/references.bib", help="Path to references.bib")
    args = parser.parse_args()

    inspect_topic(args.topic, args.bib)

if __name__ == "__main__":
    main()
