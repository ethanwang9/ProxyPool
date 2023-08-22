package proxy

import (
	"ProxyPool-MITM/global"
	"io"
	"log"
	"net/http"
)

// GetProxyUrl 获取代理服务器
func GetProxyUrl(scheme string) string {
	u := global.GetProxyAPI + scheme
	resp, err := http.Get(u)
	if err != nil {
		log.Println("获取随机代理服务器失败, Error: " + err.Error())
		return "0.0.0.0"
	}
	defer func(Body io.ReadCloser) {
		_ = Body.Close()
	}(resp.Body)

	p, _ := io.ReadAll(resp.Body)

	return "http://" + string(p)
}
