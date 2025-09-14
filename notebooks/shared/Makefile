# Fuzzingbook/Debuggingbook Makefile

# HINT: This Makefile has hundreds of goals. The most important are:
# * To see the most important goals, do "make help"
# * To build the book HTML (in html/), do "make"
# * To build the book with all components (in docs/), do "make docs"

# This Makefile requires GNU make.

# Get chapter files
CHAPTERS_MAKEFILE = Chapters.makefile
include $(CHAPTERS_MAKEFILE)

# All source notebooks
SOURCE_FILES = \
	$(FRONTMATTER) \
	$(CHAPTERS) \
	$(APPENDICES) \
	$(EXTRAS)

# The bibliography file
BIB = fuzzingbook.bib

# The utilities folder
UTILS = bookutils

# The utilities in $(UTILS)
UTILITY_FILES = \
	__init__.py \
	PrettyTable.py \
	README.md \
	import_notebooks.py \
	setup.py

# Where the notebooks are
NOTEBOOKS = notebooks

# Where the shared files are
SHARED = notebooks/shared/

# Derived versions including HTML, SVG, and text output cells (for Web)
FULL_NOTEBOOKS = full_notebooks

# Derived versions including PNG and text output cells,
# but without excursions (for LaTeX and PDF)
RENDERED_NOTEBOOKS = rendered

# Git repo
GITHUB_REPO = https://github.com/uds-se/$(PROJECT)/
BINDER_URL =  https://mybinder.org/v2/gh/uds-se/$(PROJECT)/HEAD?labpath=docs/beta/notebooks/00_Table_of_Contents.ipynb
PROJECT_URL = https://www.$(PROJECT).org/beta/

# Sources in the notebooks folder
SOURCES = $(SOURCE_FILES:%=$(NOTEBOOKS)/%)
CHAPTER_SOURCES = $(CHAPTERS:%=$(NOTEBOOKS)/%)
ALL_CHAPTER_SOURCES = $(CHAPTERS:%=$(NOTEBOOKS)/%)
PUBLIC_SOURCES = $(PUBLIC_CHAPTERS:%=$(NOTEBOOKS)/%)
READY_SOURCES = $(READY_CHAPTERS:%=$(NOTEBOOKS)/%)
TODO_SOURCES = $(TODO_CHAPTERS:%=$(NOTEBOOKS)/%)
NEW_SOURCES = $(NEW_CHAPTERS:%=$(NOTEBOOKS)/%)
APPENDICES_SOURCES = $(APPENDICES:%=$(NOTEBOOKS)/%)

# Where to place the pdf, html, slides
PDF_TARGET      = pdf/
NBPDF_TARGET    = nbpdf/
HTML_TARGET     = html/
SLIDES_TARGET   = slides/
CODE_TARGET     = python_code/
MYPY_TARGET     = mypy/
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
BETA_FLAG = --include-ready --include-todo
endif
ifndef BETA
# Avoid warning: undefined variable `BETA_FLAG'
BETA_FLAG = 
endif

# Files to appear in the table of contents
ifndef BETA
CHAPTER_SOURCES := $(PUBLIC_CHAPTERS:%=$(NOTEBOOKS)/%)
endif
ifdef BETA
PUBLIC_CHAPTERS := $(CHAPTERS)
endif
TOC_CHAPTERS := $(PUBLIC_CHAPTERS)
TOC_APPENDICES = $(APPENDICES)

# Files to appear on the Web page
DOCS = \
	$(FRONTMATTER:%.ipynb=%) \
	$(TOC_CHAPTERS:%.ipynb=%) \
	$(APPENDICES:%.ipynb=%) \
	$(EXTRAS:%.ipynb=%)


# Various derived files
TEXS      = $(SOURCE_FILES:%.ipynb=$(PDF_TARGET)%.tex)
PDFS      = $(SOURCE_FILES:%.ipynb=$(PDF_TARGET)%.pdf)
NBPDFS    = $(SOURCE_FILES:%.ipynb=$(NBPDF_TARGET)%.pdf)
HTMLS     = $(SOURCE_FILES:%.ipynb=$(HTML_TARGET)%.html)
SLIDES    = $(SOURCE_FILES:%.ipynb=$(SLIDES_TARGET)%.slides.html)
PYS       = $(SOURCE_FILES:%.ipynb=$(CODE_TARGET)%.py) \
				$(CODE_TARGET)setup.py \
				$(CODE_TARGET)__init__.py
MYPYS     = $(SOURCE_FILES:%.ipynb=$(MYPY_TARGET)%.py)
WORDS     = $(SOURCE_FILES:%.ipynb=$(WORD_TARGET)%.docx)
MARKDOWNS = $(SOURCE_FILES:%.ipynb=$(MARKDOWN_TARGET)%.md)
EPUBS     = $(SOURCE_FILES:%.ipynb=$(EPUB_TARGET)%.epub)
FULLS     = $(FULL_NOTEBOOKS)/$(UTILS) \
				$(UTILITY_FILES:%=$(FULL_NOTEBOOKS)/$(UTILS)/%) \
				$(SOURCE_FILES:%.ipynb=$(FULL_NOTEBOOKS)/%.ipynb) 
RENDERS = $(SOURCE_FILES:%.ipynb=$(RENDERED_NOTEBOOKS)/%.ipynb)

DEPENDS   = $(SOURCE_FILES:%.ipynb=$(DEPEND_TARGET)%.makefile)

CHAPTER_PYS = $(CHAPTERS:%.ipynb=$(CODE_TARGET)%.py)

PDF_FILES     = $(SOURCE_FILES:%.ipynb=$(PDF_TARGET)%_files)
NBPDF_FILES   = $(SOURCE_FILES:%.ipynb=$(NBPDF_TARGET)%_files)
HTML_FILES    = $(SOURCE_FILES:%.ipynb=$(HTML_TARGET)%_files)
SLIDES_FILES  = $(SOURCE_FILES:%.ipynb=$(SLIDES_TARGET)%_files)

SITEMAP_SVG = $(NOTEBOOKS)/PICS/Sitemap.svg


# Configuration
# The site
SITE = https://www.$(PROJECT).org

# What we use for production: nbpublish (preferred), bookbook, or nbconvert
PUBLISH ?= nbpublish

# What we use for LaTeX: latexmk (preferred), or pdflatex
LATEX ?= latexmk

## Tools
# Python
PYTHON ?= python3

# Python warning level
# Turn warnings into errors unless we're in C
ifeq ($(origin CI),environment)
PYTHON_WARNLEVEL =
else
PYTHON_WARNLEVEL = -W error
endif

# Jupyter
JUPYTER ?= jupyter

# The nbpublish tool (preferred; https://github.com/chrisjsewell/ipypublish)
# (see nbpublish -h for details)
NBPUBLISH ?= \
	PYTHONPATH=$(SHARED) $(PYTHON) $(SHARED)bin/nbpublish
NBPUBLISH_OPTIONS ?= -log warning

# The bookbook tool (okay for chapters and books; but no citations yet)
# https://github.com/takluyver/bookbook
BOOKBOOK_LATEX ?= $(PYTHON) -m bookbook.latex
BOOKBOOK_HTML  ?= $(PYTHON) -m bookbook.html

# The nbconvert alternative (okay for chapters; doesn't work for book; no citations)
NBCONVERT ?= $(JUPYTER) nbconvert
NBCONVERT_OPTIONS ?= --log-level=WARN

# Notebook merger
NBMERGE = $(PYTHON) utils/nbmerge.py

# LaTeX
PDFLATEX ?= pdflatex
XELATEX ?= xelatex
BIBTEX ?= bibtex
LATEXMK ?= latexmk
LATEXMK_OPTS ?= -xelatex -quiet -f -interaction=nonstopmode

# Word
PANDOC ?= pandoc

# Markdown (see https://github.com/aaren/notedown)
NOTEDOWN ?= notedown

# Style checks
PYCODESTYLE ?= pycodestyle
PYCODESTYLE_CFG = $(CODE_TARGET)pycodestyle.cfg

AUTOPEP8 ?= autopep8
AUTOPEP8_CFG = $(CODE_TARGET)autopep8.cfg
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


# Book base name
BOOK = $(PROJECT)

ifeq ($(PUBLISH),bookbook)
# Use bookbook
CONVERT_TO_HTML   = $(NBCONVERT) $(NBCONVERT_OPTIONS) --to html --output-dir=$(HTML_TARGET)
CONVERT_TO_TEX    = $(NBCONVERT) $(NBCONVERT_OPTIONS) --to latex --template $(PROJECT).tplx --output-dir=$(PDF_TARGET)
BOOK_TEX    = $(PDF_TARGET)$(BOOK).tex
BOOK_PDF    = $(PDF_TARGET)$(BOOK).pdf
BOOK_HTML   = $(HTML_TARGET)$(BOOK).html
BOOK_HTML_FILES = $(HTML_TARGET)$(BOOK)_files
BOOK_PDF_FILES  = $(PDF_TARGET)$(BOOK)_files
PUBLISH_PLUGINS = 
else
ifeq ($(PUBLISH),nbpublish)
# Use nbpublish
CONVERT_TO_HTML   = $(NBPUBLISH) $(NBPUBLISH_OPTIONS) -f html_ipypublish_chapter --outpath $(HTML_TARGET)
CONVERT_TO_TEX    = $(NBPUBLISH) $(NBPUBLISH_OPTIONS) -f latex_ipypublish_chapter --outpath $(PDF_TARGET)
# CONVERT_TO_SLIDES = $(NBPUBLISH) $(NBPUBLISH_OPTIONS) -f slides_ipypublish_all --outpath $(SLIDES_TARGET)
BOOK_TEX    = $(PDF_TARGET)$(BOOK).tex
BOOK_PDF    = $(PDF_TARGET)$(BOOK).pdf
BOOK_HTML   = $(HTML_TARGET)$(BOOK).html
BOOK_HTML_FILES = $(HTML_TARGET)$(BOOK)_files
BOOK_PDF_FILES  = $(PDF_TARGET)$(BOOK)_files
PUBLISH_PLUGINS = \
    ipypublish_plugins/html_ipypublish_chapter.py \
	ipypublish_plugins/latex_ipypublish_book.py \
	ipypublish_plugins/latex_ipypublish_chapter.py
else
# Use standard Jupyter tools
CONVERT_TO_HTML   = $(NBCONVERT) $(NBCONVERT_OPTIONS) --to html --output-dir=$(HTML_TARGET)
CONVERT_TO_TEX    = $(NBCONVERT) $(NBCONVERT_OPTIONS) --to latex --template $(PROJECT).tplx --output-dir=$(PDF_TARGET)
# CONVERT_TO_SLIDES = $(NBCONVERT) $(NBCONVERT_OPTIONS) --to slides --output-dir=$(SLIDES_TARGET)
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
CONVERT_TO_PYTHON = PYTHONPATH=notebooks:$$PYTHONPATH \
	$(PYTHON) $(EXPORT_NOTEBOOK_CODE)

# This would be the Jupyter alternative
# CONVERT_TO_PYTHON = $(NBCONVERT) $(NBCONVERT_OPTIONS) --to python --output-dir=$(CODE_TARGET)

# For slides, we use the standard Jupyter tools
# Main reason: Jupyter has a neat interface to control slides/sub-slides/etc
CONVERT_TO_SLIDES = $(NBCONVERT) $(NBCONVERT_OPTIONS) --to slides --output-dir=$(SLIDES_TARGET)
REVEAL_JS = $(SLIDES_TARGET)reveal.js

# For Word .docx files, we start from the HTML version
CONVERT_TO_WORD = $(PANDOC) 

# For Markdown .md files, we use markdown
# Note: adding --run re-executes all code
# CONVERT_TO_MARKDOWN = $(NOTEDOWN) --to markdown
CONVERT_TO_MARKDOWN = $(NBCONVERT) $(NBCONVERT_OPTIONS) --to markdown --output-dir=$(MARKDOWN_TARGET)

# Run
# fuzzingbook/WhenToStopFuzzing needs about 120 seconds to render
# debuggingbook/Tracing may need up to 10 minutes
EXECUTE_TIMEOUT ?= 140
EXECUTE_OPTIONS ?= --ExecutePreprocessor.timeout=$(EXECUTE_TIMEOUT)
EXECUTE_NOTEBOOK = $(TIME) $(NBCONVERT) $(NBCONVERT_OPTIONS) $(EXECUTE_OPTIONS) --to notebook --execute --output-dir=$(FULL_NOTEBOOKS)

# Render
RENDER_NOTEBOOK = RENDER_HTML=1 $(NBCONVERT) $(NBCONVERT_OPTIONS) $(EXECUTE_OPTIONS) --to notebook --execute --output-dir=$(RENDERED_NOTEBOOKS)

# Refresh browser after re-creating html
REFRESH_HTML = \
osascript -e 'tell application "Safari" to set URL of document of window 1 to URL of document of window 1'

# Zip
ZIP ?= zip
ZIP_OPTIONS = -r


# Short targets
# Default target is to build everything needed for publishing,
# such that we can run "make -k" in a loop
.PHONY: chapters web default
web default: setup html code test-types test-code test-imports test-packages slides
chapters: html

# The book is recreated after any change to any source
.PHONY: book all and more
book $(PROJECT):	book-html book-pdf
all:	chapters pdf code slides book
and more:	word markdown epub

# Individual targets
.PHONY: html pdf python code slides word doc docx md markdown epub
.PHONY: full-notebooks check-notebooks full fulls rendered-notebooks rendered  renders refresh book-pdf book-html
html:	ipypublish-chapters $(HTMLS)
pdf:	ipypublish-chapters $(PDFS)
nbpdf:	ipypublish-chapters $(NBPDFS)
python code:	$(PYS)
slides: $(SLIDES) 
word doc docx: $(WORDS)
md markdown: $(MARKDOWNS)
epub: $(EPUBS)
full-notebooks check-notebooks full fulls: $(FULLS)
rendered-notebooks rendered renders: $(RENDERS)
refresh: html
	$(REFRESH_HTML)
book-pdf $(PROJECT)-pdf:  ipypublish-book $(BOOK_PDF)
book-html $(PROJECT)-html: ipypublish-book $(BOOK_HTML)

.PHONY: ipypublish-book ipypublish-chapters
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

.PHONY: edit jupyter lab notebook
# Invoke notebook and editor: `make jupyter lab`
edit notebook:
	$(JUPYTER) notebook

lab:
	$(JUPYTER) lab
	
jupyter:


# Help
.PHONY: help
help:
	@echo "Welcome to the '$(PROJECT)' Makefile!"
	@echo ""
	@echo "* make chapters (default) -> HTML and code for all chapters (notebooks)"
	@echo "* make (pdf|html|code|slides|word|markdown) -> given subcategory only"
	@echo "* make book -> entire book in PDF and HTML"
	@echo "* make all -> all inputs in all output formats"
	@echo "* make reformat -> reformat notebook Python code according to PEP8 guidelines"
	@echo "* make style -> style checker"
	@echo "* make crossref -> cross reference checker"
	@echo "* make stats -> report statistics"
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
	
# Setup repo
.PHONY: setup
setup: .gitignore
.gitignore: shared/gitignore
	$(RM) $@
	cp $< $@

# Run a notebook, (re)creating all output cells
ADD_METADATA = $(SHARED)utils/add_metadata.py
NBAUTOSLIDE = $(SHARED)utils/nbautoslide.py
NBSYNOPSIS = $(SHARED)utils/nbsynopsis.py
NBSHORTEN = $(SHARED)utils/nbshorten.py
EXPORT_NOTEBOOK_CODE = $(SHARED)utils/export_notebook_code.py 

# Commit new synopsis pics after a change (not during CI)
ifeq ($(origin CI),environment)
COMMIT_SYNOPSIS =
else
# COMMIT_SYNOPSIS = -git commit -m "Update synopsis" $(NOTEBOOKS)/PICS/*synopsis*
COMMIT_SYNOPSIS =
endif

# These notebooks can't be run under CI, as they interact with Firefox
# So we simply copy them instead
ifeq ($(origin CI),environment)
$(FULL_NOTEBOOKS)/Tracking.ipynb: $(NOTEBOOKS)/Tracking.ipynb
	cp -r $< $@
$(FULL_NOTEBOOKS)/GUIFuzzer.ipynb: $(NOTEBOOKS)/GUIFuzzer.ipynb
	cp -r $< $@
$(FULL_NOTEBOOKS)/FuzzingInTheLarge.ipynb: $(NOTEBOOKS)/FuzzingInTheLarge.ipynb
	cp -r $< $@
endif

$(FULL_NOTEBOOKS)/%.ipynb: $(NOTEBOOKS)/%.ipynb $(DEPEND_TARGET)%.makefile $(ADD_METADATA) $(NBAUTOSLIDE) $(NBSYNOPSIS)
	$(EXECUTE_NOTEBOOK) $< || $(EXECUTE_NOTEBOOK) $<
	$(PYTHON) $(ADD_METADATA) --project $(PROJECT) $@ > $@~ && mv $@~ $@
	$(PYTHON) $(NBAUTOSLIDE) --in-place $@
	$(PYTHON) $(NBSYNOPSIS) --project $(PROJECT) --update $@
	$(COMMIT_SYNOPSIS)
	
$(RENDERED_NOTEBOOKS)/%.ipynb: $(NOTEBOOKS)/%.ipynb \
	$(DEPEND_TARGET)%.makefile $(ADD_METADATA) $(NBAUTOSLIDE) \
	$(NBSYNOPSIS) $(NBSHORTEN) $(SHARED)$(UTILS)/__init__.py
	$(RENDER_NOTEBOOK) $< || $(RENDER_NOTEBOOK) $<
	$(PYTHON) $(ADD_METADATA) --project $(PROJECT) $@ > $@~ && mv $@~ $@
	$(PYTHON) $(NBAUTOSLIDE) --in-place $@
	RENDER_HTML=1 $(PYTHON) $(NBSYNOPSIS) --project $(PROJECT) --update $@
	$(COMMIT_SYNOPSIS)
	$(PYTHON) $(NBSHORTEN) --link-to "$(SITE)/html/" --in-place $@

$(FULL_NOTEBOOKS)/$(UTILS):
	$(MKDIR) $(FULL_NOTEBOOKS)/$(UTILS)

$(FULL_NOTEBOOKS)/$(UTILS)/%: $(SHARED)$(UTILS)/%
	@test -d $(FULL_NOTEBOOKS)/$(UTILS) || \
		$(MKDIR) $(FULL_NOTEBOOKS)/$(UTILS)
	cp -r $< $@



# Conversion rules - chapters
ifeq ($(LATEX),pdflatex)
# Use PDFLaTeX
$(PDF_TARGET)%.pdf:	$(PDF_TARGET)%.tex $(BIB)
	@echo Running LaTeX...
	@-test -L $(PDF_TARGET)PICS || ln -s ../$(NOTEBOOKS)/PICS $(PDF_TARGET)
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	-cd $(PDF_TARGET) && $(BIBTEX) $*
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	cd $(PDF_TARGET) && $(PDFLATEX) $*
	@cd $(PDF_TARGET) && $(RM) $*.aux $*.bbl $*.blg $*.log $*.out $*.toc $*.frm $*.lof $*.lot $*.fls
	@cd $(PDF_TARGET) && $(RM) -r $*_files
	@echo Created $@
	@$(OPEN) $@
else
# Use LaTeXMK
$(PDF_TARGET)%.pdf:	$(PDF_TARGET)%.tex $(BIB)
	@echo Running LaTeXMK...
	@-test -L $(PDF_TARGET)PICS || ln -s ../$(NOTEBOOKS)/PICS $(PDF_TARGET)
	cd $(PDF_TARGET) && $(LATEXMK) $(LATEXMK_OPTS) $*
	@cd $(PDF_TARGET) && $(RM) $*.aux $*.bbl $*.blg $*.log $*.out $*.toc $*.frm $*.lof $*.lot $*.fls $*.fdb_latexmk $*.xdv
	@echo Created $@
	@$(OPEN) $@
endif

# Keep the .tex files
.PRECIOUS: $(PDF_TARGET)%.tex

POST_TEX = utils/post_tex

$(PDF_TARGET)%.tex:	$(RENDERED_NOTEBOOKS)/%.ipynb $(BIB) $(PUBLISH_PLUGINS) $(SHARED)$(ADD_METADATA) $(SHARED)$(POST_TEX)
	$(eval TMPDIR := $(shell mktemp -d))
	$(PYTHON) $(ADD_METADATA) --project $(PROJECT) --titlepage $< > $(TMPDIR)/$(notdir $<)
	cp -r $(NOTEBOOKS)/PICS $(BIB) $(TMPDIR)
	$(CONVERT_TO_TEX) $(TMPDIR)/$(notdir $<)
	$(POST_TEX) $@ > $@~ && mv $@~ $@
	@-$(RM) -fr $(TMPDIR)
	@cd $(PDF_TARGET) && $(RM) $*.nbpub.log

# The psot-html.py script
POST_HTML ?= $(SHARED)utils/post_html.py

# Its options
POST_HTML_OPTIONS = $(BETA_FLAG) \
	--project="$(PROJECT)" \
	--title="$(BOOKTITLE)" \
	--authors="$(AUTHORS)" \
	--twitter="$(TWITTER)" \
	--mastodon="$(MASTODON)" \
	--all-chapters="$(ALL_CHAPTER_SOURCES) $(APPENDICES_SOURCES)" \
	--public-chapters="$(CHAPTER_SOURCES) $(APPENDICES_SOURCES)" \
	--ready-chapters="$(READY_SOURCES)" \
	--todo-chapters="$(TODO_SOURCES)" \
	--new-chapters="$(NEW_SOURCES)"

HTML_DEPS = $(BIB) $(PUBLISH_PLUGINS) $(POST_HTML) \
	$(CHAPTERS_MAKEFILE) $(BIBCHECK)

# Check bib
BIBER = biber
BIBCHECK = .$(BIB).ascii .$(BIB).python .$(BIB).biber 
checkbib check-bib: $(BIBCHECK)
	@echo "Check completed; $(BIB) is ok"

check-bib-ascii: .$(BIB).ascii
.$(BIB).ascii: $(BIB)
	@echo "Checking $(BIB) for 7-bit ASCII encoding"
	@if grep -Hn '[^[:print:]]' fuzzingbook.bib; then false; fi
	@touch $@

check-bib-python: .$(BIB).python
.$(BIB).python: $(BIB)
	@echo "Checking $(BIB) for Python usage with bibtexparser"
	@$(PYTHON) -c 'import bibtexparser; fd = open("$(BIB)"); bibtexparser.load(fd); fd.close()'
	@touch $@

check-bib-biber: .$(BIB).biber
.$(BIB).biber: $(BIB)
	@echo "Checking $(BIB) for LaTeX usage with Biber"
	@if which $(BIBER) > /dev/null; then $(BIBER) --tool --validate-datamodel --quiet $(BIB); else :; fi
	@$(RM) fuzzingbook_bibertool.bib fuzzingbook.bib.blg
	@touch .$(BIB).biber

.PHONY: checkbib check-bib check-bib-ascii check-bib-python check-bib-biber
	

# index.html comes with relative links (html/) such that the beta version gets the beta menu
$(DOCS_TARGET)index.html: \
	$(FULL_NOTEBOOKS)/index.ipynb $(HTML_DEPS)
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(HTML_TARGET) || $(MKDIR) $(HTML_TARGET)
	$(CONVERT_TO_HTML) $<
	mv $(HTML_TARGET)index.html $@
	@cd $(HTML_TARGET) && $(RM) -r index.nbpub.log index_files
	@$(PYTHON) $(POST_HTML) --menu-prefix=html/ --home $(POST_HTML_OPTIONS)$(HOME_POST_HTML_OPTIONS) $@
	@$(OPEN) $@

# 404.html comes with absolute links (/html/) such that it works anywhare
# https://help.github.com/articles/creating-a-custom-404-page-for-your-github-pages-site/
$(DOCS_TARGET)404.html: $(FULL_NOTEBOOKS)/404.ipynb $(HTML_DEPS)
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(HTML_TARGET) || $(MKDIR) $(HTML_TARGET)
	$(CONVERT_TO_HTML) $<
	mv $(HTML_TARGET)404.html $@
	@cd $(HTML_TARGET) && $(RM) -r 404.nbpub.log 404_files
	@$(PYTHON) $(POST_HTML) --menu-prefix=/html/ --home $(POST_HTML_OPTIONS) $@
	(echo '---'; echo 'permalink: /404.html'; echo '---'; cat $@) > $@~ && mv $@~ $@
	@$(OPEN) $@

$(DOCS_TARGET)html/00_Index.html: \
	$(DOCS_TARGET)notebooks/00_Index.ipynb $(HTML_DEPS)
	$(CONVERT_TO_HTML) $<
	@cd $(HTML_TARGET) && $(RM) -r 00_Index.nbpub.log 00_Index_files
	@cd $(DOCS_TARGET)html && $(RM) -r 00_Index.nbpub.log 00_Index_files
	mv $(HTML_TARGET)00_Index.html $@
	@$(PYTHON) $(POST_HTML) $(POST_HTML_OPTIONS) $@

$(DOCS_TARGET)html/00_Table_of_Contents.html: \
	$(DOCS_TARGET)notebooks/00_Table_of_Contents.ipynb \
	$(SITEMAP_SVG) $(HTML_DEPS) $(NBTOC)
	$(CONVERT_TO_HTML) $<
	@cd $(HTML_TARGET) && $(RM) -r 00_Table_of_Contents.nbpub.log 00_Table_of_Contents_files
	@cd $(DOCS_TARGET)html && $(RM) -r 00_Table_of_Contents.nbpub.log 00_Table_of_Contents_files
	mv $(HTML_TARGET)00_Table_of_Contents.html $@
	@$(PYTHON) $(POST_HTML) $(POST_HTML_OPTIONS) $@
	@$(OPEN) $@

$(HTML_TARGET)%.html: $(FULL_NOTEBOOKS)/%.ipynb $(HTML_DEPS)
	@test -d $(HTML_TARGET) || $(MKDIR) $(HTML_TARGET)
	$(CONVERT_TO_HTML) $<
	@cd $(HTML_TARGET) && $(RM) $*.nbpub.log $*_files/$(BIB)
	@$(PYTHON) $(POST_HTML) $(POST_HTML_OPTIONS) $@
	@if grep -i '\[unresolved citation' $@; then false; fi
	@-test -L $(HTML_TARGET)PICS || ln -s ../$(NOTEBOOKS)/PICS $(HTML_TARGET)
	@$(OPEN) $@

$(SLIDES_TARGET)%.slides.html: $(FULL_NOTEBOOKS)/%.ipynb $(BIB) $(NBSHORTEN)
	@test -d $(SLIDES_TARGET) || $(MKDIR) $(SLIDES_TARGET)
	$(eval TMPDIR := $(shell mktemp -d))
	sed 's/\.ipynb)/\.slides\.html)/g' $< > $(TMPDIR)/$(notdir $<)
	$(PYTHON) $(NBSHORTEN) --skip-slides --in-place $(TMPDIR)/$(notdir $<)
	$(CONVERT_TO_SLIDES) $(TMPDIR)/$(notdir $<)
	@cd $(SLIDES_TARGET) && $(RM) $*.nbpub.log $*_files/$(BIB)
	@-test -L $(HTML_TARGET)PICS || ln -s ../$(NOTEBOOKS)/PICS $(HTML_TARGET)
	@-$(RM) -fr $(TMPDIR)
	@$(OPEN) $@


# Rules for beta targets
.FORCE:
ifndef BETA
beta/%: .FORCE
	@$(MAKE) BETA=beta $(@:beta/=)

$(DOCS_TARGET)beta/%: .FORCE
	@$(MAKE) BETA=beta $(@:beta/=)

%-beta: .FORCE
	@$(MAKE) BETA=beta $(@:-beta=)

%-all: % %-beta
	@true

.PHONY: beta
beta: default-beta
else:
beta:
endif


# Reconstructing the reveal.js dir
.PHONY: reveal.js
$(REVEAL_JS) reveal.js: .FORCE
	@-test -d "$(REVEAL_JS)" || (cd $(SLIDES_TARGET); \
		git submodule add https://github.com/hakimel/reveal.js.git)
	git submodule update --remote
	-git commit -m "Update from source" $(REVEAL_JS)

$(CODE_TARGET)setup.py: $(CODE_TARGET)setup.py.in
	cat $< > $@
	chmod +x $@

$(CODE_TARGET)__init__.py: $(CODE_TARGET)__init__.py.in $(CHAPTERS_MAKEFILE)
	cat $< > $@
	(for module in $(IMPORTS); do echo "# from . import $$module"; done) | grep -v '^.*[0-9][0-9]_.*' >> $@
	chmod +x $@

# For code, we use our own exporter

# In our CI environment, CI=true is set
ifeq ($(origin CI),environment)
# CI mode: Create code from local notebooks,
# such that we don't have to execute the notebooks
$(CODE_TARGET)%.py: $(NOTEBOOKS)/%.ipynb $(EXPORT_NOTEBOOK_CODE)
	@test -d $(CODE_TARGET) || $(MKDIR) $(CODE_TARGET)
	$(CONVERT_TO_PYTHON) --project $(PROJECT) $< > $@~ && mv $@~ $@
	# $(AUTOPEP8) $(AUTOPEP8_OPTIONS) $@
	-chmod +x $@
else
# Normal mode: Create code from full notebooks,
# such that we get the full outputs in the synopsis
$(CODE_TARGET)%.py: $(FULL_NOTEBOOKS)/%.ipynb $(EXPORT_NOTEBOOK_CODE)
	@test -d $(CODE_TARGET) || $(MKDIR) $(CODE_TARGET)
	$(CONVERT_TO_PYTHON) --project $(PROJECT) $< > $@~ && mv $@~ $@
	# $(AUTOPEP8) $(AUTOPEP8_OPTIONS) $@
	-chmod +x $@
endif


# mypy stuff always comes directly from notebooks
mypy: $(MYPYS)
$(MYPY_TARGET)%.py: $(NOTEBOOKS)/%.ipynb $(EXPORT_NOTEBOOK_CODE)
	@test -d $(MYPY_TARGET) || $(MKDIR) $(MYPY_TARGET)
	$(CONVERT_TO_PYTHON) --project $(PROJECT) --mypy $< > $@~ && mv $@~ $@

# Markdown
$(MARKDOWN_TARGET)%.md:	$(RENDERED_NOTEBOOKS)/%.ipynb $(BIB)
	$(RM) -r $(MARKDOWN_TARGET)$(basename $(notdir $<)).md \
		$(MARKDOWN_TARGET)$(basename $(notdir $<))_files
	$(CONVERT_TO_MARKDOWN) $<

# For word, we convert from the HTML file
$(WORD_TARGET)%.docx: $(HTML_TARGET)%.html $(WORD_TARGET)pandoc.css
	$(PANDOC) --css=$(WORD_TARGET)pandoc.css $< -o $@

# Epub comes from the markdown file
$(EPUB_TARGET)%.epub: $(MARKDOWN_TARGET)%.md
	cd $(MARKDOWN_TARGET); $(PANDOC) -o ../$@ ../$<
	

# NBPDF files - generated from HMTL, with embedded notebooks
# See instructions at https://github.com/betatim/notebook-as-pdf
HTMLTONBPDF = $(SHARED)utils/htmltonbpdf.py

$(NBPDF_TARGET)%.pdf:  $(HTML_TARGET)/%.html $(RENDERED_NOTEBOOKS)/%.ipynb $(HTMLTONBPDF) $(HTML_TARGET)custom.css
	@test -d $(NBPDF_TARGET) || $(MKDIR) $(NBPDF_TARGET)
	$(PYTHON) $(HTMLTONBPDF) --attach --fix-html-links $${PWD}/$(HTML_TARGET)$(basename $(notdir $<)).html $(RENDERED_NOTEBOOKS)/$(basename $(notdir $<)).ipynb $@
	sed "s!$(HTML_TARGET)!$(NBPDF_TARGET)!g" $@ > $@~ && mv $@~ $@


# Conversion rules - entire book
# We create a fuzzingbook/ or debuggingbook/ folder 
# with the chapters ordered by number, 
# and let the fuzzingbook converters run on this
ifeq ($(PUBLISH),nbpublish)
# With nbpublish
$(PDF_TARGET)$(BOOK).tex: $(RENDERS) $(BIB) $(PUBLISH_PLUGINS) $(CHAPTERS_MAKEFILE)
	-$(RM) -r $(BOOK)
	$(MKDIR) $(BOOK)
	chapter=0; \
	for file in $(SOURCE_FILES); do \
		chnum=$$(printf "%02d" $$chapter); \
	    ln -s ../$(RENDERED_NOTEBOOKS)/$$file $(BOOK)/$$(echo $$file | sed 's/.*/Ch'$${chnum}'_&/g'); \
		chapter=$$(expr $$chapter + 1); \
	done
	ln -s ../$(BIB) $(BOOK)
	$(NBPUBLISH) $(NBPUBLISH_OPTIONS) -f latex_ipypublish_book --outpath $(PDF_TARGET) $(BOOK)
	$(POST_TEX) $@ > $@~ && mv $@~ $@
	$(RM) -r $(BOOK)
	cd $(PDF_TARGET) && $(RM) $(BOOK).nbpub.log
	@echo Created $@

$(HTML_TARGET)$(BOOK).html: $(FULLS) $(BIB) $(POST_HTML)
	-$(RM) -r $(BOOK)
	$(MKDIR) $(BOOK)
	chapter=0; \
	for file in $(SOURCE_FILES); do \
		chnum=$$(printf "%02d" $$chapter); \
	    ln -s ../$(FULL_NOTEBOOKS)/$$file $(BOOK)/$$(echo $$file | sed 's/.*/Ch'$${chnum}'_&/g'); \
		chapter=$$(expr $$chapter + 1); \
	done
	ln -s ../$(BIB) $(BOOK)
	$(CONVERT_TO_HTML) $(BOOK)
	$(PYTHON) $(SHARED)utils/nbmerge.py $(BOOK)/Ch*.ipynb > notebooks/$(BOOK).ipynb
	@$(PYTHON) $(POST_HTML) $(BETA_FLAG) $(POST_HTML_OPTIONS) $@
	$(RM) -r $(BOOK) notebooks/$(BOOK).ipynb
	cd $(HTML_TARGET) && $(RM) $(BOOK).nbpub.log $(BOOK)_files/$(BIB)
	@echo Created $@
else
# With bookbook
$(PDF_TARGET)$(BOOK).tex: $(RENDERS) $(BIB) $(PUBLISH_PLUGINS) $(CHAPTERS_MAKEFILE)
	-$(RM) -r $(BOOK)
	$(MKDIR) $(BOOK)
	chapter=0; \
	for file in $(SOURCE_FILES); do \
		chnum=$$(printf "%02d" $$chapter); \
		ln -s ../$(RENDERED_NOTEBOOKS)/$$file book/$$(echo $$file | sed 's/.*/'$${chnum}'-&/g'); \
		chapter=$$(expr $$chapter + 1); \
	done
	cd book; $(BOOKBOOK_LATEX)
	mv book/combined.tex $@
	$(POST_TEX) $@ > $@~ && mv $@~ $@
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


## Jupyter Book (experimental)
JUPYTER_BOOK = jupyter-book
jb jupyter-book: $(JB_LINKS) _build/index.html
jb-links: $(JB_LINKS)

JB_LINKS = $(FULL_NOTEBOOKS)/_config.yml $(FULL_NOTEBOOKS)/_toc.yml $(FULL_NOTEBOOKS)/_build

$(FULL_NOTEBOOKS)/_config.yml: _config.yml
	cd $(FULL_NOTEBOOKS); ln -s ../_config.yml .

$(FULL_NOTEBOOKS)/_toc.yml: _toc.yml
	cd $(FULL_NOTEBOOKS); ln -s ../_toc.yml .

$(FULL_NOTEBOOKS)/_build: _build
	cd $(FULL_NOTEBOOKS); ln -s ../_build .

_build/index.html: $(FULLS)
	cd $(FULL_NOTEBOOKS); $(JUPYTER_BOOK) build .


## Some checks

# Style checks
.PHONY: style check-style checkstyle
style check-style checkstyle: $(PYS) $(PYCODESTYLE_CFG)
	$(PYCODESTYLE) --config $(PYCODESTYLE_CFG) $(PYS)
	@echo "All style checks passed."
	
# Automatic formatting
.PHONY: autopep8 reformat
autopep8 reformat: $(PYCODESTYLE_CFG)
	$(NBAUTOPEP8) --split-cells --jobs -1 $(AUTOPEP8_OPTIONS) $(SOURCES)
	@echo "Code reformatting complete.  Use 'make full' to re-execute and test notebooks."


# List of Cross References
.PHONY: check-crossref crossref xref
check-crossref crossref xref: $(SOURCES)
	@echo "Referenced notebooks (* = missing)"
	@files=$$(grep '\.ipynb)' $(SOURCES) | sed 's/.*[(]\([a-zA-Z0-9_][a-zA-Z0-9_-]*\.ipynb\)[)].*/\1/' | grep -v http | sort | uniq); \
	for file in $$files; do \
		if [ -f $(NOTEBOOKS)/$$file ]; then \
		    echo '  ' $$file; \
		else \
			echo '* ' $$file "- in" $$(cd $(NOTEBOOKS); grep -l $$file $(SOURCE_FILES)); \
		fi \
	done


# Stats
.PHONY: stats
stats: $(SOURCES)
	@cd $(NOTEBOOKS); ../$(SHARED)utils/nbstats.py $(SOURCE_FILES)

# Run all code.  This should produce no failures.
PY_SUCCESS_MAGIC = "--- Code check passed ---"
PYS_OUT = $(SOURCE_FILES:%.ipynb=$(CODE_TARGET).%.py.out)
$(CODE_TARGET).%.py.out:	$(CODE_TARGET)%.py
	@echo Running $<...
	@if $(PYTHON) $(PYTHON_WARNLEVEL) $< > $@ 2>&1; then \
		echo $(PY_SUCCESS_MAGIC) >> $@; \
		exit 0; \
	else \
	    echo Re-running $<...; \
	    if $(PYTHON) $(PYTHON_WARNLEVEL) $< > $@ 2>&1; then \
		    echo $(PY_SUCCESS_MAGIC) >> $@; \
		    exit 0; \
		else \
			echo "Error while running $<" >> $@; \
			tail $@; \
			touch -r $< -A -010000 $@ 2> /dev/null || touch -r $< --date='-1 hour' $@; \
			exit 1; \
		fi; \
	fi


# No need to check if these work; they are not run by users anyway
$(CODE_TARGET).Tracking.py.out: $(CODE_TARGET)Tracking.py
	@echo Skipping $<...
	@echo $(PY_SUCCESS_MAGIC) > $@

# These still need to be fixed
$(CODE_TARGET).Alhazen.py.out: $(CODE_TARGET)Alhazen.py
	@echo Skipping $<...
	@echo $(PY_SUCCESS_MAGIC) > $@
$(CODE_TARGET).Slicer.py.out: $(CODE_TARGET)Slicer.py
	@echo Skipping $<...
	@echo $(PY_SUCCESS_MAGIC) > $@
$(CODE_TARGET).IllustratedCode.py.out: $(CODE_TARGET)IllustratedCode.py
	@echo Skipping $<...
	@echo $(PY_SUCCESS_MAGIC) > $@


.PHONY: test-code
test-code: code $(PYS_OUT)

.PHONY: check-code
check-code: test-code
	@files_with_errors=$$(grep --files-without-match -- $(PY_SUCCESS_MAGIC) $(PYS_OUT)); \
	if [ -z "$$files_with_errors" ]; then \
		echo "All code checks passed."; \
	else \
		echo "Check these files for errors: $$files_with_errors"; \
		exit 1; \
	fi

# Import all code.  This should produce no output (or error messages).
IMPORTS = $(subst .ipynb,,$(CHAPTERS) $(APPENDICES))
IMPORTS_OUT = $(CODE_TARGET).import_all.py.out

.PHONY: test-import test-imports
test-import test-imports: code $(IMPORTS_OUT)

.PHONY: check-import check-imports
check-import check-imports: test-imports
	@echo "All import checks passed."

$(IMPORTS_OUT): $(PYS)
	@echo "#!/usr/bin/env $(PYTHON)" > import_all.py
	@(for module in $(IMPORTS); do echo import code.$$module; done) | grep -v '^.*[0-9][0-9]_.*' >> import_all.py
	$(PYTHON) import_all.py 2>&1 | tee $@
	@$(RM) import_all.py
	@test ! -s $@
	
# Same as above, but using Python standard packages only; import should work too
check-standard-imports: code
	# PYTHONPATH= $(MAKE) check-imports

PACKAGES_OUT = $(CODE_TARGET).import_packages.py.out
.PHONY: test-packages
test-packages: $(PACKAGES_OUT)

check-package check-packages: test-packages
	@echo "Package check passed."

$(PACKAGES_OUT): $(PYS)
	@echo "#!/usr/bin/env $(PYTHON)" > import_packages.py
	@(for module in $(IMPORTS); do echo import code.$$module; done) | grep -v '^import code.[0-9][0-9]' >> import_packages.py
	$(PYTHON) import_packages.py 2>&1 | tee $@
	@$(RM) import_packages.py
	@test ! -s $@


# Static type checking
MYPY = mypy 
# MYPYS = $(SOURCE_FILES:%.ipynb=$(MYPY_TARGET)%.py)
MYPYS_OUT = $(SOURCE_FILES:%.ipynb=$(MYPY_TARGET).%.py.out)
$(MYPY_TARGET).%.py.out: $(MYPY_TARGET)%.py $(MYPY_TARGET)mypy.ini
	@echo Type-checking $<...
	@if $(MYPY) --config-file $(MYPY_TARGET)mypy.ini $< > $@ 2>&1; then \
		echo $(PY_SUCCESS_MAGIC) >> $@; \
		exit 0; \
	else \
		echo "Error type checking $<" >> $@; \
		cat $@; \
		touch -r $< $@; \
		touch -A -010000 $@; \
		exit 1; \
	fi

UTILS_MYPY_OUT = $(MYPY_TARGET).$(UTILS).py.out
$(UTILS_MYPY_OUT): $(UTILITY_FILES:%=$(SHARED)$(UTILS)/%) $(MYPY_TARGET)mypy.ini
	@echo Type-checking $(SHARED)$(UTILS)...
	@if $(MYPY) --config-file $(MYPY_TARGET)mypy.ini --follow-imports=skip $(SHARED)$(UTILS) > $@ 2>&1; then \
		echo $(PY_SUCCESS_MAGIC) >> $@; \
		exit 0; \
	else \
		echo "Error type checking $<" >> $@; \
		cat $@; \
		touch -r $< $@; \
		touch -A -010000 $@; \
		exit 1; \
	fi

test-types: $(SOURCE_FILES:%.ipynb=$(MYPY_TARGET)%.py) \
	$(UTILS_MYPY_OUT) $(MYPYS_OUT)

check-types: test-types
	@files_with_errors=$$(grep --files-without-match -- $(PY_SUCCESS_MAGIC) $(MYPYS_OUT) $(UTILS_MYPY_OUT)); \
	if [ -z "$$files_with_errors" ]; then \
		echo "All type checks passed."; \
	else \
		echo "Check these files for errors: $$files_with_errors"; \
		exit 1; \
	fi
	
# These still need to be fixed
$(MYPY_TARGET).Alhazen.py.out: $(MYPY_TARGET)Alhazen.py
	@echo Skipping $<...
	@echo $(PY_SUCCESS_MAGIC) > $@


.PHONY: run
run: check-types check-imports check-standard-imports check-package check-code

# Todo checks
check-todo todo:
	@grep '\\todo' $(ALL_CHAPTER_SOURCES); \
	if [ $$? = 0 ]; then exit 1; else \
	echo "No todos in $(PUBLIC_CHAPTERS:%.ipynb=%) $(READY_CHAPTERS:%.ipynb=%)"; exit 0; fi

# Spell checks
NBSPELLCHECK = $(SHARED)utils/nbspellcheck.py
.PHONY: spell spellcheck check-spell
spell spellcheck check-spell:
	$(NBSPELLCHECK) $(SOURCES)


# All checks
.PHONY: check check-all
check check-all: check-import check-package check-types check-code check-style check-crossref check-todo
	
# Add notebook metadata (add table of contents, bib reference, etc.)
.PHONY: metadata
metadata: $(ADD_METADATA)
	@for notebook in $(SOURCES); do \
		echo "Adding metadata to $$notebook...\c"; \
		$(PYTHON) $(ADD_METADATA) --project $(PROJECT) $$notebook > $$notebook~ || exit 1; \
		if diff $$notebook $$notebook~; then \
			echo "unchanged."; \
		else \
		    mv $$notebook~ $$notebook; \
			echo "done."; \
		fi; \
		$(RM) $$notebook~; \
	done


## Publishing
.PHONY: docs
docs: publish-notebooks publish-index publish-html publish-code publish-dist \
	publish-slides publish-pics \
	$(DOCS_TARGET)index.html $(DOCS_TARGET)404.html README.md binder/postBuild
	@echo "Now use 'make publish-all' to commit changes to docs."

# github does not like script and iframe tags;
# links to notebooks need to get adapted
README.md: $(MARKDOWN_TARGET)index.md Makefile BADGES.md
	sed 's!<script.*</script>!!g' $< | \
	sed '/<iframe.*/,/.*<\/iframe>/d' | \
	sed 's!(\([_a-zA-Z0-9]*\).ipynb)!($(SITE)/html/\1.html)!g'> $@~
	cat BADGES.md $@~ > $@
	$(RM) $@~

.PHONY: publish
publish: run quick-publish
quick-publish: docs
	git add $(DOCS_TARGET)* binder/postBuild README.md \
		 $(NOTEBOOKS)/PICS/*-synopsis-*
	-git status
	-git commit -m "Doc update" 
	@echo "Now use 'make push' to place docs on website and trigger a mybinder update"

# Add/update HTML code in Web pages
.PHONY: publish-html publish-html-setup
publish-html: html publish-html-setup \
	$(DOCS_TARGET)html/00_Index.html \
	$(DOCS_TARGET)html/00_Table_of_Contents.html \
	$(DOCS_TARGET)html/custom.css \
	$(DOCS_TARGET)html/mastodon-timeline.css \
	$(DOCS_TARGET)html/mastodon-timeline.js \
	$(DOCS:%=$(DOCS_TARGET)html/%.html) \
	$(DOCS:%=$(DOCS_TARGET)html/%_files)

publish-html-setup:
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)html || $(MKDIR) $(DOCS_TARGET)html
	
$(DOCS_TARGET)html/%: $(HTML_TARGET)%
	$(RM) -r $@
	cp -r $< $@

# Add/update Python code on Web pages
.PHONY: publish-code publish-code-setup
publish-code: $(CODE_TARGET) publish-code-setup \
	$(DOCS_TARGET)code/LICENSE.md \
	$(DOCS_TARGET)code/README.md \
	$(DOCS_TARGET)code/requirements.txt \
	$(DOCS_TARGET)code/setup.py \
	$(DOCS_TARGET)code/__init__.py \
	$(UTILITY_FILES:%=$(DOCS_TARGET)code/$(UTILS)/%) \
	$(PUBLIC_CHAPTERS:%.ipynb=$(DOCS_TARGET)code/%.py) \
	$(APPENDICES:%.ipynb=$(DOCS_TARGET)code/%.py)

publish-code-setup:
	@test -d $(DOCS_TARGET) \
		|| $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)code \
		|| $(MKDIR) $(DOCS_TARGET)code
	@test -d $(DOCS_TARGET)code/$(UTILS) \
		|| $(MKDIR) $(DOCS_TARGET)code/$(UTILS)
	
$(DOCS_TARGET)code/%: $(CODE_TARGET)%
	cp -r $< $@

$(DOCS_TARGET)code/requirements.txt: requirements.txt
	cp -r $< $@

.PHONY: dist publish-dist
dist publish-dist: publish-code toc \
	$(DOCS_TARGET)dist/$(PROJECT)-code.zip \
	$(DOCS_TARGET)dist/$(PROJECT)-notebooks.zip

DIST_CODE_FILES = \
	$(DOCS_TARGET)code/LICENSE.md \
	$(DOCS_TARGET)code/README.md \
	$(DOCS_TARGET)code/requirements.txt \
	$(DOCS_TARGET)code/setup.py \
	$(DOCS_TARGET)code/__init__.py

clean-dist:
	$(RM) -r $(CODE_TARGET)__pycache__
	-chmod +w $(CODE_TARGET)$(UTILS) $(CODE_TARGET)$(UTILS)/__pycache__
	$(RM) -r $(CODE_TARGET)$(UTILS)/__pycache__
	-find $(DOCS_TARGET) -name __pycache__ -exec $(RM) -r {} \;
	-find $(DOCS_TARGET) -name .ipynb_checkpoints -exec $(RM) -r {} \;

$(DOCS_TARGET)dist/$(PROJECT)-code.zip: \
	$(PYS) $(DIST_CODE_FILES) $(CHAPTERS_MAKEFILE) clean-dist
	@-mkdir $(DOCS_TARGET)dist
	$(RM) -r $(DOCS_TARGET)dist/*
	$(RM) -r $(DOCS_TARGET)$(PROJECT)
	mkdir $(DOCS_TARGET)$(PROJECT)
	ln -s ../code $(DOCS_TARGET)$(PROJECT)/$(PROJECT)
	mv $(DOCS_TARGET)$(PROJECT)/$(PROJECT)/setup.py $(DOCS_TARGET)$(PROJECT)
	mv $(DOCS_TARGET)$(PROJECT)/$(PROJECT)/README.md $(DOCS_TARGET)$(PROJECT)
	mv $(DOCS_TARGET)$(PROJECT)/$(PROJECT)/requirements.txt $(DOCS_TARGET)$(PROJECT)
	cd $(DOCS_TARGET)$(PROJECT); PYTHONPATH= $(PYTHON) ./setup.py sdist
	mv $(DOCS_TARGET)$(PROJECT)/dist/* $(DOCS_TARGET)dist
	# mv $(DOCS_TARGET)$(PROJECT)/*.egg-info $(DOCS_TARGET)dist
	$(RM) -r $(DOCS_TARGET)$(PROJECT)/*.egg-info
	$(RM) -r $(DOCS_TARGET)$(PROJECT)/dist $(DOCS_TARGET)$(PROJECT)/build
	cd $(DOCS_TARGET); $(ZIP) $(ZIP_OPTIONS) $(PROJECT)-code.zip $(PROJECT)
	mv $(DOCS_TARGET)$(PROJECT)-code.zip $(DOCS_TARGET)dist
	$(RM) -r $(DOCS_TARGET)$(PROJECT) $(DOCS_TARGET)code/$(PROJECT)
	$(RM) -r $(DOCS_TARGET)code/dist $(DOCS_TARGET)code/*.egg-info
	@echo "Created code distribution files in $(DOCS_TARGET)dist"
	
$(DOCS_TARGET)dist/$(PROJECT)-notebooks.zip: $(FULLS) $(CHAPTERS_MAKEFILE) \
	clean-dist
	cd $(DOCS_TARGET); ln -s notebooks $(PROJECT)-notebooks
	cd $(DOCS_TARGET); \
		$(ZIP) $(ZIP_OPTIONS) $(PROJECT)-notebooks.zip $(PROJECT)-notebooks
	$(RM) $(DOCS_TARGET)$(PROJECT)-notebooks
	for file in $(EXTRAS); do \
		$(ZIP) $(DOCS_TARGET)$(PROJECT)-notebooks.zip -d $(PROJECT)-notebooks/$$file; \
	done
	# -$(ZIP) $(DOCS_TARGET)$(PROJECT)-notebooks.zip -d '$(PROJECT)-notebooks/data/*'
	mv $(DOCS_TARGET)$(PROJECT)-notebooks.zip $@
	@echo "Created notebook distribution files in $(DOCS_TARGET)dist"


# Add/update slides on Web pages
.PHONY: publish-slides publish-slides-setup
publish-slides: slides publish-slides-setup \
	$(PUBLIC_CHAPTERS:%.ipynb=$(DOCS_TARGET)slides/%.slides.html) \
	$(APPENDICES:%.ipynb=$(DOCS_TARGET)slides/%.slides.html) \
	$(REVEAL_JS) $(DOCS_TARGET)slides/reveal.js
	@-rm -fr $(DOCS_TARGET)slides/.git

publish-slides-setup:
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)slides || $(MKDIR) $(DOCS_TARGET)slides

$(DOCS_TARGET)slides/%: $(SLIDES_TARGET)%
	-rm -fr $@
	cp -r $< $@


# Add/update notebooks on Web pages
.PHONY: publish-notebooks publish-notebooks-setup
publish-notebooks: full-notebooks publish-notebooks-setup \
	$(DOCS_TARGET)notebooks/custom.css \
	$(DOCS_TARGET)notebooks/$(BIB) \
	$(DOCS_TARGET)notebooks/LICENSE.md \
	$(DOCS_TARGET)notebooks/README.md \
	$(DOCS_TARGET)notebooks/requirements.txt \
	$(DOCS:%=$(DOCS_TARGET)notebooks/%.ipynb) \
	$(UTILITY_FILES:%=$(DOCS_TARGET)notebooks/$(UTILS)/%)

publish-notebooks-setup:
	@test -d $(DOCS_TARGET) \
		|| $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)notebooks \
		|| $(MKDIR) $(DOCS_TARGET)notebooks
	@test -d $(DOCS_TARGET)notebooks/$(UTILS) \
		|| $(MKDIR) $(DOCS_TARGET)notebooks/$(UTILS)

$(DOCS_TARGET)notebooks/%: $(FULL_NOTEBOOKS)/%
	cp -r $< $@

$(DOCS_TARGET)notebooks/requirements.txt: requirements.txt
	cp -r $< $@
$(DOCS_TARGET)notebooks/LICENSE,md: LICENSE.md
	cp -r $< $@


.PHONY: publish-index
publish-index: $(DOCS_TARGET)notebooks/00_Index.ipynb


# Add/update pics on Web pages
.PHONY: publish-pics publish-pics-setup
publish-pics: publish-pics-setup $(NOTEBOOKS)/PICS
	cp -pr $(NOTEBOOKS)/PICS $(DOCS_TARGET)notebooks

publish-pics-setup:
	@test -d $(DOCS_TARGET) || $(MKDIR) $(DOCS_TARGET)
	@test -d $(DOCS_TARGET)PICS || $(MKDIR) $(DOCS_TARGET)PICS
	$(RM) -fr $(DOCS_TARGET)html/PICS; ln -s ../$(NOTEBOOKS)/PICS $(DOCS_TARGET)html
	$(RM) -fr $(DOCS_TARGET)slides/PICS; ln -s ../$(NOTEBOOKS)/PICS $(DOCS_TARGET)slides


# Table of contents
NBTOC = $(SHARED)utils/nbtoc.py
.PHONY: toc
toc: $(DOCS_TARGET)notebooks/00_Table_of_Contents.ipynb
$(DOCS_TARGET)notebooks/00_Table_of_Contents.ipynb: $(NBTOC) \
	$(TOC_CHAPTERS:%=$(DOCS_TARGET)notebooks/%) \
	$(TOC_APPENDICES:%=$(DOCS_TARGET)notebooks/%) \
	$(CHAPTERS_MAKEFILE) \
	$(SITEMAP_SVG)
	$(RM) $@
	$(PYTHON) $(SHARED)utils/nbtoc.py \
		--title="$(BOOKTITLE)" \
		--chapters="$(TOC_CHAPTERS:%=$(DOCS_TARGET)notebooks/%)" \
		--appendices="$(TOC_APPENDICES:%=$(DOCS_TARGET)notebooks/%)" > $@
	$(EXECUTE_NOTEBOOK) $@ && mv $(FULL_NOTEBOOKS)/00_Table_of_Contents.ipynb $@
	$(PYTHON) $(ADD_METADATA) --project $(PROJECT) $@ > $@~ && mv $@~ $@
	$(JUPYTER) trust $@
	@$(OPEN) $@

		
# Index
.PHONY: index
index: $(DOCS_TARGET)notebooks/00_Index.ipynb $(DOCS_TARGET)html/00_Index.html
$(DOCS_TARGET)notebooks/00_Index.ipynb: $(SHARED)utils/nbindex.py \
	$(TOC_CHAPTERS:%=$(DOCS_TARGET)notebooks/%) \
	$(TOC_APPENDICES:%=$(DOCS_TARGET)notebooks/%) \
	$(CHAPTERS_MAKEFILE)
	(cd $(NOTEBOOKS); $(PYTHON) ../$(SHARED)utils/nbindex.py $(TOC_CHAPTERS) $(APPENDICES)) > $@
	@$(OPEN) $@
	
## Synopsis
update-synopsis synopsis:
	$(PYTHON) $(NBSYNOPSIS) --project $(PROJECT) --update $(ALL_CHAPTER_SOURCES)
	$(COMMIT_SYNOPSIS)

no-synopsis:
	@echo Chapters without synopsis:
	@grep -L '## Synopsis' $(ALL_CHAPTER_SOURCES) | grep -v '[0-9]'
	

# App icon
appicon: $(NOTEBOOKS)/PICS/appicon.png
$(NOTEBOOKS)/PICS/appicon.png: $(NOTEBOOKS)/PICS/Icon.png
	-chmod +w $(SHARED)icon_gen
	cp $(NOTEBOOKS)/PICS/Icon.png $(SHARED)icon_gen
	(cd $(SHARED)icon_gen; $(PYTHON) icon_gen.py)
	cp $(SHARED)icon_gen/out/Icon-114.png $@
	$(RM) -r $(SHARED)icon_gen/out


## Python packages
# After this, you can do 'pip install fuzzingbook / debuggingbook' 
# and then 'from fuzzingbook.Fuzzer import Fuzzer' :-)
.PHONY: upload upload-dist upload-test
upload upload-dist: dist
	cd $(DOCS_TARGET); twine upload --repository $(PROJECT) dist/*.tar.gz
	@echo "Use 'pip install $(PROJECT)' to install"

upload-test: dist
	cd $(DOCS_TARGET); twine upload --repository $(PROJECT)-test dist/*.tar.gz
	@echo "Use 'pip install --extra-index-url https://test.pypi.org/simple/ $(PROJECT)' to install"


## Binder services
# Make sure we have our custom.css in Binder, too
binder/postBuild: binder/postBuild.template $(HTML_TARGET)custom.css
	cat binder/postBuild.template $(HTML_TARGET)custom.css > $@
	echo END >> $@
	chmod +x $@

# Force recreation of binder service; avoids long waiting times for first user
.PHONY: binder
binder: .FORCE
	open $(BINDER_URL)

# Sync the 'shared' folder from debuggingbook (leader) to fuzzingbook (follower)
SHARED_LEADER = debuggingbook
SHARED_FOLLOWER = fuzzingbook
.PHONY: shared
shared: clean-dist
	@if [ -d ../$(SHARED_FOLLOWER) ]; then \
		echo "Copying $(SHARED) from $(SHARED_LEADER) -> $(SHARED_FOLLOWER)"; \
		chmod -R +w ../$(SHARED_FOLLOWER)/$(SHARED); \
		$(RM) -r ../$(SHARED_FOLLOWER)/$(SHARED); \
		cp -pr ../$(SHARED_LEADER)/$(SHARED) ../$(SHARED_FOLLOWER)/$(SHARED); \
		chmod -R -w ../$(SHARED_FOLLOWER)/$(SHARED); \
		cd ../$(SHARED_FOLLOWER); \
		git commit -m "Update from $(SHARED_LEADER)" notebooks/shared; \
	fi; \
	exit 0

# After a git push, we want binder to update; "make push" does this
.PHONY: push
push: .FORCE shared
	git push
	open $(BINDER_URL)
	open $(PROJECT_URL)

# Debugging binder
# This is the same system as mybinder uses, but should be easier to debug
# See https://repo2docker.readthedocs.io/en/latest/
# and https://discourse.jupyter.org/t/tip-debug-binder-builds-faster-with-repo2docker/
.PRECIOUS: binder/binder.log
.PHONY: binder-local debug-binder
binder-local debug-binder: binder/binder.log binder/postBuild
binder/binder.log: .FORCE
	@echo Writing output to $@
	@docker version > /dev/null
	@# jupyter-repo2docker --debug $(GITHUB_REPO) 2>&1 | tee $@
	repo2docker -v '.:.' --Repo2Docker.platform=linux/amd64 . 2>&1 | tee $@


## Running Jupyter in docker
.PHONY: docker docker-image docker-push docker-release docker-shell docker-run
DOCKER_USERNAME = zeller24
GIT_HASH = $(shell git log --format="%h" -n 1)
DOCKER_TAG = $(DOCKER_USERNAME)/$(PROJECT)
DOCKER_PLATFORM = linux/amd64,linux/arm64
DOCKERFILE = binder/Dockerfile
JUPYTER_TOKEN=$(PROJECT)
JUPYTER_PORT=8888

# Use this first to creata a docker image
docker-image: $(DOCKERFILE) $(SOURCES) binder/postBuild
	docker build --tag $(DOCKER_TAG) --platform $(DOCKER_PLATFORM) binder

# Once the image is built, access it via a shell
docker-shell:
	docker run -it --rm $(DOCKER_TAG) bash

# Main usage: run jupyter lab in the image
docker-run docker:
	(sleep 2; open http://127.0.0.1:$(JUPYTER_PORT)/lab?token=$(JUPYTER_TOKEN)) &
	docker run -it --rm -p $(JUPYTER_PORT):$(JUPYTER_PORT) -e JUPYTER_TOKEN=$(JUPYTER_TOKEN) $(DOCKER_TAG) jupyter lab --ip=0.0.0.0 --port=$(JUPYTER_PORT) --no-browser

# Publish image on docker hub
docker-push:
	docker push $(DOCKER_TAG)

docker-tag:
	docker pull $(DOCKER_TAG)
	docker tag  $(DOCKER_TAG):latest $(DOCKER_TAG):$(GIT_HASH)
	docker push $(DOCKER_TAG):latest

publish-docker: docker-image docker-push docker-tag

# Cleanup unused space	
docker-clean:
	docker system prune --all --force


## Getting rid of stray processes and workspaces
kill:
	-pkill -HUP -l -f jupyter-lab Firefox.app firefox-bin runserver
	$(RM) $$HOME/.jupyter/lab/workspaces/*.jupyterlab-workspace

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
	  $(PDF_TARGET)*.xdv \
	  $(PDF_TARGET)*.fdb_latexmk

.PHONY: clean-code clean-chapters clean-book clean-aux clean-pdf
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

.PHONY: clean-full-notebooks clean-full clean-fulls 
.PHONY: clean-rendered-notebooks clean-rendered clean-renders
.PHONY: clean-docs clean realclean
clean-full-notebooks clean-full clean-fulls:
	$(RM) $(FULLS)

clean-rendered-notebooks clean-rendered clean-renders:
	$(RM) $(RENDERS)

clean-docs:
	$(RM) -r $(DOCS_TARGET)html $(DOCS_TARGET)code \
	 	$(DOCS_TARGET)slides $(DOCS_TARGET)index.html $(DOCS_TARGET)404.html \ 		$(DOCS_TARGET)PICS $(DOCS_TARGET)notebooks

clean: clean-code clean-chapters clean-book clean-aux clean-docs clean-fulls clean-renders
	@echo "All derived files deleted"

realclean: clean
	cd $(PDF_TARGET); $(RM) *.pdf
	cd $(HTML_TARGET); $(RM) *.html; $(RM) -r *_files
	cd $(SLIDES_TARGET); $(RM) *.html
	cd $(CODE_TARGET); $(RM) *.py *.py.out .*.py.out
	cd $(MYPY_TARGET); $(RM) *.py *.py.out .*.py.out
	cd $(WORD_TARGET); $(RM) *.docx
	cd $(MARKDOWN_TARGET); $(RM) *.md
	@echo "All old files deleted"


## A bit of Makefile debugging
# See http://www.drdobbs.com/tools/debugging-makefiles/197003338#

# Use "make print-VAR" to see the value of VAR, e.g. "make print-NBDEPEND"
print-%: ; @$(error $* = $($*) (defined as $* = $(value $*) from $(origin $*)))

# Use "make DEBUG=1" to get better diagnostics why a command gets executed
ifdef DEBUG
OLD_SHELL := $(SHELL)
SHELL = $(warning creating $@ from $^: $? is newer)$(OLD_SHELL)
endif


## Dependencies as graph
NBDEPEND = $(SHARED)utils/nbdepend.py
SITEMAP_OPTIONS = --graph --transitive-reduction --project $(PROJECT) # --cluster-by-parts

sitemap: $(SITEMAP_SVG)
	-open $(SITEMAP_SVG)

$(SITEMAP_SVG): $(CHAPTER_SOURCES) $(NBDEPEND)
	$(PYTHON) $(NBDEPEND) $(SITEMAP_OPTIONS) $(CHAPTER_SOURCES) > $@~ && mv $@~ $@
	@$(OPEN) $@

$(HTML_TARGET)/Tours.html: $(SITEMAP_SVG)
$(FULL_NOTEBOOKS)/Tours.ipynb: $(SITEMAP_SVG)	
$(RENDERED_NOTEBOOKS)/Tours.ipynb: $(SITEMAP_SVG)	
# $(CODE_TARGET)Tours.py: $(SITEMAP_SVG)

$(HTML_TARGET)/00_Table_of_Contents.html: $(SITEMAP_SVG) $(NBTOC)
$(FULL_NOTEBOOKS)/00_Table_of_Contents.ipynb: $(SITEMAP_SVG) $(NBTOC)
$(RENDERED_NOTEBOOKS)/00_Table_of_Contents.ipynb: $(SITEMAP_SVG) $(NBTOC)
# $(CODE_TARGET)00_Table_of_Contents.py: $(SITEMAP_SVG)


## Dependencies - should come at the very end
# See http://make.mad-scientist.net/papers/advanced-auto-dependency-generation/ for inspiration
$(DEPEND_TARGET)%.makefile: $(NOTEBOOKS)/%.ipynb
	@echo "Rebuilding $@"
	@test -d $(DEPEND_TARGET) || $(MKDIR) $(DEPEND_TARGET)
	@for import in $$($(PYTHON) $(NBDEPEND) $<); do \
		if [ -f $(NOTEBOOKS)/$$import.ipynb ]; then \
			notebooks="$$notebooks $$""(NOTEBOOKS)/$$import.ipynb"; \
			imports="$$imports $$""(CODE_TARGET)$$import.py"; \
			mypys="$$mypys $$""(MYPY_TARGET)$$import.py"; \
		fi; \
	done; \
	( \
		echo '# $(basename $(notdir $<)) dependencies'; \
		echo ''; \
		echo '$$''(FULL_NOTEBOOKS)/$(notdir $<):' $$notebooks; \
		echo ''; \
		echo '$$''(RENDERED_NOTEBOOKS)/$(notdir $<):' $$notebooks; \
		echo ''; \
		echo '$$''(CODE_TARGET).$(notdir $(<:%.ipynb=.%.py.out)):' $$imports; \
		echo ''; \
		echo '$$''(MYPY_TARGET).$(notdir $(<:%.ipynb=.%.py.out)):' $$mypys; \
	) > $@


.PHONY: depend
depend: $(DEPENDS)

include $(wildcard $(DEPENDS))
