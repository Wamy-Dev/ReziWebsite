import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote
import logging
import requests
from scrapy.http import HtmlResponse
from decouple import config

class GameBountySpider(scrapy.Spider):
    name = "gamebountyspider"
    allowed_domains = ["gamebounty.world"]
    start_urls = ["https://gamebounty.world/singleplayer/"]

    def parse(self, response):
        request = requests.get("https://gamebounty.world/wp-json/pikapika/v1/articlesforwamy", headers={
            "User-Agent": "Rezi",
            "Content-Type": "application/json",
            "api-key": config("GAMEBOUNTY_API_KEY")
        })
        data = request.json()
        for game in data:
            logging.info(game)
            game_item = GameItem()
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["link"] = game["link"]
            game_item["title"] = game["title"]
            game_item["system"] = ["pc", "repacks"]
            game_item["icon"] = "PC"
            game_item["core"] = None
            game_item["bios"] = None
            game_item["playable"] = False
            game_item["site"] = "Gamebounty"
            yield game_item