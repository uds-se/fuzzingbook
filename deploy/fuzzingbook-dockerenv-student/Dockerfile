FROM fuzzingbook/user

# Quit root mode
USER root

COPY start-student.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-student.sh

# Quit root mode
USER $NB_UID

ENTRYPOINT "start-student.sh"
