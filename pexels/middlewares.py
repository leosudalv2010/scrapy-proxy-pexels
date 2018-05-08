# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random


class ProxyMiddleware(object):
    def __init__(self):
        with open('pexels/proxy/proxy_https_verified.txt', 'r') as f:
            self.proxy_pool_https = f.readlines()

    def process_request(self, request, spider):
        # filter the repeated proxy
        while True:
            proxy_raw_https = random.choice(self.proxy_pool_https).strip()
            proxy = 'https://' + proxy_raw_https
            if proxy != request.meta.get('proxy'):
                break
        # set up proxy
        request.meta['proxy'] = proxy
        return

