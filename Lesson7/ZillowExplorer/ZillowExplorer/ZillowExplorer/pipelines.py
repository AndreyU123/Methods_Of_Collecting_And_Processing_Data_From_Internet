# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import scrapy

class ZillowExplorerPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        self.zillow_db = client.ZillowDB

    def process_item(self, item, spider):
        item_dict = {'title': item['title'], 'fotos': item['fotos'],'description': item['description'], 'parameters' : item['parameters'],'location' : item['location']}
        collection = self.zillow_db['ZillowCollection']
        collection.insert_one(item_dict)
        return item
