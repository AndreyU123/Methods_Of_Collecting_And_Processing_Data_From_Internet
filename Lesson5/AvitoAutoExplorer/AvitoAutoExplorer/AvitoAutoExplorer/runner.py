from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from AvitoAutoExplorer.AvitoAutoExplorer import settings
import AvitoAutoExplorer.AvitoAutoExplorer.spiders
from AvitoAutoExplorer.AvitoAutoExplorer.spiders.AvitoAutoHandler import AvitoAutoHandlerSpider

if __name__ =='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoAutoHandlerSpider)
   # process.crawl(OtherSpider)
    process.start()