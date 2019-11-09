from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from InstagramExplorer.config import INSTANT_LOGIN, INSTANT_PASS, INSTANT_PARS_USERS, INSTANT_POSTS_COUNT_PER_USER
from InstagramExplorer.InstagramExplorer import settings
import InstagramExplorer.InstagramExplorer.spiders
from InstagramExplorer.InstagramExplorer.spiders.instagramSpider import InstagramSpider

if __name__ =='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider,INSTANT_LOGIN, INSTANT_PASS, INSTANT_PARS_USERS, INSTANT_POSTS_COUNT_PER_USER)
   # process.crawl(OtherSpider)
    process.start()