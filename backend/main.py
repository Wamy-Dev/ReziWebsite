from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#scrapers
from scraper.spiders.fitgirlrepacks import FitgirlSpider
from scraper.spiders.gog import GogSpider
crawler = CrawlerProcess(get_project_settings())

#put scrapers
crawler.crawl(FitgirlSpider)
crawler.crawl(GogSpider)

crawler.start()
