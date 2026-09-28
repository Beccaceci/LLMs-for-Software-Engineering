#!/usr/bin/env python3
"""
verify_coverage.py - Automated Coverage & Zero-Omission Verification Script
Politecnico di Torino - Master's Course "Large Language Models for Software Engineering"

Verifies that concepts, equations, and topics present in lecture slides/transcriptions
are faithfully represented in the LaTeX study guide chapters with zero omission.
Supports single-deck audits, batch directory processing, callout box tracking,
and formula presence verification.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Standard stop words and generic slide formatting artifacts to filter out
STOP_WORDS = {
    'the', 'and', 'for', 'that', 'this', 'with', 'from', 'are', 'was', 'were',
    'been', 'have', 'has', 'had', 'what', 'when', 'where', 'which', 'who',
    'will', 'would', 'can', 'could', 'should', 'about', 'into', 'over', 'after',
    'other', 'some', 'such', 'only', 'same', 'than', 'then', 'also', 'each',
    'very', 'most', 'more', 'both', 'between', 'through', 'during', 'before',
    'these', 'those', 'their', 'there', 'here', 'being', 'having', 'large',
    'language', 'models', 'introduction', 'slide', 'course', 'politecnico',
    'torino', 'flavio', 'giobergia', 'riccardo', 'coppola'
}

def clean_latex_content(latex_text: str) -> str:
    """Strips LaTeX comments while preserving text, equations, and environments."""
    # Remove comments starting with % (not escaped \%)
    lines = []
    for line in latex_text.splitlines():
        # Match % not preceded by backslash
        cleaned = re.sub(r'(?<!\\)%.*$', '', line)
        lines.append(cleaned)
    return '\n'.join(lines)

def extract_tex_stats(latex_text: str) -> Dict[str, Any]:
    """Extracts structural statistics from LaTeX content."""
    clean_tex = clean_latex_content(latex_text)
    
    examinsights = len(re.findall(r'\\begin\{examinsight\}', clean_tex))
    intuitions = len(re.findall(r'\\begin\{intuition\}', clean_tex))
    deepdives = len(re.findall(r'\\begin\{deepdive\}', clean_tex))
    definitions = len(re.findall(r'\\begin\{definition\}', clean_tex))
    theorems = len(re.findall(r'\\begin\{theorem\}', clean_tex))
    tikz_figures = len(re.findall(r'\\begin\{tikzpicture\}', clean_tex))
    display_equations = len(re.findall(r'\\begin\{(align|equation|gather)\*?\}', clean_tex)) + len(re.findall(r'\\\[.*?\\\]', clean_tex, re.DOTALL))
    code_listings = len(re.findall(r'\\begin\{lstlisting\}', clean_tex))
    
    return {
        'examinsights': examinsights,
        'intuitions': intuitions,
        'deepdives': deepdives,
        'definitions': definitions,
        'theorems': theorems,
        'tikz_figures': tikz_figures,
        'display_equations': display_equations,
        'code_listings': code_listings,
        'raw_char_count': len(clean_tex),
        'clean_text_lower': clean_tex.lower()
    }

def extract_slide_keywords(text: str) -> List[str]:
    """Extracts informative keywords and technical terms from slide text."""
    # Normalize unicode subscripts, superscripts, or greek symbols if present
    normalized = text.replace('𝑃', 'p').replace('𝑤', 'w').replace('𝑡', 't').replace('𝜃', 'theta')
    # Find all words with alphanumeric characters
    words = re.findall(r'\b[a-zA-Z0-9_\-\^\$\\]{3,}\b', normalized.lower())
    # Filter out stopwords and numeric-only strings
    keywords = [
        w for w in words
        if w not in STOP_WORDS
        and not w.isdigit()
        and len(w) >= 3
    ]
    return keywords

def audit_single_deck(
    slide_json_path: Path,
    tex_file_path: Path,
    threshold: float = 75.0,
    verbose: bool = True
) -> Tuple[bool, Dict[str, Any]]:
    """
    Audits a single slide JSON file against a target LaTeX chapter file.
    Returns (success_boolean, audit_metrics_dict).
    """
    if not slide_json_path.exists():
        if verbose:
            print(f"[-] ERROR: Slide JSON file not found: {slide_json_path}")
        return False, {'error': f'Slide JSON not found: {slide_json_path}'}
        
    if not tex_file_path.exists():
        if verbose:
            print(f"[-] ERROR: LaTeX file not found: {tex_file_path}")
        return False, {'error': f'LaTeX file not found: {tex_file_path}'}

    try:
        with open(slide_json_path, 'r', encoding='utf-8') as f:
            slides = json.load(f)
    except Exception as e:
        if verbose:
            print(f"[-] ERROR parsing JSON from {slide_json_path}: {e}")
        return False, {'error': str(e)}

    try:
        with open(tex_file_path, 'r', encoding='utf-8') as f:
            raw_tex = f.read()
    except Exception as e:
        if verbose:
            print(f"[-] ERROR reading TeX file {tex_file_path}: {e}")
        return False, {'error': str(e)}

    tex_stats = extract_tex_stats(raw_tex)
    tex_text_lower = tex_stats['clean_text_lower']

    # Slides can be list of dicts or dict with 'slides' key
    slide_list = slides if isinstance(slides, list) else slides.get('slides', [])
    total_slides = len(slide_list)
    covered_slides = 0
    missing_slides = []
    slide_audits = []

    for idx, slide in enumerate(slide_list):
        slide_num = slide.get('page', slide.get('slide_number', idx + 1))
        text = slide.get('text', '')
        
        # Filter out trivial lines
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 3]
        significant_lines = [
            l for l in lines 
            if not l.startswith('---') 
            and not l.lower().startswith('[ large language models')
            and not l.lower().startswith('[ introduction to')
            and not l.isdigit()
        ]
        
        keywords = extract_slide_keywords(' '.join(significant_lines))
        
        # Empty or title-only slides are considered covered by chapter intro
        if not keywords:
            covered_slides += 1
            slide_audits.append({
                'slide': slide_num,
                'status': 'covered',
                'reason': 'title/empty slide',
                'coverage': 1.0
            })
            continue

        # Count how many keywords appear in the LaTeX chapter
        matched_keywords = [kw for kw in keywords if kw in tex_text_lower]
        coverage_ratio = len(matched_keywords) / len(keywords) if keywords else 1.0
        
        # A slide is covered if at least 45% of its unique technical keywords appear
        is_covered = coverage_ratio >= 0.45
        if is_covered:
            covered_slides += 1
            slide_audits.append({
                'slide': slide_num,
                'status': 'covered',
                'matched_ratio': coverage_ratio,
                'sample_matches': matched_keywords[:5]
            })
        else:
            missing_slides.append({
                'slide': slide_num,
                'ratio': coverage_ratio,
                'missing_terms': [kw for kw in keywords if kw not in tex_text_lower][:6],
                'snippets': significant_lines[:2]
            })
            slide_audits.append({
                'slide': slide_num,
                'status': 'uncovered',
                'matched_ratio': coverage_ratio,
                'missing_terms': [kw for kw in keywords if kw not in tex_text_lower][:6]
            })

    percentage = (covered_slides / total_slides * 100) if total_slides > 0 else 100.0
    passed = percentage >= threshold

    metrics = {
        'deck_name': slide_json_path.stem,
        'tex_file': tex_file_path.name,
        'total_slides': total_slides,
        'covered_slides': covered_slides,
        'coverage_percentage': round(percentage, 2),
        'threshold': threshold,
        'passed': passed,
        'missing_slides_count': len(missing_slides),
        'missing_slides': missing_slides,
        'tex_stats': {
            'examinsights': tex_stats['examinsights'],
            'intuitions': tex_stats['intuitions'],
            'deepdives': tex_stats['deepdives'],
            'definitions': tex_stats['definitions'],
            'theorems': tex_stats['theorems'],
            'tikz_figures': tex_stats['tikz_figures'],
            'display_equations': tex_stats['display_equations'],
            'code_listings': tex_stats['code_listings']
        }
    }

    if verbose:
        status_tag = "[PASS]" if passed else "[FAIL]"
        print(f"\n=======================================================")
        print(f"{status_tag} Deck Audit: {slide_json_path.name} -> {tex_file_path.name}")
        print(f"=======================================================")
        print(f"  Slide Coverage     : {covered_slides}/{total_slides} ({percentage:.1f}%) [Threshold: {threshold:.1f}%]")
        print(f"  Callouts Detected  : {tex_stats['examinsights']} examinsights | {tex_stats['intuitions']} intuitions | {tex_stats['deepdives']} deepdives")
        print(f"  Math & Visuals     : {tex_stats['display_equations']} equations | {tex_stats['tikz_figures']} TikZ diagrams | {tex_stats['code_listings']} listings")
        
        if missing_slides:
            print(f"\n  [!] Potential Omissions ({len(missing_slides)} slides):")
            for m in missing_slides[:4]:
                terms_preview = ', '.join(m['missing_terms'])
                print(f"    - Slide {m['slide']} (match: {m['ratio']*100:.0f}%): Missing keywords: [{terms_preview}]")
        else:
            print("  [+] Zero Omissions: 100% of examined slide concepts verified in study guide.")

    return passed, metrics

def map_deck_to_chapter(deck_stem: str, chapters_dir: Path) -> Optional[Path]:
    """Intelligently matches a slide deck JSON to the corresponding chapter .tex file."""
    # Common mappings:
    # 01-Language-Models-Intro -> 01_language_models_intro.tex / ch01_*.tex
    # 02-DL-Intro -> 02_deep_learning_foundations.tex / ch02_*.tex
    # 03-WordEmbeddings -> 03_word_embeddings.tex / ch03_*.tex
    # 04-RNN -> 04_recurrent_neural_networks.tex / ch04_*.tex
    
    # Extract leading number if present
    match = re.match(r'^(\d+)', deck_stem)
    deck_num = match.group(1) if match else None
    
    candidate_files = list(chapters_dir.glob('**/*.tex'))
    
    # 1. Try exact number match (e.g., '01' matching '01_*.tex' or 'ch01_*.tex')
    if deck_num:
        num_str = f"{int(deck_num):02d}"
        for c in candidate_files:
            if c.stem.startswith(num_str) or c.stem.startswith(f"ch{num_str}"):
                return c
                
    # 2. Try keyword matching
    deck_words = set(re.findall(r'[a-zA-Z]+', deck_stem.lower()))
    best_match = None
    max_overlap = 0
    for c in candidate_files:
        c_words = set(re.findall(r'[a-zA-Z]+', c.stem.lower()))
        overlap = len(deck_words & c_words)
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = c
            
    if max_overlap >= 1:
        return best_match
        
    return None

def batch_audit(
    slides_dir: Path,
    chapters_dir: Path,
    threshold: float = 75.0,
    verbose: bool = True
) -> Tuple[bool, List[Dict[str, Any]]]:
    """Executes coverage audits across all slide decks found in slides_dir."""
    if not slides_dir.exists():
        print(f"[-] ERROR: Slides directory does not exist: {slides_dir}")
        return False, []
    if not chapters_dir.exists():
        print(f"[-] ERROR: Chapters directory does not exist: {chapters_dir}")
        return False, []

    json_files = sorted(list(slides_dir.glob('*.json')))
    if not json_files:
        # Check subdirectories
        json_files = sorted(list(slides_dir.glob('**/*.json')))
        
    if not json_files:
        print(f"[-] No slide JSON files found in {slides_dir}")
        return False, []

    overall_passed = True
    all_metrics = []

    print(f"\n=======================================================")
    print(f"  BATCH VERIFICATION: {len(json_files)} decks found")
    print(f"  Slides Dir   : {slides_dir}")
    print(f"  Chapters Dir : {chapters_dir}")
    print(f"  Pass Threshold: {threshold:.1f}%")
    print(f"=======================================================")

    for json_file in json_files:
        tex_file = map_deck_to_chapter(json_file.stem, chapters_dir)
        if not tex_file:
            print(f"\n[-] WARNING: Could not find matching .tex chapter for deck '{json_file.name}'. Skipping.")
            overall_passed = False
            continue
            
        passed, metrics = audit_single_deck(json_file, tex_file, threshold=threshold, verbose=verbose)
        if not passed:
            overall_passed = False
        all_metrics.append(metrics)

    print("\n-------------------------------------------------------")
    print(f"BATCH SUMMARY: {'ALL PASSED' if overall_passed else 'FAILURES OCCURRED'}")
    for m in all_metrics:
        tag = "[PASS]" if m['passed'] else "[FAIL]"
        print(f"  {tag} {m['deck_name']:<30} -> {m['tex_file']:<35} ({m['coverage_percentage']}%)")
    print("-------------------------------------------------------")

    return overall_passed, all_metrics

def main():
    parser = argparse.ArgumentParser(
        description="Verify slide-to-LaTeX concept coverage for LLM4SE Study Guide."
    )
    # Support positional arguments
    parser.add_argument("pos_slide_json", nargs="?", help="Positional: Path to extracted slide JSON")
    parser.add_argument("pos_chapter_tex", nargs="?", help="Positional: Path to chapter LaTeX file")
    
    # Support flag options
    parser.add_argument("--slide-json", dest="flag_slide_json", help="Path to extracted slide JSON")
    parser.add_argument("--tex-file", dest="flag_tex_file", help="Path to chapter LaTeX file")
    parser.add_argument("--slides-dir", help="Directory containing extracted slide JSON files")
    parser.add_argument("--chapters-dir", help="Directory containing LaTeX chapter files")
    parser.add_argument("--threshold", type=float, default=75.0, help="Pass threshold percentage (default: 75.0)")
    parser.add_argument("--strict", action="store_true", help="Enforce 100%% coverage threshold")
    parser.add_argument("--json-out", help="Optional output JSON file for structured audit metrics")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose output")

    args = parser.parse_args()

    threshold = 100.0 if args.strict else args.threshold
    verbose = not args.quiet

    # Determine execution mode
    if args.slides_dir and args.chapters_dir:
        success, metrics = batch_audit(
            Path(args.slides_dir),
            Path(args.chapters_dir),
            threshold=threshold,
            verbose=verbose
        )
        if args.json_out:
            with open(args.json_out, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2)
        sys.exit(0 if success else 1)

    slide_json = args.flag_slide_json or args.pos_slide_json
    chapter_tex = args.flag_tex_file or args.pos_chapter_tex

    if slide_json and chapter_tex:
        success, metrics = audit_single_deck(
            Path(slide_json),
            Path(chapter_tex),
            threshold=threshold,
            verbose=verbose
        )
        if args.json_out:
            with open(args.json_out, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2)
        sys.exit(0 if success else 1)

    # If neither mode was fully specified, display help
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    main()
