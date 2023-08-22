package show

import (
	"ProxyPool-MITM/global"
	"fmt"
)

func Logo() {
	asciiArt := `
 ____                      ____             _ 
|  _ \ _ __ _____  ___   _|  _ \ ___   ___ | |
| |_) | '__/ _ \ \/ / | | | |_) / _ \ / _ \| |
|  __/| | | (_) >  <| |_| |  __/ (_) | (_) | |
|_|   |_|  \___/_/\_\\__, |_|   \___/ \___/|_|
                     |___/                     

`
	fmt.Print(asciiArt)
	fmt.Println("【 ProxyPool-MITM 中间人代理转发服务端 】")
	fmt.Printf("Author: %s\t Version: %s\t Github: %s\n", global.APPAuthor, global.APPVersion, global.AppUrl)
	fmt.Println(">>>>>>>>>>>>>>>")
}
