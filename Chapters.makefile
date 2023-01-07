# Fuzzingbook Makefile
# This file defines the chapter files to be included

# Name of the project
PROJECT = fuzzingbook

# Some metadata
BOOKTITLE = The Fuzzing Book
AUTHORS = Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler
TWITTER = @FuzzingBook

# Chapter(s) to be marked as "new" in menu
NEW_CHAPTERS = \
	FuzzingWithConstraints.ipynb

# Chapters to include in the book, in this order.
# * Chapters in `..._PART` get published.
# * Chapters in `..._PART_READY` only get published as beta, with a disclaimer.
# * Chapters in `..._PART_TODO` only get published as beta, with a disclaimer.
#      and a "todo" (wrench) marker in the menu.

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

SEMANTIC_PART = \
	04_Semantical_Fuzzing.ipynb \
	FuzzingWithConstraints.ipynb \
	GrammarMiner.ipynb \
	InformationFlow.ipynb \
	ConcolicFuzzer.ipynb \
	SymbolicFuzzer.ipynb \
	DynamicInvariants.ipynb
SEMANTIC_PART_READY = 
SEMANTIC_PART_TODO = 

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
	AcademicPrototyping.ipynb \
	PrototypingWithPython.ipynb \
	ExpectError.ipynb \
	Timer.ipynb \
	Timeout.ipynb \
	ClassDiagram.ipynb \
	RailroadDiagrams.ipynb \
	ControlFlow.ipynb

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
	$(SEMANTIC_PART) \
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
	$(SEMANTIC_PART) \
	$(SEMANTIC_PART_READY) \
	$(SEMANTIC_PART_TODO) \
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
	$(SEMANTIC_PART_READY) \
	$(DOMAINS_PART_READY) \
	$(MANAGEMENT_PART_READY)

TODO_CHAPTERS = \
	$(INTRO_PART_TODO) \
	$(LEXICAL_PART_TODO) \
	$(SYNTACTICAL_PART_TODO) \
	$(SEMANTIC_PART_TODO) \
	$(DOMAINS_PART_TODO) \
	$(MANAGEMENT_PART_TODO)

## Specific settings
# No timeouts; debuggingbook/GreyboxFuzzer can take up to 10 minutes to run
EXECUTE_TIMEOUT = 600
TIME = time