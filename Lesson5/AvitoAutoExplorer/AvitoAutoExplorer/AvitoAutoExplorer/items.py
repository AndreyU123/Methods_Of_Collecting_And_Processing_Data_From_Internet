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

def cleaner_params(item):
    result = item.split('">')[-1].split(':')
    key = result[0]
    value = result[-1].split('</span>')[-1].split('</')[0][:-1]
    return {key: value}


def dict_params(items):
    result = {}
    for itm in items:
        result.update(itm)
    return result


class AvitoAutoExplorerItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    fotos = scrapy.Field(input_processor=MapCompose(cleaner_foto))
    price = scrapy.Field(output_processor=TakeFirst())
    characteristics = scrapy.Field(input_processor=MapCompose(cleaner_params), output_processor=dict_params)
    details= scrapy.Field(output_processor=TakeFirst())
   # VIN_data= scrapy.Field(output_processor=TakeFirst())

