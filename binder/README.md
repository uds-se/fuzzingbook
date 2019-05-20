This folder holds the configuration files for the Binder service.
See [repo2docker](https://repo2docker.readthedocs.io/en/latest/) for details.

The configuration files are:

* apt.txt - APT Packages (= Linux programs) used
* environment.yml - Python packages used
* requirements.txt - more Python packages used

These files can also be used to create a conda environment for the book as follows:

```
conda env create -f binder/environment.yml
source activate fuzzingbook
```
