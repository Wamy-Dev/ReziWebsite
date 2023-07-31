import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

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
        list = response.css("table.rom_listing_table tr")
        for game in list:
            game_item = GameItem()
            titleitem = game.css("td a ::text").getall()
            for each in titleitem:
                if len(each) > 1 and each != "":
                    game_item["title"] = unquote(each.strip())
                else:
                    continue
            link = game.css("td a ::attr(href)").get()
            if link:
                game_item["link"] = game.css("td a ::attr(href)").get()
            else:
                continue
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["icon"] = "3DS"
            game_item["system"] = ["3ds", "nintendo 3ds", "n3ds"]
            game_item["core"] = None
            game_item["bios"] = None
            game_item["playable"] = False
            yield game_item