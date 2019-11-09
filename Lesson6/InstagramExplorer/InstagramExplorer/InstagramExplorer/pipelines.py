# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import scrapy
#from scrapy.pipelines.images import ImagesPipeline

class InstagramExplorerPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        self.instagram_db = client.InstagramDB

    def process_item(self, item, spider):
        item_dict={'user': item['user'],'following_users': item['following_users']}
        collection = self.instagram_db['InstagramCollection']
        collection.insert_one(item_dict)
        return item