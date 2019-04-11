FROM jupyter/scipy-notebook

LABEL maintainer="Nataniel Borges Jr."
LABEL description="v0.1"

USER root

# Install required APT packages
RUN apt-get update
RUN apt-get install -y --no-install-recommends graphviz curl inkscape bc ed texinfo groff wget
RUN if [ "$publish" = "yes" ]; then apt-get install -y --no-install-recommends firefox vim tmux ; fi
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

USER $NB_UID

ARG publish=yes
ARG branch=master

# Install required python packages
RUN if [ "$publish" = "yes" ]; then conda install -c anaconda python=3.6 ; fi
RUN if [ "$publish" = "yes" ]; then conda install -c conda-forge geckodriver ; fi
RUN if [ "$publish" = "yes" ]; then conda install -c conda-forge selenium ; fi
RUN if [ "$publish" = "yes" ]; then pip install ipypublish==0.6.7 autopep8 yapf ; fi
RUN pip install jupyter jupyterlab matplotlib scipy numpy pandas graphviz svglib jupyter_contrib_nbextensions mypy notedown nbdime nbstripout astunparse enforce==0.3.4 showast astor z3-solver tornado
RUN pip install git+https://github.com/ttylec/pyan#egg=pyan

WORKDIR /home/$NB_USER

# Clone the repo
RUN git clone --branch ${branch} https://github.com/uds-se/fuzzingbook.git
RUN fix-permissions /home/$NB_USER/fuzzingbook

USER root

# Activate nbdime and nbstripout
#RUN nbdime config-git --enable
RUN nbdime extensions --enable
RUN nbdime config-git --enable --global
#RUN nbstripout --install --attributes .gitattributes
WORKDIR /home/$NB_USER/fuzzingbook

# enable nbdime for JupyterLab
RUN conda install -c conda-forge nodejs # you
#RUN jupyter labextension install nbdime-jupyterlab

# Install aditional extensions (ToC and exercise)
RUN jupyter contrib nbextension install --user
RUN jupyter nbextension enable toc2/main --user
RUN jupyter nbextension enable exercise2/main --user

#RUN jupyter extensions enable nbdime --user -py
# Other useful extensions
RUN jupyter nbextension enable codefolding/main --user
RUN jupyter nbextension enable execute_time/main --user
RUN jupyter nbextension enable varInspector/main --user
RUN jupyter nbextension enable collapsible_headings/main --user
RUN jupyter nbextension enable select_keymap/main --user
RUN jupyter nbextension enable spellchecker/main --user
RUN jupyter nbextension enable scratchpad/main --user

RUN if [ "$publish" = "yes" ]; then jupyter nbextension enable code_prettify/autopep8 --user ; fi
RUN if [ "$publish" = "yes" ]; then jupyter nbextension enable code_prettify/code_prettify --user ; fi

# run matplotlib once to generate the font cache
RUN python -c "import matplotlib as mpl; mpl.use('Agg'); import pylab as plt; fig, ax = plt.subplots(); fig.savefig('test.png')"
RUN test -e test.png
RUN rm test.png

# Trust notebooks such that users can see their HTML and JS output
RUN jupyter trust /home/$NB_USER/fuzzingbook/notebooks/*.ipynb /home/$NB_USER/fuzzingbook/docs/notebooks/*.ipynb /home/$NB_USER/fuzzingbook/docs/beta/notebooks/*.ipynb

# Copy Andreas' css to jupyter
RUN mkdir /home/$NB_USER/.jupyter/custom
RUN fix-permissions /home/$NB_USER/.jupyter
RUN wget -O /home/$NB_USER/.jupyter/custom/custom.css https://github.com/uds-se/fuzzingbook/blob/master/docs/beta/notebooks/custom.css
RUN ls

# Fix directory permissions
RUN fix-permissions /home/$NB_USER/.local
RUN fix-permissions /home/$NB_USER/.local/share/jupyter

# Remove temporary content
RUN apt-get clean
RUN apt-get autoremove
RUN rm -rf /var/lib/apt/lists/*

COPY start-singleuser-custom.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-singleuser-custom.sh
RUN mv /usr/local/bin/start-singleuser.sh /usr/local/bin/start-singleuser-old.sh
#RUN cp /usr/local/bin/custom-start.sh /usr/local/bin/start-singleuser.sh

# Quit root mode
USER $NB_UID
ENV EXECUTE_TIMEOUT=3000
