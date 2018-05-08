# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, Join
import datetime


class PexelItem(Item):
    collection = 'pexels-images-{}'.format(str(datetime.datetime.now()).split('.')[0])

    keyword = Field(
        output_processor=Join(),
    )
    page = Field(
        output_processor=Join(),
    )
    image_url = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join(),
    )
    image_path = Field()

