import scrapy
import json
from scraper.items import GameItem
from datetime import datetime
from uuid import uuid4
from urllib.parse import unquote

class PokemonromSpider(scrapy.Spider):
    # json file with inputs
    f = open('input.json')
    data = json.load(f)
    name = "pokemonromspider"
    allowed_domains = ["pokemonrom.net"]
    start_urls = data["pokemonrom.net"]
    
    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        list = response.css("div.vce-loop-wrap article h2.entry-title a")
        for game in list:
            game_item = GameItem()
            link = game.css("::attr(href)").get()
            game_item["link"] = link
            game_item["title"] = unquote(game.css("::text").get())
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            yield game_item