import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4

class XciNspSpider(scrapy.Spider):

    name = "xcinspspider"
    allowed_domains = ["xcinsp.com"]
    start_urls = ["https://www.xcinsp.com/"]

    def parse(self, response):
        list = response.css("ul.dhswp-html-sitemap-post-list li")
        for game in list:
            game_item = GameItem()
            game_item["link"] = game.css("a ::attr(href)").get()
            game_item["title"] = game.css("a ::text").get()
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item