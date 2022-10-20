import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4

class SteamripSpider(scrapy.Spider):

    name = "steamripspider"
    allowed_domains = ["xcinsp.com"]
    start_urls = ["https://steamrip.com/games-list/"]

    def parse(self, response):
        list = response.css("div.az-list-container ul.az-list li.az-list-item a")
        for game in list:
            game_item = GameItem()
            link = game.css("::attr(href)").get()
            game_item["link"] = f"https://steamrip.com{link}"
            game_item["title"] = game.css("::text").get()
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item