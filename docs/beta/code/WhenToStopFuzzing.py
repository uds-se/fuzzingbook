#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "When To Stop Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/WhenToStopFuzzing.html
# Last change: 2021-06-08 13:01:16+02:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''
The Fuzzing Book - When To Stop Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python WhenToStopFuzzing.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.WhenToStopFuzzing import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/WhenToStopFuzzing.html


For more details, source, and documentation, see
"The Fuzzing Book - When To Stop Fuzzing"
at https://www.fuzzingbook.org/html/WhenToStopFuzzing.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# When To Stop Fuzzing
# ====================

if __name__ == '__main__':
    print('# When To Stop Fuzzing')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from . import Fuzzer
from . import Coverage

## The Enigma Machine
## ------------------

if __name__ == '__main__':
    print('\n## The Enigma Machine')



### The Kenngruppenbuch

if __name__ == '__main__':
    print('\n### The Kenngruppenbuch')



import string

if __name__ == '__main__':
    import numpy
    from numpy.random import choice
    from numpy.random import shuffle
    from numpy import log

if __name__ == '__main__':
    letters = list(string.ascii_letters[26:])  # upper-case characters
    trigrams = [str(a + b + c) for a in letters for b in letters for c in letters]
    shuffle(trigrams)

if __name__ == '__main__':
    trigrams[:10]

if __name__ == '__main__':
    k_book = {}  # Kenngruppenbuch

    for i in range(1, len(trigrams) + 1):
        trigram = trigrams[i - 1]
        # choose weights according to Benford's law
        k_book[trigram] = log(1 + 1 / i) / log(26**3 + 1)

if __name__ == '__main__':
    random_trigram = choice(list(k_book.keys()), p=list(k_book.values()))
    random_trigram

if __name__ == '__main__':
    k_book[random_trigram]

### Fuzzing the Enigma

if __name__ == '__main__':
    print('\n### Fuzzing the Enigma')



from .Fuzzer import RandomFuzzer
from .Fuzzer import Runner

class EnigmaMachine(Runner):
    def __init__(self, k_book):
        self.k_book = k_book
        self.reset()

    def reset(self):
        """Resets the key register"""
        self.msg2key = {}
        
    def internal_msg2key(self, message):
        """Internal helper method. 
           Returns the trigram for an encoded message."""
        if not message in self.msg2key:
            # Simulating how an officer chooses a key from the Kenngruppenbuch to encode the message.
            self.msg2key[message] = choice(list(self.k_book.keys()), p=list(self.k_book.values()))
        trigram = self.msg2key[message]
        return trigram

    def naval_enigma(self, message, key):
        """Returns true if 'message' is encoded with 'key'"""
        if key == self.internal_msg2key(message):
            return True
        else:
            return False

class EnigmaMachine(EnigmaMachine):
    def run(self, tri):
        """PASS if cur_msg is encoded with trigram tri"""
        if self.naval_enigma(self.cur_msg, tri):
            outcome = self.PASS
        else:
            outcome = self.FAIL

        return (tri, outcome)

if __name__ == '__main__':
    enigma = EnigmaMachine(k_book)
    enigma.cur_msg = "BrEaK mE. L0Lzz"
    enigma.run("AAA")

class BletchleyPark(object):
    def __init__(self, enigma):
        self.enigma = enigma
        self.enigma.reset()
        self.enigma_fuzzer = RandomFuzzer(
            min_length=3,
            max_length=3,
            char_start=65,
            char_range=26)
        
    def break_message(self, message):
        """Returning the trigram for an encoded message"""
        self.enigma.cur_msg = message
        while True:
            (trigram, outcome) = self.enigma_fuzzer.run(self.enigma)
            if outcome == self.enigma.PASS:
                break
        return trigram

from .Timer import Timer

if __name__ == '__main__':
    enigma = EnigmaMachine(k_book)
    bletchley = BletchleyPark(enigma)

    with Timer() as t:
        trigram = bletchley.break_message("BrEaK mE. L0Lzz")

if __name__ == '__main__':
    trigram

if __name__ == '__main__':
    '%f seconds' % t.elapsed_time()

if __name__ == '__main__':
    'Bletchley cracks about %d messages per second' % (1/t.elapsed_time())

### Turing's Observations

if __name__ == '__main__':
    print("\n### Turing's Observations")



from collections import defaultdict

if __name__ == '__main__':
    n = 100  # messages to crack

if __name__ == '__main__':
    observed = defaultdict(int)
    for msg in range(0, n):
        trigram = bletchley.break_message(msg)
        observed[trigram] += 1

    # list of trigrams that have been observed
    counts = [k for k, v in observed.items() if int(v) > 0]

    t_trigrams = len(k_book)
    o_trigrams = len(counts)

if __name__ == '__main__':
    "After cracking %d messages, we observed %d out of %d trigrams." % (
        n, o_trigrams, t_trigrams)

if __name__ == '__main__':
    singletons = len([k for k, v in observed.items() if int(v) == 1])

if __name__ == '__main__':
    "From the %d observed trigrams, %d were observed only once." % (
        o_trigrams, singletons)

class BletchleyPark(BletchleyPark):
    
    
    def break_message(self, message):
        """Returning the trigram for an encoded message"""
        # For the following experiment, we want to make it practical
        #   to break a large number of messages. So, we remove the
        #   loop and just return the trigram for a message.
        #
        # enigma.cur_msg = message
        # while True:
        #     (trigram, outcome) = self.enigma_fuzzer.run(self.enigma)
        #     if outcome == self.enigma.PASS:
        #         break
        trigram = enigma.internal_msg2key(message)
        return trigram
    
    def break_n_messages(self, n):
        """Returns how often each trigram has been observed, 
           and #trigrams discovered for each message."""
        observed = defaultdict(int)
        timeseries = [0] * n

        # Crack n messages and record #trigrams observed as #messages increases
        cur_observed = 0
        for cur_msg in range(0, n):
            trigram = self.break_message(cur_msg)
            
            observed[trigram] += 1
            if (observed[trigram] == 1):
                cur_observed += 1
            timeseries[cur_msg] = cur_observed
            
        return (observed, timeseries)

if __name__ == '__main__':
    n = 2000        # messages to crack

if __name__ == '__main__':
    bletchley = BletchleyPark(enigma)
    (observed, timeseries) = bletchley.break_n_messages(n)

if __name__ == '__main__':
    singletons = len([k for k, v in observed.items() if int(v) == 1])
    gt = singletons / n
    gt

if __name__ == '__main__':
    repeats = 1000  # experiment repetitions    

if __name__ == '__main__':
    newly_discovered = 0
    for cur_msg in range(n, n + repeats):
        trigram = bletchley.break_message(cur_msg)
        if(observed[trigram] == 0):
            newly_discovered += 1

    newly_discovered / repeats

if __name__ == '__main__':
    1 - gt

if __name__ == '__main__':
    1 / gt

# %matplotlib inline

if __name__ == '__main__':
    import matplotlib.pyplot as plt

if __name__ == '__main__':
    frequencies = [v for k, v in observed.items() if int(v) > 0]
    frequencies.sort(reverse=True)
    # Uncomment to see how often each discovered trigram has been observed
    # print(frequencies)

    # frequency of rare trigrams
    plt.figure(num=None, figsize=(12, 4), dpi=80, facecolor='w', edgecolor='k')
    plt.subplot(1, 2, 1)
    plt.hist(frequencies, range=[1, 21], bins=numpy.arange(1, 21) - 0.5)
    plt.xticks(range(1, 21))
    plt.xlabel('# of occurances (e.g., 1 represents singleton trigrams)')
    plt.ylabel('Frequency of occurances')
    plt.title('Figure 1. Frequency of Rare Trigrams')

    # trigram discovery over time
    plt.subplot(1, 2, 2)
    plt.plot(timeseries)
    plt.xlabel('# of messages cracked')
    plt.ylabel('# of trigrams discovered')
    plt.title('Figure 2. Trigram Discovery Over Time');

if __name__ == '__main__':
    singletons = len([v for k, v in observed.items() if int(v) == 1])
    total = len(frequencies)

    print("%3d of %3d trigrams (%.3f%%) have been observed   1 time (i.e., are singleton trigrams)."
          % (singletons, total, singletons * 100 / total))

    print("%3d of %3d trigrams ( %.3f%%) have been observed %d times."
          % (1, total, 1 / total, frequencies[0]))

if __name__ == '__main__':
    print("Trigram : Frequency")
    for trigram in sorted(observed, key=observed.get, reverse=True):
        if observed[trigram] > 10:
            print("    %s : %d" % (trigram, observed[trigram]))

class BletchleyPark(BletchleyPark):
    
    def __init__(self, enigma):
        super().__init__(enigma)
        self.cur_attempts = 0
        self.cur_observed = 0
        self.observed = defaultdict(int)
        self.timeseries = [None] * max_attempts * 2
    
    def break_message(self, message):
        """Returns the trigram for an encoded message, and
           track #trigrams observed as #attempts increases."""
        self.enigma.cur_msg = message
        while True:
            self.cur_attempts += 1                                 # NEW
            (trigram, outcome) = self.enigma_fuzzer.run(self.enigma)
            self.timeseries[self.cur_attempts] = self.cur_observed # NEW
            if outcome == self.enigma.PASS: 
                break
        return trigram
    
    def break_max_attempts(self, max_attempts):
        """Returns #messages successfully cracked after a given #attempts."""
        cur_msg  = 0
        n_messages = 0

        while True:
            trigram = self.break_message(cur_msg)
            
            # stop when reaching max_attempts
            if self.cur_attempts >= max_attempts:
                break
                
            # update observed trigrams
            n_messages += 1
            self.observed[trigram] += 1
            if (self.observed[trigram] == 1):
                self.cur_observed += 1
                self.timeseries[self.cur_attempts] = self.cur_observed
            cur_msg += 1
        return n_messages

if __name__ == '__main__':
    max_attempts = 100000

if __name__ == '__main__':
    bletchley = BletchleyPark(enigma)
    original = bletchley.break_max_attempts(max_attempts)
    original

class BoostedBletchleyPark(BletchleyPark):
    
    def break_message(self, message):
        """Returns the trigram for an encoded message, and
           track #trigrams observed as #attempts increases."""
        self.enigma.cur_msg = message
        
        # boost cracking by trying observed trigrams first
        for trigram in sorted(self.prior, key=self.prior.get, reverse=True):
            self.cur_attempts += 1
            (_, outcome) = self.enigma.run(trigram)
            self.timeseries[self.cur_attempts] = self.cur_observed
            if outcome == self.enigma.PASS:
                return trigram
            
        # else fall back to normal cracking
        return super().break_message(message)

if __name__ == '__main__':
    boostedBletchley = BoostedBletchleyPark(enigma)
    boostedBletchley.prior = observed
    boosted = boostedBletchley.break_max_attempts(max_attempts)
    boosted

if __name__ == '__main__':
    line_old, = plt.plot(bletchley.timeseries, label="Bruteforce Strategy")
    line_new, = plt.plot(boostedBletchley.timeseries, label="Boosted Strategy")
    plt.legend(handles=[line_old, line_new])
    plt.xlabel('# of cracking attempts')
    plt.ylabel('# of trigrams discovered')
    plt.title('Trigram Discovery Over Time');

## Estimating the Probability of Path Discovery
## --------------------------------------------

if __name__ == '__main__':
    print('\n## Estimating the Probability of Path Discovery')



from .Coverage import Coverage, cgi_decode

if __name__ == '__main__':
    encoded = "Hello%2c+world%21"
    with Coverage() as cov:
        decoded = cgi_decode(encoded)

if __name__ == '__main__':
    decoded

if __name__ == '__main__':
    print(cov.coverage());

### Trace Coverage

if __name__ == '__main__':
    print('\n### Trace Coverage')



import pickle
import hashlib

def getTraceHash(cov):
    pickledCov = pickle.dumps(cov.coverage())
    hashedCov = hashlib.md5(pickledCov).hexdigest()
    return hashedCov

if __name__ == '__main__':
    inp1 = "a+b"
    inp2 = "a+b+c"
    inp3 = "abc"

    with Coverage() as cov1:
        cgi_decode(inp1)
    with Coverage() as cov2:
        cgi_decode(inp2)
    with Coverage() as cov3:
        cgi_decode(inp3)

if __name__ == '__main__':
    inp1, inp2

if __name__ == '__main__':
    cov1.coverage() - cov2.coverage()

if __name__ == '__main__':
    getTraceHash(cov1)

if __name__ == '__main__':
    getTraceHash(cov2)

if __name__ == '__main__':
    assert getTraceHash(cov1) == getTraceHash(cov2)

if __name__ == '__main__':
    inp1, inp3

if __name__ == '__main__':
    cov1.coverage() - cov3.coverage()

if __name__ == '__main__':
    getTraceHash(cov1)

if __name__ == '__main__':
    getTraceHash(cov3)

if __name__ == '__main__':
    assert getTraceHash(cov1) != getTraceHash(cov3)

### Measuring Trace Coverage over Time

if __name__ == '__main__':
    print('\n### Measuring Trace Coverage over Time')



def population_trace_coverage(population, function):
    cumulative_coverage = []
    all_coverage = set()
    cumulative_singletons = []
    cumulative_doubletons = []
    singletons = set()
    doubletons = set()

    for s in population:
        with Coverage() as cov:
            try:
                function(s)
            except BaseException:
                pass
        cur_coverage = set([getTraceHash(cov)])

        # singletons and doubletons -- we will need them later
        doubletons -= cur_coverage
        doubletons |= singletons & cur_coverage
        singletons -= cur_coverage
        singletons |= cur_coverage - (cur_coverage & all_coverage)
        cumulative_singletons.append(len(singletons))
        cumulative_doubletons.append(len(doubletons))

        # all and cumulative coverage
        all_coverage |= cur_coverage
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage, cumulative_singletons, cumulative_doubletons

if __name__ == '__main__':
    all_coverage = population_trace_coverage([inp1, inp2, inp3], cgi_decode)[0]
    assert len(all_coverage) == 2

from .Fuzzer import RandomFuzzer
from .Coverage import population_coverage
from html.parser import HTMLParser

if __name__ == '__main__':
    trials = 50000  # number of random inputs generated

def my_parser(inp):
    parser = HTMLParser()  # resets the HTMLParser object for every fuzz input
    parser.feed(inp)

if __name__ == '__main__':
    fuzzer = RandomFuzzer(min_length=1, max_length=100,
                          char_start=32, char_range=94)

    # create population of fuzz inputs
    population = []
    for i in range(trials):
        population.append(fuzzer.fuzz())

    # execute and measure trace coverage
    trace_timeseries = population_trace_coverage(population, my_parser)[1]

    # execute and measure code coverage
    code_timeseries = population_coverage(population, my_parser)[1]

    # plot trace coverage over time
    plt.figure(num=None, figsize=(12, 4), dpi=80, facecolor='w', edgecolor='k')
    plt.subplot(1, 2, 1)
    plt.plot(trace_timeseries)
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('# of traces exercised')
    plt.title('Trace Coverage Over Time')

    # plot code coverage over time
    plt.subplot(1, 2, 2)
    plt.plot(code_timeseries)
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('# of statements covered')
    plt.title('Code Coverage Over Time');

### Evaluating the Discovery Probability Estimate

if __name__ == '__main__':
    print('\n### Evaluating the Discovery Probability Estimate')



if __name__ == '__main__':
    repeats = 500      # experiment repetitions
    measurements = 100  # experiment measurements

if __name__ == '__main__':
    emp_timeseries = []
    all_coverage = set()
    step = int(trials / measurements)

    for i in range(0, trials, step):
        if i - step >= 0:
            for j in range(step):
                inp = population[i - j]
                with Coverage() as cov:
                    try:
                        my_parser(inp)
                    except BaseException:
                        pass
                all_coverage |= set([getTraceHash(cov)])

        discoveries = 0
        for _ in range(repeats):
            inp = fuzzer.fuzz()
            with Coverage() as cov:
                try:
                    my_parser(inp)
                except BaseException:
                    pass
            if getTraceHash(cov) not in all_coverage:
                discoveries += 1
        emp_timeseries.append(discoveries / repeats)

if __name__ == '__main__':
    gt_timeseries = []
    singleton_timeseries = population_trace_coverage(population, my_parser)[2]
    for i in range(1, trials + 1, step):
        gt_timeseries.append(singleton_timeseries[i - 1] / i)

if __name__ == '__main__':
    line_emp, = plt.semilogy(emp_timeseries, label="Empirical")
    line_gt, = plt.semilogy(gt_timeseries, label="Good-Turing")
    plt.legend(handles=[line_emp, line_gt])
    plt.xticks(range(0, measurements + 1, int(measurements / 5)),
               range(0, trials + 1, int(trials / 5)))
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('discovery probability')
    plt.title('Discovery Probability Over Time');

### Discovery Probability Quantifies Residual Risk

if __name__ == '__main__':
    print('\n### Discovery Probability Quantifies Residual Risk')



## How Do We Know When to Stop Fuzzing?
## ------------------------------------

if __name__ == '__main__':
    print('\n## How Do We Know When to Stop Fuzzing?')



### A Success Estimator

if __name__ == '__main__':
    print('\n### A Success Estimator')



if __name__ == '__main__':
    trials = 400000
    fuzzer = RandomFuzzer(min_length=2, max_length=4,
                          char_start=32, char_range=32)
    population = []
    for i in range(trials):
        population.append(fuzzer.fuzz())

    _, trace_ts, f1_ts, f2_ts = population_trace_coverage(population, my_parser)

if __name__ == '__main__':
    time = int(trials / 2)
    time

if __name__ == '__main__':
    f1 = f1_ts[time]
    f2 = f2_ts[time]
    Sn = trace_ts[time]
    if f2 > 0:
        hat_S = Sn + f1 * f1 / (2 * f2)
    else:
        hat_S = Sn + f1 * (f1 - 1) / 2

if __name__ == '__main__':
    time

if __name__ == '__main__':
    Sn

if __name__ == '__main__':
    hat_S

if __name__ == '__main__':
    100 * Sn / hat_S

if __name__ == '__main__':
    trials

if __name__ == '__main__':
    trace_ts[trials - 1]

### Extrapolating Fuzzing Success

if __name__ == '__main__':
    print('\n### Extrapolating Fuzzing Success')



if __name__ == '__main__':
    prediction_ts = [None] * time
    f0 = hat_S - Sn

    for m in range(trials - time):
        assert (time * f0 + f1) != 0 , 'time:%s f0:%s f1:%s' % (time, f0,f1)
        prediction_ts.append(Sn + f0 * (1 - (1 - f1 / (time * f0 + f1)) ** m))

if __name__ == '__main__':
    plt.figure(num=None, figsize=(12, 3), dpi=80, facecolor='w', edgecolor='k')
    plt.subplot(1, 3, 1)
    plt.plot(trace_ts, color='white')
    plt.plot(trace_ts[:time])
    plt.xticks(range(0, trials + 1, int(time)))
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('# of traces exercised')

    plt.subplot(1, 3, 2)
    line_cur, = plt.plot(trace_ts[:time], label="Ongoing fuzzing campaign")
    line_pred, = plt.plot(prediction_ts, linestyle='--',
                          color='black', label="Predicted progress")
    plt.legend(handles=[line_cur, line_pred])
    plt.xticks(range(0, trials + 1, int(time)))
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('# of traces exercised')

    plt.subplot(1, 3, 3)
    line_emp, = plt.plot(trace_ts, color='grey', label="Actual progress")
    line_cur, = plt.plot(trace_ts[:time], label="Ongoing fuzzing campaign")
    line_pred, = plt.plot(prediction_ts, linestyle='--',
                          color='black', label="Predicted progress")
    plt.legend(handles=[line_emp, line_cur, line_pred])
    plt.xticks(range(0, trials + 1, int(time)))
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('# of traces exercised');

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Estimate and Evaluate the Discovery Probability for Statement Coverage

if __name__ == '__main__':
    print('\n### Exercise 1: Estimate and Evaluate the Discovery Probability for Statement Coverage')



#### Part 1: Population Coverage

if __name__ == '__main__':
    print('\n#### Part 1: Population Coverage')



from .Coverage import population_coverage, Coverage
...

def population_stmt_coverage(population, function):
    cumulative_coverage = []
    all_coverage = set()
    cumulative_singletons = []
    cumulative_doubletons = []
    singletons = set()
    doubletons = set()

    for s in population:
        with Coverage() as cov:
            try:
                function(s)
            except BaseException:
                pass
        cur_coverage = cov.coverage()

        # singletons and doubletons
        doubletons -= cur_coverage
        doubletons |= singletons & cur_coverage
        singletons -= cur_coverage
        singletons |= cur_coverage - (cur_coverage & all_coverage)
        cumulative_singletons.append(len(singletons))
        cumulative_doubletons.append(len(doubletons))

        # all and cumulative coverage
        all_coverage |= cur_coverage
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage, cumulative_singletons, cumulative_doubletons

#### Part 2: Population

if __name__ == '__main__':
    print('\n#### Part 2: Population')



from .Fuzzer import RandomFuzzer
from html.parser import HTMLParser
...

if __name__ == '__main__':
    trials = 2000  # increase to 10000 for better convergences. Will take a while..

def my_parser(inp):
    parser = HTMLParser()  # resets the HTMLParser object for every fuzz input
    parser.feed(inp)

if __name__ == '__main__':
    fuzzer = RandomFuzzer(min_length=1, max_length=1000,
                          char_start=0, char_range=255)

if __name__ == '__main__':
    population = []
    for i in range(trials):
        population.append(fuzzer.fuzz())

#### Part 3: Estimating Probabilities

if __name__ == '__main__':
    print('\n#### Part 3: Estimating Probabilities')



if __name__ == '__main__':
    measurements = 100  # experiment measurements
    step = int(trials / measurements)

    gt_timeseries = []
    singleton_timeseries = population_stmt_coverage(population, my_parser)[2]
    for i in range(1, trials + 1, step):
        gt_timeseries.append(singleton_timeseries[i - 1] / i)

#### Part 4: Empirical Evaluation

if __name__ == '__main__':
    print('\n#### Part 4: Empirical Evaluation')



if __name__ == '__main__':
    repeats = 100

if __name__ == '__main__':
    emp_timeseries = []
    all_coverage = set()
    for i in range(0, trials, step):
        if i - step >= 0:
            for j in range(step):
                inp = population[i - j]
                with Coverage() as cov:
                    try:
                        my_parser(inp)
                    except BaseException:
                        pass
                all_coverage |= cov.coverage()

        discoveries = 0
        for _ in range(repeats):
            inp = fuzzer.fuzz()
            with Coverage() as cov:
                try:
                    my_parser(inp)
                except BaseException:
                    pass
            # If intersection not empty, a new stmt was (dis)covered
            if cov.coverage() - all_coverage:
                discoveries += 1
        emp_timeseries.append(discoveries / repeats)

# %matplotlib inline
# import matplotlib.pyplot as plt
# line_emp, = plt.semilogy(emp_timeseries, label="Empirical")
# line_gt, = plt.semilogy(gt_timeseries, label="Good-Turing")
# plt.legend(handles=[line_emp, line_gt])
# plt.xticks(range(0, measurements + 1, int(measurements / 5)),
#            range(0, trials + 1, int(trials / 5)))
# plt.xlabel('# of fuzz inputs')
# plt.ylabel('discovery probability')
# plt.title('Discovery Probability Over Time');

### Exercise 2: Extrapolate and Evaluate Statement Coverage

if __name__ == '__main__':
    print('\n### Exercise 2: Extrapolate and Evaluate Statement Coverage')



#### Part 1: Create Population

if __name__ == '__main__':
    print('\n#### Part 1: Create Population')



if __name__ == '__main__':
    trials = 400  # Use 400000 for actual solution.  This takes a while!

if __name__ == '__main__':
    population = []
    for i in range(trials):
        population.append(fuzzer.fuzz())

    _, stmt_ts, Q1_ts, Q2_ts = population_stmt_coverage(population, my_parser)

#### Part 2: Compute Estimate

if __name__ == '__main__':
    print('\n#### Part 2: Compute Estimate')



if __name__ == '__main__':
    time = int(trials / 4)
    Q1 = Q1_ts[time]
    Q2 = Q2_ts[time]
    Sn = stmt_ts[time]

    if Q2 > 0:
        hat_S = Sn + Q1 * Q1 / (2 * Q2)
    else:
        hat_S = Sn + Q1 * (Q1 - 1) / 2

    print("After executing %d fuzz inputs, we have covered %d **(%.1f %%)** statements.\n" % (time, Sn, 100 * Sn / hat_S) +
          "After executing %d fuzz inputs, we estimate there are %d statements in total.\n" % (time, hat_S) +
          "After executing %d fuzz inputs, we have covered %d statements." % (trials, stmt_ts[trials - 1]))

#### Part 3: Compute and Evaluate Extrapolator

if __name__ == '__main__':
    print('\n#### Part 3: Compute and Evaluate Extrapolator')



if __name__ == '__main__':
    prediction_ts = [None] * time
    Q0 = hat_S - Sn

    for m in range(trials - time):
        prediction_ts.append(Sn + Q0 * (1 - (1 - Q1 / (time * Q0 + Q1)) ** m))

if __name__ == '__main__':
    plt.figure(num=None, figsize=(12, 3), dpi=80, facecolor='w', edgecolor='k')
    plt.subplot(1, 3, 1)
    plt.plot(stmt_ts, color='white')
    plt.plot(stmt_ts[:time])
    plt.xticks(range(0, trials + 1, int(time)))
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('# of statements exercised')

    plt.subplot(1, 3, 2)
    line_cur, = plt.plot(stmt_ts[:time], label="Ongoing fuzzing campaign")
    line_pred, = plt.plot(prediction_ts, linestyle='--',
                          color='black', label="Predicted progress")
    plt.legend(handles=[line_cur, line_pred])
    plt.xticks(range(0, trials + 1, int(time)))
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('# of statements exercised')

    plt.subplot(1, 3, 3)
    line_emp, = plt.plot(stmt_ts, color='grey', label="Actual progress")
    line_cur, = plt.plot(stmt_ts[:time], label="Ongoing fuzzing campaign")
    line_pred, = plt.plot(prediction_ts, linestyle='--',
                          color='black', label="Predicted progress")
    plt.legend(handles=[line_emp, line_cur, line_pred])
    plt.xticks(range(0, trials + 1, int(time)))
    plt.xlabel('# of fuzz inputs')
    plt.ylabel('# of statements exercised');
