# gstbook Makefile

# Current sources.  Files starting with '_' are not included in the book.
SOURCES = \
	_Guide_for_Authors.ipynb \
	ch00_Title.ipynb \
	ch01_Fuzzer.ipynb \
	ch02_Coverage.ipynb

# Where to place the result
CONVERTED = converted/

# Various derived files
TEXS   = $(SOURCES:%.ipynb=$(CONVERTED)%.tex)
PDFS   = $(SOURCES:%.ipynb=$(CONVERTED)%.pdf)
HTMLS  = $(SOURCES:%.ipynb=$(CONVERTED)%.html)
SLIDES = $(SOURCES:%.ipynb=$(CONVERTED)%.slides.html)
PYS    = $(SOURCES:%.ipynb=$(CONVERTED)%.py)
FILES  = $(SOURCES:%.ipynb=$(CONVERTED)%_files)

# Standard Jupyter tools
CONVERT_TO_PYTHON = jupyter nbconvert --to python

# Use standard Jupyter tools
# CONVERT_TO_HTML   = jupyter nbconvert --to html
# CONVERT_TO_TEX    = jupyter nbconvert --to latex --template gstbook.tplx
# BOOK_TEX   =
# BOOK_PDF   =
# BOOK_HTML  =
# BOOK_FILES =

# Use nbpublish (see nbpublish -h for details)
CONVERT_TO_HTML   = nbpublish -f html_ipypublish_all
CONVERT_TO_TEX    = nbpublish -f latex_ipypublish_all
CONVERT_TO_SLIDES = nbpublish -f slides_ipypublish_all
BOOK_TEX    = $(CONVERTED)book.tex
BOOK_PDF    = $(CONVERTED)book.pdf
BOOK_HTML   = $(CONVERTED)book.html
BOOK_FILES  = $(CONVERTED)book_files

# Short targets
all:	chapters book
chapters: pdf html
book:	book-pdf book-html
pdf:	$(PDFS)
html:	$(HTMLS)
code:	$(PYS)
slides:	$(SLIDES)
book-pdf:  $(BOOK_PDF)
book-html: $(BOOK_HTML)

edit:	
	jupyter notebook

# Conversion rules - chapters
$(CONVERTED)%.pdf:	$(CONVERTED)%.tex
	pdflatex $<
	-bibtex $*
	pdflatex $<
	pdflatex $<
	-mv $*.pdf $(CONVERTED)
	$(RM) $*.tex $*.aux $*.bbl $*.blg $*.log $*.out $*.toc

$(CONVERTED)%.tex:	%.ipynb
	$(CONVERT_TO_TEX) $<

$(CONVERTED)%.html:	%.ipynb
	$(CONVERT_TO_HTML) $<

$(CONVERTED)%.py:	%.ipynb
	$(CONVERT_TO_PYTHON) $<

# Conversion rules - entire book
$(CONVERTED)book.tex:	$(SOURCES)
	-ln -s . book
	$(CONVERT_TO_TEX) book
	$(RM) book

$(CONVERTED)book.html:	$(SOURCES)
	-ln -s . book
	$(CONVERT_TO_HTML) book
	$(RM) book

# Cleanup
AUX = *.aux *.bbl *.blg *.log *.out *.toc *.frm *.lof *.lot \
	  $(CONVERTED)*.aux \
	  $(CONVERTED)*.bbl \
	  $(CONVERTED)*.blg \
	  $(CONVERTED)*.log \
	  $(CONVERTED)*.out \
	  $(CONVERTED)*.toc \
	  $(CONVERTED)*.frm \
	  $(CONVERTED)*.lof \
	  $(CONVERTED)*.lot
	  
	  
clean:
	$(RM) $(TEXS) $(PDFS) $(HTMLS) $(SLIDES) $(PYS)
	$(RM) $(BOOK_TEX) $(BOOK_PDF) $(BOOK_HTML)
	$(RM) -r $(FILES) $(BOOK_FILES)
	$(RM) $(AUX)
