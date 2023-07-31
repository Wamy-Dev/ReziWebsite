import scrapy

class GameItem(scrapy.Item):
    id = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    system = scrapy.Field()
    icon = scrapy.Field()
    core = scrapy.Field()
    bios = scrapy.Field()
    playable = scrapy.Field()
    igdb_url = scrapy.Field()