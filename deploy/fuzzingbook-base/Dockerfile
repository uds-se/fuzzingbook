# We start with a bare minimum. This image has at the time of writing 27MB. 
FROM ubuntu

# Please change to whoever is going to maintain this.
LABEL Sascha Just <sascha.just@cispa.saarland>
LABEL description="v0.1"

# Tell debian that we are not in interactive mode.
ENV DEBIAN_FRONTEND noninteractive

# FB_USER holds the username (and thus group and home name) of our notebook user. 
ARG FB_USER=fuzzingbook
ENV FB_USER=${FB_USER}

# Specify whether we install publish extensions.
ARG PUBLISH=no

# This specifies the git repository that you want to clone.
ARG OWNER=uds-se
ENV OWNER=${OWNER}
ARG REPO=https://github.com/${OWNER}/fuzzingbook.git

# Since you are running git within the container, this specifies the branch we
# want to checkout and work on.
# I'd prefer mounting the clone from the host machine into the container which would
# drastically reduce the size of the image—not just because of the size of the Git 
# repository, but also because all of the dependencies we have to install to bring a 
# Git client. This almost doubles the size of the
ARG BRANCH=master

# The directory that is used for the clone and for the jupyter notebook as base
# directory. 
ARG BASEDIR=FuzzingBook

# Here, we specify package versions. This simplifies updates of individual packages
# and dependencies without changing the actual routines within the Dockerfile.
ARG FUZZINGBOOK_VERSION=master 
ARG FUZZMANAGER_VERSION=0.3.2 
ARG GRCOV_VERSION=0.3.2 
ARG TINI_VERSION=0.18.0

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
ADD requirements.txt /root/install-requirements.txt
# ADD https://raw.githubusercontent.com/$OWNER/fuzzingbook/${FUZZINGBOOK_VERSION}/deploy/fuzzingbook-base/requirements.txt /root/install-requirements.txt
ADD https://raw.githubusercontent.com/$OWNER/fuzzingbook/$FUZZINGBOOK_VERSION/binder/requirements.txt /root/fuzzingbook-requirements.txt
ADD https://raw.githubusercontent.com/MozillaSecurity/FuzzManager/${FUZZMANAGER_VERSION}/server/requirements.txt /root/fuzzmanager-requirements.txt

# Same for the ubuntu packages. These have been moved to a file to facilitate 
# the installation and mainenance. 
ADD apt.txt /root/install-packages.txt
# ADD https://raw.githubusercontent.com/$OWNER/fuzzingbook/${FUZZINGBOOK_VERSION}/deploy/fuzzingbook-base/apt.txt /root/install-packages.txt
ADD https://raw.githubusercontent.com/$OWNER/fuzzingbook/${FUZZINGBOOK_VERSION}/binder/apt.txt /root/fuzzingbook-packages.txt

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
    npm \
  && apt-get install --no-install-recommends -y $(<install-packages.txt) $(grep -v -e '^\s*#' fuzzingbook-packages.txt) \
  && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
  && echo 'LANG="en_US.UTF-8"' > /etc/default/locale \
  && dpkg-reconfigure --frontend=noninteractive locales \
  && update-locale LANG=en_US.UTF-8 \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3 get-pip.py \
  && pip3 install \
      jupyter \
      jupyterhub \
      -r install-requirements.txt \
      -r fuzzingbook-requirements.txt \
  && pip3 install \
      -r fuzzmanager-requirements.txt \
      https://github.com/MozillaSecurity/FuzzManager/archive/${FUZZMANAGER_VERSION}.tar.gz \
  && npm install -g configurable-http-proxy \
  && curl -o grcov-linux-x86_64.tar.bz2 --location https://github.com/mozilla/grcov/releases/download/v${GRCOV_VERSION}/grcov-linux-x86_64.tar.bz2 \
  && tar xjf grcov-linux-x86_64.tar.bz2 \
  && mv grcov /usr/local/bin/ \
  && rm -f *-requirements.txt *-packages.txt grcov-linux-x86_64.tar.bz2 \
  && apt-get clean \
  && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

ADD notebookapp.py /usr/local/lib/python3.6/dist-packages/notebook/notebookapp.py

# We run tini as an entry point. 
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ENTRYPOINT ["/tini", "--"]

# Switch to the notebook user and prepare the work environment.
USER ${FB_USER}
WORKDIR /home/${FB_USER}

# Patch to change certain FuzzManager settings
ADD settings.py.patch /home/${FB_USER}/settings.py.patch

# Clone the fuzzingbook repository and use it as working directory for 
# the jupyter instance. We shallow clone and omit history at this point
# to speed up initial build process. You can change (remove the switch)
# this at any time to get a full clone.
RUN git clone --branch ${BRANCH} --depth 1 https://github.com/$OWNER/fuzzingbook.git ${BASEDIR} \
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
  && mkdir -p .jupyter/custom && cp ${BASEDIR}/docs/beta/notebooks/custom.css .jupyter/custom/ \
  && curl -o fuzzmanager.tar.gz --location https://github.com/MozillaSecurity/FuzzManager/archive/0.3.2.tar.gz \
  && tar xzf fuzzmanager.tar.gz \
  && rm -f fuzzmanager.tar.gz \
  && mv FuzzManager-${FUZZMANAGER_VERSION} FuzzManager \
  && python3 FuzzManager/server/manage.py migrate \
  && python3 FuzzManager/server/manage.py createsuperuser --username demo --email demo@example.com --no-input \
  && python3 FuzzManager/server/manage.py shell -c 'from django.contrib.auth.models import User; user = User.objects.get(username="demo"); user.set_password("demo"); user.save();' \
  && echo -ne "[Main]\nsigdir = /home/${FB_USER}/signatures/\ntool = fuzzingbook\nserverport = 8000\nserverproto = http\nserverhost = 127.0.0.1\nserverauthtoken = " > .fuzzmanagerconf \
  && python3 FuzzManager/server/manage.py get_auth_token demo >> .fuzzmanagerconf \
  && mkdir /home/${FB_USER}/signatures/ \
  && (cd FuzzManager && patch -p1 < /home/${FB_USER}/settings.py.patch)

# Adding configuration for jupyter. This sets a constant token, such that connecting
# with external tools like VSCode, Atom or IntelliJ can use a constant config. 
ADD --chown=fuzzingbook:fuzzingbook jupyter_notebook_config.py /home/${FB_USER}/.jupyter/

USER root
ADD startup.sh /startup.sh
ADD startup-user.sh /startup-user.sh

# I am running notebook here. Feel free to change this to hub, lab, or whatever you guys prefer.
EXPOSE 8000 8888
CMD bash /startup.sh
