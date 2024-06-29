# Dockerfile for fuzzingbook/debuggingbook (experimental)

# The repo2docker script takes a _very_ long time to execute,
# causing timeouts on mybinder. So, we provide this lightweight
# Dockerfile instead.

# To test, use
# docker build -t my-image binder

# For more infp, see
# https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
# https://github.com/binder-examples/minimal-dockerfile

# From minimal-dockerfile
# FROM python:3.10-slim
# From docker2repo
FROM docker.io/library/buildpack-deps:jammy

# Project name
ARG PROJECT=fuzzingbook
ARG REPO=https://github.com/uds-se/${PROJECT}.git

# Install git and pip
RUN apt-get update
RUN apt-get install -y git python3 pip gcc

# Some version info
RUN echo "This is ${PROJECT} with $(python3 --version)"

# Install jupyter
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache notebook jupyterlab

# Add the default user
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER=${NB_USER}
ENV HOME=/home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}

# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
WORKDIR ${HOME}

RUN git clone --depth 1 ${REPO}
RUN chown -R ${NB_UID} ${HOME}
WORKDIR ${PROJECT}

# Install the required Linux packages
RUN apt-get install -y $(grep -v '^#' binder/apt.txt); exit 0

# From here on, we are a user
USER ${NB_USER}

# Add local bin path
ENV PATH="/home/${NB_USER}/.local/bin:$PATH"

# Set up the conda environment
# (Skipping for now, as installing conda is hard)
# RUN conda env create -f binder/environment.yml
# RUN conda activate myenv

# Install the required Python packages
RUN pip install -r requirements.txt; exit 0
RUN pip install -r binder/requirements.txt; exit 0

# Run the postBuild script
RUN bash binder/postBuild
