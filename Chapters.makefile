# Fuzzingbook Makefile
# This file defines the chapter files to be included

# Chapters to include in the book, in this order
# Chapters that are out on the website
PUBLIC_CHAPTERS = \
	$(INTRO_PART) \
	$(LEXICAL_PART) \
	$(SYNTACTICAL_PART) \
	$(SEMANTICAL_PART) \
	$(DOMAINS_PART)

INTRO_PART = \
	01_Intro.ipynb \
	Intro_Testing.ipynb
	# Tour.ipynb

LEXICAL_PART = \
	02_Lexical_Fuzzing.ipynb \
	Fuzzer.ipynb \
	Coverage.ipynb \
	MutationFuzzer.ipynb \
	# SBST.ipynb

SYNTACTICAL_PART = \
	03_Syntactical_Fuzzing.ipynb \
	Grammars.ipynb \
	GrammarFuzzer.ipynb \
	GrammarCoverageFuzzer.ipynb \
	ProbabilisticGrammarFuzzer.ipynb \
	GeneratorGrammarFuzzer.ipynb \
	Parser.ipynb \
	# Reducer.ipynb
	
SEMANTICAL_PART = \
	04_Semantical_Fuzzing.ipynb \
	# SymbolicFuzzer.ipynb \
	# InformationFlow.ipynb \
	# GrammarMiner.ipynb \

DOMAINS_PART = \
	05_Domain-Specific_Fuzzing.ipynb \
	ConfigurationFuzzer.ipynb \
	APIFuzzer.ipynb \
	Carver.ipynb \
	# WebFuzzer.ipynb \
	# GUIFuzzer.ipynb \
	# FuzzingInTheLarge.ipynb
	# WhenToStopFuzzing.ipynb

# Chapters that are ready for release (= the current chapters for the students)
READY_CHAPTERS = \
	06_Unreleased.ipynb \
	Reducer.ipynb \
	WebFuzzer.ipynb \
	GUIFuzzer.ipynb \
	SBST.ipynb \
	GrammarMiner.ipynb \

# Chapters that still are work in progress
TODO_CHAPTERS = \
	InformationFlow.ipynb \
	# SymbolicFuzzer.ipynb
	# FuzzingInTheLarge.ipynb
	# WhenToStopFuzzing.ipynb

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
