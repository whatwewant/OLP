#!/bin/bash

# PACKAGES
pip install virtualenv virtualenvwrapper

# virtualenvwrapper
[[ -f "$HOME/.zshrc" ]] && \
    Xshrc="$HOME/.zshrc" || \
    Xshrc="$HOME/.bashrc"

cat $Xshrc | grep -i virtualenvwrapper.sh >> /dev/null 2>&1 || \
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> $Xshrc

source /usr/local/bin/virtualenvwrapper.sh

workon | grep django || mkvirtualenv -p python2 django

workon django && pip install -r /opt/OLP/requirements.txt

