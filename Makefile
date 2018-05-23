# gstbook Makefile

# Current sources.  Files starting with '_' are not included in the book.
GUIDE = _Guide_for_Authors
CH00  = ch00_Title
CH01  = ch01_Fuzzer
CH02  = ch02_Coverage

SOURCES = \
	$(GUIDE).ipynb \
	$(CH00).ipynb \
	$(CH01).ipynb \
	$(CH02).ipynb

# The bibliography file
BIB = gstbook.bib

# Where to place the pdf, html, slides
PDF_TARGET    = pdf/
HTML_TARGET   = html/
SLIDES_TARGET = slides/
CODE_TARGET   = code/

# Various derived files
TEXS   = $(SOURCES:%.ipynb=$(PDF_TARGET)%.tex)
PDFS   = $(SOURCES:%.ipynb=$(PDF_TARGET)%.pdf)
HTMLS  = $(SOURCES:%.ipynb=$(HTML_TARGET)%.html)
SLIDES = $(SOURCES:%.ipynb=$(SLIDES_TARGET)%.slides.html)
PYS    = $(SOURCES:%.ipynb=$(CODE_TARGET)%.py)

PDF_FILES     = $(SOURCES:%.ipynb=$(PDF_TARGET)%_files)
HTML_FILES    = $(SOURCES:%.ipynb=$(HTML_TARGET)%_files)
SLIDES_FILES  = $(SOURCES:%.ipynb=$(SLIDES_TARGET)%_files)

## Tools
# The nbpublish tool (preferred; https://github.com/chrisjsewell/ipypublish)
# (see nbpublish -h for details)
NBPUBLISH ?= nbpublish

# The nbconvert alternative (okay for chapters; doesn't work for book)
NBCONVERT ?= jupyter nbconvert

# LaTeX
PDFLATEX ?= pdflatex
BIBTEX ?= bibtex

ifndef PUBLISH
# Determine publishing program
OUT := $(shell which $(NBPUBLISH) > /dev/null && echo yes)
ifeq ($(OUT),yes)
# We have nbpublish
PUBLISH = nbpublish
else
# Issue a warning message
OUT := $(shell $(NBPUBLISH) -h > /dev/null)
# We have nbconvert
PUBLISH = nbconvert
endif
endif

ifeq ($(PUBLISH),nbpublish)
CONVERT_TO_HTML   = $(NBPUBLISH) -f html_ipypublish_all --outpath $(HTML_TARGET)
CONVERT_TO_TEX    = $(NBPUBLISH) -f latex_ipypublish_all --outpath $(PDF_TARGET)
# CONVERT_TO_SLIDES = $(NBPUBLISH) -f slides_ipypublish_all --outpath $(SLIDES_TARGET)
BOOK_TEX    = $(PDF_TARGET)book.tex
BOOK_PDF    = $(PDF_TARGET)book.pdf
BOOK_HTML   = $(HTML_TARGET)book.html
BOOK_HTML_FILES = $(HTML_TARGET)book_files
BOOK_PDF_FILES  = $(PDF_TARGET)book_files
else
# Use standard Jupyter tools
HAVE_NBPUBLISH = 0
CONVERT_TO_HTML   = $(NBCONVERT) --to html --output-dir=$(HTML_TARGET)
CONVERT_TO_TEX    = $(NBCONVERT) --to latex --template gstbook.tplx --output-dir=$(PDF_TARGET)
# CONVERT_TO_SLIDES = $(NBCONVERT) --to slides --output-dir=$(SLIDES_TARGET)
BOOK_TEX   = 
BOOK_PDF   = 
BOOK_HTML  = 
BOOK_HTML_FILES = 
BOOK_PDF_FILES  = 
endif

# For Python, we can always use the standard Jupyter tools
CONVERT_TO_PYTHON = $(NBCONVERT) --to python --output-dir=$(CODE_TARGET)

# For slides, we also use the standard Jupyter tools
# Main reason: Jupyter has a neat interface to control slides/sub-slides/etc
CONVERT_TO_SLIDES = $(NBCONVERT) --to slides --output-dir=$(SLIDES_TARGET)


# Short targets
# Default target is "chapters", as that's what you'd typically like to recreate after a change
chapters: html pdf code

# Individual chapters
guide: $(HTML_TARGET)$(GUIDE).html $(PDF_TARGET)$(GUIDE).pdf
ch00: $(HTML_TARGET)$(CH00).html $(PDF_TARGET)$(CH00).pdf
ch01: $(HTML_TARGET)$(CH01).html $(PDF_TARGET)$(CH01).pdf
ch02: $(HTML_TARGET)$(CH02).html $(PDF_TARGET)$(CH02).pdf

# The book is recreated after any change to any source
book:	book-html book-pdf
all:	chapters slides book

# Individual targets
html:	ipypublish-chapters $(HTMLS)
pdf:	ipypublish-chapters $(PDFS)
python code:	$(PYS)
slides:	$(SLIDES)

book-pdf:  ipypublish-book $(BOOK_PDF)
book-html: ipypublish-book $(BOOK_HTML)

ifeq ($(PUBLISH),nbpublish)
ipypublish-book:
ipypublish-chapters:
else
ipypublish-book:
	@echo "To create the book, you need the 'nbpublish' program."
	@echo "This is part of the 'ipypublish' package"
	@echo "at https://github.com/chrisjsewell/ipypublish"
ipypublish-chapters:
	@echo "Warning: Using '$(NBCONVERT)' instead of '$(NBPUBLISH)'"
	@echo "Documents will be created without citations and references"
	@echo "Install the 'ipypublish' package"
	@echo "from https://github.com/chrisjsewell/ipypublish"
endif

# Invoke notebook and editor
edit jupyter notebook:
	jupyter notebook

# Help
help:
	@echo "Use 'make chapters' (default), 'make book', 'make code'"
	@echo "Generated PDFs are written to '$(PDF_TARGET)' folder"
	@echo "Generated HTML is written to '$(PDF_HTML)' folder"
	@echo "Code is written to current folder"
	@echo "Use make PUBLISH=(nbconvert|nbpublish) to define a converter (default: auto)"
	@echo "Use 'make clean' to cleanup"

# Conversion rules - chapters
$(PDF_TARGET)%.pdf:	$(PDF_TARGET)%.tex $(BIB)
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	-cd $(PDF_TARGET) && $(BIBTEX) $*
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	@cd $(PDF_TARGET) && $(RM) $*.aux $*.bbl $*.blg $*.log $*.out $*.toc $*.frm \
		$*.lof $*.lot
	@cd $(PDF_TARGET) && $(RM) -r $*.tex $*_files
	@echo Created $@

$(PDF_TARGET)%.tex:	%.ipynb $(BIB)
	$(CONVERT_TO_TEX) $<
	@cd $(PDF_TARGET) && $(RM) $*.nbpub.log

$(HTML_TARGET)%.html:	%.ipynb $(BIB)
	$(CONVERT_TO_HTML) $<
	@cd $(HTML_TARGET) && $(RM) $*.nbpub.log $*_files/$(BIB)

$(SLIDES_TARGET)%.slides.html:	%.ipynb $(BIB)
	$(CONVERT_TO_SLIDES) $<
	@cd $(SLIDES_TARGET) && $(RM) $*.nbpub.log $*_files/$(BIB)

# For code, we comment out gstbook imports, ensuring we import a .py and not the .ipynb file
$(CODE_TARGET)%.py:	%.ipynb
	$(CONVERT_TO_PYTHON) $<
	sed 's/^import gstbook.*/# & # only in notebook/' $@ > $@~ && mv $@~ $@

# Conversion rules - entire book
$(PDF_TARGET)book.tex:	$(SOURCES) $(BIB)
	-ln -s . book
	$(CONVERT_TO_TEX) book
	$(RM) book
	cd $(PDF_TARGET) && $(RM) book.nbpub.log
	@echo Created $@

$(HTML_TARGET)book.html:	$(SOURCES) $(BIB)
	-ln -s . book
	$(CONVERT_TO_HTML) book
	$(RM) book
	cd $(HTML_TARGET) && $(RM) book.nbpub.log book_files/$(BIB)
	@echo Created $@

# Cleanup
AUX = *.aux *.bbl *.blg *.log *.out *.toc *.frm *.lof *.lot \
	  $(PDF_TARGET)*.aux \
	  $(PDF_TARGET)*.bbl \
	  $(PDF_TARGET)*.blg \
	  $(PDF_TARGET)*.log \
	  $(PDF_TARGET)*.out \
	  $(PDF_TARGET)*.toc \
	  $(PDF_TARGET)*.frm \
	  $(PDF_TARGET)*.lof \
	  $(PDF_TARGET)*.lot

clean-code:
	$(RM) $(PYS)

clean-chapters:
	$(RM) $(TEXS) $(PDFS) $(HTMLS) $(SLIDES)
	$(RM) -r $(PDF_FILES) $(HTML_FILES) $(SLIDES_FILES)

clean-book:
	$(RM) $(BOOK_TEX) $(BOOK_PDF) $(BOOK_HTML)
	$(RM) -r $(BOOK_HTML_FILES) $(BOOK_PDF_FILES)

clean-aux:
	$(RM) $(AUX)

clean: clean-code clean-chapters clean-book clean-aux
	@echo "All derived files deleted"
