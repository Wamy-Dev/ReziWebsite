import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class CPGSpider(scrapy.Spider):

    name = "cpgspider"
    allowed_domains = ["https://cpgrepacks.site/"]
    start_urls = ["https://cpgrepacks.site/"]

    def parse(self, response):
        total_pages = response.css("div.pagination a ::text").getall()[-2]
        current_page = response.css("div.pagination span.current ::text").get()
        if total_pages and current_page:
            if int(current_page) == 1:
                for page_number in range(2, int(total_pages) + 1):
                    yield response.follow(url=f'https://cpgrepacks.site/page/{page_number}')
        list = response.css("h1.entry-title a")
        for game in list:
            game_item = GameItem()
            game_item["link"] = game.css("::attr(href)").get()
            game_item["title"] = unquote(game.css("::text").get())
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["system"] = ["pc", "repacks"]
            game_item["icon"] = "PC"
            yield game_item