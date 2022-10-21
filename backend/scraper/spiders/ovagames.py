import scrapy
import json
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class OvaGamesSpider(scrapy.Spider):
    # json file with inputs
    f = open('input.json')
    data = json.load(f)
    name = "ovagamesspider"
    allowed_domains = ["ovagames.com"]
    start_urls = data["ovagames.com"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.getpages)

    def getpages(self, response):
            total_pages = response.css("span.pages ::text").get().split(" ")[-1]
            current_page = response.css("span.current ::text").get()
            if total_pages and current_page:
                if int(current_page) == 1:
                    for page_number in range(2, int(total_pages) + 1):
                        yield scrapy.Request(url=f'{response.request.url}/page/{page_number}', callback=self.parse_page)

    def parse_page(self, response):
        list = response.css("div.post-wrapper")
        for game in list:
            game_item = GameItem()
            link = game.css("a ::attr(href)").get()
            game_item["link"] = link
            game_item["title"] = unquote(game.css("a ::text").get().strip())
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item