# ProxyPool

项目主要通过爬虫和隧道代理技术，自动采集网络中发布的公共代理隧道并使用多线程技术实时校验可用性，实现了 **自动化爬虫代理池** 功能。 

用户通过连接隧道代理动态转发请求内容，在隧道内每一个请求通过一个随机 IP 进行转发。 通过隧道代理技术，实现流量智能分流、自动切换、自动优选, 简言之 **每次代理请求都会自动切换新代理**。

![Version](https://img.shields.io/badge/Version-1.1.0-blue)
![GitHub](https://img.shields.io/github/license/ethanwang9/ProxyPool)
![Update Time](https://img.shields.io/badge/UpdateTime-2025/07/08-green)


```text
 ____                      ____             _ 
|  _ \ _ __ _____  ___   _|  _ \ ___   ___ | |
| |_) | '__/ _ \ \/ / | | | |_) / _ \ / _ \| |
|  __/| | | (_) >  <| |_| |  __/ (_) | (_) | |
|_|   |_|  \___/_/\_\__, |_|   \___/ \___/|_|
                     |___/
```

更多语言文档: [English](README.md)、[中文文档](README_ZH.md)

## 部署

部署方式待更新

## 使用

使用方式待更新

## 更新日志
- v1.1.0
  - 特征
    - TODO...
  - 更新时间：2025-07-08
- v 1.0.0
  - 特性
    - HTTP 透明代理服务端, 自动代理转发请求内容, 自适应 HTTP/HTTPS 类型代理
    - 使用中间人代理动态转发消息
    - 自动采集代理地址
    - 自动维护代理地址
    - 提供随机返回 HTTP/HTTPS 类型代理地址 HTTP 接口服务
  - 更新时间: 2023-08-24