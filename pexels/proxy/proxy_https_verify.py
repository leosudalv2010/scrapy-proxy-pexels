# encoding=utf-8

import requests


class VerifyProxy(object):
    def __init__(self, proxy_list, user_agent):
        self.proxy_list = proxy_list
        self.headers = {
            'User-Agent': user_agent
        }
        self.filter_proxy_list = []
        self.verified_proxy_list = []

    def process_proxy(self):
        print('\n'+'\n'+'----------------------')
        print('start verifying!!!')
        self.duplicatefilter(self.proxy_list)
        print('filter_proxy_list:')
        print(self.filter_proxy_list)
        self.verify_proxy(self.filter_proxy_list)
        print('\n'+'verified_proxy_list:')
        print(self.verified_proxy_list)
        self.output_proxy(self.verified_proxy_list)

    def duplicatefilter(self, proxy_list):
        proxy_seen = set()
        for proxy in proxy_list:
            if proxy in proxy_seen:
                print('found duplicate proxy :{}'.format(proxy))
            else:
                proxy_seen.add(proxy)
                self.filter_proxy_list.append(proxy)

    def verify_proxy(self, proxy_list):
        # verify the proxies
        for proxy in proxy_list:
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
            }
            status_code = 200
            for i in range(2):
                if status_code != 200:
                    break
                try:
                    response = requests.get('https://www.pexels.com/', headers=self.headers, proxies=proxies, timeout=5)
                    # print(response.text)
                    status_code = response.status_code
                except:
                    status_code = 0
                    print('ConnectionError')
            if status_code == 200:
                print('got a verified proxy:{}'.format(proxy))
                self.verified_proxy_list.append(proxy)

    def output_proxy(self, proxy_list):
        with open('proxy_https_verified.txt', 'w') as f:
            for proxy in proxy_list:
                f.write(proxy + '\n')





