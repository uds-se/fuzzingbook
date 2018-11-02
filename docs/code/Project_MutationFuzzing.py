#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Project_MutationFuzzing.html
# Last change: 2018-10-30 13:23:20+01:00
#
#
# Copyright (c) 2018 Saarland University, CISPA, authors, and contributors
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


import fuzzingbook_utils

# # Project 1 - Mutation Fuzzing

if __name__ == "__main__":
    print('# Project 1 - Mutation Fuzzing')




import sys
import logging
import os

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

if __name__ == "__main__":
    # Required to run svglib on Python3
    xrange = range


if __name__ == "__main__":
    logging.disable(logging.ERROR)

    RUN_EVALUATION = False
    DEBUG = True
    COUNT = 0

    def parse_svg(data):
        if DEBUG:
            global COUNT
            if COUNT % 1000 == 0:
                print(COUNT)
            COUNT += 1

        pdf_file = 'tmp.pdf'
        png_file = 'tmp.png'
        svg_file = 'tmp.svg'
        try:
            with open(svg_file, "w") as f:
                f.write(data)

            drawing = svg2rlg(svg_file)

            assert(drawing is not None)

            renderPDF.drawToFile(drawing, pdf_file)
            #renderPM.drawToFile(drawing, png_file)

            return drawing
        finally:
            if os.path.exists(svg_file):
                os.remove(svg_file)

            if os.path.exists(png_file):
                os.remove(png_file)

            if os.path.exists(pdf_file):
                os.remove(pdf_file)


if __name__ == "__main__":
    xrange(10)


if __name__ == "__main__":
    parse_svg("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <path d="M17,30l19-12l43,54l-17,15zM14,84c12-20 46-61 61-72l13,19 c-17,10-50,50-60,64z" fill="#C30" stroke-linejoin="round" stroke-width="6" stroke="#C30"></path>
    </svg>""")


# ## Auxiliary functions

if __name__ == "__main__":
    print('\n## Auxiliary functions')




import sys
from lxml import etree

def svg_as_tree(data):
    """Converts a String representation of an SVG into an ElementTree and returns its root

    :param data: String representation of an SVG
    :return: ElementTree https://docs.python.org/3/library/xml.etree.elementtree.html
    """
    parser = etree.XMLParser(encoding='utf-8')
    root = etree.fromstring(data.encode('utf-8'), parser=parser)
    return root

if __name__ == "__main__":
    svg_string = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <path d="M19,19h58v58h-58z" stroke="#000" fill="none" stroke-width="4"/>
      <path d="M17,30l19-12l43,54l-17,15zM14,84c12-20 46-61 61-72l13,19 c-17,10-50,50-60,64z" fill="#C30" stroke-linejoin="round" stroke-width="6" stroke="#C30"/>
      <cicle/>
    </svg>
    """
    root_node = svg_as_tree(svg_string)
    print("%s - %s" % (root_node.tag, root_node.attrib))


if __name__ == "__main__":
    # Printing immediate child nodes:
    for child in root_node:
        print("%s - %s" % (child.tag, child.attrib))


if __name__ == "__main__":
    # Accessing and changing properties
    first_child = root_node[0]
    print("old value of stroke-width: %s" % first_child.attrib['stroke-width'])

    first_child.attrib['stroke-width'] = "99"
    print("new value of stroke-width: %s" % first_child.attrib['stroke-width'])


if __name__ == "__main__":
    new_string = etree.tostring(root_node)
    print(new_string)


# # Fuzzer template

if __name__ == "__main__":
    print('\n# Fuzzer template')




if __package__ is None or __package__ == "":
    from Coverage import Coverage
else:
    from .Coverage import Coverage

from MutationFuzzer import MutationCoverageFuzzer, FunctionCoverageRunner

class Project1MutationCoverageFuzzer(MutationCoverageFuzzer):
    def __init__(self, min_mutations=2, max_mutations=10):
        seed = self._get_initial_seed()
        super().__init__(seed, min_mutations, max_mutations)

    def _get_initial_seed(self):
        """Gets the initial seed for the fuzzer

        :return: List of SVG in string format
        """

        seed_dir = os.path.join(".", "data", "svg-full")
        seed_files = list(filter(lambda f: ".svg" in f, os.listdir(seed_dir)))

        seed = []
        for f in seed_files:
            with open(os.path.join(seed_dir, f)) as x:
                s = ''.join(x.readlines()).strip()
                seed.append(s)

        print("Seed size: " + str(len(seed)) + " files")
        return seed

# ## Fuzzing the _svglib_

if __name__ == "__main__":
    print('\n## Fuzzing the _svglib_')




if __package__ is None or __package__ == "":
    from ExpectError import ExpectTimeout, ExpectError
else:
    from .ExpectError import ExpectTimeout, ExpectError


class FunctionCoverageRunnerWithTimeout(FunctionCoverageRunner):
    def __init__(self, function, timeout=1):
        self._timeout = timeout
        super().__init__(function)

    def run(self, inp):
        outcome = self.FAIL
        result = None
        self._coverage = []
        
        with ExpectError(mute=True):
            with ExpectTimeout(self._timeout, mute=True):
                result = self.run_function(inp)
                outcome = self.PASS

        return result, outcome

if __name__ == "__main__":
    parse_svg_runner = FunctionCoverageRunnerWithTimeout(parse_svg)


import datetime
import random

def run_experiment(fuzzer, start_seed=2000, end_seed=2005, trials=10000):
    print("Started fuzzing at %s" % str(datetime.datetime.now()))

    experiment_population = []
    for seed in range(start_seed, end_seed):
        print("Starting seed %d at %s" % (seed, str(datetime.datetime.now())))
        random.seed(seed)

        fuzzer.reset()
        fuzzer.runs(parse_svg_runner, trials)

        experiment_population.append(fuzzer.population)

    print("Finished fuzzing at %s" % str(datetime.datetime.now()))
    
    return experiment_population

if __name__ == "__main__":
    mutation_fuzzer = Project1MutationCoverageFuzzer()


if __name__ == "__main__":
    experiment_population = run_experiment(mutation_fuzzer, trials=10)


# ## Obtaining the population coverage

if __name__ == "__main__":
    print('\n## Obtaining the population coverage')




import matplotlib.pyplot as plt

def population_coverage(population, function):
    cumulative_coverage = []
    all_coverage = set()

    for s in population:
        with Coverage() as cov:
            with ExpectError(mute=True):
                with ExpectTimeout(1, mute=True):
                    function(s)
        all_coverage |= cov.coverage()
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage

# # Your code

if __name__ == "__main__":
    print('\n# Your code')




class Project1MutationCoverageFuzzer(Project1MutationCoverageFuzzer):
    # <Write your code here>
    pass

# # Evaluation

if __name__ == "__main__":
    print('\n# Evaluation')




def evaluate(populations):
    global COUNT
    coverages = []
    seen_statements = set()

    for idx, population in enumerate(populations):
        COUNT = 0
        all_coverage, cumulative_coverage = population_coverage(
            populations[idx], parse_svg)

        seen_statements |= all_coverage
        coverages.append(len(all_coverage))

        plt.plot(cumulative_coverage)
        plt.title('Coverage of parse_svg() with random inputs')
        plt.xlabel('# of inputs')
        plt.ylabel('lines covered')
        print("Covered lines (run %d) %d" % (idx, len(all_coverage)))
        print("Unique elements (run %d) %d" % (idx, len(cumulative_coverage)))        

    return tuple([sum(coverages) / len(coverages), len(seen_statements)])

if __name__ == "__main__":
    print("Average coverage: %d - Total achieved coverage: %d" % evaluate(experiment_population))


# ## Evaluation scheme

if __name__ == "__main__":
    print('\n## Evaluation scheme')




if __name__ == "__main__":
    if RUN_EVALUATION:
        print("Initializing evaluation")
        parse_svg_runner = FunctionCoverageRunnerWithTimeout(parse_svg)
        mutation_fuzzer = Project1MutationCoverageFuzzer()
        print("Running experiment")
        experiment_population = run_experiment(mutation_fuzzer, trials=10000)


if __name__ == "__main__":
    if RUN_EVALUATION:
        print("Computing results")
        avg_statements, total_statements = evaluate(experiment_population)

        print("Final result: Average coverage: %d - Total achieved coverage: %d" % (avg_statements, total_statements))

