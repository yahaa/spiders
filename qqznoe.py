# -*- coding: utf-8 -*-
import re
import requests
import cookielib
from PIL import Image
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'}
url='https://user.qzone.qq.com'
session = requests.Session()
session.verify=False
data={'user':'1477765176','password':'ASDFGHJKL159753@'}
resp=session.post(url,data=data,headers=headers)
print resp.text