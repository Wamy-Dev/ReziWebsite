import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class GogSpider(scrapy.Spider):

    name = "gogspider"
    allowed_domains = ["gog-games.com"]
    start_urls = ["https://gog-games.com/search/all/1/title/asc/any"]

    def parse(self, response):
        total_pages = response.css("div.pagination a.btn ::text").getall()[-1]
        current_page = response.css("div.pagination span.blue ::text").get()
        if total_pages and current_page:
            if int(current_page) == 1:
                for page_number in range(2, int(total_pages) + 1):
                    yield response.follow(url=f'https://gog-games.com/search/all/{page_number}/title/asc/any')
        list = response.css("div.game-blocks a.block")
        for game in list:
            link = game.css("::attr(href)").get()
            game_item = GameItem()
            game_item["link"] = f"https://gog-games.com/{link}"
            game_item["title"] = unquote(game.css("div.info span.title ::text").get())
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item