# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def map_photos(values):
    return values

class ZillowExplorerItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    fotos = scrapy.Field(input_processor=MapCompose(map_photos))
    description=scrapy.Field(output_processor=TakeFirst())
    parameters=scrapy.Field(output_processor=TakeFirst())
    location=scrapy.Field(output_processor=TakeFirst())


