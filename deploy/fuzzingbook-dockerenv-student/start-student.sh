#!/bin/bash

# First: Update from github
cd /home/jovyan/fuzzingbook
git config --global user.email "fuzzingbook@example.com"
git config --global user.name "Fuzzingbook Docker"
git stash
git pull origin master
git stash apply
# if conflict on pop:
git merge --strategy-option ours

cd ~

# Start Jupyter Lab
set -e

jupyter notebook --notebook-dir='/home/jovyan/fuzzingbook/docs/beta/notebooks/'
