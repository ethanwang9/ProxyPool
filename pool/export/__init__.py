# name: 变量
# author: Ethan.Wang
import logging
import os

# ==========
# 全局变量
# ==========
# 软件版权信息
APPAuthor = "Ethan.Wang"
APPVersion = "1.0.0"
AppUrl = "github.com/ethanwang9/ProxyPool"

# 软件信息
# ServerPort = 23457
ServerPort = os.environ.get('RUN_PORT')
Check_Max = 1000

# redis 程序信息
RedisDefaultValue = 10
RedisSuccessValue = 20
RedisErrorValue = 0

# redis 认证信息
# RedisHost = "localhost"
# RedisPwd = "123456"
RedisHost = os.environ.get('REDIS_HOST')
RedisPort = os.environ.get('REDIS_PORT')
RedisPwd = os.environ.get('REDIS_PASSWORD')