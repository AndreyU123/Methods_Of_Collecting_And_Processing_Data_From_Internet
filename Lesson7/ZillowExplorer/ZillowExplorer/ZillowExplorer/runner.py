from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from ZillowExplorer.config import ZILLOW_PARS_CITIES
from ZillowExplorer.ZillowExplorer import settings
import ZillowExplorer.ZillowExplorer.spiders
from ZillowExplorer.ZillowExplorer.spiders.ZillowSpider import ZillowSpider

if __name__ =='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(ZillowSpider,ZILLOW_PARS_CITIES)
   # process.crawl(OtherSpider)
    process.start()