# Fuzzingbook Makefile
# This file defines the chapter files to be included

# Chapters to include in the book, in this order
# Chapters that are out on the website

INTRO_PART = \
	01_Intro.ipynb \
	Intro_Testing.ipynb \
	
INTRO_PART_READY = 
INTRO_PART_TODO = \
	# Tour.ipynb


LEXICAL_PART = \
	02_Lexical_Fuzzing.ipynb \
	Fuzzer.ipynb \
	Coverage.ipynb \
	MutationFuzzer.ipynb \

LEXICAL_PART_READY = \
	SBST.ipynb
LEXICAL_PART_TODO = \
	# AFLFast.ipynb


SYNTACTICAL_PART = \
	03_Syntactical_Fuzzing.ipynb \
	Grammars.ipynb \
	GrammarFuzzer.ipynb \
	GrammarCoverageFuzzer.ipynb \
	ProbabilisticGrammarFuzzer.ipynb \
	GeneratorGrammarFuzzer.ipynb \
	Parser.ipynb \
	
LEXICAL_PART_READY = \
	Reducer.ipynb
LEXICAL_PART_TODO =

	
SEMANTICAL_PART = \
	04_Semantical_Fuzzing.ipynb

SEMANTICAL_PART_READY = \
	GrammarMiner.ipynb
SEMANTICAL_PART_TODO = \
	InformationFlow.ipynb \
	# SymbolicFuzzer.ipynb

DOMAINS_PART = \
	05_Domain-Specific_Fuzzing.ipynb \
	ConfigurationFuzzer.ipynb \
	APIFuzzer.ipynb \
	Carver.ipynb \
	
DOMAINS_PART_READY = \
	WebFuzzer.ipynb \
	GUIFuzzer.ipynb
DOMAINS_PART_TODO = \
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
