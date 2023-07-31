import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class SteamripSpider(scrapy.Spider):

    name = "steamripspider"
    allowed_domains = ["xcinsp.com"]
    start_urls = ["https://steamrip.com/games-list/"]

    def parse(self, response):
        list = response.css("div.az-list-container ul.az-list li.az-list-item a")
        for game in list:
            game_item = GameItem()
            link = game.css("::attr(href)").get()
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["link"] = f"https://steamrip.com{link}"
            game_item["title"] = unquote(game.css("::text").get()).replace("Free Download", "")
            game_item["system"] = ["pc", "repacks"]
            game_item["icon"] = "PC"
            game_item["core"] = None
            game_item["bios"] = None
            game_item["playable"] = False
            yield game_item