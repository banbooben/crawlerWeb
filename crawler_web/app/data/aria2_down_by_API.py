# -*- coding:utf-8 -*-

import requests
import json
url = 'http://192.168.2.151:6800/jsonrpc'
download_url = "https://coding.net/u/mofiter/p/public_files/git/raw/master/go_to_bottom_button.png"
json_rpc = json.dumps({
    "jsonrpc":
    "2.0",
    "method":
    "aria2.addUri",
    "id":
    "123456",
    "params": [
        "token:sarmn.cn",
        [
            "https://pic1.zhimg.com/v2-3b4fc7e3a1195a081d0259246c38debc_1200x500.jpg"
        ], {
            "out": "QQ1235.jpg",
            "dir": "/media/armn/cache/test",
            "pause": "false",
            "split": "5",
            "max-connection-per-server": "5",
            "seed-ratio": "0"
        }
    ]
})
response = requests.post(url=url, data=json_rpc)
print(response.status_code)
print(response.content.decode("utf-8"))
print(response.headers)