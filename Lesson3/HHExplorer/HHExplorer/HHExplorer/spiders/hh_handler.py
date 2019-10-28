# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class HhHandlerSpider(scrapy.Spider):
    name = 'hh_handler'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=Go+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82/'] #поиск Go программиста

    def parse(self, response:HtmlResponse):
        pagination=response.xpath('//a[contains(@data-qa, "pager-next")]/@href').extract()
        if len(pagination) > 0:
            next_link = pagination[-1]
            yield response.follow(next_link, callback=self.parse)
        #print(response.url)
        vacancies = response.xpath('//a[contains(@data-qa, "vacancy-serp__vacancy-title")]/@href').extract()
        for itm in vacancies:
            yield response.follow(itm, callback=self.parse_vacancies)

    def parse_vacancies(self, response: HtmlResponse):
        vacancy_title=response.css('div.vacancy-title h1.header::text').extract_first()
        vacancy_title2 = response.css('div.vacancy-title h1.header span::text').extract_first()
        if vacancy_title2 is not None:
            vacancy_title = vacancy_title+vacancy_title2

        vacancy_salary=response.css('div.vacancy-title p.vacancy-salary::text').extract_first()
        hh_employer_url = response.xpath('//a[@itemprop="hiringOrganization"]/@href').extract_first()
        employer_title = response.xpath('//a[@itemprop="hiringOrganization"]/span[@itemprop="name"]/text()').extract_first()
        base_url = 'https://hh.ru'
        if hh_employer_url is None:
            hh_employer_url=""
        else:
            hh_employer_url = f"{base_url}{hh_employer_url}"

        key_skills=response.xpath('//span[@data-qa="skills-element"]//span[@data-qa="bloko-tag__text"]/text()').extract()
        # print(employer_title)
        # print(hh_employer_url)
        # print(vacancy_title)
        # print(vacancy_salary)
        # print(key_skills)
        item = { 'employer_title': employer_title,'vacancy_title': vacancy_title,'vacancy_salary': vacancy_salary,'hh_employer_url': hh_employer_url,'key_skills': key_skills}
        if hh_employer_url !="":
            yield response.follow(hh_employer_url, callback=self.parse_employer, cb_kwargs={'item': item})


    def parse_employer(self, response: HtmlResponse,item):
        official_employer_url = response.css('a.company-url::attr(href)').extract_first()
        if official_employer_url is None:
            official_employer_url=""

        item["official_employer_url"] = official_employer_url
        # print(official_employer_url)
        #print(item)
        yield item
