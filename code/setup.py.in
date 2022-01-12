#!/usr/bin/env python

import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read().decode('utf-8')

# See https://packaging.python.org/tutorials/packaging-projects/ for details
setuptools.setup(
    name="fuzzingbook",
    version="1.0.6",
    author="Andreas Zeller et al.",
    author_email="zeller@cispa.de",
    description="Code for 'The Fuzzing Book' (https://www.fuzzingbook.org/)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.fuzzingbook.org/",
    packages=['fuzzingbook', 'fuzzingbook.bookutils'],
    python_requires='>=3.9',  # Mostly for ast.unparse()
    # packages=setuptools.find_packages(),

    # From requirements.txt
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'cargo>=0.3',
        'diff_match_patch>=20200713',
        'easyplotly>=0.1.3',
        'enforce>=0.3.4',
        'fuzzingbook>=0.8.1',
        'graphviz>=0.14.2',
        'ipython>=7.16.1',
        'lxml>=4.5.1',
        'Markdown>=3.3.4',
        'matplotlib>=3.3.2',
        'multiprocess>=0.70.12.2',
        'nbconvert>=6.0.7',
        'nbformat>=5.0.8',
        'networkx>=2.5',
        'numpy>=1.16.5',
        'pandas>=1.3.3',
        'notedown>=1.5.1',
        # Can't have external packages referenced on pypi, so commented out:
        # 'pyan@git+https://github.com/uds-se/pyan#egg=pyan',
        'pydot>=1.4.2',
        'pyparsing==2.4.7',  # newer versions conflict with bibtexparser
        'pydriller>=2.0',
        'Pygments>=2.7.1',
        'python-magic>=0.4.18',
        'scikit_learn>=0.23.2',
        'scipy>=1.7.1',
        'selenium>=3.141.0',
        'showast>=0.2.4',
        'svglib>=1.1.0',
        'types-Markdown>=3',
        'yapf>=0.31.0',
        'z3-solver>=4.8.13.0',
    ],

    # See https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Education :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Security"
    ],
)
