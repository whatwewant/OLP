#!/usr/bin/env python
# coding=utf-8
#*************************************************************************
#	> File Name: JianShu_Django.py
#	> Author: Potter
#	> Mail: tobewhatwewant@gmail.com
#	> Created Time: 2014年08月30日 星期六 10时10分24秒
# ************************************************************************/

import requests
from bs4 import BeautifulSoup
import re
import time

from shortcuts import write_article_unknown_category_and_author

def get_title_and_content(aid):
    html = requests.get(r'http://jianshu.io/p/{id}'.format(id=aid))
    html_content = BeautifulSoup(html.content)

    title = html_content.find('h1', {'class': 'title'}).getText()
    content = html_content.find('div', {'class': 'show-content'}).prettify()
    print title

    return (title, content)

def get_aids():
    index = requests.get(r'http://jianshu.io')
    aids = re.findall('href="/p/([^"]+)#comments"', index.content)
    for i in range(5):
        if i == 0:
            continue
        daily = requests.get(r'http://jianshu.io/top/daily?page='+str(i))
        weekly = requests.get(r'http://jianshu.io/top/weekly?page='+str(i))
        monthly = requests.get(r'http://jianshu.io/top/monthly?page='+str(i))
        aids += re.findall('href="/p/([^"]+)#comments"', daily.content)
        aids += re.findall('href="/p/([^"]+)#comments"', weekly.content)
        aids += re.findall('href="/p/([^"]+)#comments"', monthly.content)
        time.sleep(5)

    print aids

    return aids

def store():
    ''''''
    aids = get_aids()
    for aid in aids:
        title, content = get_title_and_content(aid)
        write_article_unknown_category_and_author(title, content)
        time.sleep(3)
