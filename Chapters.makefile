# Fuzzingbook Makefile
# This file defines the chapter files to be included

# Chapters to include in the book, in this order
# Chapters that are out on the website
PUBLIC_CHAPTERS = \
	Intro_Testing.ipynb \
	Fuzzer.ipynb \
	Coverage.ipynb \
	MutationFuzzer.ipynb \
	Grammars.ipynb \
	GrammarFuzzer.ipynb \
	GrammarCoverageFuzzer.ipynb \
	ConfigurationFuzzer.ipynb \

# Chapters that are ready for release (and with the students)
READY_CHAPTERS = \
	Parser.ipynb \
	ProbabilisticGrammarFuzzer.ipynb \

# Chapters that still are work in progress
TODO_CHAPTERS = \
	ConstraintGrammarFuzzer.ipynb \
	APIFuzzer.ipynb \
	Carver.ipynb \
	Reducer.ipynb \
	WebFuzzer.ipynb \
	InformationFlow.ipynb \
	GrammarMiner.ipynb \

	# Oracles.ipynb
	# SearchBasedFuzzer.ipynb
	# SymbolicFuzzer.ipynb
	# FuzzingInTheLarge.ipynb

# Appendices for the book
APPENDICES = \
	ExpectError.ipynb \
	Timer.ipynb \
	RailroadDiagrams.ipynb

# Additional notebooks for special pages (not to be included in distributions)
FRONTMATTER = \
	index.ipynb
EXTRAS = \
	Guide_for_Authors.ipynb \
	Template.ipynb \
	404.ipynb
