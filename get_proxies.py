import requests
import os
from bs4 import BeautifulSoup

url = 'http://www.xicidaili.com/nn/1'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
s = requests.get(url,headers=headers)
soup = BeautifulSoup(s.text,'lxml')
ips = soup.select('#ip_list tr')
with open('proxies.txt','w') as f:
    for i in ips:
        try:
            ipp = i.select('td')
            ip = ipp[1].text
            host = ipp[2].text
            f.write(ip)
            f.write('\t')
            f.write(host)
            f.write('\n')
            print(ip,host)
        except:
            print('Acquisition failed')