#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

def transform_ip_to_address(ip):
    search_url = r'http://ip.taobao.com/service/getIpInfo.php?ip={ip_addr}'.format(ip_addr=ip)
    address = u'未知'
    jd = requests.get(search_url).json()['data']
    if jd:
        address = jd['country']+jd['city']

    return address
