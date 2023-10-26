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
    
    def start_requests(self):
        for item in self.start_urls:
            yield scrapy.Request(item["games"], callback=self.parse_page, cb_kwargs=dict(system=item["system"], icon=item["icon"]))

    def parse_page(self, response, icon, system):
        list = response.css("div.vce-loop-wrap article h2.entry-title a")
        for game in list:
            game_item = GameItem()
            link = game.css("::attr(href)").get()
            game_item["id"] = str(uuid4()) + datetime.now().strftime('%Y%m-%d%H-%M%S-')
            game_item["link"] = link
            game_item["title"] = unquote(game.css("::text").get()).replace("ROM", "")
            game_item["system"] = system
            game_item["icon"] = icon
            game_item["core"] = None
            game_item["bios"] = None
            game_item["playable"] = False
            game_item["site"] = "Pokemonrom"
            yield game_item