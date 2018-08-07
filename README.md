# Generating Software Tests

This is the repository for the book "Generating Software Tests" (working title)

Project page:

	 https://projects.cispa.saarland/zeller/gstbook

## Summary

The idea is to have a _textbook on software test generation,_ teaching students and professionals alike the latest and greatest concepts in test generation.  The book would come with plenty of code samples that allow the reader to immediately try out the concepts as well as extend them for her/his own purposes.  These code samples would come in Python, as the language easily allows for all sorts of code analysis.

## Contents and Organization

The contents and organization of the book would roughly be based on the lecture “Security Testing” that Andreas and Rahul are currently running.  A typical set of chapters could be based on the lectures we have prepared, plus a few more:

* Preface
1. Introduction to Testing
2. Text-Based Fuzzing
3. Mutation-Based Fuzzing
4. Fuzzing and Debugging
5. Grammar-Based Fuzzing
6. Fuzzing Function Calls
7. Fuzzing User Interfaces
8. Parsing and Mutating Inputs
9. Search-Based Testing
10. Constraint-Based Testing
11. Mining Grammars
12. Fuzzing and Mutations
13. Probabilistic Testing
14. Carving Unit Tests
15. Fuzzing and Invariants
16. Protection and Repair
* Glossary


Each chapter would be about 10–20 pages in length, such that the book overall would have about 300 pages.  Keep in mind that the code is (mostly) part of the book, so this is programming as well as writing. Each chapter would come with exercises, typically extending the given code in some way, as well as references to related work.



### Title

The working title of the book is "Generating Software Tests".  So far, this has not seen any major objection.


### Glossary

I will start with a glossary of terms that should be consistently used throughout the book.



## Publishing

### Open Source

Jupyter notebooks have a lot of benefits for teaching.  We should therefore make our material available as open source under some permissive license:

* **Notebooks** can be placed online, rendered within Gitlab or Github and available for download.  The MyBinder service even allows to run them interactively in a browser.

* **HTML** is probably the most accessible format; we can make HTML pages available on a site.

* **Code** can be made available for download.

We can have new chapters being published in regular intervals (i.e., one per week), announced on Facebook, Twitter, etc.  This should create some buzz for the printed book and give our colleagues opportunity for feedback.

### Book

The **PDF** version is something I would rather publish as a book.  To create value over the (online) HTML/notebook versions, I would suggest to include *additional chapters* with authors from the field who would then explain how the concepts from the book translate to large-scale, industrial settings.

I would not mind if the proceedings from the book went to some charity or public cause.  Suggestions are welcome!


## Design

### PDF

The printed version (paper and/or PDF/ebook) will be handled by the publisher.  We need to make sure that we can still maintain our source code; that is, we have to include the publisher's style files and react to comments.


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


