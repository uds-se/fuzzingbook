# Fuzzingbook Makefile
# This file defines the chapter files to be included

# Name of the project
PROJECT = fuzzingbook

# Some metadata
BOOKTITLE = The Fuzzing Book
AUTHORS = Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler
TWITTER = @FuzzingBook

# Chapter(s) to be marked as "new" in menu
NEW_CHAPTERS = 

# Chapters to include in the book, in this order
INTRO_PART = \
	01_Intro.ipynb \
	Tours.ipynb \
	Intro_Testing.ipynb
INTRO_PART_READY =
INTRO_PART_TODO =

LEXICAL_PART = \
	02_Lexical_Fuzzing.ipynb \
	Fuzzer.ipynb \
	Coverage.ipynb \
	MutationFuzzer.ipynb \
	GreyboxFuzzer.ipynb \
	SearchBasedFuzzer.ipynb \
	MutationAnalysis.ipynb
LEXICAL_PART_READY = 
LEXICAL_PART_TODO = 

SYNTACTICAL_PART = \
	03_Syntactical_Fuzzing.ipynb \
	Grammars.ipynb \
	GrammarFuzzer.ipynb \
	GrammarCoverageFuzzer.ipynb \
	Parser.ipynb \
	ProbabilisticGrammarFuzzer.ipynb \
	GeneratorGrammarFuzzer.ipynb \
	GreyboxGrammarFuzzer.ipynb \
	Reducer.ipynb
SYNTACTICAL_PART_READY =
SYNTACTICAL_PART_TODO = 

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

MANAGEMENT_PART = \
	06_Managing_Fuzzing.ipynb \
 	FuzzingInTheLarge.ipynb \
	WhenToStopFuzzing.ipynb
MANAGEMENT_PART_READY =
MANAGEMENT_PART_TODO =

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
	ReleaseNotes.ipynb \
	Importing.ipynb \
	Guide_for_Authors.ipynb \
	Template.ipynb \
	404.ipynb

# These chapters will show up in the "public" version
PUBLIC_CHAPTERS = \
	$(INTRO_PART) \
	$(LEXICAL_PART) \
	$(SYNTACTICAL_PART) \
	$(SEMANTICAL_PART) \
	$(DOMAINS_PART) \
	$(MANAGEMENT_PART)

# These chapters will show up in the "beta" version
CHAPTERS = \
	$(INTRO_PART) \
	$(INTRO_PART_READY) \
	$(INTRO_PART_TODO) \
	$(LEXICAL_PART) \
	$(LEXICAL_PART_READY) \
	$(LEXICAL_PART_TODO) \
	$(SYNTACTICAL_PART) \
	$(SYNTACTICAL_PART_READY) \
	$(SYNTACTICAL_PART_TODO) \
	$(SEMANTICAL_PART) \
	$(SEMANTICAL_PART_READY) \
	$(SEMANTICAL_PART_TODO) \
	$(DOMAINS_PART) \
	$(DOMAINS_PART_READY) \
	$(DOMAINS_PART_TODO) \
	$(MANAGEMENT_PART) \
	$(MANAGEMENT_PART_READY) \
	$(MANAGEMENT_PART_TODO)

READY_CHAPTERS = \
	$(INTRO_PART_READY) \
	$(LEXICAL_PART_READY) \
	$(SYNTACTICAL_PART_READY) \
	$(SEMANTICAL_PART_READY) \
	$(DOMAINS_PART_READY) \
	$(MANAGEMENT_PART_READY)

TODO_CHAPTERS = \
	$(INTRO_PART_TODO) \
	$(LEXICAL_PART_TODO) \
	$(SYNTACTICAL_PART_TODO) \
	$(SEMANTICAL_PART_TODO) \
	$(DOMAINS_PART_TODO) \
	$(MANAGEMENT_PART_TODO)

