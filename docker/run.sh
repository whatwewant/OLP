#!/bin/bash
# 
# set -e
service mysql restart
source /usr/local/bin/virtualenvwrapper.sh
workon django

cd /opt/OLP
./manage.py syncdb --noinput
# ; ./manage.py migrate
# uwsgi --ini uwsgi.ini
