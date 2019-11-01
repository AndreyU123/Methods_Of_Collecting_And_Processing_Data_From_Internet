# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqldatabase.database import AvitoExplorerBase
from sqldatabase.models import Flats,Addresses,Base
import scrapy
from scrapy.pipelines.images import ImagesPipeline

base_url = 'https://www.avito.ru/'

class AvitoexplorerPipeline(object):
    def __init__(self):
        bd_url = 'sqlite:///avitoexplorer_base.sqlite'
        self.bd = AvitoExplorerBase(Base, bd_url)



    def process_item(self, item, spider):
        str_address=item['address']
        if str_address is not None:
            str_address=str(str_address).split(',')

        house= ''
        street=''
        city=''
        if len(str_address)>=3:
            house=str_address[len(str_address)-1]
            street=str_address[len(str_address)-2]
            city=str_address[len(str_address)-3]

        address = Addresses(city,street,house)
        fotos=str(item['fotos']).replace('[','').replace(']','').replace('\'','')
        author_url=item['author_url']
        if item['author_url'] is not None:
            author_url=f'{base_url}{ author_url}'

        flat=Flats(item['title'],fotos,item['price'],item['announcement_url'],author_url,address)
        self.bd.session.add(flat)
        self.bd.session.commit()
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