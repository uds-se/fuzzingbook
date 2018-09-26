import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fuzzingbook",
    version="0.1",
    author="Andreas Zeller et al.",
    author_email="zeller@cs.uni-saarland.de",
    description="Code for 'Generating Software Tests'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.fuzzingbook.org/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing"
    ],
)
