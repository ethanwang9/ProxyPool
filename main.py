# name: 程序入口
# author: Ethan.Wang
from datetime import datetime, timedelta

import export
import sites
from proxy.check import Check
from service.flask import FlaskService
from service.rediscon import RedisCon


def show():
    logo = '''
 ____                      ____             _ 
|  _ \ _ __ _____  ___   _|  _ \ ___   ___ | |
| |_) | '__/ _ \ \/ / | | | |_) / _ \ / _ \| |
|  __/| | | (_) >  <| |_| |  __/ (_) | (_) | |
|_|   |_|  \___/_/\_\\__, |_|   \___/ \___/|_|
                     |___/
'''
    print(logo)
    print("【 ProxyPool-Pool 代理爬虫池 】")
    print("Author: %s\t Version: %s\t Github: %s" % (export.APPAuthor, export.APPVersion, export.AppUrl))
    print(">>>>>>>>>>>>>>>")


def initRedis(rdb):
    is_break = False

    # 1. 校验数据库是否有内容
    # 1.1 获取代理池
    getTime = rdb.get_proxy_get_time()
    if getTime == {}:
        print("初始化数据库-获取代理中...")
        sites.run(rdb)
        print("初始化数据库-获取代理已完成")
        is_break = True
    # 1.2 校验代理
    checkTime = rdb.get_proxy_check_time()
    if len(checkTime) == 0 or checkTime == "":
        print("初始化数据库-校验代理运行中...")
        Check(rdb).run()
        print("初始化数据库-校验代理已完成")
        is_break = True

    if is_break:
        print("初始化数据库校验已完成")
        return

    # 2. 校验数据库时间
    # 2.1 获取代理池
    getTime = rdb.get_proxy_get_time()
    getTimeObj = datetime.strptime(
        datetime.fromtimestamp(getTime['time']).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'
    ) + timedelta(hours=1)
    if datetime.now() > getTimeObj:
        print("初始化数据库-更新代理中...")
        sites.run(rdb)
        print("初始化数据库-更新代理已完成")
    # 2.2 校验代理
    checkTime = rdb.get_proxy_check_time()
    checkTimeObj = datetime.strptime(
        datetime.fromtimestamp(int(checkTime)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'
    ) + timedelta(minutes=5)
    if datetime.now() > checkTimeObj:
        print("初始化数据库-校验代理运行中...")
        Check(rdb).run()
        print("初始化数据库-校验代理已完成")

    print("初始化数据库校验已完成")


if __name__ == '__main__':
    # 显示程序LOGO
    show()

    # 初始化 redis
    rdb = RedisCon()

    # 初始化数据库内容
    initRedis(rdb)

    # API接口
    print("ProxyPool-Pool 运行端口号: %d" % export.ServerPort)
    FlaskService(rdb, port=export.ServerPort).run()
