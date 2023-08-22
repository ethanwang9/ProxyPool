package proxy

import (
	"github.com/elazarl/goproxy"
	"log"
	"net/http"
	"net/url"
	"time"
)

// Mitm 中间人代理转发服务
func Mitm() *goproxy.ProxyHttpServer {
	proxy := goproxy.NewProxyHttpServer()
	proxy.CertStore = NewCertStorage()
	proxy.Verbose = false
	proxy.OnRequest().HandleConnect(goproxy.AlwaysMitm)
	proxy.OnRequest().DoFunc(func(req *http.Request, ctx *goproxy.ProxyCtx) (*http.Request, *http.Response) {
		reqCount := 0
		var resp *http.Response
		for {
			if reqCount >= 10 {
				break
			}
			resp = forward(req, GetProxyUrl(req.URL.Scheme))
			if resp.StatusCode == http.StatusOK {
				break
			}
			reqCount++
		}
		return nil, resp
	})
	return proxy
}

// HTTP请求转发服务
func forward(r *http.Request, proxyURL string) *http.Response {
	proxyURLParsed, _ := url.Parse(proxyURL)

	// 创建请求
	proxyReq := &http.Request{
		Method: r.Method,
		URL:    r.URL,
		Header: make(http.Header),
	}

	// 重写 header
	for k, v := range r.Header {
		proxyReq.Header.Set(k, v[0])
	}

	// 设置代理服务器
	client := &http.Client{
		Transport: &http.Transport{
			Proxy: func(_ *http.Request) (*url.URL, error) {
				return proxyURLParsed, nil
			},
		},
		Timeout: time.Second * 10,
	}

	// 返回数据
	resp, err := client.Do(proxyReq)
	if err != nil {
		return goproxy.NewResponse(r, goproxy.ContentTypeHtml, http.StatusBadGateway, "")
	} else {
		log.Printf("代理请求成功, Host: %s %s ProxyServer: %s\n", r.Method, r.URL, proxyURL)
		return resp
	}
}
