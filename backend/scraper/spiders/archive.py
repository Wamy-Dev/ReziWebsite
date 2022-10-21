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
    
    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        list = response.css("table.directory-listing-table tr")
        for game in list:
            game_item = GameItem()
            link = game.css("td a ::attr(href)").get()
            game_item["link"] = response.request.url + "/" + link
            game_item["title"] = unquote(game.css("td a ::text").get())
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item