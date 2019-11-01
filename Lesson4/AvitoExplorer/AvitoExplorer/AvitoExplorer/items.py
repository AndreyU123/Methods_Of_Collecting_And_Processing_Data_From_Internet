# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst

def cleaner_foto(values):
    if(values[:2]) == '//':
        return f'http:{values}'
    return values

class AvitoexplorerItem(scrapy.Item):
    address = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    fotos = scrapy.Field(input_processor=MapCompose(cleaner_foto))
    price = scrapy.Field(output_processor=TakeFirst())
    announcement_url = scrapy.Field(output_processor=TakeFirst())
    author_url = scrapy.Field(output_processor=TakeFirst())

