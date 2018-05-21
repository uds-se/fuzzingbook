# Simple Makefile

SOURCES = \
	Guide\ for\ Authors.ipynb \
	ch01_Fuzzer.ipynb \
	ch02_Coverage.ipynb

PDFS  = $(SOURCES:%.ipynb=%.pdf)
HTMLS = $(SOURCES:%.ipynb=%.html)
PYS   = $(SOURCES:%.ipynb=%.py)

%.pdf:	%.ipynb
	jupyter nbconvert --to pdf $<
	
%.html:	%.ipynb
	jupyter nbconvert --to html $<

%.py:	%.ipynb
	jupyter nbconvert --to python $<

clean:
	$(RM) $(PDFS) $(HTMLS) $(PYS)
