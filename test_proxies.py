import requests
import os
from bs4 import BeautifulSoup
url = 'https://www.baidu.com'
f = open('proxies.txt','r')
ips = f.readlines()
proxys = list()
for i in ips:
    ip = i.strip('\n').split('\t')
    proxy = 'http:\\' + ip[0] + ':' + ip[1]
    proxies = {'proxy':proxy}
    proxys.append(proxies)
# print(proxys)
for pro in proxys:
    print(pro)
    try:
        r = requests.get(url, proxies=pro)
        print(r)
    except:
        print('Request failed!')

