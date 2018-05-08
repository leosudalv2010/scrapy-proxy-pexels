# encoding=utf-8

import requests
from lxml import etree
import time
from pexels.proxy.proxy_https_verify import VerifyProxy
import sys


class GetProxy(object):
    def __init__(self, request_url, user_agent):
        self.request_url = request_url
        self.headers = {
            'User-Agent': user_agent
        }
        with open('proxy_https_verified.txt', 'r') as f:
            self.old_proxy_list = f.readlines()
        print('old_proxy_list:')
        print(self.old_proxy_list)
        self.scrap_proxy_list = []
        self.useful_proxy_list = []

    def scrap_proxy(self, url_list):
        for url in url_list:
            html = requests.get(url, headers=self.headers)
            time.sleep(1.5)
            selector = etree.HTML(html.text)
            items = selector.xpath('//table[@id="ip_list"]//tr')
            for item in items[1:]:
                if not item.xpath('td[6]/text()')[0] == 'HTTPS':
                    continue
                ip = item.xpath('td[2]/text()')[0]
                port = item.xpath('td[3]/text()')[0]
                ip_with_port = ip + ':' + port
                self.scrap_proxy_list.append(ip_with_port)

    def test_proxy(self, proxy_list):
        proxy_count = error_count = 0
        for proxy in proxy_list:
            proxy = proxy.strip()
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
            }
            status_code = 200
            for i in range(2):
                if status_code != 200:
                    break
                try:
                    response = requests.get(self.request_url, headers=self.headers, proxies=proxies, timeout=5)
                    status_code = response.status_code
                except:
                    status_code = 0
                    error_count += 1
                    print('ConnectionError at {0}th request:({1}), total:{2}, sum:{3}'.format(i+1, proxy, error_count, len(proxy_list)))
            if status_code == 200:
                proxy_count += 1
                print('got an useful proxy ({0}), total:{1}'.format(proxy, proxy_count))
                self.useful_proxy_list.append(proxy)


if __name__ == '__main__':
    # instantiate an object of the class
    request_url = 'https://www.pexels.com/'
    user_agent = 'Mozilla/5.0'
    getproxy = GetProxy(request_url=request_url, user_agent=user_agent)

    # scrap proxies from the websites
    page = 1
    start_page = 1
    print('start_page：{}'.format(start_page))
    urls_nn = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(start_page, start_page + page)]
    urls_nt = ['http://www.xicidaili.com/nt/{}'.format(i) for i in range(start_page, start_page + page)]
    urls_wn = ['http://www.xicidaili.com/wn/{}'.format(i) for i in range(start_page, start_page + page)]
    urls = urls_nn + urls_nt + urls_wn
    print('urls:')
    print(urls)
    getproxy.scrap_proxy(urls)
    print('\n'+'scrap_proxy_list ({} urls):'.format(len(getproxy.scrap_proxy_list)))
    print(getproxy.scrap_proxy_list)

    # test if the proxies are useful
    print('choose mode:\n[1]test all proxies\n[2]only test old proxies\n[other]exit')
    mode = int(input())
    if mode == 1:
        proxy_to_be_tested = getproxy.old_proxy_list + getproxy.scrap_proxy_list
    elif mode == 2:
        proxy_to_be_tested = getproxy.old_proxy_list
    else:
        print('Exit!')
        sys.exit()
    getproxy.test_proxy(proxy_to_be_tested)
    print('\n'+'useful_proxy_list:')
    print(getproxy.useful_proxy_list)

    # filter duplicate, verify the proxies and output them in the end
    verifyproxy = VerifyProxy(proxy_list=getproxy.useful_proxy_list, user_agent=user_agent)
    verifyproxy.process_proxy()












