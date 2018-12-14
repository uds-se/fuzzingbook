#!/bin/bash

# TODO: Eventually we should remove this and pin fuzzingbook to a specific version at build time
cd /home/${FB_USER}/fuzzingbook
git config --global user.email "fuzzingbook@example.com"
git config --global user.name "Fuzzingbook Docker"
git stash
git pull origin master
git stash apply
# if conflict on pop:
git merge --strategy-option ours

cd /home/${FB_USER}/FuzzManager/server/
celery -A celeryconf -l INFO -n worker@%h -Q celery worker &
python3 manage.py runserver 0.0.0.0:8000 &
cd /home/${FB_USER}
/usr/local/bin/jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser /home/${FB_USER}/${BASEDIR}
