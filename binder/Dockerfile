# Dockerfile for fuzzingbook/debuggingbook (experimental)

# The repo2docker script takes a _very_ long time to execute,
# causing timeouts on mybinder. So, we provide this lightweight
# Dockerfile instead.

# To test, use
#     make docker-image
# and then
#     make docker-run (for a jupyter notebook)
#     make docker-shell (for a bash shell)

# For more info, see
# https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
# https://github.com/binder-examples/minimal-dockerfile

# This Dockerfile is meant to be used in the mybinder environment,
# but it can also serve as a base to deploy docker images.

# From docker2repo
FROM docker.io/library/buildpack-deps:jammy

# Project name
ARG PROJECT=fuzzingbook
ARG REPO=https://github.com/uds-se/${PROJECT}.git

# Meta-data
LABEL description="${PROJECT}.org image from ${REPO}"

# Install git and pip
RUN apt-get update
RUN apt-get install -y git python3 python-is-python3 pip npm gcc

# Some version info
RUN echo "This is ${PROJECT} with $(python --version)" 1>&2

# Install jupyter
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache notebook jupyterlab

# Install mermaid
RUN npm i -g mermaid

# From postBuild script – apparently, we have to run this as root
RUN pip install jupyterlab-markup
RUN pip install jupyterlab-cell-flash
RUN jupyter labextension disable "@jupyterlab/apputils-extension:announcements"

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
# (Skipping for now, as installing conda is hard,
#  and apparently we can do without)
# RUN conda env create -f binder/environment.yml
# RUN conda activate myenv

# Install the required Python packages
RUN pip install -r requirements.txt; exit 0
RUN pip install -r binder/requirements.txt; exit 0

# Run the postBuild script (to set up Jupyter, sign notebooks and more)
RUN bash binder/postBuild

# Expose port 8888, so it can be reached from the outside (for local testing)
EXPOSE 8888

# If nothing else is specified, start a Jupyter server
CMD ["sh", "-c", "jupyter lab --port=8888 --no-browser --ip=* docs/notebooks"]
