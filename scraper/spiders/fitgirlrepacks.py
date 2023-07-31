import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class FitgirlSpider(scrapy.Spider):

    name = "fitgirlspider"
    allowed_domains = ["fitgirl-repacks.site"]
    start_urls = ["https://fitgirl-repacks.site/all-my-repacks-a-z/"]

    def parse(self, response):
        total_pages = response.css("ul.lcp_paginator li ::text").getall()[-2]
        current_page = response.css("ul.lcp_paginator li.lcp_currentpage ::text").get()
        if total_pages and current_page:
            if int(current_page) == 1:
                for page_number in range(2, int(total_pages) + 1):
                    yield response.follow(url=f'https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={page_number}')
        list = response.css("ul.lcp_catlist li")
        for game in list:
            game_item = GameItem()
            game_item["link"] = game.css("li ::attr(href)").get()
            game_item["title"] = unquote(game.css("a ::text").get())
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["system"] = ["pc", "repacks", "fitgirl"]
            game_item["icon"] = "PC"
            game_item["core"] = None
            game_item["bios"] = None
            game_item["playable"] = False
            yield game_item