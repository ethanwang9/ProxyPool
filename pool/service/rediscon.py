# name: 连接 redis 服务
# author: Ethan.Wang
import json
from datetime import datetime

import redis

import export


class RedisCon:
    def __init__(self, pwd, host="127.0.0.1", port=6379, db=0):
        self.DB = redis.Redis(host=host, port=port, db=db, password=pwd)
        self.Proxy_Success = "proxy_success"
        self.Proxy_List = "proxy_list"
        self.Proxy_Get_Time = "proxy_get_time"
        self.Proxy_Check_Time = "proxy_check_time"

    # ==========
    # proxy_list
    # ==========

    # 设置 proxy_list
    def set_proxy_list(self, ip, value):
        self.DB.hset(self.Proxy_List, ip, json.dumps(value))

    # 获取全部
    def getAll_proxy_list(self):
        d = self.DB.hgetall(self.Proxy_List)
        l = []
        for k, v in d.items():
            itemValue = json.loads(v)
            if itemValue.get('score', 0) > export.RedisErrorValue:
                l.append(itemValue)
        return l

    # 删除 proxy_list
    def del_proxy_list(self, ip):
        self.DB.hdel(self.Proxy_List, ip)

    # 清楚冗余数据
    def clean_proxy_list(self):
        d = self.DB.hgetall(self.Proxy_List)
        l = []
        for k, v in d.items():
            itemValue = json.loads(v)
            if itemValue.get('score', 0) == export.RedisErrorValue:
                l.append(k.decode())
        for v in l:
            self.del_proxy_list(v)

    # ==========
    # proxy_success
    # ==========

    # 设置 proxy_success
    def set_proxy_success(self, ip, value):
        self.DB.hset(self.Proxy_Success, ip, json.dumps(value))

    # 获取全部 proxy_success
    def getAll_proxy_success(self):
        d = self.DB.hgetall(self.Proxy_Success)
        l = []
        for k, v in d.items():
            l.append(k.decode())
        return l

    # 清空 proxy_success
    def drop_proxy_success(self):
        d = self.getAll_proxy_success()
        for v in d:
            self.DB.hdel(self.Proxy_Success, v)

    # 获取t类型的 proxy_success
    def getT_proxy_success(self, t):
        d = self.DB.hgetall(self.Proxy_Success)
        l = []
        for k, v in d.items():
            j = json.loads(v)
            if j.get('category', 'http') == t:
                l.append(k.decode())
        return l

    # ==========
    # proxy_get_time
    # ==========
    # 设置 proxy_get_time
    def set_proxy_get_time(self, data):
        self.DB.set(self.Proxy_Get_Time, json.dumps(data))

    # 获取 proxy_get_time
    def get_proxy_get_time(self):
        d = self.DB.get(self.Proxy_Get_Time)
        if d is not None:
            result = json.loads(d)
            return result
        else:
            return {}

    # ==========
    # proxy_check_time
    # ==========
    # 设置 proxy_check_time
    def set_proxy_check_time(self):
        self.DB.set(self.Proxy_Check_Time, int(datetime.now().timestamp()))

    # 获取 proxy_check_time
    def get_proxy_check_time(self):
        t = self.DB.get(self.Proxy_Check_Time)
        if t is None or t == "":
            return ""
        else:
            return t.decode('utf-8')
