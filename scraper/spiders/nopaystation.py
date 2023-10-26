import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class NoPayStationSpider(scrapy.Spider):

    name = "nopaystationspider"
    allowed_domains = ["nopaystation.com"]

    def start_requests(self):
        yield scrapy.Request(url="https://nopaystation.com/search?query=&limit=100&orderBy=completionDate&sort=DESC&missing=Hide&page=10000", callback=self.getTotalPages)

    def getTotalPages(self, response):
        global total_pages
        total_pages = response.css("a.page-link ::text").getall()[-2]
        yield scrapy.Request(url=f'https://nopaystation.com/search?query=&limit=100&orderBy=completionDate&sort=DESC&missing=Hide', callback=self.parse)

    def parse(self, response):
        current_page = response.css("li.active ::text").get()
        print(total_pages)
        if total_pages and current_page:
            if int(current_page) == 1:
                for page_number in range(2, int(total_pages) + 1):
                    yield response.follow(url=f'https://nopaystation.com/search?query=&limit=100&orderBy=completionDate&sort=DESC&missing=Hide&page={page_number}')
        list = response.css("table.resultsTable td")
        for game in list:
            system = game.css("span.badge-secondary ::text").get()
            if system == "PS3":
                system = ["ps3", "playstation 3"]
                icon = ["Playstation 3"]
            elif system == "PSV":
                system = ["psv", "playstation vita", "vita"]
                icon = ["Playstation Vita"]
            elif system == "PSP":
                system = ["psp", "playstation portable"]
                icon = ["Playstation Portable"]
            elif system == "PSX":
                system = ["psx", "playstation", "playstation 1"]
                icon = ["Playstation 1"]
            elif system == "PSM":
                system = ["psm", "playstation move", "playstation vr"]
                icon = ["Playstation Move"]
            else:
                system = []
                icon = []
            link = game.css("a ::attr(href)").get()
            game_item = GameItem()
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["link"] = f"https://nopaystation.com{link}"
            game_item["title"] = unquote(game.css("a ::text").get())
            game_item["system"] = system
            game_item["icon"] = icon
            game_item["core"] = None
            game_item["bios"] = None
            game_item["playable"] = False
            game_item["site"] = "NoPayStation"
            yield game_item