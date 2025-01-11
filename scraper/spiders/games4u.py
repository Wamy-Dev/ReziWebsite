import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4

class Games4USpider(scrapy.Spider):
    name = "games4uspider"
    allowed_domains = "games4u.org"
    start_urls = [
        "https://games4u.org/a-z-posts/"
    ]

    def parse(self, response):
        for letter in response.css("div.letter-section"):
            for game in letter.css("ul li a"):
                game_item = GameItem()
                game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
                game_item["link"] = game.css("::attr(href)").get()
                game_item["title"] = game.css("::text").get().split(" (")[0]
                game_item["system"] = ["pc", "games4u"]
                game_item["icon"] = "PC"
                game_item["core"] = None
                game_item["bios"] = None
                game_item["playable"] = False
                game_item["site"] = "Games4U"
                yield game_item
