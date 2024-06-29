# Dockerfile for fuzzingbook (experimental)

# The repo2docker script takes a _very_ long time to execute,
# causing timeouts on mybinder. So, we provide this lightweight
# Dockerfile instead.

# For more infp, see
# https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
# https://github.com/binder-examples/minimal-dockerfile

# From minimal-dockerfile
FROM python:3.10-slim

# Install jupyter
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache notebook jupyterlab

# Install git
RUN apt update
RUN apt install -y git

# Add the default user
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}
USER ${USER}

# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

# Clone the book repository
RUN git clone --depth 1 https://github.com/uds-se/fuzzingbook.git
WORKDIR fuzzingbook

# Install the required Linux packages
USER root
RUN apt install -y $(grep -v '^#' binder/apt.txt); exit 0
USER ${NB_USER}

# Set up the conda environment
# (Skipping for now, as installing conda is hard)
# RUN conda env create -f binder/environment.yml
# RUN conda activate myenv

# Install the required Python packages
RUN pip install -r binder/requirements.txt; exit 0

# Run the postBuild script
RUN bash binder/postBuild
