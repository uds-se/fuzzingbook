# Generating Software Tests

This is the repository for the book "Generating Software Tests" (working title)

Project page:

	 https://projects.cispa.saarland/zeller/gstbook

## Summary

The idea is to have a _textbook on software test generation,_ teaching students and professionals alike the latest and greatest concepts in test generation.  The book would come with plenty of code samples that allow the reader to immediately try out the concepts as well as extend them for her/his own purposes.  These code samples would come in Python, as the language easily allows for all sorts of code analysis.

## Contents and Organization

The contents and organization of the book would roughly be based on the lecture “Security Testing” that Andreas and Rahul are currently running.  A typical set of chapters could be based on the lectures we have prepared, plus a few more:

* Preface
1. Fundamentals of Testing
2. Text-Based Fuzzing
3. Grammar-Based Fuzzing
4. Generating Complex Inputs
5. Fuzzing Function Calls
6. Fuzzing User Interfaces
7. Mutation-Based Fuzzing
8. Parsing Inputs
9. Simplifying Inputs
10. Search-Based Testing
11. Evolving Test Suites
12. Solving Constraints
13. Symbolic Testing
14. Mining Grammars
15. Taint Analysis
16. Mutation Analysis
17. Probabilistic Testing
18. Generating Unit Tests
19. Carving Unit Tests
20. Inferring Invariants
21. Protection and Repair
22. Fuzzing in the Large
23. The Future of Test Generation
* Glossary

Each chapter would be about 10–20 pages in length, such that the book overall would have about 300 pages.  Keep in mind that the code is (mostly) part of the book, so this is programming as well as writing. Each chapter would come with exercises, typically extending the given code in some way, as well as references to related work.

**Open Issue:** Techniques on unstructured input (e.g. simple random fuzzing or random mutation) should be discussed first before going into grammar-based fuzzing and mutations.


### Title

The working title of the book is "Generating Software Tests".  So far, this has not seen any major objection.


### Glossary

I will start with a glossary of terms that should be consistently used throughout the book.



## Publishing

On the publishing side, the could be made available in HTML form during a “beta” phase, with new chapters being published in regular intervals (i.e., one per week), announced on Facebook, Twitter, etc.  This should create some buzz for the printed book and give our colleagues opportunity for feedback.  When the printed book comes out, my idea is that parts of the HTML (say, later chapters or later sections in a number of chapters) would no longer be accessible, asking to purchase the "final" book instead.  We can still update the original sources, such that the Python code can be up-to-date; we can also add more chapters, which would then be available in full until the next edition comes out.  We also have to find a publisher for the book, maybe revitalizing our previous relationship with Morgan Kaufmann.

## Design

### PDF

The printed version (paper and/or PDF/ebook) will be handled by the publisher.  We need to make sure that we can still maintain our source code; that is. we have to include the publisher's style files and react to comments.


### HTML

Regarding design, we will need to find someone with good knowledge in CSS and HTML design, such that we have a nice-looking HTML output.

The book "Rust by Example" has a nice functional design, also combining code snippets with explanations.  I love the way you can execute code to see the output - hey, you can even *change* the code (how?):

	https://rustbyexample.com/index.html


### Illustrations

I would love to have some full-page illustrations as in the TeXBook (maybe one per chapter?); pointers to illustrators are welcome.



## Timeframe

Finally, the timeframe. "Security testing" will be taught again starting October 2018, so this would be the time when new material can be beta-tested on a large scale, and at least the early chapters would have to be finalized.

I would love to publish one new chapter per week to the public for general comment; this is something we can also start in October 2018.

Gordon would also like to teach this in Spring 2019; at this point, the manuscript could already have significantly matured, based on feedback by our students and the public feedback.  Hence, this would serve as a second trial run; if all goes well, the manuscript could then go to the editor in Summer 2019.


