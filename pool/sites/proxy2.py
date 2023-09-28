# name: 采集站点2
# author: Ethan.Wang
# desc: https://zj.v.api.aa1.cn/api/proxyip/
import re
from datetime import datetime, timedelta

import requests
from fake_useragent import UserAgent

import export


class Proxy2:
    def __init__(self, rdb):
        self.name = "proxy2"
        self.url = "https://zj.v.api.aa1.cn/api/proxyip/"
        self.ua = UserAgent().random
        self.db = rdb

    def get(self):
        try:
            result = requests.get(url=self.url, headers={"User-Agent": self.ua})
            if result.status_code == 200:
                content = result.content.decode("utf8")
                # with open('t.html', 'r', encoding="utf8") as file:
                # file.write(content)
                # content = file.read()
                listData = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', content)
                return listData
            else:
                print("采集代理IP任务 %s, 采集站点失效" % self.name)
                return []
        except requests.exceptions.RequestException as e:
            print("采集代理IP任务 %s, 获取采集页面信息失败. Error: %s" % (self.name, str(e)))
            return []

    def run(self):
        # 校验时间 4h
        t = self.db.get_proxy_get_time()
        t2 = t.get(self.name)
        if t2 is not None:
            tItemObj = datetime.strptime(
                datetime.fromtimestamp(t[self.name]).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'
            ) + timedelta(hours=4)
            if datetime.now() <= tItemObj:
                return

        print("采集代理IP任务 %s, 正在运行..." % self.name)
        # 写入数据
        l = self.get()
        if len(l) == 0:
            print("采集代理IP任务 %s, 未采集到数据" % self.name)
        else:
            print("采集代理IP任务 %s, 写入数据中..." % self.name)
            for v in l:
                self.db.set_proxy_list(v, {
                    "ip": v,
                    "category": "",
                    "score": export.RedisDefaultValue,
                })
        # 写入时间
        t[self.name] = int(datetime.now().timestamp())
        self.db.set_proxy_get_time(t)
        print("采集代理IP任务 %s 已运行完成" % self.name)
