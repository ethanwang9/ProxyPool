# Redis 数据库
- Cache 【type】 数据缓存区域，爬虫获取的数据将会存储在该区域
- Proxy 【type】 数据优选区域，经过系统规则验证和评分后的优质数据

# 代理数据评分规则
- 默认评分：5，满分评分：10，优质代理：评分>=8，一般代理：评分7-5，评分<5则不予使用，评分<1删除
- 校验成功：+1，校验失败：-2

# 代理校验规则
1. 使用 test.ipw.cn 获取代理 IP 地址，该请求返回 IPV4/IPV6 字符串。
2. 代理 IP 地址不能为本机 IP 地址，使用 4.ipw.cn 获取本机 IPV4，使用 6.ipw.cn 获取本机 IPV6。
3. 代理 IP 地址是一个合法的 IPV4/IPV6，不区分公网/私网
4. 请求需在15秒内完成，超时无效

# 爬虫数据入库规则
1. 代理数据去重
2. 多线程批量校验代理数据有效性
3. 校验成功则写入 Redis 数据库 Cache 键，并写入默认评分信息

# 定时任务：校验代理/15Minute
1. 校验