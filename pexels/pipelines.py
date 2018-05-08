# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import pymongo
from pexels.settings import IMAGES_STORE
import os
import shutil


class NoImageFilter(object):
    def process_item(self, item, spider):
        if not item.get('image_url'):
            raise DropItem('Found item without image_url')
        return item


class DuplicateFilter(object):
    def __init__(self):
        self.image_seen = set()

    def process_item(self, item, spider):
        if item['image_url'] in self.image_seen:
            raise DropItem('Found duplicate item')
        self.image_seen.add(item['image_url'])
        return item


class MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['mydb']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.collection].insert_one(dict(item))
        return item


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

