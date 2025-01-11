import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4

class GameDriveSpider(scrapy.Spider):
    name = "gamedrivespider"
    allowed_domains = "gamedrive.org"
    start_urls = [
        "https://gamedrive.org/elamigos-repacks-a-z/",
        "https://gamedrive.org/all-dodi-repacks-a-z/",
        "https://gamedrive.org/fitgirl-repacks-a-z/",
        "https://gamedrive.org/m4ckd0ge-repacks-a-z/",
        "https://gamedrive.org/scooter-repacks-a-z/",
        ]

    def parse(self, response):
        gameList = response.css("div.letter-section")
        for letter in gameList:
            for game in letter.css("ul li a"):
                game_item = GameItem()
                game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
                game_item["link"] = game.css("::attr(href)").get()
                game_item["title"] = game.css("::text").get().split(" (")[0]
                game_item["system"] = ["pc", response.css("title::text").get().split(" Repacks")[0].lower()]
                game_item["icon"] = "PC"
                game_item["core"] = None
                game_item["bios"] = None
                game_item["playable"] = False
                game_item["site"] = "Gamedrive.org"
                yield game_item
