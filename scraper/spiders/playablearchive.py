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
            request = scrapy.Request(item["games"], callback=self.parse_page, cb_kwargs=dict(type=item["type"], icon=item["icon"], system=item["system"]))
            try:
                request.cb_kwargs["bios"] = item["bios"]
            except:
                request.cb_kwargs["bios"] = None
            yield request
        
    def parse_page(self, response, type, bios, icon, system):
        list = response.css("table.directory-listing-table tr")
        for game in list:
            game_item = GameItem()
            link = game.css("td a ::attr(href)").get()
            title = unquote(game.css("td a ::text").get())
            if title == " Go to parent directory" or title.endswith(".jpg") or title.endswith(".torrent") or title.endswith(".xml") or title.endswith(".sqlite") or title.endswith(".txt"):
                continue
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["link"] = response.request.url + "/" + link
            game_item["title"] = title
            game_item["system"] = system
            game_item["icon"] = icon
            game_item["core"] = type
            game_item["bios"] = bios
            game_item["playable"] = True
            yield game_item