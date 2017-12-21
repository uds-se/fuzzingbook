## Generating Software Tests

This is the repository for the book "Generating Software Tests" (working title)

Project page: https://projects.cispa.saarland/zeller/gstbook

# Summary

The idea is to have a textbook on software test generation, teaching students and professionals alike the latest and greatest concepts in test generation.  The book would come with plenty of code samples that allow the reader to immediately try out the concepts as well as extend them for her/his own purposes.  These code samples would come in Python, as the language easily allows for all sorts of code analysis.

# Contents and Organization

The contents and organization of the book would roughly be based on the lecture “Security Testing” that Andreas and Rahul are currently running.  A typical set of chapters could be based on the lectures we have prepared, plus a few more:

1. Introduction
2. Fundamentals of Testing
3. Text-Based Fuzzing
4. Grammar-Based Fuzzing
5. Generating Complex Inputs
6. Mutation-Based Fuzzing
7. Parsing Inputs
8. Simplifying Inputs
9. Search-Based Testing
10. Evolving Test Suites
11. Solving Constraints
12. Symbolic Testing
13. Mining Grammars
14. Taint Analysis
15. Mutation Analysis
16. Probabilistic Testing
17. Generating Unit Tests
18. Carving Unit Tests
19. Inferring Invariants
20. Protection and Repair
21. Fuzzing in the Large
22. The Future of Test Generation
* Appendix: Glossary

Each chapter would be about 10–20 pages in length, such that the book overall would have about 300 pages.  Keep in mind that the code is (mostly) part of the book, so this is programming as well as writing. Each chapter would come with exercises, typically extending the given code in some way, as well as references to related work.  All titles, including the book title itself, are also up for discussion.

# Technical Organization

On the technical side, I would like to adopt a “literate programming” style, where each chapter comes in a single file from which one can extract

* a LaTeX file, to be converted into PDF
* a HTML file, to be read in the browser
* a Python file with all the code

The “literate programming" style would also allow to execute the code samples as they are being typeset; this allows for quality assurance as well as easy explanation of what the code is doing.  For your convenience, the "ptangle-demo" folder holds an example with one .texw source file and derived HTML, PDF, and Python files; note how everything including syntax highlighting is done from one source.  We will have a git repo and an automated test suite.

# Publishing

On the publishing side, the could be made available in HTML form during a “beta” phase, with new chapters being published in regular intervals (i.e., one per week), announced on Facebook, Twitter, etc.  This should create some buzz for the printed book and give our colleagues opportunity for feedback.  When the printed book comes out, my idea is that parts of the HTML (say, later chapters or later sections in a number of chapters) would no longer be accessible, asking to purchase the "final" book instead.  We can still update the original sources, such that the Python code can be up-to-date; we can also add more chapters, which would then be available in full until the next edition comes out.  We also have to find a publisher for the book, maybe revitalizing our previous relationship with Morgan Kaufmann.

# Design

Regarding design, we will need to find someone with good knowledge in CSS and HTML design, such that we have a nice-looking HTML output; the printed version (paper and PDF/ebook) will be handled by the publisher.  I would love to have some full-page illustrations as in the TeXBook (maybe one per chapter?); 
pointers to illustrators are welcome.

# Timeframe

Finally, the timeframe. "Security testing" will be taught again starting October 2018, so this would be the time when new material can be beta-tested on a large scale.  (Maybe Gordon would also like to teach it?)  Hence, October 2018 would be the time when all (or at least the early) chapters would have to be finalized.  The final manuscript would then go to the editor early 2019.