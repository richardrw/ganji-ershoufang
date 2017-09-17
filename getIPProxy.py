#coding=utf-8

import requests
import json
import random

def getIPProxyFrom(url='http://127.0.0.1:8000'):
    proxyList = json.loads(requests.get(url).content)
    choiceProxy = random.choice(proxyList)
    ip = choiceProxy[0]
    port = choiceProxy[1]
    proxy = {'http':'{}:{}'.format(ip, port)}
    return proxy

if __name__ == '__main__':
    while True:
        proxy = getIPProxyFrom()
        print(proxy)
