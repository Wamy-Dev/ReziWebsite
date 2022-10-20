import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4

class ThreeDSRomsSpider(scrapy.Spider):

    name = "3dsromsspider"
    allowed_domains = ["3dsroms.org"]
    start_urls = ["https://3dsroms.org/"]

    def parse(self, response):
        total_pages = response.css("a.page-numbers ::text").getall()[-2]
        current_page = response.css("span.current ::text").get()
        if total_pages and current_page:
            if int(current_page) == 1:
                for page_number in range(2, int(total_pages) + 1):
                    yield response.follow(url=f'https://3dsroms.org/page/{page_number}/')
        list = response.css("table.rom_listing_table tr td a")
        for game in list:
            game_item = GameItem()
            game_item["link"] = game.css("::attr(href)").get()
            game_item["title"] = game.css("::text").get().strip()
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item