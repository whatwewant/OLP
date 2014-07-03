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

os=$(cat /etc/issue)

# Before Installation, we need some download tools
which pip > /dev/null
if [ "$?" != "0" ]; then
	if [ "$(echo $os | grep -i 'arch' | wc -l)" != "0" ]; then
		sudo pacman -S --noconfirm python-pip
	elif [ "$(echo $os | grep -i 'ubuntu' | wc -l)" != "0" ]; then
    	sudo apt-get install -y python-pip
	fi
fi

which virtualenv > /dev/null
if [ "$?" != "0" ]; then
	if [ "$(echo $os | grep -i 'arch' | wc -l)" != "0" ]; then
		sudo pacman -S --noconfirm python-virtualenv python-setuptools
	elif [ "$(echo $os | grep -i 'ubuntu' | wc -l)" != "0" ]; then
    	sudo apt-get install -y python-virtualenv python-setuptools
	fi
fi

# git-flow
if [ "$(echo $os | grep -i 'arch' | wc -l)" != "0" ]; then
	##
	# PIL : make need freetype/freetype.h
	if [ ! -d "/usr/include/freetype" ]; then
		sudo ln -s /usr/include/freetype2 /usr/include/freetype
	fi
	#
	which git > /dev/null
	if [ "$?" != "0" ]; then
		sudo pacman -S --noconfirm git
	fi
elif [ "$(echo $os | grep -i 'ubuntu' | wc -l)" != "0" ]; then
	sudo apt-get install -y git-flow python-dev
	#sudo apt-get install -y mysql-server mysql-client apache2
    #sudo apt-get install -y libapache2-mod-wsgi
    # ubuntu install python-mysqldb
    #sudo apt-get install -y python-mysqldb
    # for 'pip install mysql-python': sh: 1: mysql_config: not found
    #sudo apt-get install -y libmysqld-dev libmysqlclient-dev
fi

# pip install mysql-python
#pip install mysql-python

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

# 8 uwsgi
echo $packages | grep -i uwsgi > /dev/null
if [ "$?" != "0" ]; then
    pip install uwsgi
else
    echo "已安装uwsgi" | tee install.log
fi

# 9 flup
echo $packages | grep -i flup > /dev/null
if [ "$?" != "0" ]; then
    pip install flup
else
    echo "已安装flup" | tee install.log
fi


# Clear
cd $CurrentDir
rm -rf $BuildDir

exit 0
