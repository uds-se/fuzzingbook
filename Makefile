# How to construct the individual files.  Needs ptangle and pweave.
# See http://mpastell.com/pweave/

# Main source
MAIN = gstbook

TMP = tmp

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
all:	 ${MAIN}.py ${MAIN}.pdf ${MAIN}.html
	
${MAIN}.pdf:	${MAIN}.tex
	echo > include.tex
	${PDFLATEX} -shell-escape ${LATEXOPTS} $<

${MAIN}.html:	${MAIN}.tex
	echo > include.tex
	${HTLATEX} $< "" "" "" -shell-escape ${LATEXOPTS}
	
# Recipes for ptangle, pweave, etc
%.pdf:	%.tex
	echo '\includeonly{$(basename $< .tex)}' > include.tex
	${PDFLATEX} -shell-escape ${LATEXOPTS} -jobname ${TMP} ${MAIN}.tex
	mv ${TMP}.pdf $@

# FIXME: Does not move CSS files
# FIXME: Do not overwrite gstbook.html
%.html:	%.tex
	echo '\includeonly{$(basename $< .tex)}' > include.tex
	${HTLATEX} ${MAIN}.tex "" "" "" -shell-escape ${LATEXOPTS} ${MAIN}.tex
	mv ${MAIN}.html $@

%.tex: 	%.texw
	${PWEAVE} -f texminted $<
	
%.py:	%.texw
	${PTANGLE} $<

clean:	FORCE
	${RM} ${TEMP} ${MAIN}.tex ${MAIN}.pdf ${MAIN}.html ${MAIN}.py
	
FORCE:	