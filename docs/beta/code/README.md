# Code for "The Fuzzing Book"

This folder holds the code from "The Fuzzing Book".  This book addresses the problem of software bugs by automating software testing, specifically by _generating tests automatically_. Recent years have seen the development of novel techniques that lead to dramatic improvements in test generation and software testing. They now are mature enough to be assembled in a book - even with executable code.

For details (and all of the book!), see the web site: https://www.fuzzingbook.org/


## Using the Code

The book has plenty of examples for using the code; you are encouraged to read it and then to use this code to try things out.

### Importing

You can import the modules in your own projects and use the infrastructure, as in

```python
from fuzzingbook.Fuzzer import RandomFuzzer
f = RandomFuzzer()
f.fuzz()
```

### Running
	
You can also execute the files directly to run the examples from the book, as in

```shell
$ ./Fuzzer.py
```

Enjoy!	


## License

Copyright (c) 2018-2020 CISPA, Saarland University, authors, and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
