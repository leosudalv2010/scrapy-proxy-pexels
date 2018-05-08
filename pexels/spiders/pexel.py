# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from pexels.items import PexelItem


class PexelSpider(scrapy.Spider):
    name = 'pexel'
    allowed_domains = ['pexels.com']

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            page = 1
            url = 'https://www.pexels.com/search/{0}/?page={1}'.format(keyword, page)
            yield scrapy.Request(url, callback=self.parse, meta={'keyword': keyword, 'page': page})

    def parse(self, response):
        keyword = response.meta['keyword']
        page = response.meta['page']
        images = response.xpath('//article[starts-with(@class, "photo-item")]')
        for image in images:
            loader = ItemLoader(item=PexelItem())
            loader.add_value('keyword', keyword)
            loader.add_value('page', str(page))
            loader.add_value('image_url', image.xpath('a[@class="js-photo-link"]/img/@data-big-src').extract_first())
            yield loader.load_item()
        self.logger.info('Page {} of {} is completed'.format(page, keyword))
        # go to next page
        if page < self.settings.get('MAX_PAGE'):
            page += 1
            next_url = 'https://www.pexels.com/search/{0}/?page={1}'.format(keyword, page)
            yield scrapy.Request(next_url, callback=self.parse, meta={'keyword': keyword, 'page': page})





