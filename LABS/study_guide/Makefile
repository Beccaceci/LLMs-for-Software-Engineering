LABS = labs
TEX_ENGINE = latexmk -pdf -interaction=nonstopmode -synctex=1

.PHONY: all pdf clean distclean

all: pdf

pdf:
	$(TEX_ENGINE) $(LABS).tex

clean:
	latexmk -c
	rm -f *.aux *.log *.toc *.out *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz *.bcf *.run.xml *.lof *.lot
	find chapters -name "*.aux" -o -name "*.log" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" -o -name "*.toc" -delete
	find frontmatter -name "*.aux" -o -name "*.log" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.out" -delete

distclean: clean
	rm -f $(LABS).pdf
	find chapters -name "*.pdf" -delete
