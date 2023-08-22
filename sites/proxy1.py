# name: 采集站点1
# author: Ethan.Wang
# desc: https://ip.ihuan.me/
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import export


class Proxy1:
    def __init__(self, rdb):
        self.name = "proxy1"
        self.url_cookie = "https://ip.ihuan.me/ti.html"
        self.url_key = "https://ip.ihuan.me/mouse.do"
        self.url_ip = "https://ip.ihuan.me/tqdl.html"
        self.db = rdb
        self.ua = UserAgent().random
        self.cookie_statistics = ""
        self.key = ""
        self.getCookie()
        self.getKey()

    def getCookie(self):
        headers = {
            "Referer": "https://ip.ihuan.me/",
            "User-Agent": self.ua,
        }
        result = requests.get(url=self.url_cookie, headers=headers)
        cookie = result.cookies.get("statistics")
        self.cookie_statistics = cookie

    def getKey(self):
        headers = {
            "Cookie": f"statistics={self.cookie_statistics}",
            "Referer": "https://ip.ihuan.me/ti.html",
            "User-Agent": self.ua,
        }
        result = requests.get(url=self.url_key, headers=headers)
        # 提取key
        pattern = r'.val\("(.+)"\);'
        matches = re.findall(pattern, result.text)
        if matches[0]:
            self.key = matches[0]

    def getIP(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"statistics={self.cookie_statistics}",
            "Origin": "https://ip.ihuan.me",
            "Referer": "https://ip.ihuan.me/ti.html",
            "User-Agent": self.ua,
        }
        data = {
            "num": 3000,
            "port": "",
            "kill_port": "",
            "address": "",
            "kill_address": "",
            "anonymity": "",
            "type": "",
            "post": "",
            "sort": "",
            "key": self.key,
        }
        result = requests.post(url=self.url_ip, headers=headers, data=data)
        # with open('t.html', 'w', encoding='utf-8') as file:
        #     file.write(result.text)
        # 提取ip
        soup = BeautifulSoup(result.text, 'html.parser')
        try:
            ip_list = [item.strip() for item in soup.find('div', class_='panel-body').stripped_strings]
        except AttributeError:
            ip_list = []

        return ip_list

    def run(self):
        # 校验时间 2h
        t = self.db.get_proxy_get_time()
        t2 = t.get(self.name)
        if t2 is not None:
            tItemObj = datetime.strptime(
                datetime.fromtimestamp(t[self.name]).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'
            ) + timedelta(hours=2)
            if datetime.now() <= tItemObj:
                return

        print("采集代理IP任务 %s, 正在运行..." % self.name)
        # 写入数据
        i = self.getIP()
        for v in i:
            # 处理异常数据
            match = re.match(r'^0{1,2}\d\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$', v)
            if match:
                result = re.sub(r'\b0+(\d)', r'\1', v)
                self.db.set_proxy_list(result, {
                    "ip": result,
                    "category": "",
                    "score": export.RedisDefaultValue,
                })
            else:
                self.db.set_proxy_list(v, {
                    "ip": v,
                    "category": "",
                    "score": export.RedisDefaultValue,
                })
        # 写入时间
        t[self.name] = int(datetime.now().timestamp())
        self.db.set_proxy_get_time(t)
        print("采集代理IP任务 %s 已运行完成" % self.name)
