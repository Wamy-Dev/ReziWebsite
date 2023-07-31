import scrapy
import json
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class ArchiveSpider(scrapy.Spider):
    # json file with inputs
    f = open('input.json')
    data = json.load(f)
    name = "archivespider"
    allowed_domains = ["archive.org"]
    start_urls = data["archive.org"]
    
    def start_requests(self):
        for item in self.start_urls:
            yield scrapy.Request(item["games"], callback=self.parse_page, cb_kwargs=dict(system=item["system"], icon=item["icon"]))

    def parse_page(self, response, system, icon):
        list = response.css("table.directory-listing-table tr")
        for game in list:
            game_item = GameItem()
            link = game.css("td a ::attr(href)").get()
            title = unquote(game.css("td a ::text").get())
            if title == " Go to parent directory" or title.endswith(".jpg") or title.endswith(".torrent") or title.endswith(".xml") or title.endswith(".sqlite") or title.endswith(".txt"):
                continue
            game_item["link"] = response.request.url + "/" + link
            game_item["title"] = title
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["system"] = system
            game_item["icon"] = icon
            game_item["core"] = None
            game_item["bios"] = None
            game_item["playable"] = False
            yield game_item