MAIN = main
LABS = labs
TEX_ENGINE = latexmk -pdf -interaction=nonstopmode -synctex=1

.PHONY: all lectures labs pdf clean distclean chapter lab help

all: lectures labs

pdf: lectures

lectures:
	cd lectures && $(TEX_ENGINE) $(MAIN).tex

labs:
	cd laboratories && $(TEX_ENGINE) $(LABS).tex

# Standalone single lecture chapter build: make chapter CH=part1_foundations/01_language_models_intro
chapter:
	@if [ -z "$(CH)" ]; then echo "Error: Please specify CH=part_dir/chapter (e.g. CH=part1_foundations/01_language_models_intro)"; exit 1; fi
	cd lectures/chapters/$$(dirname $(CH)) && latexmk -pdf -interaction=nonstopmode $$(basename $(CH)).tex

# Standalone single laboratory build: make lab LAB=01_pytorch_foundations
lab:
	@if [ -z "$(LAB)" ]; then echo "Error: Please specify LAB=lab_name (e.g. LAB=01_pytorch_foundations)"; exit 1; fi
	cd laboratories/chapters && latexmk -pdf -interaction=nonstopmode $$(basename $(LAB)).tex

clean:
	rm -f *.aux *.log *.toc *.out *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz *.bcf *.run.xml *.lof *.lot
	cd lectures && latexmk -c && rm -f *.aux *.log *.toc *.out *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz *.bcf *.run.xml *.lof *.lot
	cd laboratories && latexmk -c && rm -f *.aux *.log *.toc *.out *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz *.bcf *.run.xml *.lof *.lot
	find lectures/chapters -name "*.aux" -o -name "*.log" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" -o -name "*.toc" -delete
	find lectures/frontmatter -name "*.aux" -o -name "*.log" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" -delete
	find laboratories/chapters -name "*.aux" -o -name "*.log" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" -o -name "*.toc" -delete
	find laboratories/frontmatter -name "*.aux" -o -name "*.log" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" -delete

distclean: clean
	rm -f lectures/$(MAIN).pdf laboratories/$(LABS).pdf
	find lectures/chapters -name "*.pdf" -delete
	find laboratories/chapters -name "*.pdf" -delete

help:
	@echo "Politecnico di Torino - LLM4SE Study Guide Build System"
	@echo "Targets:"
	@echo "  make all       - Build both Volume I (lectures) and Volume II (laboratories)"
	@echo "  make lectures  - Build Volume I: Lecture Notes & Theory (lectures/main.pdf)"
	@echo "  make labs      - Build Volume II: Laboratory Practicum (laboratories/labs.pdf)"
	@echo "  make chapter   - Build a single lecture chapter (CH=part1_foundations/01_language_models_intro)"
	@echo "  make lab       - Build a single laboratory chapter (LAB=01_pytorch_foundations)"
	@echo "  make clean     - Clean intermediate build files"
	@echo "  make distclean - Clean all intermediate files and generated PDFs"
