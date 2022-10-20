import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4

class AbandonwareSpider(scrapy.Spider):

    name = "abandonwarespider"
    allowed_domains = ["myabandonware.com"]
    start_urls = ["https://myabandonware.com/browse/name/"]

    def parse(self, response):
        total_pages = response.css("div.pagination a ::text").getall()[-1]
        current_page = response.css("div.pagination a.current ::text").get()
        if total_pages and current_page:
            if int(current_page) == 1:
                for page_number in range(2, int(total_pages) + 1):
                    yield response.follow(url=f'https://www.myabandonware.com/browse/name/page/{page_number}/')
        list = response.css("div.games div.itemListGame a.name")
        for game in list:
            link = game.css("::attr(href)").get()
            game_item = GameItem()
            game_item["link"] = f"https://myabandonware.com{link}"
            game_item["title"] = game.css("::text").get()
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item