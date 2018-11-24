# We start with a bare minimum. This image has at the time of writing 27MB. 
FROM ubuntu

# Please change to whoever is going to maintain this.
LABEL Sascha Just <sascha.just@cispa.saarland>
LABEL description="v0.1"

# FB_USER holds the username (and thus group and home name) of our notebook user. 
ARG FB_USER=fuzzingbook

# Specify whether we install publish extensions.
ARG PUBLISH

# Since you are running git within the container, this specifies the branch we
# want to checkout and work on.
# I'd prefer mounting the clone from the host machine into the container which would
# drastically reduce the size of the image—not just because of the size of the Git 
# repository, but also because all of the dependencies we have to install to bring a 
# Git client. This almost doubles the size of the image.
ARG BRANCH=master

# The directory that is used for the clone and for the jupyter notebook as base
# directory. 
ARG BASEDIR=work

# Here, we specify package versions. This simplifies updates of individual packages
# and dependencies without changing the actual routines within the Dockerfile.
ENV TINI_VERSION=0.18.0 \
    FUZZMANAGER_VERSION=0.3.2 \
    FUZZINGBOOK_VERSION=0.1

# Set the default shell from /bin/sh to /bin/bash. 
SHELL ["/bin/bash", "-c"]

# This gets rid of all man pages and docs when installing packages using apt.
# The image is not made for comfortable shell access but only to serve the
# fuzzingbook using jupyter notebook/hub.
ADD 01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc

# Create the notebook user and its home directory.
RUN useradd -c 'FuzzingBook User' -d /home/${FB_USER} -m -s /bin/bash -U ${FB_USER} 

# Set the current working directory to the superuser's home
USER root
WORKDIR /root

# I moved all python package dependencies to an external file.
# This avoids convolution of the Dockerfile while providing a central point for 
# authors to add dependencies they require. Please keep in mind, that we also
# pull dependencies for fuzzmanager from the fuzzmanager GitHub repository which
# should not collide. Chris losened the dependencies of fuzzmanager quite a bit.
# So far, the only package for our internal dependencies are numpy; hence I 
# removed it from the file and kept everything else I could find in the original
# Dockerfile. 
# 
# TODO: Once this is merged upstream, we can just provide the link to the file 
# in the corresponding tag in the repository on GitHub as we do for fuzzmanager
# in the superuser installation block below, e.g.
# https://raw.githubusercontent.com/uds-se/fuzzingbook/${FUZZINGBOOK_VERSION}/deploy/fuzzingbook-base/requirements.txt
ADD fuzzingbook-requirements-${FUZZINGBOOK_VERSION}.txt /root/fuzzingbook-requirements.txt

# Same for the ubuntu packages. These have been moved to a file to facilitate 
# the installation and mainenance. Can also be changed to a link to the GitHub
# repository once merged.
# https://raw.githubusercontent.com/uds-se/fuzzingbook/${FUZZINGBOOK_VERSION}/deploy/fuzzingbook-base/packages.txt
ADD fuzzingbook-packages-${FUZZINGBOOK_VERSION}.txt /root/fuzzingbook-packages.txt

# Install python3, curl and git using apt.
# Install pip manually (to avoid installing 0.9 using apt first, upgrading and 
# fixing the installation later on)
# We need distutils to work-around most python2to3 issues.
# Lastly, install all python packages that are required to run jupyter, fuzzmanager
# and fuzzingbook notebooks. 
# Clean up after us (IN THE SAME RUN COMMAND). This is important. If we do this
# in two steps, the intermediate image layers will grow significantly in size. 
RUN set -x \
  && apt-get update \
  && apt-get install -y curl \
  && apt-get install --no-install-recommends -y \
    python3 \
    python3-distutils \
    git \
  && apt-get install --no-install-recommends -y $(<fuzzingbook-packages.txt) \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3 get-pip.py \
  && curl -o fuzzmanager-requirements.txt https://raw.githubusercontent.com/MozillaSecurity/FuzzManager/${FUZZMANAGER_VERSION}/server/requirements.txt \
  && pip3 install jupyter -r fuzzingbook-requirements.txt -r fuzzmanager-requirements.txt https://github.com/MozillaSecurity/FuzzManager/archive/${FUZZMANAGER_VERSION}.tar.gz \
  && rm -f fuzzingbook-requirements.txt fuzzmanager-requirements.txt fuzzingbook-packages.txt \
  && apt-get clean \
  && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

# We run tini as an entry point. 
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# Switch to the notebook user and prepare the work environment.
USER ${FB_USER}
WORKDIR /home/${FB_USER}

# clone the fuzzingbook repository and use it as working directory for 
# the jupyter instance. 
RUN git clone --branch ${BRANCH} https://github.com/uds-se/fuzzingbook.git ${BASEDIR} \
  && nbdime extensions --enable \
  && jupyter nbextension enable nbdime --py \
  && nbdime config-git --enable --global \
  && jupyter contrib nbextension install --user \
  && for extension in \
      toc2/main \
      exercise2/main \
      codefolding/main \
      execute_time/main \
      varInspector/main \
      collapsible_headings/main \
      select_keymap/main \
      spellchecker/main \
      scratchpad/main; do \
       jupyter nbextension enable --user "$extension"; \
     done \
  && test -n $PUBLISH && for extension in \
      code_prettify/autopep8 \
      code_prettify/code_prettify; do \
        jupyter nbextension enable --user "$extension"; \
     done || true \
  && shopt -s globstar \
  && jupyter trust ${BASEDIR}/**/*.ipynb \
  && mkdir -p .jupyter/custom && cp ${BASEDIR}/docs/beta/notebooks/custom.css .jupyter/custom/
CMD /usr/local/bin/jupyter notebook --ip=0.0.0.0 --port=8080 ${HOME}/${BASEDIR}
