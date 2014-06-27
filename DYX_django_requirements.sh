#!/bin/bash
# Program:
#	Auto Install Necessary Tools For Project 'OLP'
#
# History:
#	2014/05/02	Potter	Version 1.0.0
#
#--------------------------------------------------------------
#	Requirements:
#		1. django==1.5.5
#		2. django-debug-toolbar==1.2.
#		3. Python Imaging Library (PIL) 1.7
#       4. south
#	
#	Platform:
#		Ubuntu

ScriptName="This Script"
CurrentDir=$(pwd)
BuildDir=${CurrentDir}"/BuildANO"

rm -rf $BuildDir	
mkdir $BuildDir	
cd $BuildDir

# Before Installation, we need some download tools
which pip > /dev/null
if [ "$?" != "0" ]; then
    sudo apt-get install -y python-pip python-dev
fi

which virtualenv > /dev/null
if [ "$?" != "0" ]; then
    sudo apt-get install -y python-virtualenv python-setuptools
fi

# git-flow
sudo apt-get install git-flow

# all installed packages
packages=$(pip list)

# 1. Install django==1.5.5
echo $packages | grep Django | grep 1.5.5 > /dev/null
if [ "$?" != "0" ]; then
    pip install django==1.5.5
    if [ "$?" != "0" ]; then
	    git clone https://github.com/django/django.git django1.5.x
	    cd django.1.5.x
	    python setup.py install
	    cd ..
    fi
else
    echo "已安装django==1.5.5" | tee install.log
fi

# 2. Install django-debug-toolbar=1.2 ( Here will Instll latest Version, now is 1.2)
echo $packages | grep django-debug-toolbar | grep 1.2> /dev/null
if [ "$?" != "0" ]; then
    git clone https://github.com/django-debug-toolbar/django-debug-toolbar.git django-debug-toolbar
    cd django-debug-toolbar
    python setup.py install
    cd ..
else
    echo "已安装django-debug-tools==1.2" | tee install.log
fi

# 3. Install Python Imaging Library (PIL) 1.1.7
echo $packages | grep PIL | grep 1.1.7 > /dev/null
if [ "$?" != "0" ]; then
    easy_install -f http://www.pythonware.com/products/pil/ Imaging
    if [ "$?" != "0" ]; then
	    wget https://gitcafe.com/Potter/Softwares/raw/master/Imaging-1.1.7.tar.gz
	    tar -zxvf Imaging-1.1.7.tar.gz
	    cd Imaging*
	    python setup.py install
	    cd ..
    fi
else
    echo "已安装PIL==1.1.7" | tee install.log
fi

# 4 south
echo $packages | grep -i south > /dev/null
if [ "$?" != "0" ]; then
    pip install south
else
    echo "已安装South" | tee install.log
fi

# 5 linaro-django-pagination 第三方分页插件
echo $packages | grep -i linaro-django-pagination > /dev/null
if [ "$?" != "0" ]; then
    pip install linaro-django-pagination
else
    echo "已安装linaro-django-pagination" | tee install.log
fi

# 6 ipython
echo $packages | grep -i ipython > /dev/null
if [ "$?" != "0" ]; then
    pip install ipython
else
    echo "已安装ipython" | tee install.log
fi

# 7 requests
echo $packages | grep -i requests > /dev/null
if [ "$?" != "0" ]; then
    pip install requests
else
    echo "已安装requests" | tee install.log
fi

# Clear
cd $CurrentDir
rm -rf $BuildDir

exit 0
