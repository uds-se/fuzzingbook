# Fuzzingbook Makefile
# This file defines the chapter files to be included

# Most recent chapter
NEW_CHAPTERS = Carver.ipynb

# Chapters to include in the book, in this order

INTRO_PART = \
	01_Intro.ipynb \
	Intro_Testing.ipynb
INTRO_PART_READY = 
INTRO_PART_TODO = \
	# Tour.ipynb

LEXICAL_PART = \
	02_Lexical_Fuzzing.ipynb \
	Fuzzer.ipynb \
	Coverage.ipynb \
	MutationFuzzer.ipynb
LEXICAL_PART_READY = \
	SearchBasedFuzzer.ipynb
LEXICAL_PART_TODO = \
	# AFLFast.ipynb

SYNTACTICAL_PART = \
	03_Syntactical_Fuzzing.ipynb \
	Grammars.ipynb \
	GrammarFuzzer.ipynb \
	GrammarCoverageFuzzer.ipynb \
	Parser.ipynb \
	ProbabilisticGrammarFuzzer.ipynb \
	GeneratorGrammarFuzzer.ipynb \
	Reducer.ipynb
SYNTACTICAL_PART_READY = 
SYNTACTICAL_PART_TODO =
	
SEMANTICAL_PART = 
SEMANTICAL_PART_READY = \
	04_Semantical_Fuzzing.ipynb \
	GrammarMiner.ipynb
	InformationFlow.ipynb \
SEMANTICAL_PART_TODO = \
	# SymbolicFuzzer.ipynb

DOMAINS_PART = \
	05_Domain-Specific_Fuzzing.ipynb \
	ConfigurationFuzzer.ipynb \
	APIFuzzer.ipynb \
	Carver.ipynb
DOMAINS_PART_READY = \
	WebFuzzer.ipynb \
	GUIFuzzer.ipynb
DOMAINS_PART_TODO =

MANAGEMENT_PART = 
MANAGEMENT_PART_READY =
MANAGEMENT_PART_TODO = \
	06_Managing_Fuzzing.ipynb \
 	FuzzingInTheLarge.ipynb
	# WhenToStopFuzzing.ipynb


# Appendices for the book
APPENDICES = \
	ExpectError.ipynb \
	Timer.ipynb \
	ControlFlow.ipynb \
	RailroadDiagrams.ipynb

# Additional notebooks for special pages (not to be included in distributions)
FRONTMATTER = \
	index.ipynb
EXTRAS = \
	Guide_for_Authors.ipynb \
	Template.ipynb \
	404.ipynb
