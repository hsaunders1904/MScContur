
.SUFFIXES:
.SUFFIXES: .aux .bbl .pdf
.SECONDARY:

LATEX = pdflatex --shell-escape
BIBTEX = bibtex

BASENAME = simple

BIB_STEM = $(patsubst %.bbl, %, $@)
TEX_STEM = $(patsubst %.pdf, %, $@)

note:
	$(LATEX)  ${BASENAME}
	$(LATEX)  ${BASENAME}
	$(BIBTEX) ${BASENAME}
	$(LATEX)  ${BASENAME}
	$(LATEX)  ${BASENAME}

#Try and run latex only when necessary.  Hmm, dependecies on included tex files...
note: $(BASENAME).pdf

$(BASENAME).aux: $(BASENAME).tex 

%.aux: %.tex
	$(LATEX) $^

%.bbl: %.bib
	$(BIBTEX) $(BIB_STEM)
	$(LATEX) $(BIB_STEM).tex

%.pdf: %.aux %.bbl 
	$(LATEX) $(TEX_STEM).tex

clean:
	rm -f *.aux *.bbl *.dvi ${BASENAME}.pdf *.log *.blg

.PHONY: note
