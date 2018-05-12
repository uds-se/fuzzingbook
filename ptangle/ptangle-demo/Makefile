# How to construct the individual files.  Needs ptangle and pweave.
# See http://mpastell.com/pweave/

# Commands
PDFLATEX = pdflatex
HTLATEX = htlatex
PWEAVE = pweave
PTANGLE = ptangle

# Options for LaTeX
LATEXOPTS = -interaction=nonstopmode -file-line-error-style

# Temporary files
TEMP = *.4ct *.4tc *.aux *.css *.dvi *.idv *.lg *.log *.out *.tmp *.xref *x.png

# Default target
all:	 Delta-Debugging.py Delta-Debugging.pdf Delta-Debugging.html

# Recipes for ptangle, pweave, etc
%.pdf:	%.tex
	${PDFLATEX} -shell-escape ${LATEXOPTS} $<

%.tex: 	%.texw
	${PWEAVE} -f texminted $<

%.html:	%.tex
	${HTLATEX} $< "" "" "" -shell-escape ${LATEXOPTS}
	
%.py:	%.texw
	${PTANGLE} $<

clean:	FORCE
	${RM} ${TEMP} Delta-Debugging.tex Delta-Debugging.pdf Delta-Debugging.html Delta-Debugging.py
	
FORCE:	