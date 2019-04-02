# Fuzzingbook Makefile
# This file defines the chapter files to be included

# Chapter(s) to be marked as "new" in menu
NEW_CHAPTERS = SearchBasedFuzzer.ipynb

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
	MutationFuzzer.ipynb \
	SearchBasedFuzzer.ipynb
LEXICAL_PART_READY = 
LEXICAL_PART_TODO = \
	# AFLFast.ipynb

SYNTACTICAL_PART = \
	03_Syntactical_Fuzzing.ipynb \
	Grammars.ipynb \
	GrammarFuzzer.ipynb \
	GrammarCoverageFuzzer.ipynb \
	Parser.ipynb \
	LangFuzzer.ipynb \
	ProbabilisticGrammarFuzzer.ipynb \
	GeneratorGrammarFuzzer.ipynb \
	Reducer.ipynb
SYNTACTICAL_PART_READY =
SYNTACTICAL_PART_TODO = \
	EvoGrammarFuzzer.ipynb
	
SEMANTICAL_PART = \
	04_Semantical_Fuzzing.ipynb \
	GrammarMiner.ipynb \
	InformationFlow.ipynb \
	ConcolicFuzzer.ipynb \
	SymbolicFuzzer.ipynb \
	DynamicInvariants.ipynb
SEMANTICAL_PART_READY =
SEMANTICAL_PART_TODO =

DOMAINS_PART = \
	05_Domain-Specific_Fuzzing.ipynb \
	ConfigurationFuzzer.ipynb \
	APIFuzzer.ipynb \
	Carver.ipynb \
	WebFuzzer.ipynb \
	GUIFuzzer.ipynb
DOMAINS_PART_READY = 
DOMAINS_PART_TODO =

MANAGEMENT_PART = 
MANAGEMENT_PART_READY =
MANAGEMENT_PART_TODO = \
	06_Managing_Fuzzing.ipynb \
 	FuzzingInTheLarge.ipynb \
	WhenToStopFuzzing.ipynb

# Appendices for the book
APPENDICES = \
	99_Appendices.ipynb \
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
