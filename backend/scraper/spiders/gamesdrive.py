import scrapy
import json
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class GamesdriveSpider(scrapy.Spider):
    # json file with inputs
    f = open('input.json')
    data = json.load(f)
    name = "gamesdrivespider"
    allowed_domains = ["gamesdrive.net"]
    start_urls = data["gamesdrive.net"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.getpages)

    def getpages(self, response):
            total_pages = response.css("a.pagination_last ::text").get()
            current_page = response.css("span.pagination_current ::text").get()
            if total_pages and current_page:
                if int(current_page) == 1:
                    for page_number in range(2, int(total_pages) + 1):
                        yield scrapy.Request(url=f'{response.request.url}?page={page_number}', callback=self.parse_page)

    def parse_page(self, response):
        print("running")
        list = response.css("span.subject_new a")
        for game in list:
            game_item = GameItem()
            link = game.css("::attr(href)").get()
            game_item["link"] = f'https://gamesdrive.net/{link}'
            game_item["title"] = unquote(game.css("::text").get().split("|")[0].replace(".", " ").split("( ")[0])
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item