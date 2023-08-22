package main

import (
	"ProxyPool-MITM/global"
	"ProxyPool-MITM/proxy"
	"ProxyPool-MITM/show"
	"log"
	"net/http"
)

func main() {
	// 显示程序logo
	show.Logo()

	// 运行代理服务
	log.Println("ProxyPool-MITM 运行端口号: " + global.ServerPort)
	cli := proxy.Mitm()
	err := http.ListenAndServe("127.0.0.1:"+global.ServerPort, cli)
	if err != nil {
		log.Panic("启动中间人代理转发服务失败, Error: " + err.Error())
		return
	}
}
