# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from AvitoExplorer.AvitoExplorer.items import AvitoexplorerItem
import scrapy
from scrapy.http import HtmlResponse


class AvitohandlerSpider(scrapy.Spider):
    name = 'AvitoHandler'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/kvartiry?cd=1/']


    def parse(self, response:HtmlResponse):
        next_page=response.xpath(
            '//div[contains(@class,"pagination")]/'
            'div[contains(@class,"pagination-nav")]/'
            'a[contains(@class,"js-pagination-next")]/@href'
        ).extract_first()
        yield response.follow(next_page,callback=self.parse)

        announcements=response.xpath(
            '//div[contains(@class,"catalog_table")]'
            '//div[contains(@class,"item")]'
            '//h3[@data-marker="item-title"]/a/@href'
        ).extract()

        for announcement in announcements:
            yield response.follow(announcement, callback=self.prase_announcement)


    def prase_announcement(selfself,response:HtmlResponse):
        loader = ItemLoader(item=AvitoexplorerItem(), response=response)
        loader.add_xpath('address', '//div[@class="item-address"]/span[@class="item-address__string"]/text()')
        loader.add_xpath('title', '//h1[@class="title-info-title"]/span[@itemprop="name"]/text()')
        loader.add_xpath('price', '//div[@class="item-price"]//span[@class="js-item-price"]/@content')
        loader.add_xpath('fotos','//div[contains(@class,"js-gallery-img-frame")]/@data-url')
        loader.add_value('announcement_url',response.request.url)
        loader.add_xpath('author_url', '//div[@class="seller-info-name js-seller-info-name"]/a/@href')
        yield loader.load_item()


