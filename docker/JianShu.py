#!/usr/bin/env python
# coding=utf-8
#*************************************************************************
#       > File Name: JianShu_Django.py
#       > Author: Potter
#       > Mail: tobewhatwewant@gmail.com
#       > Created Time: 2014年08月30日 星期六 10时10分24秒
# ************************************************************************/

import requests
from bs4 import BeautifulSoup
import re
import time
import os, sys
from django.core.management import setup_environ
from OLP import settings


from utils.shortcuts import write_article_unknown_category_and_author

reload(sys)
sys.setdefaultencoding('utf-8')

def get_title_and_content(aid):
    html = requests.get(r'http://www.jianshu.com/p/{id}'.format(id=aid))
    html_content = BeautifulSoup(html.content)

    title = html_content.find('h1', {'class': 'title'}).getText()
    content = html_content.find('div', {'class': 'show-content'}).prettify()

    return (title, content)

def get_aids():
    index = requests.get(r'http://www.jianshu.com')
    aids = re.findall('href="/p/([^"]+)#comments"', index.content)
    for i in range(5):
        if i == 0:
            continue
        daily = requests.get(r'http://www.jianshu.com/top/daily?page='+str(i))
        weekly = requests.get(r'http://www.jianshu.com/top/weekly?page='+str(i))
        monthly = requests.get(r'http://www.jianshu.com/top/monthly?page='+str(i))
        aids += re.findall('href="/p/([^"]+)#comments"', daily.content)
        aids += re.findall('href="/p/([^"]+)#comments"', weekly.content)
        aids += re.findall('href="/p/([^"]+)#comments"', monthly.content)
        time.sleep(5)

    print(aids)
    return aids

def store():
    ''''''
    aids = get_aids()
    fp = open("jianshu.history", "a+")
    tmp = [ x.strip() for x in fp.readlines() ]
    fp.close()
    for aid in aids:
        if aid not in tmp:
            title, content = get_title_and_content(aid)
            write_article_unknown_category_and_author(title, content)
            tmp.append(aid)
        else:
            print aid + "已存在"
    # keep aids
    with open("jianshu.history", "w+") as Jfp:
        for aid in tmp:
            Jfp.write(aid + '\n')

if __name__ == '__main__':
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OLP.settings")
    setup_environ(settings)
    store()

