# Scrapy-proxy-pexels
This project is constructed to automatically download pictures from pexels.com with different proxies
## 1 Preparation
Make sure to install Python 3.6 and MongoDB.<br>
Make sure to install the following libs: scrapy, pymongo, requests, lxml.
## 2 Configuration for enabling proxy
#### 2.1 Set a custom ProxyMiddleware
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
#### 2.2 Enable DOWNLOADER_MIDDLEWARES in settings.py
    DOWNLOADER_MIDDLEWARES = {
    'pexels.middlewares.ProxyMiddleware': 300,
    }
#### 2.3 Important modification
    CONCURRENT_REQUESTS_PER_IP = 16
    DOWNLOAD_TIMEOUT = 10
    RETRY_TIMES = 100
DOWNLOAD_TIMEOUT is reduced to 10 to quickly pass unefficient proxies. RETRY_TIMES is increased to 100 to make sure all the requests can be completed.
#### 2.4 Additional scrips
"proxy_https.py" and "proxy_https_verify.py" are created to gather free proxies, varify them and stored in "proxy_https_verified.txt".
## 3 Configuration for picture downloading
#### 3.1 Set a custom ImagePipeline
    import scrapy
    from scrapy.pipelines.images import ImagesPipeline
    from pexels.settings import IMAGES_STORE
    import os
    import shutil

    class ImagePipeline(ImagesPipeline):
        def get_media_requests(self, item, info):
            yield scrapy.Request(item['image_url'])

        def item_completed(self, results, item, info):
            image_path = [x['path'] for ok, x in results if ok]
            if not image_path:
                raise DropItem("Image can't be downloaded")
            # remove the images to new path (in order to group the images by searching keyword)
            old_image_path = IMAGES_STORE + '/' + image_path[0]
            new_image_path = IMAGES_STORE + '/' + item['keyword'] + '/' + image_path[0].split('/')[-1]
            # create dir if not exist
            if not os.path.exists(IMAGES_STORE + '/' + item['keyword']):
                os.mkdir(IMAGES_STORE + '/' + item['keyword'])
            # key remove step
            shutil.move(old_image_path, new_image_path)
            # add image path to item field
            item['image_path'] = new_image_path
            return item
The subclass ImagePipeline is wrote for Scrapy to automatically download the pictures from item['image_url'] and then group the downloaded pictures by their searching keyworwds.
#### 3.2 Enable pipelines in settings.py
    ITEM_PIPELINES = {
        'pexels.pipelines.NoImageFilter': 301,
        'pexels.pipelines.DuplicateFilter': 302,
        'pexels.pipelines.ImagePipeline': 303,
        'pexels.pipelines.MongoPipeline': 304,
    }
#### 3.3 Create a path to store downloaded pictures
    IMAGES_STORE = './images'
IMAGES_STORE must be created otherwise the pictures will not be downloaded.
# 4 Summary
Proxies are used in this project to avoid being blocked by the websites because of too frequent visits.
ImagePipeline is enabled to download pictures and group them by searching keywords.