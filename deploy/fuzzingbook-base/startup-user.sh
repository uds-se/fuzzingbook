#!/bin/bash
cd /home/${FB_USER}/FuzzManager/server/
celery -A celeryconf -l INFO -n worker@%h -Q celery worker &
python3 manage.py runserver 0.0.0.0:8000 &
cd /home/${FB_USER}
/usr/local/bin/jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser /home/${FB_USER}/${BASEDIR}
