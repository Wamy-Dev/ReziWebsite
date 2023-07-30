BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False

ITEM_PIPELINES = {
    "scraper.pipelines.BasicPipeline": 200,
}

FEEDS = {
    'rezi.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        }
}