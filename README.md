# ProxyPool

This project primarily uses web crawling and tunnel proxy technology to automatically collect public proxy tunnels published on the network and uses multi-threading technology to verify their availability in real-time, implementing an **automated web crawler proxy pool** function.

Users can dynamically forward request content by connecting to tunnel proxies, where each request within the tunnel is forwarded through a random IP. Through tunnel proxy technology, intelligent traffic distribution, automatic switching, and automatic optimization are achieved. In simple terms, **each proxy request will automatically switch to a new proxy**.

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

More language document: [English](README.md)、[中文文档](README_ZH.md)

More history version: v1.0.0 [Github link](https://github.com/ethanwang9/ProxyPool/releases/tag/1.0.0) [Gitee link](https://gitee.com/EthanWang9/ProxyPool/tree/1.0.0)

## Deployment

TODO

## Usage

TODO

## Changelog
- v1.1.0
  - Features
    - TODO...
  - Update time: 2025-07-08
- v 1.0.0
  - Features
    - HTTP transparent proxy server, automatically forwards proxy request content, adaptive HTTP/HTTPS proxy types
    - Uses man-in-the-middle proxy to dynamically forward messages
    - Automatic proxy address collection
    - Automatic proxy address maintenance
    - Provides HTTP interface service that randomly returns HTTP/HTTPS proxy addresses
  - Update time: 2023-08-24