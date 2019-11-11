from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from AvitoExplorer.AvitoExplorer import settings
from AvitoExplorer.AvitoExplorer.spiders.AvitoHandler import AvitohandlerSpider

if __name__ =='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitohandlerSpider)
   # process.crawl(OtherSpider)
    process.start()