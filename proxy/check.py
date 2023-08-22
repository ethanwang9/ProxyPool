# name: 多线程代理校验
# author: Ethan.Wang

import ipaddress
from concurrent.futures import ThreadPoolExecutor

import requests
import urllib3

import export


class Check:
    def __init__(self, rdb):
        self.check_url_http = "http://4.ipw.cn"
        self.check_url_https = "https://4.ipw.cn"
        self.db = rdb
        self.local_ip = ""
        urllib3.disable_warnings()
        self.getLocalIP()

    # 获取本机公网IP
    def getLocalIP(self):
        v = requests.get(url=self.check_url_https, timeout=5, verify=False)
        self.local_ip = v.text

    # 验证代理
    def checkProxy(self, proxy):
        isCheck = {
            "isOk": False,
            "isHttps": False,
        }

        # 校验https
        try:
            r_https = requests.get(url=self.check_url_https, proxies={'https': proxy}, timeout=10, verify=False)
            # print("https校验结果：", r_https.status_code, r_https.text, proxy)
            if r_https.status_code == 200 and self.check_ip(r_https.text):
                isCheck["isOk"] = True
                isCheck["isHttps"] = True
            else:
                isCheck["isOk"] = False
                isCheck["isHttps"] = False
        except requests.exceptions.RequestException:
            isCheck["isOk"] = False
            isCheck["isHttps"] = False

        if isCheck["isOk"] and isCheck["isHttps"]:
            return {"ip": proxy, "category": "https"}

        # 校验http
        try:
            r_http = requests.get(url=self.check_url_http, proxies={'http': proxy}, timeout=10, verify=False)
            # print("http校验结果：", r_http.status_code, r_http.text, proxy)
            if r_http.status_code == 200 and self.check_ip(r_http.text):
                isCheck["isOk"] = True
                isCheck["isHttps"] = False
            else:
                isCheck["isOk"] = False
                isCheck["isHttps"] = False
        except requests.exceptions.RequestException:
            isCheck["isOk"] = False
            isCheck["isHttps"] = False

        if isCheck["isOk"] and (not isCheck["isHttps"]):
            return {"ip": proxy, "category": "http"}

        # 返回数据
        return ""

    # 判断IP地址是否符合条件
    def check_ip(self, ip):
        f = True

        # 判断IP是否为公网IP
        try:
            t = ipaddress.ip_address(ip)
            f = not t.is_private
        except ValueError:
            return False

        # 判断IP是否为本机公网IP
        if f and self.local_ip == ip:
            return False
        else:
            return True

    # 多线程代理校验
    def threadCheckProxy(self, ip_list, work):
        thread_list = []
        success_list = []

        # ip 去重
        ip_list = list(set(ip_list))

        # 多线程验证代理
        pool = ThreadPoolExecutor(max_workers=work)
        for v in ip_list:
            t = pool.submit(self.checkProxy, v)
            thread_list.append(t)

        for i, v in enumerate(thread_list):
            if len(v.result()) != 0:
                success_list.append(v.result())

        pool.shutdown()

        return success_list

    # 运行代理校验任务
    def run(self):
        print("校验代理IP任务正在运行中...")

        # ==========
        # 校验 proxy_success
        # ==========
        print("校验代理IP任务, 校验 proxy_success...")

        # 获取所有 proxy_success
        s = self.db.getAll_proxy_success()

        # 运行多线程校验任务
        sc = self.threadCheckProxy(s, 500)

        # 清空 proxy_success
        self.db.drop_proxy_success()

        # 设置成功的IP
        for v in sc:
            self.db.set_proxy_success(v.get("ip"), {
                "ip": v.get("ip"),
                "category": v.get("category"),
            })

        print("校验代理IP任务, 校验 proxy_success 已完成")

        # ==========
        # 校验 proxy_list
        # ==========
        print("校验代理IP任务, 校验 proxy_list...")

        # 获取所有 redis proxy_list 数据
        d = self.db.getAll_proxy_list()
        dl = []
        for v in d:
            dl.append(v.get("ip"))

        # 运行多线程校验任务
        c = self.threadCheckProxy(dl, 1000)

        # 设置成功的IP, 并添加到 proxy_success
        for v in c:
            self.db.set_proxy_list(v.get("ip"), {
                "ip": v.get("ip"),
                "category": v.get("category"),
                "score": export.RedisSuccessValue,
            })
            self.db.set_proxy_success(v.get("ip"), {
                "ip": v.get("ip"),
                "category": v.get("category"),
            })

        # 设置失败的IP score-1
        for v in d:
            flag = True
            for v2 in c:
                if v.get("ip") == v2.get("ip"):
                    flag = False
            if flag:
                self.db.set_proxy_list(v.get("ip"), {
                    "ip": v.get("ip"),
                    "category": v.get("category"),
                    "score": v.get("score") - 1,
                })

        print("校验代理IP任务, 校验 proxy_list 已完成")

        # ==========
        # 删除 proxy_list 0
        # ==========
        self.db.clean_proxy_list()
        print("校验代理IP任务, 已清楚冗余数据")

        self.db.set_proxy_check_time()
        print("校验代理IP任务已完成")
