# -*- coding: utf-8 -*-
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode, urljoin
from copy import deepcopy
from scrapy.loader import ItemLoader
from ZillowExplorer.ZillowExplorer.items import ZillowExplorerItem
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

class ZillowSpider(scrapy.Spider):
    name = 'ZillowSpider'
    allowed_domains = ['zillow.com', 'photos.zillowstatic.com', 'zillowstatic.com']
    start_urls = ['http://zillow.com/']
    base_url = 'https://www.zillow.com/'
    browser = webdriver.Firefox(executable_path=r'E:\GeekBrains\Methods_Of_Collecting_And_Processing_Data_From_Internet\HomeWork\ZillowExplorer\geckodriver.exe')

    def __init__(self, pars_cities, *args, **kwargs):
        self.pars_cities_names = pars_cities
        super().__init__(*args, *kwargs)

    def parse(self, response: HtmlResponse):
        for city in self.pars_cities_names:
            url=urljoin(self.base_url,city)
            yield response.follow(url, callback=self.parse_city)


    def parse_city(self,response: HtmlResponse):
        next = response.css('.zsg-pagination-next a::attr(href)').extract_first()
        yield response.follow(next, callback=self.parse_city)

        real_estate_list = response.css('div#grid-search-results ul.photo-cards li article a.list-card-link::attr(href)')
        for adv in real_estate_list.extract():
            yield response.follow(adv, callback=self.pars_adv)

    def pars_adv(self, response: HtmlResponse):
        self.browser.get(response.url)
        titles=response.xpath('//header/h1[@class="ds-address-container"]/span/text()').extract()
        title_list=[]
        for item in titles:
            if(item not in title_list):
                title_list.append(item)

        title= "".join(title_list)
        location=title_list[2]
        description=response.xpath('//div[@class="Text-sc-1vuq29o-0 sc-kkGfuU fHFAGp"]/text()').extract_first()

        parameters = {}
        properties_names=response.xpath('//ul[@class="ds-home-fact-list"]/li[@class="ds-home-fact-list-item"]/span[@class="ds-standard-label ds-home-fact-label"]/text()').extract()
        properties_values=response.xpath('//ul[@class="ds-home-fact-list"]/li[@class="ds-home-fact-list-item"]/span[@class="ds-body ds-home-fact-value"]/text()').extract()
        for i in range(min(len(properties_names),len(properties_values))):
            parameters.update({properties_names[i].replace(':','') : properties_values[i]})

        media = self.browser.find_element_by_css_selector('.ds-media-col')
        photo_pic_img_len = len(self.browser.find_elements_by_xpath(
            '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))

        while True:
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            tmp_len = len(self.browser.find_elements_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))
            if photo_pic_img_len == tmp_len:
                break

            photo_pic_img_len = len(self.browser.find_elements_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))

        fotos = [itm.get_attribute('srcset').split(' ')[-2] for itm in
                  self.browser.find_elements_by_xpath(
                      '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
                  ]
        item = ItemLoader(ZillowExplorerItem(), response)
        item.add_value('title', title)
        item.add_value('fotos', fotos)
        item.add_value('description', description)
        item.add_value('parameters', parameters)
        item.add_value('location',location)

        yield item.load_item()

    def __del__(self):
        self.browser.close()