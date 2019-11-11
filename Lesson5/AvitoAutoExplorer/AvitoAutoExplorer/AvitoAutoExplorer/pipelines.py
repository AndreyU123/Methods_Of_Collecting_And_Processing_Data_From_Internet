# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class AvitoExplorerPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        self.avito_bd = client.AvitoAuto

    def process_item(self, item, spider):
        fotos=str(item['fotos']).replace('[','').replace(']','').replace('\'','')
        item_dict={'fotos':fotos,'title': item['title'],'price': item['price'],'characteristics': item['characteristics'],'details': item['details']} #'VIN_data' : item['VIN_data']
        collection = self.avito_bd['AvitoAutoCollection']
        collection.insert_one(item_dict)
        return item


class AvitoPhotosPiplines(ImagesPipeline):

    def get_media_requests(self,item,info):
        if item['fotos']:
            for img in item['fotos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    pass

    def item_completed(self,results,item,info):
        if results:
            tmp=[itm[1]['url'] for itm in results if itm[0]]
            item['fotos']=tmp
        return item