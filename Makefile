# How to construct the individual files.  Needs ptangle and pweave.
# See http://mpastell.com/pweave/

# Example usages:
# make (or make all)        - Make everything
# make gstbook.pdf          - Make the whole book as one PDF
# make 01-intro.pdf         - Make one chapter as PDF
# make 01-intro.html        - Make one chapter as HTML
# make 01-intro.py          - Make one chapter's python files


# Main source
MAIN = gstbook

TMP = tmp

# Commandsx
PDFLATEX = pdflatex
HTLATEX = htlatex
PWEAVE = pweave
PTANGLE = ptangle

# Options for LaTeX
LATEXOPTS = -interaction=nonstopmode -file-line-error-style

# Temporary files
TEMP = *.4ct *.4tc *.aux *.css *.dvi *.idv *.lg *.log *.out *.tmp *.xref *x.png

# Chapters
CHAPTERS = \
	01-intro.texw \
	02-fundamentals.texw
	
# Code
CODE = ${CHAPTERS:.texw=.py}

# HTML files
HTML = ${CHAPTERS:.texw=.html}

# Default target
all:	pdf code html 
	
pdf:	${MAIN}.pdf 

py python code:	${MAIN}.py ${CODE}
	
html:	${HTML}

FORCE:	

# Main targets
${MAIN}.pdf:	${MAIN}.tex ${CHAPTERS:.texw=.tex}
	echo > include.tex
	${PDFLATEX} -shell-escape ${LATEXOPTS} $<

${MAIN}.html:	${MAIN}.tex
	echo > include.tex
	${HTLATEX} $< "" "" "" -shell-escape ${LATEXOPTS}
	
include.tex:
	touch $@

# Recipes for ptangle, pweave, etc
%.pdf:	%.tex
	echo '\includeonly{$(basename $< .tex)}' > include.tex
	${PDFLATEX} -shell-escape ${LATEXOPTS} -jobname ${TMP} ${MAIN}.tex
	mv ${TMP}.pdf $@

# FIXME: Does not move CSS files
# FIXME: Do not overwrite gstbook.html
%.html:	%.tex	${MAIN}.tex
	echo '\includeonly{$(basename $< .tex)}' > include.tex
	${HTLATEX} ${MAIN}.tex "" "" "" -shell-escape ${LATEXOPTS} ${MAIN}.tex
	mv ${MAIN}.html $@

%.tex: 	%.texw
	${PWEAVE} -f texminted $<
	
%.py:	%.texw
	${PTANGLE} $<

# Cleanup
clean:	FORCE
	${RM} ${TEMP} ${MAIN}.tex ${MAIN}.pdf ${MAIN}.html ${MAIN}.py \
	${CHAPTERS:.texw=.tex}
	
