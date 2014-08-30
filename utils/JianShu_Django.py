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

from shortcuts import write_article_unknown_category_and_author

def get_title_and_content(aid):
    html = requests.get(r'http://jianshu.io/p/{id}'.format(id=aid))
    html_content = BeautifulSoup(html.content)

    title = html_content.find('h1', {'class': 'title'}).getText()
    content = html_content.find('div', {'class': 'show-content'}).prettify()
    print title

    return (title, content)

def get_aids():
    html = requests.get(r'http://jianshu.io/top/weekly')
    aids = re.findall('href="/p/([^"]+)#comments"', html.content)

    return aids

def store():
    ''''''
    aids = get_aids()
    for aid in aids:
        title, content = get_title_and_content(aid)
        write_article_unknown_category_and_author(title, content)
