# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from AvitoAutoExplorer.AvitoAutoExplorer.items import AvitoAutoExplorerItem
import scrapy
from scrapy.http import HtmlResponse
import json

class AvitoAutoHandlerSpider(scrapy.Spider):
    name = 'AvitoAutoHandler'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/avtomobili/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//div[contains(@class,"pagination")]/'
            'div[contains(@class,"pagination-nav")]/'
            'a[contains(@class,"js-pagination-next")]/@href'
        ).extract_first()
        yield response.follow(next_page, callback=self.parse)

        announcements = response.xpath(
            '//div[contains(@class,"catalog_table")]'
            '//div[contains(@class,"item")]'
            '//h3[@data-marker="item-title"]/a/@href'
        ).extract()

        for announcement in announcements:
            yield response.follow(announcement, callback=self.prase_announcement)

    def prase_announcement(self, response: HtmlResponse):
        temp=response.xpath('//div[@class="autoteka-teaser-wrapper"]//p[@data-marker="subtitle"]/text()')
        data_item_id=response.xpath('//div[@class="js-autoteka-teaser"]/@data-item-id').extract_first()

        title=response.xpath('//h1[@class="title-info-title"]/span[@itemprop="name"]/text()').extract_first()
        price=response.xpath('//div[@class="item-price"]//span[@class="js-item-price"]/@content').extract_first()
        fotos=response.xpath('//div[contains(@class,"js-gallery-img-frame")]/@data-url').extract()
        characteristics=response.xpath('//div[@class="item-params"]/ul[@class="item-params-list"]/li').extract()
        item = {'title' : title, 'price' : price,'fotos' : fotos, 'characteristics' : characteristics}
        spec_url=f'https://www.avito.ru/js/items/{data_item_id}/car_spec?'
        yield response.follow(spec_url,callback=self.prase_car_spec, cb_kwargs={'item': item})


    def prase_car_spec(self, response: HtmlResponse,item):
        row_data=response.body_as_unicode()
        details=json.loads(row_data)
        if details is not None and details['success']==True and details['spec'] is not None:
            item['details']=details['spec']
        else:
            item['details']=''

        loader = ItemLoader(item=AvitoAutoExplorerItem(), response=response)
        loader.add_value('title', item['title'])
        loader.add_value('price', item['price'])
        loader.add_value('fotos', item['fotos'] )
        loader.add_value('characteristics',item['characteristics'])
        loader.add_value('details',item['details'])
        yield loader.load_item()


