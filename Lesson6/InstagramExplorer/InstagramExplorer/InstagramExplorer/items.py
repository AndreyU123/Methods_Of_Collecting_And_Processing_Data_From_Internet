# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class InstagramExplorerItem(scrapy.Item):
    user = scrapy.Field(output_processor=TakeFirst())
    following_users = scrapy.Field(output_processor=TakeFirst())


