#!/bin/bash
# 
# *************************************************
# File Name    : mysql-init.sh
# Author       : Cole Smith
# Mail         : tobewhatwewant@gmail.com
# Github       : whatwewant
# Created Time : 2016年03月27日 星期日 00时30分19秒
# *************************************************
sudo service mysql restart
if [ $? -eq 0 ]; then
    echo "mysql startup successful!"
else
    echo "mysql startup failed!"
    exit 1
fi

echo "create Online Learning Platform database, user, password"
mysql -uroot -p'pw123456' -e "CREATE DATABASE olp character SET utf8; CREATE user 'olpuser'@'127.0.0.1' IDENTIFIED BY 'olppassword'; GRANT ALL privileges ON olp.* TO 'olpuser'@'127.0.0.1'; FLUSH PRIVILEGES;"
