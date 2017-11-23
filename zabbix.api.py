#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-11-23 16:53:43
# @Last Modified by:   anchen
# @Last Modified time: 2017-11-23 17:09:02
import json
import requests

url = 'http://47.52.92.208/zabbix/api_jsonrpc.php'
headers = {"Content-Type":"application/json"}
data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "Admin",
        "password": "baidu.com123",
        "userData": "true"
    },
    "id":1
}
data = json.dumps(data)
r = requests.post(url, headers=headers, data=data)
print(r.text)