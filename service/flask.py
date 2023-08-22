# name: API接口任务
# author: Ethan.Wang
import random

from flask import Flask, request
from flask_apscheduler import APScheduler
from gevent import pywsgi

import sites
from proxy.check import Check


class FlaskService:
    def __init__(self, rdb, port=23457, host="0.0.0.0"):
        # 数据库服务
        self.db = rdb

        # API服务
        self.app = Flask(__name__)
        self.port = port
        self.host = host

        # CRON服务
        self.app.config['SCHEDULER_API_ENABLED'] = True
        self.app.config['SCHEDULER_MISFIRE_GRACE_TIME'] = 120
        self.cron = APScheduler()
        self.cron.init_app(self.app)

    def service_cron(self):
        @self.cron.task('cron', minute='*/5')
        def do_check():
            print("定时任务-校验代理运行中...")
            Check(self.db).run()
            print("定时任务-校验代理已完成")

        @self.cron.task('cron', hour='*/1')
        def do_get():
            print("定时任务-获取代理中...")
            sites.run(self.db)
            print("定时任务-获取代理已完成")

    def service_api(self):
        @self.app.route("/get")
        def getRandomProxyServer():
            t = request.args.get("t")
            arr = self.db.getT_proxy_success(t)
            n = random.randint(0, len(arr) - 1)
            return arr[n]

    def run(self):
        # 定时任务
        self.service_cron()
        self.cron.start()
        # HTTP接口服务
        self.service_api()
        server = pywsgi.WSGIServer((self.host, self.port), self.app)
        server.serve_forever()
