import scrapy
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4

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
            link = game.css("a ::attr(href)").get()
            game_item = GameItem()
            game_item["link"] = f"https://nopaystation.com{link}"
            game_item["title"] = game.css("a ::text").get()
            game_item["id"] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            yield game_item