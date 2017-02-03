# -*- coding: utf-8 -*-
import re
import requests
import cookielib
from PIL import Image
import time
import json

login_url = 'http://xk.autoisp.shu.edu.cn/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'}

session = requests.Session()


def getcaptch():
    url = 'http://xk.autoisp.shu.edu.cn/Login/GetValidateCode?' + \
        str(int(time.time() * 1000)) + '1486121679147'
    response = session.get(url, headers=headers)
    with open('shup.gif', 'wb') as f:
        f.write(response.content)
        f.close()
    try:
        img = Image.open('shup.gif')
        img.show()
        img.close()
    except Exception, e:
        print e
    p = raw_input('plese input captch')
    return p


def login(username, password):
    data = {
        'txtUserName': username,
        'txtPassword': password,
        'txtValiCode': getcaptch()
    }
    try:
    	resp=session.post(login_url,data=data,headers=headers)
    	print resp.text
    except:
    	print 'xxxxx'




