#!/usr/bin/env bash
# ==============================================================================
# Politecnico di Torino - LLM4SE Study Guide Build Script
# ==============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -d "$PROJECT_ROOT/study_guide" ]; then
    cd "$PROJECT_ROOT/study_guide"
else
    cd "$PROJECT_ROOT"
fi

usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  (no args)               Compile entire study guide (main.tex) via latexmk"
    echo "  --chapter <path>        Compile a single standalone chapter (e.g. chapters/part1_foundations/01_language_models_intro.tex)"
    echo "  --pdflatex              Compile entire study guide using manual multi-pass pdflatex + bibtex"
    echo "  --clean                 Remove temporary auxiliary files"
    echo "  --distclean             Remove auxiliary files and generated PDFs"
    echo "  --help                  Display this help message"
}

clean_aux() {
    echo "Cleaning auxiliary files..."
    latexmk -c 2>/dev/null || true
    rm -f *.aux *.log *.toc *.out *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz *.bcf *.run.xml *.lof *.lot
    find chapters frontmatter -name "*.aux" -o -name "*.log" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" -o -name "*.toc" 2>/dev/null | xargs rm -f 2>/dev/null || true
    echo "Auxiliary files cleaned."
}

distclean() {
    clean_aux
    echo "Removing compiled PDFs..."
    rm -f main.pdf
    find chapters frontmatter -name "*.pdf" 2>/dev/null | xargs rm -f 2>/dev/null || true
    echo "Clean completed."
}

build_chapter() {
    local ch_path="$1"
    if [ ! -f "$ch_path" ]; then
        echo "Error: Chapter file '$ch_path' does not exist."
        exit 1
    fi
    local ch_dir="$(dirname "$ch_path")"
    local ch_file="$(basename "$ch_path")"
    echo "Compiling standalone chapter: $ch_path"
    (
        cd "$ch_dir"
        latexmk -pdf -interaction=nonstopmode -synctex=1 "$ch_file"
    )
    echo "Standalone chapter compiled successfully: ${ch_path%.tex}.pdf"
}

build_pdflatex() {
    echo "Running manual multi-pass pdflatex + bibtex build..."
    pdflatex -interaction=nonstopmode main.tex
    bibtex main || true
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex
    echo "Build completed: main.pdf"
}

build_main() {
    echo "Building full study guide via latexmk..."
    latexmk -pdf -interaction=nonstopmode -synctex=1 main.tex
    echo "Build completed successfully: main.pdf"
}

case "$1" in
    "")
        build_main
        ;;
    --chapter)
        if [ -z "$2" ]; then
            echo "Error: Missing chapter file argument."
            usage
            exit 1
        fi
        build_chapter "$2"
        ;;
    --pdflatex)
        build_pdflatex
        ;;
    --clean)
        clean_aux
        ;;
    --distclean)
        distclean
        ;;
    --help|-h)
        usage
        ;;
    *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
esac
