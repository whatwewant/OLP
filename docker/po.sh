#!/bin/bash
export DJANGO_SETTINGS_MODULE=OLP.settings
source /usr/local/bin/virtualenvwrapper.sh
workon django

cd /opt/OLP
python JianShu.py
