import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class ScooterRepacksSpider(scrapy.Spider):

    name = "scooterrepacksspider"
    allowed_domains = ["scooter-repacks.site"]
    start_urls = ["https://scooter-repacks.site/all-my-repacks/"]

    def parse(self, response):
        list = response.css("ul.az-columns li a")
        for game in list:
            game_item = GameItem()
            link = game.css("::attr(href)").get()
            game_item["link"] = link
            game_item["title"] = unquote(game.css("::text").get().strip().split(" (")[0])
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item