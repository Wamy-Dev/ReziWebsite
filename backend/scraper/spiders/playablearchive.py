import scrapy
import json
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class ArchivePlayableSpider(scrapy.Spider):
    # json file with inputs
    f = open('input.json')
    data = json.load(f)
    name = "archivegamespider"
    allowed_domains = ["archive.org"]
    urls = data["playablearchive.org"]

    def start_requests(self):
        for item in self.urls:
            request = scrapy.Request(item["games"], callback=self.parse_page, cb_kwargs=dict(type=item["type"]))
            try:
                request.cb_kwargs["bios"] = "bios"
            except:
                request.cb_kwargs["bios"] = None
            yield request
        
    def parse_page(self, response, type, bios):
        list = response.css("table.directory-listing-table tr")
        for game in list:
            game_item = GameItem()
            link = game.css("td a ::attr(href)").get()
            game_item["link"] = response.request.url + "/" + link
            game_item["title"] = unquote(game.css("td a ::text").get())
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["core"] = type
            game_item["bios"] = bios
            game_item["playable"] = True
            yield game_item