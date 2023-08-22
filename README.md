# ProxyPool

项目主要实现 **自动化爬虫代理池** , 通过定时采集网络中发布的免费代理并验证其可用性.
通过 `MITM(中间人攻击)` 实现HTTP透明代理, 客户端每次请求HTTP代理, 服务端随机转发到代理池中并返回数据给客户端, 简言之**每次代理请求都是一个新的代理地址**.

![Static Badge](https://img.shields.io/badge/version-1.0.0-blue)
![GitHub](https://img.shields.io/github/license/ethanwang9/ProxyPool)


```text
 ____                      ____             _ 
|  _ \ _ __ _____  ___   _|  _ \ ___   ___ | |
| |_) | '__/ _ \ \/ / | | | |_) / _ \ / _ \| |
|  __/| | | (_) >  <| |_| |  __/ (_) | (_) | |
|_|   |_|  \___/_/\_\__, |_|   \___/ \___/|_|
                     |___/
```

## 部署

推荐使用容器例如: `Docker-Compose` 或者 `Docker` 运行此服务, 如需二进制运行文件请自行编译打包使用

国内源加速下载项目
```bash
git clone https://gitclone.com/github.com/ethanwang9/covid19.git
```

启动服务
```bash
# 使用docker-compose 后台启动
docker-compose -f deploy/docker-compose.yaml up -d
# 服务都启动成功后,使用此命令行可清除none镜像
docker system prune
```

## 使用

**HTTP透明代理:** `0.0.0.0:23456`

**代理池随机获取一个代理地址:** `0.0.0.0:23457/get?t=[ http | https ]`

## 代理站点

| 站点       | 状态 | 代码     |
|----------|----|--------|
| 小幻HTTP代理 | ✔  | proxy1 |
| 夏柔HTTP代理 | ✔  | proxy2 |

## 工作原理

`ProxyPool`使用 Python 和 Golang 开发, 使用 Redis 作为项目数据库.

Python 负责自动采集代理地址、维护代理地址有效性、提供 HTTP 代理地址相关服务

Golang 负责 HTTP 透明代理和代理转发服务

工作流程: 
1. 客户端请求 Golang 提供的 HTTP 透明代理服务 
2. 服务端收到代理请求后通过中间人攻击拦截请求, 拦截数据后转发到代理服务
3. 代理服务从 Python HTTP 服务获取一个代理地址, 代理请求客户端发送的 HTTP/HTTPS 信息. 由于网络中抓取的代理地址具有不确定性和不稳定性, 所以代理请求失败后将重试 10 次
4. 代理服务将网络数据转发到客户端

## 更新日志

- v 1.0.0
  - 特性
    - HTTP 透明代理服务端, 自动代理转发请求内容, 自适应 HTTP/HTTPS 类型代理
    - 自动采集代理地址
    - 自动维护代理地址
    - 提供随机返回 HTTP/HTTPS 类型代理地址 HTTP 接口服务
  - TODO
    - [ ] HTTP 透明代理添加账号密码认证模式
    - [ ] Python 代理站点增加 3 个
  - 更新时间: 2023-08-22 15:45:09