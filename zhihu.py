# -*- coding: utf-8 -*-
import re
import requests
import cookielib
from PIL import Image
import time
import json


class Zhihu(object):
    login_url = 'https://www.zhihu.com/login/email'
    index_url = 'https://www.zhihu.com'
    profile_url = 'https://www.zhihu.com/settings/profile'
    captcha_url = 'http://www.zhihu.com/captcha.gif?r='

    def __init__(self):
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        self.__filename = 'zhihucookie'
        self.__session = requests.Session()
        self.__session.cookies = cookielib.LWPCookieJar(self.__filename)
        self.__session.verify = False
        try:
            self.__session.cookies.load(
                filename=self.__filename, ignore_discard=True)
        except IOError, e:
            print e
            print '无法加载cookie'

    def __getxsrf(self):
        response = self.__session.get(self.index_url, headers=self.__headers)
        html = response.text
        pat = re.compile(r'<input type="hidden" name="_xsrf" value="(.*?)"')
        xsrf = re.findall(pat, html)[0]
        return xsrf

    def __getCaptcha(self):
        t = str(int(time.time() * 1000))
        captcha_url = self.captcha_url + t + "&type=login"
        response = self.__session.get(captcha_url, headers=self.__headers)
        with open('cptcha.gif', 'wb') as f:
            f.write(response.content)
        im = Image.open('cptcha.gif')
        im.show()
        captcha = raw_input('本次登录需要输入验证码： ')
        return captcha

    def login(self, username, password):
        if self.islogin():
            print '已经登录了，不需要再登录了！！！'
            return

        # 检测到11位数字则是手机登录
        if re.match(r'\d{11}$', username):
            print('使用手机登录中...')
            self.login_url = 'http://www.zhihu.com/login/phone_num'
            data = {'_xsrf': self.__getxsrf(),
                    'password': password,
                    'remember_me': 'true',
                    'phone_num': username
                    }
        else:
            print('使用邮箱登录中...')
            self.login_url = 'https://www.zhihu.com/login/email'
            data = {'_xsrf': self.__getxsrf(),
                    'password': password,
                    'remember_me': 'true',
                    'email': username
                    }
        # 若不用验证码，直接登录
        try:
            data['captcha'] = self.__getCaptcha()
            result = self.__session.post(
                self.login_url, data=data, headers=self.__headers)
            print((json.loads(result.text))['msg'])
        except Exception, e:
            print e
            print '登录出错'
        # 保存cookie到本地
        self.__session.cookies.save(ignore_discard=True, ignore_expires=True)

    def islogin(self):
        code = self.__session.get(
            self.profile_url, headers=self.__headers, allow_redirects=False).status_code
        if code == 200:
            return True
        return False


username = '1477765176@qq.com'
password = '**********'
zh = Zhihu()
zh.login(username, password)
print zh.islogin()
