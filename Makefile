# Simple Makefile

SOURCES = \
	Guide_for_Authors.ipynb \
	ch01_Fuzzer.ipynb \
	ch02_Coverage.ipynb

TEXS  = $(SOURCES:%.ipynb=%.tex)
PDFS  = $(SOURCES:%.ipynb=%.pdf)
HTMLS = $(SOURCES:%.ipynb=%.html)
PYS   = $(SOURCES:%.ipynb=%.py)
FILES = $(SOURCES:%.ipynb=%_files)

all:	pdf html code
pdf:	$(PDFS)
html:	$(HTMLS)
code:	$(PYS)

%.pdf:	%.tex
	pdflatex $<
	-bibtex $*
	pdflatex $<
	pdflatex $<
	$(RM) $*.tex $*.aux $*.bbl $*.blg $*.log $*.out

%.tex:	%.ipynb
	jupyter nbconvert --to latex --template gstbook.tplx $<
	
%.html:	%.ipynb
	jupyter nbconvert --to html $<

%.py:	%.ipynb
	jupyter nbconvert --to python $<
	
AUX = *.aux *.bbl *.blg *.log *.out

clean:
	$(RM) $(TEXS) $(PDFS) $(HTMLS) $(PYS)
	$(RM) -r $(FILES)
	$(RM) $(AUX)
