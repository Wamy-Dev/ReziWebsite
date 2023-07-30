import scrapy

class GameItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()
    core = scrapy.Field()
    bios = scrapy.Field()
    system = scrapy.Field()
    icon = scrapy.Field()
    playable = scrapy.Field()
    igdb_url = scrapy.Field()