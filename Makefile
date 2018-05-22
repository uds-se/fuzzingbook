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

BIB = gstbook.bib

# Where to place the result
CONVERTED = converted/

# Various derived files
TEXS   = $(SOURCES:%.ipynb=$(CONVERTED)%.tex)
PDFS   = $(SOURCES:%.ipynb=$(CONVERTED)%.pdf)
HTMLS  = $(SOURCES:%.ipynb=$(CONVERTED)%.html)
SLIDES = $(SOURCES:%.ipynb=$(CONVERTED)%.slides.html)
FILES  = $(SOURCES:%.ipynb=$(CONVERTED)%_files)
PYS    = $(SOURCES:%.ipynb=%.py)


# The nbpublish tool (preferred; https://github.com/chrisjsewell/ipypublish)
# (see nbpublish -h for details)
NBPUBLISH ?= nbpublish

# The nbconvert alternative (okay for chapters; doesn't work for book)
NBCONVERT ?= jupyter nbconvert

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
CONVERT_TO_HTML   = $(NBPUBLISH) -f html_ipypublish_all
CONVERT_TO_TEX    = $(NBPUBLISH) -f latex_ipypublish_all
CONVERT_TO_SLIDES = $(NBPUBLISH) -f slides_ipypublish_all
BOOK_TEX    = $(CONVERTED)book.tex
BOOK_PDF    = $(CONVERTED)book.pdf
BOOK_HTML   = $(CONVERTED)book.html
BOOK_FILES  = $(CONVERTED)book_files
else
# Use standard Jupyter tools
HAVE_NBPUBLISH = 0
CONVERT_TO_HTML   = $(NBCONVERT) --to html --output-dir=$(CONVERTED)
CONVERT_TO_TEX    = $(NBCONVERT) --to latex --template gstbook.tplx --output-dir=$(CONVERTED)
CONVERT_TO_SLIDES = error
BOOK_TEX   = 
BOOK_PDF   = 
BOOK_HTML  = 
BOOK_FILES = 
endif

# For Python, we can always use the standard Jupyter tools
CONVERT_TO_PYTHON = $(NBCONVERT) --to python

# Short targets
# Default target is "chapters", as that's what you'd typically like to recreate after a change
chapters: html pdf

# Individual chapters
guide: $(CONVERTED)$(GUIDE).html $(CONVERTED)$(GUIDE).pdf
ch00: $(CONVERTED)$(CH00).html $(CONVERTED)$(CH00).pdf
ch01: $(CONVERTED)$(CH01).html $(CONVERTED)$(CH01).pdf
ch02: $(CONVERTED)$(CH02).html $(CONVERTED)$(CH02).pdf

# The book is recreated after any change to any source
book:	book-html book-pdf
all:	chapters book

# Individual targets
html:	$(HTMLS)
pdf:	$(PDFS)
python code:	$(PYS)
slides:	$(SLIDES)

ifeq ($(PUBLISH),nbpublish)
book-pdf:  $(BOOK_PDF)
book-html: $(BOOK_HTML)
else
book-pdf book-html:
	@echo To create the book, install ipypublish
	@echo from https://github.com/chrisjsewell/ipypublish
endif

# Invoke notebook and editor
edit jupyter notebook:
	jupyter notebook

# Help
help:
	@echo "Use 'make chapters' (default), 'make book', 'make code'"
	@echo "Generated documents are written to '$(CONVERTED)' folder"
	@echo "Code is written to current folder"
	@echo "Use make PUBLISH=(nbconvert|nbpublish) to define a converter (default: auto)"
	@echo "Use 'make clean' to cleanup"

# Conversion rules - chapters
$(CONVERTED)%.pdf:	$(CONVERTED)%.tex $(BIB)
	cd $(CONVERTED) && pdflatex $*
	-cd $(CONVERTED) && bibtex $*
	cd $(CONVERTED) && pdflatex $*
	cd $(CONVERTED) && pdflatex $*
	@cd $(CONVERTED) && $(RM) $*.aux $*.bbl $*.blg $*.log $*.out $*.toc $*.frm \
		$*.lof $*.lot
	@echo Created $@

$(CONVERTED)%.tex:	%.ipynb $(BIB)
	$(CONVERT_TO_TEX) $<
	@cd $(CONVERTED) && $(RM) $*.nbpub.log

$(CONVERTED)%.html:	%.ipynb $(BIB)
	$(CONVERT_TO_HTML) $<
	@cd $(CONVERTED) && $(RM) $*.nbpub.log

$(CONVERTED)%.slides.html:	%.ipynb $(BIB)
	$(CONVERT_TO_SLIDES) $<
	@cd $(CONVERTED) && $(RM) $*.nbpub.log

%.py:	%.ipynb
	$(CONVERT_TO_PYTHON) $<

# Conversion rules - entire book
$(CONVERTED)book.tex:	$(SOURCES) $(BIB)
	-ln -s . book
	$(CONVERT_TO_TEX) book
	@$(RM) book
	@echo Created $@

$(CONVERTED)book.html:	$(SOURCES) $(BIB)
	-ln -s . book
	$(CONVERT_TO_HTML) book
	@$(RM) book
	@echo Created $@

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

clean-code:
	$(RM) $(PYS)

clean-chapters:
	$(RM) $(TEXS) $(PDFS) $(HTMLS) $(SLIDES)
	$(RM) -r $(FILES)

clean-book:
	$(RM) $(BOOK_TEX) $(BOOK_PDF) $(BOOK_HTML)
	$(RM) -r $(BOOK_FILES)

clean-aux:
	$(RM) $(AUX)

clean: clean-code clean-chapters clean-book clean-aux
	@echo "All derived files deleted"
