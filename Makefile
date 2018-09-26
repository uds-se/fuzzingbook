# Fuzzingbook Makefile

# Chapters to include in the book, in this order
PUBLIC_CHAPTERS = \
	Intro_Testing.ipynb \
	Fuzzer.ipynb

# Chapters that are ready for release
READY_CHAPTERS = \
	Coverage.ipynb \
	MutationFuzzer.ipynb \
	Grammars.ipynb

# Chapters that still are work in progress
TODO_CHAPTERS = \
	GrammarFuzzer.ipynb \
	GrammarCoverageFuzzer.ipynb \

	# Parser.ipynb
	# ProbabilisticGrammarFuzzer.ipynb
	# ConstraintGrammarFuzzer.ipynb
	# APIFuzzer.ipynb
	# GUIFuzzer.ipynb
	# GrammarMiner.ipynb
	# Reducing.ipynb
	
BETA_CHAPTERS = $(READY_CHAPTERS) $(TODO_CHAPTERS)

CHAPTERS = $(PUBLIC_CHAPTERS) $(BETA_CHAPTERS)

# Additional notebooks (not to be included)
FRONTMATTER = \
	index.ipynb
APPENDICES = \
	Guide_for_Authors.ipynb \
	Template.ipynb \
	ExpectError.ipynb \
	Timer.ipynb \
	404.ipynb

# All source notebooks
SOURCE_FILES = \
	$(FRONTMATTER) \
	$(CHAPTERS) \
	$(APPENDICES)

# The bibliography file
BIB = fuzzingbook.bib

# Where the notebooks are
NOTEBOOKS = notebooks

# Derived versions with output cells
FULL_NOTEBOOKS = full_notebooks

# Git repo
GITHUB_REPO = https://github.com/uds-se/fuzzingbook/
BINDER_URL = https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks

# Sources in the notebooks folder
SOURCES = $(SOURCE_FILES:%=$(NOTEBOOKS)/%)
PUBLIC_SOURCES = $(PUBLIC_CHAPTERS:%=$(NOTEBOOKS)/%)
BETA_SOURCES = $(BETA_CHAPTERS:%=$(NOTEBOOKS)/%)

# Where to place the pdf, html, slides
PDF_TARGET      = pdf/
HTML_TARGET     = html/
SLIDES_TARGET   = slides/
CODE_TARGET     = code/
MARKDOWN_TARGET = markdown/
WORD_TARGET     = word/
EPUB_TARGET     = epub/
DEPEND_TARGET   = .depend/
DOCS_TARGET     = docs/

# If BETA=y, we create files in the "beta" subdir.  Use 'make docs-beta', 'make html-beta' to invoke
ifdef BETA
DOCS_TARGET    := docs/beta/
HTML_TARGET    := beta/$(HTML_TARGET)
SLIDES_TARGET  := beta/$(SLIDES_TARGET)
CODE_TARGET    := beta/$(CODE_TARGET)
BETA_FLAG = "--include-beta"
endif


# Various derived files
TEXS      = $(SOURCE_FILES:%.ipynb=$(PDF_TARGET)%.tex)
PDFS      = $(SOURCE_FILES:%.ipynb=$(PDF_TARGET)%.pdf)
HTMLS     = $(SOURCE_FILES:%.ipynb=$(HTML_TARGET)%.html) $(DOCS_TARGET)index.html $(DOCS_TARGET)404.html
SLIDES    = $(SOURCE_FILES:%.ipynb=$(SLIDES_TARGET)%.slides.html)
PYS       = $(SOURCE_FILES:%.ipynb=$(CODE_TARGET)%.py)
WORDS     = $(SOURCE_FILES:%.ipynb=$(WORD_TARGET)%.docx)
MARKDOWNS = $(SOURCE_FILES:%.ipynb=$(MARKDOWN_TARGET)%.md)
EPUBS     = $(SOURCE_FILES:%.ipynb=$(EPUB_TARGET)%.epub)
FULLS     = $(SOURCE_FILES:%.ipynb=$(FULL_NOTEBOOKS)/%.ipynb)
DEPENDS   = $(SOURCE_FILES:%.ipynb=$(DEPEND_TARGET)%.ipynb_depend)

CHAPTER_PYS = $(CHAPTERS:%.ipynb=$(CODE_TARGET)%.py)

PDF_FILES     = $(SOURCE_FILES:%.ipynb=$(PDF_TARGET)%_files)
HTML_FILES    = $(SOURCE_FILES:%.ipynb=$(HTML_TARGET)%_files)
SLIDES_FILES  = $(SOURCE_FILES:%.ipynb=$(SLIDES_TARGET)%_files)

# Configuration
# What we use for production: nbpublish (preferred), bookbook, or nbconvert
PUBLISH ?= nbpublish

# What we use for LaTeX: latexmk (preferred), or pdflatex
LATEX ?= latexmk

## Tools
# Python
PYTHON ?= python3

# The nbpublish tool (preferred; https://github.com/chrisjsewell/ipypublish)
# (see nbpublish -h for details)
NBPUBLISH ?= nbpublish

# The bookbook tool (okay for chapters and books; but no citations yet)
# https://github.com/takluyver/bookbook
BOOKBOOK_LATEX ?= $(PYTHON) -m bookbook.latex
BOOKBOOK_HTML  ?= $(PYTHON) -m bookbook.html

# The nbconvert alternative (okay for chapters; doesn't work for book; no citations)
NBCONVERT ?= jupyter nbconvert

# Notebook merger
NBMERGE = $(PYTHON) utils/nbmerge.py

# LaTeX
PDFLATEX ?= pdflatex
BIBTEX ?= bibtex
LATEXMK ?= latexmk
LATEXMK_OPTS ?= -pdf -quiet

# Word
PANDOC ?= pandoc

# Markdown (see https://github.com/aaren/notedown)
NOTEDOWN ?= notedown

# Style checks
PYCODESTYLE ?= pycodestyle
PYCODESTYLE_CFG = code/pycodestyle.cfg

AUTOPEP8 ?= autopep8
AUTOPEP8_CFG = code/autopep8.cfg
AUTOPEP8_OPTIONS = --global-config $(AUTOPEP8_CFG) --aggressive --in-place
NBAUTOPEP8 = $(PYTHON) utils/nbautopep8.py

# Program to open files after creating, say OPEN=open (default: ignore; "true" does nothing)
OPEN ?= true

# Make directory
MKDIR = mkdir -p

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
PUBLISH_PLUGINS = 
endif
endif

ifndef LATEX
# Determine publishing program
OUT := $(shell which $(LATEXMK) > /dev/null && echo yes)
ifeq ($(OUT),yes)
# We have latexmk
LATEX = $(LATEXMK)
else
# Issue a warning message
OUT := $(shell $(LATEXMK) -h > /dev/null)
# We have pdflatex
LATEX = $(PDFLATEX)
endif
endif


ifeq ($(PUBLISH),bookbook)
# Use bookbook
CONVERT_TO_HTML   = $(NBCONVERT) --to html --output-dir=$(HTML_TARGET)
CONVERT_TO_TEX    = $(NBCONVERT) --to latex --template fuzzingbook.tplx --output-dir=$(PDF_TARGET)
BOOK_TEX    = $(PDF_TARGET)book.tex
BOOK_PDF    = $(PDF_TARGET)book.pdf
BOOK_HTML   = $(HTML_TARGET)book.html
BOOK_HTML_FILES = $(HTML_TARGET)book_files
BOOK_PDF_FILES  = $(PDF_TARGET)book_files
PUBLISH_PLUGINS = 
else
ifeq ($(PUBLISH),nbpublish)
# Use nbpublish
CONVERT_TO_HTML   = $(NBPUBLISH) -f html_ipypublish_chapter --outpath $(HTML_TARGET)
CONVERT_TO_TEX    = $(NBPUBLISH) -f latex_ipypublish_chapter --outpath $(PDF_TARGET)
# CONVERT_TO_SLIDES = $(NBPUBLISH) -f slides_ipypublish_all --outpath $(SLIDES_TARGET)
BOOK_TEX    = $(PDF_TARGET)book.tex
BOOK_PDF    = $(PDF_TARGET)book.pdf
BOOK_HTML   = $(HTML_TARGET)book.html
BOOK_HTML_FILES = $(HTML_TARGET)book_files
BOOK_PDF_FILES  = $(PDF_TARGET)book_files
PUBLISH_PLUGINS = \
    ipypublish_plugins/html_ipypublish_chapter.py \
	ipypublish_plugins/latex_ipypublish_book.py \
	ipypublish_plugins/latex_ipypublish_chapter.py
else
# Use standard Jupyter tools
CONVERT_TO_HTML   = $(NBCONVERT) --to html --output-dir=$(HTML_TARGET)
CONVERT_TO_TEX    = $(NBCONVERT) --to latex --template fuzzingbook.tplx --output-dir=$(PDF_TARGET)
# CONVERT_TO_SLIDES = $(NBCONVERT) --to slides --output-dir=$(SLIDES_TARGET)
BOOK_TEX   = 
BOOK_PDF   = 
BOOK_HTML  = 
BOOK_HTML_FILES = 
BOOK_PDF_FILES  = 
PUBLISH_PLUGINS = 
endif
endif

# For Python, we use our own script that takes care of distinguishing 
# main (script) code from definitions to be imported
EXPORT_NOTEBOOK_CODE = fuzzingbook_utils/export_notebook_code.py 
CONVERT_TO_PYTHON = $(PYTHON) $(EXPORT_NOTEBOOK_CODE)

# This would be the Jupyter alternative
# CONVERT_TO_PYTHON = $(NBCONVERT) --to python --output-dir=$(CODE_TARGET)

# For slides, we use the standard Jupyter tools
# Main reason: Jupyter has a neat interface to control slides/sub-slides/etc
CONVERT_TO_SLIDES = $(NBCONVERT) --to slides --output-dir=$(SLIDES_TARGET)
REVEAL_JS = $(SLIDES_TARGET)reveal.js

# For Word .docx files, we start from the HTML version
CONVERT_TO_WORD = $(PANDOC) 

# For Markdown .md files, we use markdown
# Note: adding --run re-executes all code
# CONVERT_TO_MARKDOWN = $(NOTEDOWN) --to markdown
CONVERT_TO_MARKDOWN = $(NBCONVERT) --to markdown --output-dir=$(MARKDOWN_TARGET)

# Run
EXECUTE_NOTEBOOK = $(NBCONVERT) --to notebook --execute --output-dir=$(FULL_NOTEBOOKS)

# Zip
ZIP ?= zip
ZIP_OPTIONS = -r


# Short targets
# Default target is "chapters", as that's what you'd typically like to recreate after a change
chapters default: html code

# The book is recreated after any change to any source
book:	book-html book-pdf
all:	chapters pdf code slides book
and more:	word markdown epub

# Individual targets
html:	ipypublish-chapters $(HTMLS)
pdf:	ipypublish-chapters $(PDFS)
python code:	$(PYS)
slides:	$(SLIDES) $(REVEAL_JS)
word doc docx: $(WORDS)
md markdown: $(MARKDOWNS)
epub: $(EPUBS)
full-notebooks full fulls: $(FULLS)

book-pdf:  ipypublish-book $(BOOK_PDF)
book-html: ipypublish-book $(BOOK_HTML)

ifeq ($(PUBLISH),bookbook)
ipypublish-book:
ipypublish-chapters:
else
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
endif

# Invoke notebook and editor: `make jupyter lab`
edit notebook:
	jupyter notebook

lab:
	jupyter lab
	
jupyter:


# Help
help:
	@echo "Welcome to the 'fuzzingbook' Makefile!"
	@echo ""
	@echo "* make chapters (default) -> HTML and code for all chapters (notebooks)"
	@echo "* make (pdf|html|code|slides|word|markdown) -> given subcategory only"
	@echo "* make book -> entire book in PDF and HTML"
	@echo "* make all -> all inputs in all output formats"
	@echo "* make reformat -> reformat notebook Python code according to PEP8 guidelines"
	@echo "* make style -> style checker"
	@echo "* make crossref -> cross reference checker"
	@echo "* make clean -> delete all derived files"
	@echo ""
	@echo "Created files end here:"
	@echo "* PDFs -> '$(PDF_TARGET)', HTML -> '$(HTML_TARGET)', Python code -> '$(CODE_TARGET)', Slides -> '$(SLIDES_TARGET)'"
	@echo "* Web site files -> '$(DOCS_TARGET)'"
	@echo ""
	@echo "Publish:"
	@echo "* make docs -> Create public version of current documents" 
	@echo "* make beta -> Create beta version of current documents" 
	@echo "* make publish-all -> Add docs to git, preparing for publication" 
	@echo ""
	@echo "Settings:"
	@echo "* Use make PUBLISH=(nbconvert|nbpublish|bookbook) to choose a converter"
	@echo "  (default: automatic)"
	
# Run a notebook, (re)creating all output cells
ADD_METADATA = utils/add-metadata.py
NBAUTOSLIDE = utils/nbautoslide.py
$(FULL_NOTEBOOKS)/%.ipynb: $(NOTEBOOKS)/%.ipynb $(DEPEND_TARGET)%.ipynb_depend $(ADD_METADATA)
	$(EXECUTE_NOTEBOOK) $<
	$(PYTHON) $(ADD_METADATA) $@ > $@~ && mv $@~ $@
	$(PYTHON) $(NBAUTOSLIDE) --in-place $@

# Conversion rules - chapters
ifeq ($(LATEX),pdflatex)
# Use PDFLaTeX
$(PDF_TARGET)%.pdf:	$(PDF_TARGET)%.tex $(BIB)
	@echo Running LaTeX...
	@-test -L $(PDF_TARGET)PICS || ln -s ../PICS $(PDF_TARGET)
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	-cd $(PDF_TARGET) && $(BIBTEX) $*
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	@cd $(PDF_TARGET) && $(RM) $*.aux $*.bbl $*.blg $*.log $*.out $*.toc $*.frm $*.lof $*.lot $*.fls
	@cd $(PDF_TARGET) && $(RM) -r $*.tex $*_files
	@echo Created $@
	@$(OPEN) $@
else
# Use LaTeXMK
$(PDF_TARGET)%.pdf:	$(PDF_TARGET)%.tex $(BIB)
	@echo Running LaTeXMK...
	@-test -L $(PDF_TARGET)PICS || ln -s ../PICS $(PDF_TARGET)
	cd $(PDF_TARGET) && $(LATEXMK) $(LATEXMK_OPTS) $*
	@cd $(PDF_TARGET) && $(RM) $*.aux $*.bbl $*.blg $*.log $*.out $*.toc $*.frm $*.lof $*.lot $*.fls $*.fdb_latexmk
	@cd $(PDF_TARGET) && $(RM) -r $*.tex $*_files
	@echo Created $@
	@$(OPEN) $@
endif

$(PDF_TARGET)%.tex:	$(FULL_NOTEBOOKS)/%.ipynb $(BIB) $(PUBLISH_PLUGINS)
	$(CONVERT_TO_TEX) $<
	@cd $(PDF_TARGET) && $(RM) $*.nbpub.log

$(DOCS_TARGET)index.html: \
	$(FULL_NOTEBOOKS)/index.ipynb $(PUBLISH_PLUGINS) utils/post-html.py
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(HTML_TARGET) || $(MKDIR) $(HTML_TARGET)
	$(CONVERT_TO_HTML) $<
	mv $(HTML_TARGET)index.html $@
	@cd $(HTML_TARGET) && $(RM) -r index.nbpub.log index_files
	$(PYTHON) utils/post-html.py --menu-prefix=html/ --home $(BETA_FLAG) \
		--public-chapters="$(PUBLIC_SOURCES)" --beta-chapters="$(BETA_SOURCES)" $@
	@$(OPEN) $@

# https://help.github.com/articles/creating-a-custom-404-page-for-your-github-pages-site/
$(DOCS_TARGET)404.html: \
	$(FULL_NOTEBOOKS)/404.ipynb $(PUBLISH_PLUGINS) utils/post-html.py
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(HTML_TARGET) || $(MKDIR) $(HTML_TARGET)
	$(CONVERT_TO_HTML) $<
	mv $(HTML_TARGET)404.html $@
	@cd $(HTML_TARGET) && $(RM) -r 404.nbpub.log 404_files
	$(PYTHON) utils/post-html.py --menu-prefix=/html/ --home $(BETA_FLAG) \
		--public-chapters="$(PUBLIC_SOURCES)" --beta-chapters="$(BETA_SOURCES)" $@
	(echo '---'; echo 'permalink: /404.html'; echo '---'; cat $@) > $@~ && mv $@~ $@
	@$(OPEN) $@

$(HTML_TARGET)%.html: \
	$(FULL_NOTEBOOKS)/%.ipynb $(BIB) $(PUBLISH_PLUGINS) utils/post-html.py
	@test -d $(HTML_TARGET) || $(MKDIR) $(HTML_TARGET)
	$(CONVERT_TO_HTML) $<
	@cd $(HTML_TARGET) && $(RM) $*.nbpub.log $*_files/$(BIB)
	$(PYTHON) utils/post-html.py $(BETA_FLAG) \
		--public-chapters="$(PUBLIC_SOURCES)" --beta-chapters="$(BETA_SOURCES)" $@
	@-test -L $(HTML_TARGET)PICS || ln -s ../PICS $(HTML_TARGET)
	@$(OPEN) $@

$(SLIDES_TARGET)%.slides.html: $(FULL_NOTEBOOKS)/%.ipynb $(BIB)
	@test -d $(SLIDES_TARGET) || $(MKDIR) $(SLIDES_TARGET)
	$(eval TMPDIR := $(shell mktemp -d))
	sed 's/\.ipynb)/\.slides\.html)/g' $< > $(TMPDIR)/$(notdir $<)
	$(CONVERT_TO_SLIDES) $(TMPDIR)/$(notdir $<)
	@cd $(SLIDES_TARGET) && $(RM) $*.nbpub.log $*_files/$(BIB)
	@-test -L $(HTML_TARGET)PICS || ln -s ../PICS $(HTML_TARGET)
	@-$(RM) -fr $(TMPDIR)
	@$(OPEN) $@

# Rules for beta targets
ifndef BETA
beta/%:
	$(MAKE) BETA=beta $(@:beta/=)

$(DOCS_TARGET)beta/%:
	$(MAKE) BETA=beta $(@:beta/=)

%-beta:
	$(MAKE) BETA=beta $(@:-beta=)

%-all: % %-beta
	@true

beta: docs-beta
endif


# Reconstructing the reveal.js dir
$(REVEAL_JS):
	git submodule update --init


# For code, we comment out fuzzingbook imports, 
# ensuring we import a .py and not the .ipynb file
$(CODE_TARGET)%.py: $(NOTEBOOKS)/%.ipynb $(EXPORT_NOTEBOOK_CODE)
	@test -d $(CODE_TARGET) || $(MKDIR) $(CODE_TARGET)
	$(CONVERT_TO_PYTHON) $< > $@~ && mv $@~ $@
	# $(AUTOPEP8) $(AUTOPEP8_OPTIONS) $@
	-chmod +x $@


# Markdown
$(MARKDOWN_TARGET)%.md:	$(FULL_NOTEBOOKS)/%.ipynb $(BIB)
	$(RM) -r $(MARKDOWN_TARGET)$(basename $(notdir $<)).md $(MARKDOWN_TARGET)$(basename $(notdir $<))_files
	$(CONVERT_TO_MARKDOWN) $<

# For word, we convert from the HTML file
$(WORD_TARGET)%.docx: $(HTML_TARGET)%.html $(WORD_TARGET)pandoc.css
	$(PANDOC) --css=$(WORD_TARGET)pandoc.css $< -o $@

# Epub comes from the markdown file
$(EPUB_TARGET)%.epub: $(MARKDOWN_TARGET)%.md
	cd $(MARKDOWN_TARGET); $(PANDOC) -o ../$@ ../$<

# Conversion rules - entire book
# We create a book/ folder with the chapters ordered by number, 
# and let the book converters run on this
ifeq ($(PUBLISH),nbpublish)
# With nbpublish
$(PDF_TARGET)book.tex: $(FULLS) $(BIB) $(PUBLISH_PLUGINS)
	-$(RM) -r book
	$(MKDIR) book
	chapter=0; \
	for file in $(SOURCE_FILES); do \
		chnum=$$(printf "%02d" $$chapter); \
	    ln -s ../$(FULL_NOTEBOOKS)/$$file book/$$(echo $$file | sed 's/.*/Ch'$${chnum}'_&/g'); \
		chapter=$$(expr $$chapter + 1); \
	done
	ln -s ../$(BIB) book
	$(NBPUBLISH) -f latex_ipypublish_book --outpath $(PDF_TARGET) book
	$(RM) -r book
	cd $(PDF_TARGET) && $(RM) book.nbpub.log
	@echo Created $@

$(HTML_TARGET)book.html: $(FULLS) $(BIB) utils/post-html.py
	-$(RM) -r book
	$(MKDIR) book
	chapter=0; \
	for file in $(SOURCE_FILES); do \
		chnum=$$(printf "%02d" $$chapter); \
	    ln -s ../$(FULL_NOTEBOOKS)/$$file book/$$(echo $$file | sed 's/.*/Ch'$${chnum}'_&/g'); \
		chapter=$$(expr $$chapter + 1); \
	done
	ln -s ../$(BIB) book
	$(CONVERT_TO_HTML) book
	$(PYTHON) utils/nbmerge.py book/Ch*.ipynb > notebooks/book.ipynb
	$(PYTHON) utils/post-html.py $(BETA_FLAG) \
		--public-chapters="$(PUBLIC_SOURCES)" --beta-chapters="$(BETA_SOURCES)" $@
	$(RM) -r book notebooks/book.ipynb
	cd $(HTML_TARGET) && $(RM) book.nbpub.log book_files/$(BIB)
	@echo Created $@
else
# With bookbook
$(PDF_TARGET)book.tex: $(FULLS) $(BIB) $(PUBLISH_PLUGINS)
	-$(RM) -r book
	$(MKDIR) book
	chapter=0; \
	for file in $(SOURCE_FILES); do \
		chnum=$$(printf "%02d" $$chapter); \
		ln -s ../$(FULL_NOTEBOOKS)/$$file book/$$(echo $$file | sed 's/.*/'$${chnum}'-&/g'); \
		chapter=$$(expr $$chapter + 1); \
	done
	cd book; $(BOOKBOOK_LATEX)
	mv book/combined.tex $@
	$(RM) -r book
	@echo Created $@

$(HTML_TARGET)book.html: $(FULLS) $(BIB) $(PUBLISH_PLUGINS)
	-$(RM) -r book
	$(MKDIR) book
	for file in $(SOURCE_FILES); do \
	    ln -s ../$(FULL_NOTEBOOKS)/$$file book/$$(echo $$file | sed 's/[^-0-9]*\([-0-9][0-9]*\)_\(.*\)/\1-\2/g'); \
	done
	cd book; $(BOOKBOOK_HTML)
	mv book/html/index.html $@
	mv book/html/*.html $(HTML_TARGET)
	$(RM) -r book
	@echo Created $@
endif



## Some checks

# Style checks
style check-style checkstyle: $(PYS) $(PYCODESTYLE_CFG)
	$(PYCODESTYLE) --config $(PYCODESTYLE_CFG) $(PYS)
	@echo "All style checks passed."
	
# Automatic formatting
autopep8 reformat: $(PYCODESTYLE_CFG)
	$(NBAUTOPEP8) --split-cells --jobs -1 $(AUTOPEP8_OPTIONS) $(SOURCES)
	@echo "Code reformatting complete.  Use 'make full' to re-execute and test notebooks."


# List of Cross References
check-crossref crossref xref: $(SOURCES)
	@echo "Referenced notebooks (* = missing)"
	@files=$$(grep '\.ipynb)' $(SOURCES) | sed 's/.*[(]\([a-zA-Z0-9_][a-zA-Z0-9_]*\.ipynb\)[)].*/\1/' | sort | uniq); \
	for file in $$files; do \
		if [ -f $(NOTEBOOKS)/$$file ]; then \
		    echo '  ' $$file; \
		else \
			echo '* ' $$file; \
		fi \
	done

# Run all code.  This should produce no failures.
PYS_OUT = $(SOURCE_FILES:%.ipynb=$(CODE_TARGET)%.py.out)
$(CODE_TARGET)%.py.out:	$(CODE_TARGET)%.py
	$(PYTHON) $< > $@ 2>&1 || (echo "Error while running $(PYTHON)" >> $@; tail $@; exit 1)

check-code: code $(PYS_OUT)
	@grep "^Error while running" $(PYS_OUT) || echo "All code checks passed."
	
# Import all code.  This should produce no output (or error messages).
check-import: $(CODE_TARGET)import_all.py
	$(PYTHON) $< 2>&1 | tee $<.out
	@test ! -s $<.out && echo "All import checks passed."

IMPORTS = $(subst .ipynb,,$(SOURCE_FILES))
$(CODE_TARGET)import_all.py: Makefile
	echo "#!/usr/bin/env $(PYTHON)" > $@
	(for file in $(IMPORTS); do echo import $$file; done) >> $@
	-chmod +x $@

run: check-import check-code
	
# Spell checks
NBSPELLCHECK = utils/nbspellcheck.py
spell spellcheck check-spell:
	$(NBSPELLCHECK) $(SOURCES)


# All checks
check check-all: check-code check-import check-style check-crossref
	
# Add notebook metadata (add table of contents, bib reference, etc.)
metadata: $(ADD_METADATA)
	@for notebook in $(SOURCES); do \
		echo "Adding metadata to $$notebook...\c"; \
		$(PYTHON) $(ADD_METADATA) $$notebook > $$notebook~ || exit 1; \
		if diff $$notebook $$notebook~; then \
			echo "unchanged."; \
		else \
		    mv $$notebook~ $$notebook; \
			echo "done."; \
		fi; \
		$(RM) $$notebook~; \
	done



## Publishing

docs: publish-notebooks publish-html publish-code publish-code-zip \
	publish-slides publish-pics \
	$(DOCS_TARGET)index.html $(DOCS_TARGET)404.html README.md binder/postBuild
	@echo "Now use 'make publish' to commit changes to docs."

# github does not like script tags
README.md: $(MARKDOWN_TARGET)index.md
	sed 's!<script.*</script>!!g' $< > $@

publish: docs
	git add $(DOCS_TARGET)* binder/postBuild README.md
	-git status
	-git commit -m "Doc update" $(DOCS_TARGET) binder README.md
	@echo "Now use 'git push' to place docs on website,"
	@echo "and then 'make binder' to speed up binder startup"

# Add/update HTML code in repository
publish-html: html
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)html || $(MKDIR) $(DOCS_TARGET)html
	cp -pr $(HTML_TARGET) $(DOCS_TARGET)html

publish-code: code
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)code || $(MKDIR) $(DOCS_TARGET)code
	cp -pr $(CODE_TARGET) $(DOCS_TARGET)code
	$(RM) $(DOCS_TARGET)code/*.py.out $(DOCS_TARGET)code/*.cfg
	$(RM) -r $(DOCS_TARGET)code/__pycache__ \
	 	$(DOCS_TARGET)code/fuzzingbook_utils/__pycache__
	cp -p LICENSE.md $(DOCS_TARGET)code

publish-code-zip: delete-betas $(DOCS_TARGET)fuzzingbook-code.zip

$(DOCS_TARGET)fuzzingbook-code.zip: publish-code delete-betas
	$(RM) $(DOCS_TARGET)fuzzingbook-code $(DOCS_TARGET)fuzzingbook-code.zip
	$(RM) $(DOCS_TARGET)code/import-all.py
	ln -s code $(DOCS_TARGET)fuzzingbook-code
	cd $(DOCS_TARGET); $(ZIP) $(ZIP_OPTIONS) fuzzingbook-code.zip fuzzingbook-code
	$(RM) $(DOCS_TARGET)fuzzingbook-code

publish-slides: slides
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)slides || $(MKDIR) $(DOCS_TARGET)slides
	cp -pr $(SLIDES_TARGET) $(DOCS_TARGET)slides
	
publish-notebooks: full-notebooks
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)notebooks || $(MKDIR) $(DOCS_TARGET)notebooks
	cp -pr $(FULL_NOTEBOOKS)/* $(DOCS_TARGET)notebooks

publish-pics: PICS
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)PICS || $(MKDIR) $(DOCS_TARGET)PICS
	cp -pr PICS/* $(DOCS_TARGET)PICS
	$(RM) -fr $(DOCS_TARGET)notebooks/PICS; ln -s ../PICS $(DOCS_TARGET)notebooks
	$(RM) -fr $(DOCS_TARGET)html/PICS; ln -s ../PICS $(DOCS_TARGET)html
	$(RM) -fr $(DOCS_TARGET)slides/PICS; ln -s ../PICS $(DOCS_TARGET)slides

ifndef BETA
# Remove all chapters marked as beta
delete-betas: publish-code publish-html publish-slides
	@cd $(DOCS_TARGET); \
	for chapter in $(BETA_CHAPTERS); do \
	    module=$$(basename $$chapter .ipynb); \
		echo "Removing '$$module' (beta)"; \
		$(RM) code/$$module.py; \
		$(RM) html/$$module.html; \
		$(RM) -r html/$${module}_files; \
		$(RM) notebooks/$$module.ipynb; \
		$(RM) slides/$$module.slides.html; \
	done
endif

ifdef BETA
# On the beta site, we don't delete stuff
delete-betas:
endif

		

## Binder services
# custom.css
binder/postBuild: binder/postBuild.template $(HTML_TARGET)custom.css
	cat binder/postBuild.template $(HTML_TARGET)custom.css > $@
	echo END >> $@
	chmod +x $@

# Debugging binder
# This is the same system as mybinder uses, but should be easier to debug
# See https://repo2docker.readthedocs.io/en/latest/
.PRECIOUS: binder/binder.log
.FORCE:
debug-binder: binder/binder.log
binder/binder.log: .FORCE
	@echo Writing output to $@
	jupyter-repo2docker --debug $(GITHUB_REPO) 2>&1 | tee $@

# Force recreation of binder service; avoids long waiting times for first user
binder: .FORCE
	open $(BINDER_URL)


## Cleanup
AUX = *.aux *.bbl *.blg *.log *.out *.toc *.frm *.lof *.lot *.fls *.fdb_latexmk \
	  $(PDF_TARGET)*.aux \
	  $(PDF_TARGET)*.bbl \
	  $(PDF_TARGET)*.blg \
	  $(PDF_TARGET)*.log \
	  $(PDF_TARGET)*.out \
	  $(PDF_TARGET)*.toc \
	  $(PDF_TARGET)*.frm \
	  $(PDF_TARGET)*.lof \
	  $(PDF_TARGET)*.lot \
	  $(PDF_TARGET)*.fls \
	  $(PDF_TARGET)*.fdb_latexmk

clean-code:
	$(RM) $(PYS) $(PYS_OUT)

clean-chapters:
	$(RM) $(TEXS) $(PDFS) $(HTMLS) $(SLIDES) $(WORDS) $(MARKDOWNS)
	$(RM) -r $(PDF_FILES) $(HTML_FILES) $(SLIDES_FILES)

clean-book:
	$(RM) $(BOOK_TEX) $(BOOK_PDF) $(BOOK_HTML)
	$(RM) -r $(BOOK_HTML_FILES) $(BOOK_PDF_FILES)

clean-aux clean-pdf:
	$(RM) $(AUX)
	
clean-full-notebooks clean-full clean-fulls:
	$(RM) $(FULLS)

clean-docs:
	$(RM) -r $(DOCS_TARGET)html $(DOCS_TARGET)code \
	 	$(DOCS_TARGET)slides $(DOCS_TARGET)index.html $(DOCS_TARGET)404.html \ 		$(DOCS_TARGET)PICS $(DOCS_TARGET)notebooks

clean: clean-code clean-chapters clean-book clean-aux clean-docs clean-fulls
	@echo "All derived files deleted"

realclean: clean
	cd $(PDF_TARGET); $(RM) *.pdf
	cd $(HTML_TARGET); $(RM) *.html; $(RM) -r *_files
	cd $(SLIDES_TARGET); $(RM) *.html
	cd $(CODE_TARGET); $(RM) *.py*
	cd $(WORD_TARGET); $(RM) *.docx
	cd $(MARKDOWN_TARGET); $(RM) *.md
	@echo "All old files deleted"



## Dependencies - should come at the very end
# See http://make.mad-scientist.net/papers/advanced-auto-dependency-generation/ for inspiration
NBDEPEND = $(PYTHON) utils/nbdepend.py
$(DEPEND_TARGET)%.ipynb_depend: $(NOTEBOOKS)/%.ipynb
	@echo "Rebuilding $@"
	@test -d $(DEPEND_TARGET) || $(MKDIR) $(DEPEND_TARGET)
	@for import in `$(NBDEPEND) $<`; do \
		if [ -f $(NOTEBOOKS)/$$import.ipynb ]; then \
			echo '$$''(FULL_NOTEBOOKS)/$(notdir $<): $$''(NOTEBOOKS)/'"$$import.ipynb"; \
		fi; \
	done > $@
	
depend: $(DEPENDS)

include $(wildcard $(DEPENDS))
