import requests
import time
import random
import re
import os
from lxml import etree
from urllib.parse import urlencode


def fail_request_href(url):
    global fail_requestl_hrefl
    fail_request_hrefl.append(url)
    return fail_request_hrefl

'''设置ua'''
def UA():
    try:
        # print('UA()......')
        user_agent = ['Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
              'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
              ]
        return random.choice(user_agent)
    except:
        return UA()
def PROXY():
    try:
        # print('PROXY......')
        f = open('proxies.txt','r')
        ips = f.readlines()
        proxiesl = []
        for i in ips:
            ip = i.strip('\n').split('\t')[0]
            host = i.strip('\n').split('\t')[1]
            proxy = 'http:\\' + ip + ':' + host
            proxies = {'proxy':proxy}
            proxiesl.append(proxies)
        return random.choice(proxiesl)
    except:
        return PROXY()
def URL():
    # print('URL()......')
    try:
        urll = []
        MAX_PAGE = 5
        for i in range(1,MAX_PAGE+1):
            url = 'http://tu.jiachong.net/meinvtupian/list_43_%s.html' %str(i)
            urll.append(url)
        return urll
    except:
        return URL(MAX_PAGE)
def get_first_html(url,ua,proxy):
    try:
        # print('get_first_html()........')
        headers = {'User-Agent':ua}
        proxy = proxy
        url = url
        # print('Begining request......')
        r = requests.get(url,headers=headers,proxies=proxy,timeout=2)
        r.encoding = 'utf-8'
        if r.status_code == 200:
            # print('request successful 1')
            return r.text
    except:
        fail_request_href(url)
        # print('failed 1')


def get_first_href(html):
    # print('get_first_href()......')
    try:
        href = re.findall('href="(http://tu\.jiachong\.net/meinvtupian/.*?html)"\stitle="(.*?)"',html)
        href = list(set(href))
        i = 0
        # print('get successful 2')
        for url, title in href:
            # print(url,title)
            i += 1
            # print(i)
            path = title
            if not os.path.exists(path):
                os.mkdir(path)
            else:
                print('文件夹已存在')
        return href
    except:
        print('failed 2')
def get_each_href_text(href,ua,proxy):
    # print('get_each_href_text()......')
    try:
        headers = {
            'User-Agent':ua
            }
        proxy = proxy
        # print(href)
        for i in range(1,10):
            if i == 1:
                url = href[0]
            else:
                url = href[0].split('.')
                url = url[0]+ '.'+ url[1]+'.' + url[2] + '_' + str(i) + '.html'
            print(url)
            r = requests.get(url,headers=headers,proxies=proxy,timeout=1)
            r.encoding = 'utf-8'
            if r.status_code == 200:
                # print('successful 3')
                img = re.findall('http://t3.jiachong.net/uploads/tu/.*?jpg',r.text)
                # print(img)
                title = re.findall('<h1>(.*?)</h1>',r.text)
                # print(title[0])
                # print('successful 4')
                if img:
                    url = img[0]
                    # print('successful 4.5')
                    r = requests.get(url)
                    if r.status_code == 200:
                        img_path = '{0}/{1}.{2}'.format(href[1],title[0],'jpg')
                        print(img_path)
                        if not os.path.exists(img_path):
                            with open (img_path, 'wb') as f:
                                f.write(r.content)
                                global s
                                s += 1
                                print('successful 5')
                        else:
                            print('already download')
                    else:
                        print('failed 5')
    except:
        print('failed 3')

def main(url):
    ua = UA()
    proxy = PROXY()
    # print('Getting information from    ', url)
    html = get_first_html(url,ua,proxy)
    hrefs = get_first_href(html)
    if hrefs:
        for href in hrefs:
            get_each_href_text(href,ua,proxy)
if __name__ == '__main__':
    s = 0
    fail_request_hrefl = []
    start = time.time()
    urll = URL()
    for i in range(len(urll)):
        main(urll[i])
    fail_request_href = fail_request_href(urll[0])
    print(fail_request_href)
    print('成功获得',s,'张')#统计成功下载的照片数
    end = time.time()
    print('Total sharing time:' ,end - start)
