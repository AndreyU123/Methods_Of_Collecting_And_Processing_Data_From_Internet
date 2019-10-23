from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from HHExplorer.HHExplorer import settings
from HHExplorer.HHExplorer.spiders.hh_handler import HhHandlerSpider

if __name__ =='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhHandlerSpider)
   # process.crawl(OtherSpider)
    process.start()