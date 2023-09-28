from datetime import datetime

from .proxy1 import Proxy1
from .proxy2 import Proxy2
from .proxy3 import Proxy3


def run(rdb):
    # 运行定时任务
    Proxy1(rdb).run()
    Proxy2(rdb).run()
    Proxy3(rdb).run()

    # 记录获取代理池时间
    t = rdb.get_proxy_get_time()
    t['time'] = int(datetime.now().timestamp())
    rdb.set_proxy_get_time(t)
