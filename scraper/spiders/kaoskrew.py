import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class KaosKrewSpider(scrapy.Spider):

    name = "kaoskrewspider"
    allowed_domains = ["kaoskrew.org"]
    start_urls = ["https://kaoskrew.org/viewforum.php?f=13"]

    def parse(self, response):
        total_pages = response.css("div.pagination li ::text").getall()[-2]
        current_page = response.css("div.pagination li.active ::text").get()
        if total_pages and current_page:
            if int(current_page) == 1:
                for page_number in range(2, int(total_pages) + 1):
                    yield response.follow(url=f'https://kaoskrew.org/viewforum.php?f=13&start={page_number*50}')
        list = response.css("li.row div.list-inner a.topictitle")
        for game in list:
            link = game.css("::attr(href)").get()
            game_item = GameItem()
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["link"] = f"https://kaoskrew.org{link}"
            game_item["title"] = unquote(game.css("::text").get()).replace(".", " ")
            game_item["system"] = ["pc", "kaoskrew", "repacks"]
            game_item["icon"] = "PC"
            game_item["core"] = None
            game_item["bios"] = None
            game_item["playable"] = False
            yield game_item