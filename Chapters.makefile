# Fuzzingbook Makefile
# This file defines the chapter files to be included

# Chapters to include in the book, in this order
PUBLIC_CHAPTERS = \
	Intro_Testing.ipynb \
	Fuzzer.ipynb \
	Coverage.ipynb \
	MutationFuzzer.ipynb \
	Grammars.ipynb \
	GrammarFuzzer.ipynb

# Chapters that are ready for release
READY_CHAPTERS = \
	GrammarCoverageFuzzer.ipynb \
	ConfigurationFuzzer.ipynb

# Chapters that still are work in progress
TODO_CHAPTERS = \
	Parser.ipynb \
	ProbabilisticGrammarFuzzer.ipynb \
	Reducer.ipynb \
	Carver.ipynb \
	APIFuzzer.ipynb \
	WebFuzzer.ipynb \
	InformationFlow.ipynb \
	GrammarMiner.ipynb
	# ConstraintGrammarFuzzer.ipynb
	# GUIFuzzer.ipynb
	# SearchBasedFuzzer.ipynb
	# SymbolicFuzzer.ipynb

# Appendices for the book
APPENDICES = \
	ExpectError.ipynb \
	Timer.ipynb

# Additional notebooks for special pages (not to be included in distributions)
FRONTMATTER = \
	index.ipynb
EXTRAS = \
	Guide_for_Authors.ipynb \
	Template.ipynb \
	404.ipynb
